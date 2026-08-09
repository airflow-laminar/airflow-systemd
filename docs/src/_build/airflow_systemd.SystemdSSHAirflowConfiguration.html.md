# airflow_systemd.SystemdSSHAirflowConfiguration

### *pydantic model* airflow_systemd.SystemdSSHAirflowConfiguration[[source]](../../../_modules/airflow_systemd/config/systemd_ssh.html.md#SystemdSSHAirflowConfiguration)

Bases: [`SystemdAirflowConfiguration`](airflow_systemd.SystemdAirflowConfiguration.html.md#airflow_systemd.SystemdAirflowConfiguration)

Systemd configuration for a job managed over SSH.

#### *field* command_prefix *: str* *= ''*

Shell prefix applied before remote commands

#### *field* ssh_operator_args *: SSHTaskArgs* *[Optional]*

Airflow SSH connection and operator arguments
