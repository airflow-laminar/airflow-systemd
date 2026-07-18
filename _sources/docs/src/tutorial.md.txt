# Tutorial: run a systemd job from Airflow

In this tutorial, we will define a user-scoped systemd job in `airflow-config`
YAML and load it as an Airflow DAG.

## Install the packages

For Airflow 3, run:

```bash
pip install 'airflow-systemd[airflow3]' airflow-config
```

Use the `airflow` extra instead when running Airflow 2. The worker must have a
user systemd manager and permission to write its user unit directory.

## Define the DAG

Create `config/systemd.yaml`:

```yaml
dags:
  nightly-systemd:
    schedule: "@daily"
    start_date: "2024-01-01"
    catchup: false
    tasks:
      run-nightly:
        _target_: airflow_systemd.SystemdTask
        cfg:
          scope: user
          stop_on_exit: true
          cleanup: true
          service:
            nightly:
              unit:
                description: Nightly batch job
              service:
                type: exec
                exec_start: /opt/jobs/nightly
```

## Load the configuration

Create `nightly_systemd.py` in the DAG folder:

```python
from airflow_config import load_config

config = load_config("config", "systemd")
config.generate_in_mem()
```

## Inspect the lifecycle

Parse the DAG folder:

```bash
airflow dags list | grep nightly-systemd
airflow tasks list nightly-systemd
```

The task list includes the configure, start, check, restart, stop, and
unconfigure steps created by `Systemd`.

Trigger the DAG in a test environment containing `/opt/jobs/nightly`. The check
step remains active while the service runs and completes after systemd reports a
successful stopped unit.

You have now connected a declarative Airflow DAG to a systemd-managed process.
