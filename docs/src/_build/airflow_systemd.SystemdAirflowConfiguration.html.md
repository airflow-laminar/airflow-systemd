# airflow_systemd.SystemdAirflowConfiguration

### *pydantic model* airflow_systemd.SystemdAirflowConfiguration

Bases: [`SystemdConvenienceConfiguration`](airflow_systemd.SystemdConvenienceConfiguration.md#airflow_systemd.SystemdConvenienceConfiguration)

Systemd configuration for an Airflow-managed job.

#### *field* check_interval *: timedelta* *= datetime.timedelta(seconds=5)*

Interval between service status checks

#### *field* check_timeout *: timedelta* *= datetime.timedelta(seconds=28800)*

Timeout for service status checks

#### *field* runtime *: timedelta | None* *= None*

Maximum runtime of the systemd job

#### *field* endtime *: time | None* *= None*

End time of the systemd job

#### *field* maxretrigger *: int | None* *= None*

Maximum number of service check retriggers

#### *field* reference_date *: Literal['start_date', 'logical_date', 'data_interval_end']* *= 'data_interval_end'*

Date used to evaluate runtime and endtime

#### *field* pool *: str | Pool | None* *= None*

Airflow pool for systemd tasks

#### *field* stop_on_exit *: bool* *= True*

Stop services when the DAG finishes

#### *field* cleanup *: bool* *= True*

Remove generated unit files when the DAG finishes

#### *field* restart_on_initial *: bool* *= False*

Restart services on an initial Airflow run

#### *field* restart_on_retrigger *: bool* *= False*

Restart services when airflow-ha retriggers the job

#### systemd_json() → str

Serialize only fields understood by systemd-pydantic.
