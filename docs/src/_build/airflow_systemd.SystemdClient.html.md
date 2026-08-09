# airflow_systemd.SystemdClient

### *class* airflow_systemd.SystemdClient(cfg: [SystemdConfiguration](airflow_systemd.SystemdConfiguration.html.md#airflow_systemd.SystemdConfiguration), runner: CommandRunner | None = None)[[source]](../../../_modules/systemd_pydantic/client/systemctl.html.md#SystemdClient)

Bases: `object`

#### \_\_init_\_(cfg: [SystemdConfiguration](airflow_systemd.SystemdConfiguration.html.md#airflow_systemd.SystemdConfiguration), runner: CommandRunner | None = None)[[source]](../../../_modules/systemd_pydantic/client/systemctl.html.md#SystemdClient.__init__)

### Methods

| [`__init__`](#airflow_systemd.SystemdClient.__init__)(cfg[, runner])   |    |
|------------------------------------------------------------------------|----|
| `daemon_reload`()                                                      |    |
| `disable_units`([names])                                               |    |
| `enable_units`([names])                                                |    |
| `get_all_service_info`()                                               |    |
| `get_all_timer_info`()                                                 |    |
| `get_unit_info`(name)                                                  |    |
| `get_units_info`(names)                                                |    |
| `kill_services`()                                                      |    |
| `kill_units`(names)                                                    |    |
| `restart_services`()                                                   |    |
| `restart_units`(names)                                                 |    |
| `start_services`()                                                     |    |
| `start_timers`()                                                       |    |
| `start_units`(names)                                                   |    |
| `stop_services`()                                                      |    |
| `stop_timers`()                                                        |    |
| `stop_units`(names)                                                    |    |
