---
myst:
  heading_anchors: 3
---

# API reference

## Lifecycle classes and task models

All names below are exported from `airflow_systemd`.

| Execution | Lifecycle class | Configuration model              | `airflow-config` task model |
| --------- | --------------- | -------------------------------- | --------------------------- |
| Local     | `Systemd`       | `SystemdAirflowConfiguration`    | `SystemdTask`               |
| SSH       | `SystemdSSH`    | `SystemdSSHAirflowConfiguration` | `SystemdSSHTask`            |

`Systemd(dag, cfg, **kwargs)` adds lifecycle tasks to an existing Airflow DAG.
`cfg` accepts a configuration model or a dictionary validated as that model.
The optional `systemd_client` keyword supplies a client for client-backed
operations.

`SystemdSSH(dag, cfg, host=None, **kwargs)` adds the same lifecycle with SSH
configuration operators and an SSH-backed service client. `host` accepts an
`airflow-pydantic` `Host` or a dictionary validated as one. It overrides the
SSH target and hook; its pool is used when `cfg.pool` is unset. Constructor
keywords can override `command_prefix` and fields in `SSHOperatorArgs`.

`SystemdTaskArgs` contains `cfg` and inherited Airflow task arguments.
`SystemdSSHTaskArgs` adds optional `host: Host`. The task models' `operator`
fields resolve to their corresponding lifecycle classes and reject other
operators. `SystemdOperator`, `SystemdOperatorArgs`, `SystemdSSHOperator`, and
`SystemdSSHOperatorArgs` alias the corresponding task models.

### DAG constraints and boundaries

Both lifecycle classes set `catchup=False`, `concurrency=1`,
`max_active_tasks=1`, and `max_active_runs=1`. Generated task IDs use
`<dag_id>-<step>`, independent of a task model's `task_id`. A DAG supports one
systemd lifecycle; multiple services belong in its `cfg.service` mapping.

The exposed boundaries are `configure_systemd`, `start_services`,
`check_services`, `restart_services`, `stop_services`, and
`unconfigure_systemd`. Upstream dependencies attach to configuration;
downstream dependencies attach to unconfiguration. `systemd_client` returns the
client stored by the lifecycle.

Stop and cleanup follow the successful monitoring branch. They are not a
failure finalizer. `cleanup=False` creates a skipped unconfiguration task.
`stop_on_exit=False` creates skipped stop and unconfiguration tasks, regardless
of `cleanup`. These skipped boundaries affect downstream `all_success` tasks.

## Configuration models

`SystemdAirflowConfiguration` extends `SystemdConvenienceConfiguration`.
`SystemdSSHAirflowConfiguration` adds SSH settings. Both inherit systemd unit
models and path handling from `SystemdConfiguration`.

### Systemd fields

| Field                 | Default                     | Meaning                                                                                                |
| --------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------ |
| `service`             | Required                    | Mapping of unit names to `ServiceUnitConfiguration` models. Names without a suffix receive `.service`. |
| `timer`               | Empty mapping               | Timer unit models. Configuration writes them; the Airflow lifecycle does not start or enable timers.   |
| `scope`               | `system`                    | Manager scope: `system` or `user`. User scope adds `--user` to `systemctl` commands.                   |
| `unit_dir`            | Scope-dependent             | `/etc/systemd/system` for system scope; the parsing user's `~/.config/systemd/user` for user scope.    |
| `working_dir`         | Derived temporary directory | Directory for persisted configuration. Resolved on the parsing host when omitted.                      |
| `restart`             | `no`                        | Default `Restart=` policy for services without their own value.                                        |
| `timeout_stop_sec`    | `30s`                       | Default service stop timeout.                                                                          |
| `kill_mode`           | `control-group`             | Default termination behavior for a service's processes.                                                |
| `kill_signal`         | `SIGTERM`                   | Default stop signal.                                                                                   |
| `success_exit_status` | `[0]`                       | Accepted exit statuses used by service configuration and monitoring.                                   |
| `command_timeout`     | `60`                        | `systemctl` command timeout in seconds.                                                                |

