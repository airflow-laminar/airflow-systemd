from typing import Any
from unittest.mock import MagicMock, Mock, patch

import pytest
from airflow_pydantic import Host, Pool, SSHOperatorArgs, airflow as airflow_compat
from airflow_pydantic.migration import _airflow_3
from systemd_pydantic import UnitInfo

from airflow_systemd import (
    AirflowSSHCommandRunner,
    SystemdAirflowConfiguration,
    SystemdSSH,
    SystemdSSHAirflowConfiguration,
    SystemdSSHOperator,
    SystemdSSHOperatorArgs,
    SystemdSSHTask,
    SystemdSSHTaskArgs,
)

DAG: Any = airflow_compat.DAG


@pytest.fixture
def ssh_configuration(systemd_airflow_configuration: SystemdAirflowConfiguration) -> SystemdSSHAirflowConfiguration:
    return SystemdSSHAirflowConfiguration.model_validate(
        {
            **systemd_airflow_configuration.model_dump(),
            "command_prefix": "source /etc/profile &&",
            "ssh_operator_args": SSHOperatorArgs(ssh_hook=airflow_compat.SSHHook(remote_host="localhost")),
        }
    )


def test_ssh_command_runner():
    hook = MagicMock()
    hook.exec_ssh_client_command.return_value = 0, b"output", b"warning"
    runner = AirflowSSHCommandRunner(hook, command_prefix="source /etc/profile &&")

    result = runner.run(["systemctl", "--user", "status", "test.service"], timeout=30)

    assert result.returncode == 0
    assert result.stdout == "output"
    assert result.stderr == "warning"
    command = hook.exec_ssh_client_command.call_args.args[1]
    assert command == "source /etc/profile &&\nsystemctl --user status test.service"


def test_ssh_command_runner_builds_hook_lazily():
    hook = MagicMock()
    hook.exec_ssh_client_command.return_value = 0, b"", b""
    runner = AirflowSSHCommandRunner(ssh_conn_id="systemd-host", banner_timeout=15)

    with patch("airflow_pydantic.airflow.SSHHook", return_value=hook) as hook_type:
        runner.run(["systemctl", "--user", "status", "test.service"], timeout=30)

    hook_type.assert_called_once_with(
        ssh_conn_id="systemd-host",
        remote_host="",
        conn_timeout=None,
        cmd_timeout=None,
    )
    assert hook.banner_timeout == 15


def test_ssh_task_configuration(ssh_configuration: SystemdSSHAirflowConfiguration):
    host = Host(name="remote", pool="remote-pool")
    args = SystemdSSHTaskArgs(cfg=ssh_configuration, host=host)
    task = SystemdSSHTask(task_id="systemd-ssh", cfg=ssh_configuration, host=host)

    assert args.host == host
    assert task.operator is SystemdSSH
    assert SystemdSSHOperatorArgs is SystemdSSHTaskArgs
    assert SystemdSSHOperator is SystemdSSHTask


@pytest.mark.skipif(_airflow_3() is None, reason="Airflow not installed")
class TestSystemdSSH:
    def test_task_graph_and_commands(self, ssh_configuration: SystemdSSHAirflowConfiguration):
        dag = DAG(dag_id="systemd-ssh", schedule=None)
        systemd = SystemdSSH(dag=dag, cfg=ssh_configuration)

        assert systemd.configure_systemd in dag.tasks
        assert systemd.check_services in dag.tasks
        assert systemd.unconfigure_systemd in dag.tasks
        assert systemd._command_prefix == "source /etc/profile &&"
        assert "_systemd_convenience configure-systemd" in systemd.get_step_kwargs("configure-systemd")["command"]
        assert "_systemd_convenience unconfigure-systemd" in systemd.get_step_kwargs("unconfigure-systemd")["command"]

    def test_host_override(self, ssh_configuration: SystemdSSHAirflowConfiguration):
        host = Host(name="remote", pool="remote-pool")
        systemd = SystemdSSH(dag=DAG(dag_id="systemd-host", schedule=None), cfg=ssh_configuration, host=host)

        assert systemd._cfg.ssh_operator_args.remote_host == "remote"
        assert systemd._cfg.pool == "test-pool"

    def test_dict_configuration_and_overrides(self, ssh_configuration: SystemdSSHAirflowConfiguration):
        data = ssh_configuration.model_dump(exclude={"ssh_operator_args"})
        data["pool"] = None
        data["ssh_operator_args"] = {"ssh_conn_id": "systemd-host", "banner_timeout": 15}
        systemd = SystemdSSH(
            dag=DAG(dag_id="systemd-ssh-overrides", schedule=None),
            cfg=data,
            host={"name": "remote", "pool": "remote-pool"},
            command_prefix="source /custom/profile &&",
            conn_timeout=20,
        )

        assert systemd._cfg.ssh_operator_args.remote_host == "remote"
        assert systemd._cfg.ssh_operator_args.conn_timeout == 20
        assert isinstance(systemd._cfg.pool, Pool)
        assert systemd._cfg.pool.pool == "remote-pool"
        assert systemd._command_prefix == "source /custom/profile &&"

    def test_connection_id_builds_hook(self, ssh_configuration: SystemdSSHAirflowConfiguration):
        data = ssh_configuration.model_dump(exclude={"ssh_operator_args"})
        data["ssh_operator_args"] = {"ssh_conn_id": "systemd-host", "banner_timeout": 15}
        systemd = SystemdSSH(dag=DAG(dag_id="systemd-connection", schedule=None), cfg=data)

        assert systemd._cfg.ssh_operator_args.ssh_hook is None
        assert isinstance(systemd.systemd_client.runner, AirflowSSHCommandRunner)

    def test_remote_lifecycle(self, ssh_configuration: SystemdSSHAirflowConfiguration):
        running = UnitInfo(name="test.service", active_state="active")
        done = UnitInfo(name="test.service", active_state="inactive", result="success", exec_main_status=0)
        failed = UnitInfo(name="test.service", active_state="failed", result="exit-code", exec_main_status=1)
        client = Mock()
        client.start_services.return_value = {running.name: running}
        client.restart_services.return_value = {running.name: running}
        client.stop_services.return_value = {done.name: done}
        client.kill_services.return_value = {done.name: done}
        systemd = SystemdSSH(
            dag=DAG(dag_id="systemd-remote-lifecycle", schedule=None),
            cfg=ssh_configuration,
            systemd_client=client,
        )
        systemd.check_services._check_end_conditions = Mock(return_value=None)

        assert systemd.get_step_kwargs("start-services")["python_callable"]() is True
        systemd.check_services._check_end_conditions.return_value = "done"
        assert systemd.get_step_kwargs("start-services")["python_callable"]() is False
        systemd.check_services._check_end_conditions.return_value = None
        systemd._cfg.restart_on_retrigger = True
        assert systemd.get_step_kwargs("start-services")["python_callable"]() is True
        assert systemd.get_step_kwargs("restart-services")["python_callable"]() is True
        assert systemd.get_step_kwargs("stop-services")["python_callable"]() is True
        assert systemd.get_step_kwargs("force-kill")["python_callable"]() is True

        from airflow_ha import Action, Result

        check = systemd.get_step_kwargs("check-services")["python_callable"]
        for info, expected in (
            (done, (Result.PASS, Action.STOP)),
            (running, (Result.PASS, Action.CONTINUE)),
            (failed, (Result.FAIL, Action.RETRIGGER)),
        ):
            client.get_all_service_info.return_value = {info.name: info}
            assert check() == expected

        client.get_all_service_info.return_value = {running.name: running, "done.service": done}
        assert check() == (Result.PASS, Action.CONTINUE)
