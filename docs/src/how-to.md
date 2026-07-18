# How-to guides

These guides cover common local, remote, and lifecycle configurations.

## How to keep a service running after the DAG finishes

Disable stop and cleanup, then choose when to restart the persistent service:

```yaml
cfg:
  scope: user
  stop_on_exit: false
  cleanup: false
  restart_on_initial: true
  restart_on_retrigger: true
  service:
    api:
      service:
        type: exec
        exec_start: /opt/services/api
        restart: on-failure
```

Use this for services whose ownership remains with systemd between Airflow runs.

## How to limit monitoring

Set Airflow-specific timing fields on `SystemdAirflowConfiguration`:

```yaml
cfg:
  check_interval: 00:00:10
  check_timeout: 08:00:00
  runtime: 04:00:00
  maxretrigger: 3
  service:
    batch:
      service:
        type: exec
        exec_start: /opt/jobs/batch
```

`check_interval` controls polling, `check_timeout` controls the sensor timeout,
and `runtime` controls the allowed external job duration.

## How to manage a remote host

Use the SSH task model in `airflow-config`:

```yaml
dags:
  remote-systemd:
    schedule: "@daily"
    tasks:
      run-remote:
        _target_: airflow_systemd.SystemdSSHTask
        cfg:
          scope: user
          command_prefix: source /etc/profile &&
          ssh_operator_args:
            ssh_conn_id: systemd-host
          service:
            report:
              service:
                type: exec
                exec_start: /opt/jobs/report
```

Configuration and cleanup use Airflow's SSH operator. Status and lifecycle calls
use a `SystemdClient` command runner backed by the same SSH connection.

## How to chain the lifecycle with other tasks

The `Systemd` object behaves like a task group boundary:

```python
prepare >> systemd >> publish
```

Upstream dependencies attach to `configure_systemd`. Downstream dependencies
attach to `unconfigure_systemd`, including when cleanup is represented by a skip
task.
