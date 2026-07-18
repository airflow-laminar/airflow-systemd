from typing import Type

from airflow_pydantic import Host, ImportPath, Task, TaskArgs
from pydantic import Field, field_validator

from .systemd_ssh import SystemdSSHAirflowConfiguration

__all__ = ("SystemdSSHOperator", "SystemdSSHOperatorArgs", "SystemdSSHTask", "SystemdSSHTaskArgs")


class SystemdSSHTaskArgs(TaskArgs, extra="allow"):
    cfg: SystemdSSHAirflowConfiguration
    host: Host | None = Field(default=None, description="Host used to override the configured SSH connection")


SystemdSSHOperatorArgs = SystemdSSHTaskArgs


class SystemdSSHTask(Task, SystemdSSHTaskArgs):
    operator: ImportPath = Field(default="airflow_systemd.SystemdSSH", validate_default=True)

    @field_validator("operator")
    @classmethod
    def validate_operator(cls, value: Type) -> Type:
        from airflow_systemd.airflow import SystemdSSH

        if value is not SystemdSSH:
            raise ValueError(f"operator must be 'airflow_systemd.SystemdSSH', got: {value}")
        return value


SystemdSSHOperator = SystemdSSHTask
