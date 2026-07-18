from airflow_pydantic import SSHOperatorArgs
from pydantic import Field

from .systemd import SystemdAirflowConfiguration

__all__ = ("SSHOperatorArgs", "SystemdSSHAirflowConfiguration", "load_airflow_ssh_config")


class SystemdSSHAirflowConfiguration(SystemdAirflowConfiguration):
    """Systemd configuration for a job managed over SSH."""

    command_prefix: str = Field(default="", description="Shell prefix applied before remote commands")
    ssh_operator_args: SSHOperatorArgs = Field(
        default_factory=SSHOperatorArgs,
        description="Airflow SSH connection and operator arguments",
    )


load_airflow_ssh_config = SystemdSSHAirflowConfiguration.load
