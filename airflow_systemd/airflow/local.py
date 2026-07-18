from logging import getLogger
from typing import TYPE_CHECKING, Any, Literal

from airflow_pydantic import Pool, fail, skip
from systemd_pydantic import SystemdClient
from systemd_pydantic.convenience import (
    SystemdTaskStep,
    check_services,
    remove_systemd_config,
    restart_services,
    start_services,
    stop_services,
    write_systemd_config,
)

from airflow_systemd.config.systemd import SystemdAirflowConfiguration

if TYPE_CHECKING:
    from airflow_ha import CheckResult, HighAvailabilityOperator

    DAG = Any
    Operator = Any

__all__ = ("Systemd",)

_log = getLogger(__name__)
Step = SystemdTaskStep | Literal["force-kill"]


def _python_operator() -> Any:
    from airflow_pydantic.airflow import PythonOperator

    return PythonOperator


class Systemd:
    """Airflow task group for a locally managed systemd job."""

    def __init__(self, dag: "DAG", cfg: SystemdAirflowConfiguration | dict, **kwargs: Any):
        if isinstance(cfg, dict):
            cfg = SystemdAirflowConfiguration.model_validate(cfg)

        self._cfg = cfg
        self._pool = cfg.pool.pool if isinstance(cfg.pool, Pool) else cfg.pool
        self._systemd_client = kwargs.pop("systemd_client", SystemdClient(cfg))
        self._dag = dag

        self.setup_dag()
        self.initialize_tasks()

        self.configure_systemd >> self.start_services >> self.check_services
        self.check_services.retrigger_fail >> self.restart_services
        self.check_services.stop_pass >> self.stop_services >> self.unconfigure_systemd

        self._force_kill = self.get_step_operator("force-kill")

        PythonOperator = _python_operator()

        (
            PythonOperator(
                task_id=f"{self._dag.dag_id}-force-kill-dag",
                python_callable=skip,
                **self.get_base_operator_kwargs(),
            )
            >> self._force_kill
        )

        any_config_fail = PythonOperator(
            task_id=f"{self._dag.dag_id}-check-config-failed",
            python_callable=fail,
            trigger_rule="one_failed",
            **self.get_base_operator_kwargs(),
        )
        self.configure_systemd >> any_config_fail
        self.start_services >> any_config_fail
        self.stop_services >> any_config_fail
        self.unconfigure_systemd >> any_config_fail

    def setup_dag(self) -> None:
        self._dag.catchup = False
        self._dag.concurrency = 1
        self._dag.max_active_tasks = 1
        self._dag.max_active_runs = 1

    def initialize_tasks(self) -> None:
        PythonOperator = _python_operator()

        self._check_services = self.get_step_operator("check-services")
        self._configure_systemd = self.get_step_operator("configure-systemd")
        self._start_services = self.get_step_operator("start-services")
        if self._cfg.stop_on_exit:
            self._stop_services = self.get_step_operator("stop-services")
            if self._cfg.cleanup:
                self._unconfigure_systemd = self.get_step_operator("unconfigure-systemd")
            else:
                self._unconfigure_systemd = PythonOperator(
                    task_id=f"{self._dag.dag_id}-unconfigure-systemd",
                    python_callable=skip,
                    **self.get_base_operator_kwargs(),
                )
        else:
            self._stop_services = PythonOperator(
                task_id=f"{self._dag.dag_id}-stop-services",
                python_callable=skip,
                **self.get_base_operator_kwargs(),
            )
            self._unconfigure_systemd = PythonOperator(
                task_id=f"{self._dag.dag_id}-unconfigure-systemd",
                python_callable=skip,
                **self.get_base_operator_kwargs(),
            )
        self._restart_services = self.get_step_operator("restart-services")

    @property
    def configure_systemd(self) -> "Operator":
        return self._configure_systemd

    @property
    def start_services(self) -> "Operator":
        return self._start_services

    @property
    def check_services(self) -> "HighAvailabilityOperator":
        return self._check_services

    @property
    def stop_services(self) -> "Operator":
        return self._stop_services

    @property
    def restart_services(self) -> "Operator":
        return self._restart_services

    @property
    def unconfigure_systemd(self) -> "Operator":
        return self._unconfigure_systemd

    @property
    def systemd_client(self) -> SystemdClient:
        return self._systemd_client

    def get_base_operator_kwargs(self) -> dict[str, Any]:
        return {"dag": self._dag, "pool": self._pool}

    def get_step_kwargs(self, step: Step) -> dict[str, Any]:
        cfg = self._cfg
        if step == "configure-systemd":
            return {
                "python_callable": lambda **kwargs: (
                    self.check_services.check_end_conditions(**kwargs) is None and write_systemd_config(cfg.systemd_json(), _exit=False)
                ),
                "do_xcom_push": True,
            }
        if step == "start-services":

            def _start_services(**kwargs: Any) -> bool:
                if self.check_services.check_end_conditions(**kwargs) is not None:
                    return False
                restart = cfg.restart_on_retrigger or (cfg.restart_on_initial and self.check_services.is_initial_run(**kwargs))
                return start_services(cfg._pydantic_path, restart=restart, _exit=False)

            return {
                "python_callable": _start_services,
                "do_xcom_push": True,
            }
        if step == "stop-services":
            return {"python_callable": lambda: stop_services(cfg._pydantic_path, _exit=False), "do_xcom_push": True}
        if step == "check-services":

            def _check_services(systemd_cfg: SystemdAirflowConfiguration = cfg, **kwargs: Any) -> "CheckResult":
                from airflow_ha import Action, Result

                if check_services(systemd_cfg._pydantic_path, check_done=True, _exit=False):
                    return Result.PASS, Action.STOP
                if check_services(systemd_cfg._pydantic_path, check_running=True, _exit=False):
                    return Result.PASS, Action.CONTINUE
                if check_services(systemd_cfg._pydantic_path, _exit=False):
                    return Result.PASS, Action.CONTINUE
                return Result.FAIL, Action.RETRIGGER

            return {"python_callable": _check_services, "do_xcom_push": True}
        if step == "restart-services":
            return {"python_callable": lambda: restart_services(cfg._pydantic_path, _exit=False), "do_xcom_push": True}
        if step == "unconfigure-systemd":
            return {"python_callable": lambda: remove_systemd_config(cfg._pydantic_path, _exit=False), "do_xcom_push": True}
        if step == "force-kill":
            return {
                "python_callable": lambda: all(info.stopped() for info in self.systemd_client.kill_services().values()),
                "do_xcom_push": True,
            }
        raise NotImplementedError(f"Unknown step: {step}")

    def get_step_operator(self, step: Step) -> "Operator":
        from airflow_ha import HighAvailabilityOperator

        PythonOperator = _python_operator()

        if step == "check-services":
            return HighAvailabilityOperator(
                task_id=f"{self._dag.dag_id}-{step}",
                poke_interval=self._cfg.check_interval.total_seconds(),
                timeout=self._cfg.check_timeout.total_seconds(),
                mode="poke",
                runtime=self._cfg.runtime,
                endtime=self._cfg.endtime,
                maxretrigger=self._cfg.maxretrigger,
                reference_date=self._cfg.reference_date,
                **self.get_base_operator_kwargs(),
                **self.get_step_kwargs(step),
            )
        return PythonOperator(
            task_id=f"{self._dag.dag_id}-{step}",
            **self.get_base_operator_kwargs(),
            **self.get_step_kwargs(step),
        )

    def __lshift__(self, other: "Operator") -> "Operator":
        self.configure_systemd << other
        return self.unconfigure_systemd

    def __rshift__(self, other: "Operator") -> "Operator":
        self.unconfigure_systemd >> other
        return other

    def set_upstream(self, other: "Operator") -> None:
        self.configure_systemd.set_upstream(other)

    def set_downstream(self, other: "Operator") -> None:
        self.unconfigure_systemd.set_downstream(other)

    def update_relative(self, other: "Operator", upstream: bool = True, edge_modifier: Any = None) -> "Systemd":
        if upstream:
            self.configure_systemd.update_relative(other, upstream=True, edge_modifier=edge_modifier)
        else:
            self.unconfigure_systemd.update_relative(other, upstream=False, edge_modifier=edge_modifier)
        return self

    @property
    def leaves(self):
        return self.unconfigure_systemd.leaves

    @property
    def roots(self):
        return self.configure_systemd.roots
