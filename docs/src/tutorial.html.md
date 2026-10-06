# Tutorial: run your first systemd job

We will run a five-second service from Airflow, monitor its completion, and
remove its unit file and saved configuration.

Use an initialized Airflow 2 environment on Linux with systemd. Run the DAG
parser and all tasks as the same Unix user on that host. The user needs a
running systemd user manager and permission to write its home directory.

## Check the user manager

Run these commands as the Airflow user:

```bash
systemctl --user show -p Version
test ! -e "$HOME/.config/systemd/user/airflow-systemd-demo.service"
```

The first command prints the manager’s version. The second exits successfully
when the tutorial’s unit filename is unused. If the first command cannot connect
to the user bus, complete the [user manager setup](how-to.html.md#how-to-prepare-a-user-manager)
before continuing.

## Install the integration

In the Airflow environment, run:

```bash
pip install 'airflow-systemd[airflow]'
```

## Create the DAG

Save this as `systemd_demo.py` in your Airflow DAG folder:

```python
from datetime import datetime, timezone
from pathlib import Path

from airflow import DAG
from airflow_systemd import ServiceConfiguration, ServiceUnitConfiguration, Systemd, SystemdAirflowConfiguration

with DAG(
    dag_id="systemd-demo",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
) as dag:
    systemd = Systemd(
        dag=dag,
        cfg=SystemdAirflowConfiguration(
            scope="user",
            unit_dir=Path.home() / ".config/systemd/user",
            working_dir=Path.home() / ".local/state/airflow-systemd-demo",
            service={
                "airflow-systemd-demo": ServiceUnitConfiguration(
                    service=ServiceConfiguration(type="exec", exec_start="/bin/sleep 5"),
                ),
            },
        ),
    )
```

List the generated tasks:

```bash
airflow tasks list systemd-demo
```

Look for `systemd-demo-configure-systemd`, `systemd-demo-start-services`, and
`systemd-demo-check-services`. Restart, stop, cleanup, and failure-handling tasks
also appear.

## Run the service

Execute one DAG run locally:

```bash
airflow dags test systemd-demo 2025-01-01
```

The configure task writes the service unit and `pydantic.json`, then reloads the
user manager. The start task runs `/bin/sleep`. After the service finishes, the
check task takes its success branch. Stop and cleanup remove the unit and saved
configuration, then reload the manager again. The DAG run finishes with state
`success`; restart and force-kill branches are skipped.

Check the two generated paths:

```bash
test ! -e "$HOME/.config/systemd/user/airflow-systemd-demo.service" && echo "Unit removed"
test ! -d "$HOME/.local/state/airflow-systemd-demo" && echo "State removed"
```

You should see `Unit removed` and `State removed`.

For existing deployments, follow the [local and SSH guides](how-to.html.md). The
[configuration reference](api.html.md) lists scope and lifecycle settings.
