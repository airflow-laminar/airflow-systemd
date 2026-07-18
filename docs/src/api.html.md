# API reference

## Airflow lifecycle

| [`Systemd`](_build/airflow_systemd.Systemd.md#airflow_systemd.Systemd)(dag, cfg, \*\*kwargs)                                                | Airflow task group for a locally managed systemd job.   |
|---------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| [`SystemdSSH`](_build/airflow_systemd.SystemdSSH.md#airflow_systemd.SystemdSSH)(dag, cfg[, host])                                           | Airflow task group for a systemd job managed over SSH.  |
| [`AirflowSSHCommandRunner`](_build/airflow_systemd.AirflowSSHCommandRunner.md#airflow_systemd.AirflowSSHCommandRunner)([hook, ...])         | Run SystemdClient commands through an Airflow SSHHook.  |
| [`SystemdAirflowConfiguration`](_build/airflow_systemd.SystemdAirflowConfiguration.md#airflow_systemd.SystemdAirflowConfiguration)          | Systemd configuration for an Airflow-managed job.       |
| [`SystemdSSHAirflowConfiguration`](_build/airflow_systemd.SystemdSSHAirflowConfiguration.md#airflow_systemd.SystemdSSHAirflowConfiguration) | Systemd configuration for a job managed over SSH.       |
| [`SystemdTask`](_build/airflow_systemd.SystemdTask.md#airflow_systemd.SystemdTask)                                                          |                                                         |
| [`SystemdTaskArgs`](_build/airflow_systemd.SystemdTaskArgs.md#airflow_systemd.SystemdTaskArgs)                                              |                                                         |
| [`SystemdSSHTask`](_build/airflow_systemd.SystemdSSHTask.md#airflow_systemd.SystemdSSHTask)                                                 |                                                         |
| [`SystemdSSHTaskArgs`](_build/airflow_systemd.SystemdSSHTaskArgs.md#airflow_systemd.SystemdSSHTaskArgs)                                     |                                                         |
| [`load_airflow_config`](_build/airflow_systemd.load_airflow_config.md#airflow_systemd.load_airflow_config)([config_dir, ...])               |                                                         |
| [`load_airflow_ssh_config`](_build/airflow_systemd.load_airflow_ssh_config.md#airflow_systemd.load_airflow_ssh_config)([config_dir, ...])   |                                                         |

## Re-exported systemd models

| [`ServiceConfiguration`](_build/airflow_systemd.ServiceConfiguration.md#airflow_systemd.ServiceConfiguration)                                  | Process supervision settings from a systemd `[Service]` section.   |
|------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| [`ServiceUnitConfiguration`](_build/airflow_systemd.ServiceUnitConfiguration.md#airflow_systemd.ServiceUnitConfiguration)                      |                                                                    |
| [`TimerConfiguration`](_build/airflow_systemd.TimerConfiguration.md#airflow_systemd.TimerConfiguration)                                        | Activation settings from a systemd `[Timer]` section.              |
| [`TimerUnitConfiguration`](_build/airflow_systemd.TimerUnitConfiguration.md#airflow_systemd.TimerUnitConfiguration)                            |                                                                    |
| [`SystemdConfiguration`](_build/airflow_systemd.SystemdConfiguration.md#airflow_systemd.SystemdConfiguration)                                  | Named collection of systemd service and timer unit files.          |
| [`SystemdConvenienceConfiguration`](_build/airflow_systemd.SystemdConvenienceConfiguration.md#airflow_systemd.SystemdConvenienceConfiguration) | Systemd defaults and persisted state used by convenience commands. |
| [`SystemdClient`](_build/airflow_systemd.SystemdClient.md#airflow_systemd.SystemdClient)(cfg[, runner])                                        |                                                                    |
| [`UnitInfo`](_build/airflow_systemd.UnitInfo.md#airflow_systemd.UnitInfo)                                                                      |                                                                    |
