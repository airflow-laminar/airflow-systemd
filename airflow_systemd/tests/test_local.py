from typing import Any

import pytest
from airflow_pydantic import airflow as airflow_compat
from airflow_pydantic.migration import _airflow_3

from airflow_systemd import SystemdAirflowConfiguration

DAG: Any = airflow_compat.DAG


@pytest.mark.skipif(_airflow_3() is None, reason="Airflow not installed")
class TestSystemd:
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
