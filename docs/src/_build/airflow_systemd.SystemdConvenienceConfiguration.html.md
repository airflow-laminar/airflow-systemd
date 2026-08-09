# airflow_systemd.SystemdConvenienceConfiguration

### *pydantic model* airflow_systemd.SystemdConvenienceConfiguration[[source]](../../../_modules/systemd_pydantic/config/convenience.html.md#SystemdConvenienceConfiguration)

Bases: [`SystemdConfiguration`](airflow_systemd.SystemdConfiguration.html.md#airflow_systemd.SystemdConfiguration)

Systemd defaults and persisted state used by convenience commands.

#### *field* restart *: Literal['no', 'on-success', 'on-failure', 'on-abnormal', 'on-watchdog', 'on-abort', 'always']* *= 'no'*

#### *field* timeout_stop_sec *: str | timedelta* *= '30s'*

#### *field* kill_mode *: Literal['control-group', 'mixed', 'process', 'none']* *= 'control-group'*

#### *field* kill_signal *: str* *= 'SIGTERM'*

#### *field* success_exit_status *: list[int | str]* *= [0]*

#### *field* command_timeout *: int* *= 60*

#### rmdir() → None[[source]](../../../_modules/systemd_pydantic/config/convenience.html.md#SystemdConvenienceConfiguration.rmdir)
