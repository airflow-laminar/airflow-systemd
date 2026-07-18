import pytest
from pydantic import ValidationError

from airflow_systemd import (
    Systemd,
    SystemdAirflowConfiguration,
    SystemdOperator,
    SystemdOperatorArgs,
    SystemdTask,
    SystemdTaskArgs,
)


def test_task_args(systemd_airflow_configuration: SystemdAirflowConfiguration):
    args = SystemdTaskArgs(cfg=systemd_airflow_configuration)

    assert args.cfg == systemd_airflow_configuration
    assert SystemdOperatorArgs is SystemdTaskArgs


def test_task_default_operator(systemd_airflow_configuration: SystemdAirflowConfiguration):
    task = SystemdTask(task_id="systemd-task", cfg=systemd_airflow_configuration)

    assert task.operator is Systemd
    assert SystemdOperator is SystemdTask


def test_task_rejects_another_operator(systemd_airflow_configuration: SystemdAirflowConfiguration):
    with pytest.raises(ValidationError, match="operator must be"):
        SystemdTask(
            task_id="systemd-task",
            cfg=systemd_airflow_configuration,
            operator="airflow_systemd.SystemdTask",
        )
