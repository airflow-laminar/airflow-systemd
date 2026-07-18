from typing import Any
from unittest.mock import Mock, patch

import pytest
from airflow_pydantic import airflow as airflow_compat
from airflow_pydantic.migration import _airflow_3

from airflow_systemd import SystemdAirflowConfiguration

DAG: Any = airflow_compat.DAG


@pytest.mark.skipif(_airflow_3() is None, reason="Airflow not installed")
class TestSystemd:
    @staticmethod
    def create_systemd(systemd_airflow_configuration: SystemdAirflowConfiguration, dag_id: str = "systemd-callbacks"):
        from airflow_systemd import Systemd

        return Systemd(dag=DAG(dag_id=dag_id, schedule=None), cfg=systemd_airflow_configuration)

    def test_task_graph(self, systemd_airflow_configuration: SystemdAirflowConfiguration):
        from airflow_systemd import Systemd

        dag = DAG(dag_id="systemd-test", default_args={}, schedule=None, params={})
        systemd = Systemd(dag=dag, cfg=systemd_airflow_configuration)

        assert systemd.configure_systemd in dag.tasks
        assert systemd.start_services in dag.tasks
        assert systemd.check_services in dag.tasks
        assert systemd.restart_services in dag.tasks
        assert systemd.stop_services in dag.tasks
        assert systemd.unconfigure_systemd in dag.tasks
        assert dag.catchup is False
        assert dag.max_active_tasks == 1
        assert dag.max_active_runs == 1

    @pytest.mark.parametrize(("stop_on_exit", "cleanup"), [(False, False), (True, False)])
    def test_optional_cleanup(
        self,
        systemd_airflow_configuration: SystemdAirflowConfiguration,
        stop_on_exit: bool,
        cleanup: bool,
    ):
        from airflow_systemd import Systemd

        cfg = systemd_airflow_configuration.model_copy(update={"stop_on_exit": stop_on_exit, "cleanup": cleanup})
        dag = DAG(dag_id=f"systemd-cleanup-{stop_on_exit}-{cleanup}", schedule=None)
        systemd = Systemd(dag=dag, cfg=cfg)

        assert systemd.stop_services is not None
        assert systemd.unconfigure_systemd is not None

    def test_dict_configuration(self, systemd_airflow_configuration: SystemdAirflowConfiguration):
        from airflow_systemd import Systemd

        dag = DAG(dag_id="systemd-dict", schedule=None)
        systemd = Systemd(dag=dag, cfg=systemd_airflow_configuration.model_dump())

        assert systemd._cfg == systemd_airflow_configuration

    def test_lifecycle_callbacks(self, systemd_airflow_configuration: SystemdAirflowConfiguration):
        from airflow_ha import Action, Result

        systemd = self.create_systemd(systemd_airflow_configuration)
        systemd.check_services._check_end_conditions = Mock(return_value=None)
        systemd._cfg.restart_on_retrigger = True

        with (
            patch("airflow_systemd.airflow.local.write_systemd_config", return_value=True) as write,
            patch("airflow_systemd.airflow.local.start_services", return_value=True) as start,
            patch("airflow_systemd.airflow.local.stop_services", return_value=True) as stop,
            patch("airflow_systemd.airflow.local.restart_services", return_value=True) as restart,
            patch("airflow_systemd.airflow.local.remove_systemd_config", return_value=True) as remove,
        ):
            assert systemd.get_step_kwargs("configure-systemd")["python_callable"]() is True
            assert systemd.get_step_kwargs("start-services")["python_callable"]() is True
            assert systemd.get_step_kwargs("stop-services")["python_callable"]() is True
            assert systemd.get_step_kwargs("restart-services")["python_callable"]() is True
            assert systemd.get_step_kwargs("unconfigure-systemd")["python_callable"]() is True

        write.assert_called_once()
        start.assert_called_once_with(systemd._cfg._pydantic_path, restart=True, _exit=False)
        stop.assert_called_once()
        restart.assert_called_once()
        remove.assert_called_once()

        systemd.check_services._check_end_conditions.return_value = "done"
        assert systemd.get_step_kwargs("start-services")["python_callable"]() is False

        check = systemd.get_step_kwargs("check-services")["python_callable"]
        with patch("airflow_systemd.airflow.local.check_services", side_effect=[True]):
            assert check() == (Result.PASS, Action.STOP)
        with patch("airflow_systemd.airflow.local.check_services", side_effect=[False, True]):
            assert check() == (Result.PASS, Action.CONTINUE)
        with patch("airflow_systemd.airflow.local.check_services", side_effect=[False, False, True]):
            assert check() == (Result.PASS, Action.CONTINUE)
        with patch("airflow_systemd.airflow.local.check_services", side_effect=[False, False, False]):
            assert check() == (Result.FAIL, Action.RETRIGGER)

    def test_force_kill(self, systemd_airflow_configuration: SystemdAirflowConfiguration):
        info = Mock()
        info.stopped.return_value = True
        client = Mock()
        client.kill_services.return_value = {"test.service": info}

        from airflow_systemd import Systemd

        systemd = Systemd(
            dag=DAG(dag_id="systemd-force-kill", schedule=None),
            cfg=systemd_airflow_configuration,
            systemd_client=client,
        )

        assert systemd.systemd_client is client
        assert systemd.get_step_kwargs("force-kill")["python_callable"]() is True

    def test_chaining_helpers(self, systemd_airflow_configuration: SystemdAirflowConfiguration):
        systemd = self.create_systemd(systemd_airflow_configuration, "systemd-chaining")
        PythonOperator: Any = airflow_compat.PythonOperator
        before = PythonOperator(task_id="before", python_callable=lambda: None, dag=systemd._dag)
        after = PythonOperator(task_id="after", python_callable=lambda: None, dag=systemd._dag)

        assert systemd << before is systemd.unconfigure_systemd
        assert systemd >> after is after
        systemd.set_upstream(before)
        systemd.set_downstream(after)
        assert systemd.update_relative(before) is systemd
        assert systemd.update_relative(after, upstream=False) is systemd
        assert systemd.roots
        assert systemd.leaves
