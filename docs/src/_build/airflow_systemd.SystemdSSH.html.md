# airflow_systemd.SystemdSSH

### *class* airflow_systemd.SystemdSSH(dag: DAG, cfg: [SystemdSSHAirflowConfiguration](airflow_systemd.SystemdSSHAirflowConfiguration.html.md#airflow_systemd.SystemdSSHAirflowConfiguration) | dict, host: Host | dict | None = None, \*\*kwargs: Any)[[source]](../../../_modules/airflow_systemd/airflow/ssh.html.md#SystemdSSH)

Bases: [`Systemd`](airflow_systemd.Systemd.html.md#airflow_systemd.Systemd)

Airflow task group for a systemd job managed over SSH.

#### \_\_init_\_(dag: DAG, cfg: [SystemdSSHAirflowConfiguration](airflow_systemd.SystemdSSHAirflowConfiguration.html.md#airflow_systemd.SystemdSSHAirflowConfiguration) | dict, host: Host | dict | None = None, \*\*kwargs: Any)[[source]](../../../_modules/airflow_systemd/airflow/ssh.html.md#SystemdSSH.__init__)

### Methods

| [`__init__`](#airflow_systemd.SystemdSSH.__init__)(dag, cfg[, host])   |    |
|------------------------------------------------------------------------|----|
| `get_base_operator_kwargs`()                                           |    |
| `get_step_kwargs`(step)                                                |    |
| `get_step_operator`(step)                                              |    |
| `initialize_tasks`()                                                   |    |
| `set_downstream`(other)                                                |    |
| `set_upstream`(other)                                                  |    |
| `setup_dag`()                                                          |    |
| `update_relative`(other[, upstream, edge_modifier])                    |    |

### Attributes

| `check_services`      |    |
|-----------------------|----|
| `configure_systemd`   |    |
| `leaves`              |    |
| `restart_services`    |    |
| `roots`               |    |
| `start_services`      |    |
| `stop_services`       |    |
| `systemd_client`      |    |
| `unconfigure_systemd` |    |
