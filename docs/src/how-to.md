---
myst:
  heading_anchors: 3
---

# How-to guides

Run systemd services on an Airflow worker or an SSH host, with configuration in
Python or `airflow-config` YAML.

| Execution    | Inline Python                                              | `airflow-config`                                                   |
| ------------ | ---------------------------------------------------------- | ------------------------------------------------------------------ |
| Local worker | [Local Python DAG](#how-to-run-a-local-service-in-python)  | [Local YAML DAG](#how-to-run-a-local-service-with-airflow-config)  |
| SSH host     | [SSH Python DAG](#how-to-run-a-service-over-ssh-in-python) | [SSH YAML DAG](#how-to-run-a-service-over-ssh-with-airflow-config) |

## How to prepare a user manager

For `scope="user"`, run Airflow tasks or SSH commands as the account that owns
the services. On the target Linux host, check access as that account:

```bash
systemctl --user show -p Version
```

If services must remain available after logout, have an administrator enable
lingering for the service account, here named `airflow`:

```bash
sudo loginctl enable-linger airflow
```

For an Airflow worker or non-interactive SSH session without the user bus
variables, set them in that process's environment:

```bash
export XDG_RUNTIME_DIR="/run/user/$(id -u)"
export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"
```

Check `systemctl --user show -p Version` again. The user manager and its bus must
already be running; setting the variables only selects their addresses. For SSH,
put these exports in `cfg.command_prefix` so they apply to every remote command.

## How to run a local service in Python

Install `airflow-systemd[airflow]` in Airflow 2, or
`airflow-systemd[airflow3]` in Airflow 3. Complete the
[user manager setup](#how-to-prepare-a-user-manager).

Run all lifecycle tasks on the same Linux host as the same Unix user. Use one
worker host or route this DAG to a queue served by that host. Shared storage
does not provide access to another host's systemd manager.

Save this DAG in the DAG folder. Replace the command and paths for your worker
account, and choose a unit name reserved for this DAG:

```python
from datetime import datetime, timezone

from airflow import DAG
from airflow_systemd import ServiceConfiguration, ServiceUnitConfiguration, Systemd, SystemdAirflowConfiguration

with DAG(
    dag_id="local-systemd",
    schedule="@daily",
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
) as dag:
    systemd = Systemd(
        dag=dag,
        cfg=SystemdAirflowConfiguration(
            scope="user",
            unit_dir="/home/airflow/.config/systemd/user",
            working_dir="/var/tmp/local-systemd",
            service={
                "airflow-local-batch": ServiceUnitConfiguration(
                    service=ServiceConfiguration(type="exec", exec_start="/bin/sleep 5"),
                ),
            },
        ),
    )
```

Run `airflow tasks list local-systemd`, then trigger `local-systemd`.

## How to run a local service with airflow-config

Use the packages and worker placement from the
[local Python guide](#how-to-run-a-local-service-in-python). Install
`airflow-config` in the DAG parsing environment.

Create `config/local_systemd.yaml` beside the DAG loader:

```yaml
# @package _global_
_target_: airflow_config.Configuration

dags:
  local-systemd:
    schedule: "@daily"
    start_date: "2025-01-01"
    catchup: false
    tasks:
      run:
        _target_: airflow_systemd.SystemdTask
        cfg:
          scope: user
          unit_dir: /home/airflow/.config/systemd/user
          working_dir: /var/tmp/local-systemd
          service:
            airflow-local-batch:
              service:
                type: exec
                exec_start: /bin/sleep 5
```

Replace paths and the command for your worker account. Save `local_systemd.py`
in the DAG folder:

```python
from airflow_config import load_config

config = load_config("config", "local_systemd")
config.generate_in_mem()
```

Run `airflow tasks list local-systemd`, then trigger `local-systemd`. Deploy
either this loader or the inline Python DAG for that DAG ID.

## How to run a service over SSH in Python

Install `airflow-systemd[airflow]` in Airflow 2, or
`airflow-systemd[airflow3]` in Airflow 3. These extras include the SSH provider.
On the remote Linux host, install the convenience commands:

```bash
pip install systemd-pydantic
```

Create an Airflow SSH connection named `systemd-host` for the `airflow` account
on your target host. Complete the [user manager setup](#how-to-prepare-a-user-manager)
for that account. Ensure `systemctl` and `_systemd_convenience` are on the remote
non-interactive shell's `PATH`.

Set `unit_dir` and `working_dir` to explicit absolute paths on the remote host.
Replace `/home/airflow` below if the SSH account has a different home. If the
remote package is in a virtual environment, prepend its activation command to
`command_prefix`, for example `source /opt/systemd-venv/bin/activate`.

Save this DAG in the DAG folder:

```python
from datetime import datetime, timezone

from airflow import DAG
from airflow_pydantic import SSHOperatorArgs
from airflow_systemd import ServiceConfiguration, ServiceUnitConfiguration, SystemdSSH, SystemdSSHAirflowConfiguration

with DAG(
    dag_id="ssh-systemd",
    schedule="@daily",
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
) as dag:
    systemd = SystemdSSH(
        dag=dag,
        cfg=SystemdSSHAirflowConfiguration(
            scope="user",
            unit_dir="/home/airflow/.config/systemd/user",
            working_dir="/var/tmp/ssh-systemd",
            command_prefix=(
                'export XDG_RUNTIME_DIR="/run/user/$(id -u)"\n'
                'export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"'
            ),
            ssh_operator_args=SSHOperatorArgs(ssh_conn_id="systemd-host"),
            service={
                "airflow-ssh-batch": ServiceUnitConfiguration(
                    service=ServiceConfiguration(type="exec", exec_start="/bin/sleep 5"),
                ),
            },
        ),
    )
```

Run `airflow tasks list ssh-systemd`, then trigger `ssh-systemd`. Service start,
checks, restart, stop, and cleanup all use the configured SSH connection.

## How to run a service over SSH with airflow-config

Complete the remote package, SSH connection, and user manager setup from the
[SSH Python guide](#how-to-run-a-service-over-ssh-in-python). Install
`airflow-config` in the DAG parsing environment.

Create `config/ssh_systemd.yaml` beside the DAG loader, replacing paths and the
command for your SSH account:

```yaml
# @package _global_
_target_: airflow_config.Configuration

dags:
  ssh-systemd:
    schedule: "@daily"
    start_date: "2025-01-01"
    catchup: false
    tasks:
      run:
        _target_: airflow_systemd.SystemdSSHTask
        cfg:
          scope: user
          unit_dir: /home/airflow/.config/systemd/user
          working_dir: /var/tmp/ssh-systemd
          command_prefix: |-
            export XDG_RUNTIME_DIR="/run/user/$(id -u)"
            export DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"
          ssh_operator_args:
            ssh_conn_id: systemd-host
          service:
            airflow-ssh-batch:
              service:
                type: exec
                exec_start: /bin/sleep 5
```

If needed, add `source /opt/systemd-venv/bin/activate` as the first line of
`command_prefix`. Save `ssh_systemd.py` in the DAG folder:

```python
from airflow_config import load_config

config = load_config("config", "ssh_systemd")
config.generate_in_mem()
```

Run `airflow tasks list ssh-systemd`, then trigger `ssh-systemd`. Deploy either
this loader or the inline Python DAG for that DAG ID.

## How to use the system manager

Set `scope="system"` and `unit_dir="/etc/systemd/system"` on either Python
configuration model, or set these fields under `cfg` in YAML:

```yaml
scope: system
unit_dir: /etc/systemd/system
```

Run the lifecycle as an account authorized to write that directory and issue
system-wide `systemctl` commands. For SSH, select that account in the Airflow
connection. The client does not add `sudo` to commands. Set `service.user` on
each service if the workload should run as a different Unix user:

```yaml
service:
  airflow-system-batch:
    service:
      type: exec
      exec_start: /opt/jobs/batch
      user: airflow
```

Use a writable `working_dir` for the lifecycle account. Apply the scope and unit
directory together; changing `scope` on an already constructed model does not
recompute an existing `unit_dir`.

## How to limit monitoring or keep a service running

Set monitoring limits under `cfg` in local or SSH YAML:

```yaml
check_interval: 00:00:10
check_timeout: 08:00:00
runtime: 04:00:00
maxretrigger: 3
```

In Python, use `timedelta(seconds=10)`, `timedelta(hours=8)`, and
`timedelta(hours=4)` for the three duration fields, importing `timedelta` from
`datetime`. Use `runtime` or `endtime` to end monitoring through the stop branch;
`check_timeout` is the sensor timeout. See the
[timing reference](api.md#monitoring-and-lifecycle-fields) for reference dates.

To retain a service between runs, set `stop_on_exit=False`, `cleanup=False`,
`restart_on_initial=True`, and `restart_on_retrigger=True` in Python, or under
`cfg` in YAML:

```yaml
stop_on_exit: false
cleanup: false
restart_on_initial: true
restart_on_retrigger: true
runtime: 04:00:00
```

Keep unit names, scope, and paths stable across runs. Set an end condition for
monitoring a service that never exits. To let systemd restart it between Airflow
runs, set `restart: on-failure` inside its `service` section.

## How to chain the lifecycle with other tasks

In Python, connect existing Airflow tasks to the `Systemd` or `SystemdSSH`
object:

```python
prepare >> systemd >> publish
```

In `airflow-config`, use the task mapping key in dependencies:

```yaml
tasks:
  prepare:
    _target_: airflow_pydantic.BashTask
    bash_command: echo prepare
  run:
    _target_: airflow_systemd.SystemdTask
    dependencies: [prepare]
    cfg:
      scope: user
      unit_dir: /home/airflow/.config/systemd/user
      working_dir: /var/tmp/chained-systemd
      service:
        airflow-chained-batch:
          service:
            type: exec
            exec_start: /bin/sleep 5
  publish:
    _target_: airflow_pydantic.BashTask
    bash_command: echo publish
    dependencies: [run]
```

Upstream tasks precede configuration; downstream tasks follow unconfiguration.
Keep stop and cleanup enabled for downstream tasks with the default
`all_success` trigger rule. Disabling cleanup creates a skipped boundary task.
