# airflow_systemd.Systemd

### *class* airflow_systemd.Systemd(dag: DAG, cfg: [SystemdAirflowConfiguration](airflow_systemd.SystemdAirflowConfiguration.html.md#airflow_systemd.SystemdAirflowConfiguration) | dict, \*\*kwargs: Any)[[source]](../../../_modules/airflow_systemd/airflow/local.html.md#Systemd)

Bases: `object`

Airflow task group for a locally managed systemd job.

#### \_\_init_\_(dag: DAG, cfg: [SystemdAirflowConfiguration](airflow_systemd.SystemdAirflowConfiguration.html.md#airflow_systemd.SystemdAirflowConfiguration) | dict, \*\*kwargs: Any)[[source]](../../../_modules/airflow_systemd/airflow/local.html.md#Systemd.__init__)

### Methods

| [`__init__`](#airflow_systemd.Systemd.__init__)(dag, cfg, \*\*kwargs)   |    |
|-------------------------------------------------------------------------|----|
| `get_base_operator_kwargs`()                                            |    |
| `get_step_kwargs`(step)                                                 |    |
| `get_step_operator`(step)                                               |    |
| `initialize_tasks`()                                                    |    |
| `set_downstream`(other)                                                 |    |
| `set_upstream`(other)                                                   |    |
| `setup_dag`()                                                           |    |
| `update_relative`(other[, upstream, edge_modifier])                     |    |

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
