from airflow_pydantic import ImportPath, Task, TaskArgs
from pydantic import Field, field_validator

from .systemd import SystemdAirflowConfiguration

__all__ = ("SystemdOperator", "SystemdOperatorArgs", "SystemdTask", "SystemdTaskArgs")


class SystemdTaskArgs(TaskArgs):
    cfg: SystemdAirflowConfiguration


SystemdOperatorArgs = SystemdTaskArgs


class SystemdTask(Task, SystemdTaskArgs):
    operator: ImportPath = Field(default="airflow_systemd.Systemd", validate_default=True)

    @field_validator("operator")
    @classmethod
    def validate_operator(cls, value: type) -> type:
        from airflow_systemd.airflow import Systemd

        if value is not Systemd:
            raise ValueError(f"operator must be 'airflow_systemd.Systemd', got: {value}")
        return value


SystemdOperator = SystemdTask
