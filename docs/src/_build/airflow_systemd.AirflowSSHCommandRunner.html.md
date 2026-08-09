# airflow_systemd.AirflowSSHCommandRunner

### *class* airflow_systemd.AirflowSSHCommandRunner(hook: Any = None, command_prefix: str = '', environment: dict[str, str] | None = None, get_pty: bool = False, ssh_conn_id: str | None = None, remote_host: str = '', conn_timeout: int | None = None, cmd_timeout: int | None = None, banner_timeout: int | None = None)[[source]](../../../_modules/airflow_systemd/airflow/ssh.html.md#AirflowSSHCommandRunner)

Bases: `object`

Run SystemdClient commands through an Airflow SSHHook.

#### \_\_init_\_(hook: Any = None, command_prefix: str = '', environment: dict[str, str] | None = None, get_pty: bool = False, ssh_conn_id: str | None = None, remote_host: str = '', conn_timeout: int | None = None, cmd_timeout: int | None = None, banner_timeout: int | None = None)[[source]](../../../_modules/airflow_systemd/airflow/ssh.html.md#AirflowSSHCommandRunner.__init__)

### Methods

| [`__init__`](#airflow_systemd.AirflowSSHCommandRunner.__init__)([hook, command_prefix, ...])   |    |
|------------------------------------------------------------------------------------------------|----|
| `get_hook`()                                                                                   |    |
| `run`(command, timeout)                                                                        |    |