Per-service values take precedence over convenience defaults. `exec_start`
accepts a string or list of commands; multiple commands require `type="oneshot"`.
Commands follow systemd `ExecStart=` syntax. Shell operators require an explicit
shell command. `working_dir` stores lifecycle state; a service's
`working_directory` sets its process working directory.

Configuration writes unit files under `unit_dir` and `pydantic.json` under
`working_dir`, then reloads the manager. Cleanup stops configured timers and
services, removes their unit files and saved JSON, reloads the manager, and
removes `working_dir` only if empty. The shared unit directory remains.
Units are started directly; configuration does not enable them for boot.

`systemd_json()` returns JSON containing only fields accepted by
`SystemdConvenienceConfiguration`, excluding Airflow and SSH settings.

### Monitoring and lifecycle fields

| Field                  | Default             | Meaning                                                                           |
| ---------------------- | ------------------- | --------------------------------------------------------------------------------- |
| `check_interval`       | 5 seconds           | Polling interval for the `airflow-ha` sensor.                                     |
| `check_timeout`        | 8 hours             | Sensor timeout.                                                                   |
| `runtime`              | `None`              | Monitoring end condition relative to `reference_date`.                            |
| `endtime`              | `None`              | Time-of-day end condition passed to `airflow-ha`.                                 |
| `maxretrigger`         | `None`              | Retrigger limit passed to `airflow-ha`.                                           |
| `reference_date`       | `data_interval_end` | Reference for end conditions; also accepts `start_date` or `logical_date`.        |
| `pool`                 | `None`              | Airflow pool name or `airflow-pydantic` `Pool`.                                   |
| `stop_on_exit`         | `True`              | Enables service stop on the success path.                                         |
| `cleanup`              | `True`              | Enables unconfiguration when `stop_on_exit` is also true.                         |
| `restart_on_initial`   | `False`             | Restarts services on an initial Airflow run.                                      |
| `restart_on_retrigger` | `False`             | Uses restart during the startup step; takes precedence over `restart_on_initial`. |

Duration fields accept Python `timedelta` values or numeric seconds and duration
strings in YAML. They are passed to `HighAvailabilityOperator` as `poke_interval`,
`timeout`, `runtime`, `endtime`, `maxretrigger`, and `reference_date`. The sensor
uses `mode="poke"`.

### SSH fields and command runner

| Field               | Default                 | Meaning                                                                |
| ------------------- | ----------------------- | ---------------------------------------------------------------------- |
| `command_prefix`    | Empty string            | Shell commands prepended to remote configuration and service commands. |
| `ssh_operator_args` | Empty `SSHOperatorArgs` | SSH connection, hook, host, environment, PTY, and timeout settings.    |

`AirflowSSHCommandRunner` accepts an optional `hook`, `command_prefix`,
`environment`, `get_pty`, `ssh_conn_id`, `remote_host`, `conn_timeout`,
`cmd_timeout`, and `banner_timeout`. `get_hook()` constructs an Airflow SSH hook
lazily when no hook was supplied. `run(command: list[str], timeout: int)` shell
quotes the command arguments, applies the prefix, and returns a
`systemd-pydantic` `CommandResult` with exit status and decoded stdout/stderr.

`load_airflow_config` aliases `SystemdAirflowConfiguration.load`.
`load_airflow_ssh_config` aliases `SystemdSSHAirflowConfiguration.load`.
These load systemd configuration models; `airflow_config.load_config` loads
collections of declarative DAGs. The [how-to guides](how-to.md) cover that
workflow.

## Generated API

```{eval-rst}
.. currentmodule:: airflow_systemd

.. autosummary::
   :toctree: _build

   Systemd
   SystemdSSH
   AirflowSSHCommandRunner
   SystemdAirflowConfiguration
   SystemdSSHAirflowConfiguration
   SystemdTask
   SystemdTaskArgs
   SystemdSSHTask
   SystemdSSHTaskArgs
   load_airflow_config
   load_airflow_ssh_config
```

### Re-exported systemd models

```{eval-rst}
.. currentmodule:: airflow_systemd

.. autosummary::
   :toctree: _build

   ServiceConfiguration
   ServiceUnitConfiguration
   TimerConfiguration
   TimerUnitConfiguration
   SystemdConfiguration
   SystemdConvenienceConfiguration
   SystemdClient
   UnitInfo
```
