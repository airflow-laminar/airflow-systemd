# Why Airflow owns the schedule

Airflow and systemd can both schedule work: Airflow through DAG schedules and
systemd through timer units. `airflow-systemd` deliberately uses Airflow as the
only scheduler and starts service units directly.

Two active schedulers would create ambiguous ownership. A timer could start the
service outside a DAG run, while Airflow would still monitor, restart, or stop it
according to a different execution interval. Direct service activation keeps
each external process lifecycle attached to one DAG run. Timer models remain in
[systemd-pydantic](https://github.com/airflow-laminar/systemd-pydantic) for
deployments where systemd owns scheduling.

## Lifecycle mapping

The integration maps external process states to `airflow-ha` results. A finished
service with an accepted exit status stops monitoring successfully. A running or
otherwise healthy service continues. A failed service retriggers through the
restart path. This separates lightweight Airflow polling from process ownership:
systemd launches, signals, and records the process; Airflow coordinates the
larger workflow.

## Local and SSH execution

Local mode calls `systemd-pydantic` convenience functions on the worker.
`SystemdSSH` sends configuration commands through Airflow's SSH provider and
uses an SSH-backed `SystemdClient` for status and lifecycle operations. Both
modes expose the same task graph and Airflow-specific controls.

## Comparison with supervisord

[airflow-supervisor](https://github.com/airflow-laminar/airflow-supervisor)
creates a dedicated supervisord instance for the job. `airflow-systemd` uses the
host's existing service manager instead. Systemd is a natural fit when unit
files, journald, cgroups, and host boot relationships are already operational
standards; supervisord is useful when a self-contained process manager is easier
to provision.
