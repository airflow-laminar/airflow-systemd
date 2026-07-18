from shlex import join, quote
from typing import TYPE_CHECKING, Any

from airflow_pydantic import Host, SSHOperatorArgs
from systemd_pydantic import CommandResult, SystemdClient

from airflow_systemd.config.systemd_ssh import SystemdSSHAirflowConfiguration

from .local import Step, Systemd

if TYPE_CHECKING:
    DAG = Any
    Operator = Any

__all__ = ("AirflowSSHCommandRunner", "SystemdSSH")


class AirflowSSHCommandRunner:
    """Run SystemdClient commands through an Airflow SSHHook."""

    def __init__(
        self,
        hook: Any = None,
        command_prefix: str = "",
        environment: dict[str, str] | None = None,
        get_pty: bool = False,
        ssh_conn_id: str | None = None,
        remote_host: str = "",
        conn_timeout: int | None = None,
        cmd_timeout: int | None = None,
        banner_timeout: int | None = None,
    ):
        self.hook = hook
        self.command_prefix = command_prefix
        self.environment = environment
        self.get_pty = get_pty
        self.ssh_conn_id = ssh_conn_id
        self.remote_host = remote_host
        self.conn_timeout = conn_timeout
        self.cmd_timeout = cmd_timeout
        self.banner_timeout = banner_timeout

    def get_hook(self) -> Any:
        if self.hook is None:
            from airflow_pydantic.airflow import SSHHook

            self.hook = SSHHook(
                ssh_conn_id=self.ssh_conn_id,
                remote_host=self.remote_host,
                conn_timeout=self.conn_timeout,
                cmd_timeout=self.cmd_timeout,
            )
            if self.banner_timeout is not None:
                self.hook.banner_timeout = self.banner_timeout
        return self.hook

    def run(self, command: list[str], timeout: int) -> CommandResult:
        remote_command = "\n".join(value for value in (self.command_prefix, join(command)) if value)
        hook = self.get_hook()
        with hook.get_conn() as client:
            returncode, stdout, stderr = hook.exec_ssh_client_command(
                client,
                remote_command,
                get_pty=self.get_pty,
                environment=self.environment,
                timeout=timeout,
            )
        return CommandResult(
            command=command,
            returncode=returncode,
            stdout=stdout.decode("utf-8", "replace"),
            stderr=stderr.decode("utf-8", "replace"),
        )


class SystemdSSH(Systemd):
    """Airflow task group for a systemd job managed over SSH."""

    _cfg: SystemdSSHAirflowConfiguration

    def __init__(
        self,
        dag: "DAG",
        cfg: SystemdSSHAirflowConfiguration | dict,
        host: Host | dict | None = None,
        **kwargs: Any,
    ):
        if isinstance(cfg, dict):
            cfg = SystemdSSHAirflowConfiguration.model_validate(cfg)

        command_prefix = kwargs.pop("command_prefix", cfg.command_prefix)
        ssh_args = cfg.ssh_operator_args.model_dump(exclude_none=True)
        for name in SSHOperatorArgs.model_fields:
            if name in kwargs:
                ssh_args[name] = kwargs.pop(name)

        if host is not None:
            if isinstance(host, dict):
                host = Host.model_validate(host)
            ssh_args["remote_host"] = host.name
            ssh_args["ssh_hook"] = host.hook()
            if host.pool and not cfg.pool:
                cfg.pool = host.pool

        cfg.command_prefix = command_prefix
        cfg.ssh_operator_args = SSHOperatorArgs.model_validate(ssh_args)
        self._command_prefix = command_prefix
        self._ssh_operator_kwargs = cfg.ssh_operator_args.model_dump(
            exclude_none=True,
            exclude={
                "command",
                "dependencies",
                "operator",
                "ssh_hook_external",
                "ssh_hook_foo",
                "ssh_hook_host",
                "ssh_hook_hosts",
                "task_id",
                "type_",
            },
        )

        runner = AirflowSSHCommandRunner(
            cfg.ssh_operator_args.ssh_hook,
            command_prefix=command_prefix,
            environment=cfg.ssh_operator_args.environment,
            get_pty=bool(cfg.ssh_operator_args.get_pty),
            ssh_conn_id=cfg.ssh_operator_args.ssh_conn_id,
            remote_host=cfg.ssh_operator_args.remote_host or "",
            conn_timeout=cfg.ssh_operator_args.conn_timeout,
            cmd_timeout=cfg.ssh_operator_args.cmd_timeout,
            banner_timeout=cfg.ssh_operator_args.banner_timeout,
        )
        systemd_client = kwargs.pop("systemd_client", SystemdClient(cfg, runner=runner))
        super().__init__(dag=dag, cfg=cfg, systemd_client=systemd_client, **kwargs)

    def get_step_kwargs(self, step: Step) -> dict[str, Any]:
        cfg = self._cfg
        if step == "configure-systemd":
            command = f"_systemd_convenience {step} {quote(cfg.systemd_json())}"
            return {**self._ssh_operator_kwargs, "command": "\n".join(filter(None, (self._command_prefix, command)))}
        if step == "unconfigure-systemd":
            command = f"_systemd_convenience {step} --cfg {quote(str(cfg._pydantic_path))}"
            return {**self._ssh_operator_kwargs, "command": "\n".join(filter(None, (self._command_prefix, command)))}
        if step == "start-services":

            def _start_services(**kwargs: Any) -> bool:
                if self.check_services.check_end_conditions(**kwargs) is not None:
                    return False
                restart = cfg.restart_on_retrigger or (cfg.restart_on_initial and self.check_services.is_initial_run(**kwargs))
                infos = self.systemd_client.restart_services() if restart else self.systemd_client.start_services()
                return all(info.ok(cfg.success_exit_status) for info in infos.values())

            return {"python_callable": _start_services, "do_xcom_push": True}
        if step == "stop-services":
            return {
                "python_callable": lambda: all(info.stopped() for info in self.systemd_client.stop_services().values()),
                "do_xcom_push": True,
            }
        if step == "check-services":

            def _check_services(**kwargs: Any):
                from airflow_ha import Action, Result

                infos = self.systemd_client.get_all_service_info().values()
                if all(info.done(cfg.success_exit_status) for info in infos):
                    return Result.PASS, Action.STOP
                infos = self.systemd_client.get_all_service_info().values()
                if all(info.running() for info in infos):
                    return Result.PASS, Action.CONTINUE
                infos = self.systemd_client.get_all_service_info().values()
                if all(info.ok(cfg.success_exit_status) for info in infos):
                    return Result.PASS, Action.CONTINUE
                return Result.FAIL, Action.RETRIGGER

            return {"python_callable": _check_services, "do_xcom_push": True}
        if step == "restart-services":
            return {
                "python_callable": lambda: all(info.ok(cfg.success_exit_status) for info in self.systemd_client.restart_services().values()),
                "do_xcom_push": True,
            }
        return super().get_step_kwargs(step)

    def get_step_operator(self, step: Step) -> "Operator":
        if step in {"configure-systemd", "unconfigure-systemd"}:
            from airflow_pydantic import airflow as airflow_compat

            SSHOperator: Any = airflow_compat.SSHOperator
            return SSHOperator(
                task_id=f"{self._dag.dag_id}-{step}",
                **self.get_base_operator_kwargs(),
                **self.get_step_kwargs(step),
            )
        return super().get_step_operator(step)
