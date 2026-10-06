# airflow-systemd

Run and monitor systemd-managed jobs from Apache Airflow.

[![Build Status](https://github.com/airflow-laminar/airflow-systemd/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/airflow-laminar/airflow-systemd/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/airflow-laminar/airflow-systemd/branch/main/graph/badge.svg)](https://codecov.io/gh/airflow-laminar/airflow-systemd)
[![License](https://img.shields.io/github/license/airflow-laminar/airflow-systemd)](https://github.com/airflow-laminar/airflow-systemd)
[![PyPI](https://img.shields.io/pypi/v/airflow-systemd.svg)](https://pypi.python.org/pypi/airflow-systemd)

Manage services on an Airflow worker's systemd manager or on an SSH host.
Define units directly in a Python DAG or in `airflow-config` YAML.

```python
from datetime import datetime, timezone
from pathlib import Path

from airflow import DAG
from airflow_systemd import ServiceConfiguration, ServiceUnitConfiguration, Systemd, SystemdAirflowConfiguration

with DAG(
    dag_id="nightly-systemd",
    schedule="@daily",
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
) as dag:
    systemd = Systemd(
        dag=dag,
        cfg=SystemdAirflowConfiguration(
            scope="user",
            unit_dir=Path.home() / ".config/systemd/user",
            working_dir=Path.home() / ".local/state/nightly-systemd",
            service={
                "airflow-nightly": ServiceUnitConfiguration(
                    service=ServiceConfiguration(type="exec", exec_start="/bin/sleep 5"),
                ),
            },
        ),
    )
```

The lifecycle writes unit files, reloads the manager, starts services, monitors
state with `airflow-ha`, and stops and removes generated configuration on
successful completion. `SystemdSSH` performs configuration and service
operations over the configured SSH connection.

## Documentation

Start with the [tutorial](docs/src/tutorial.md) to run a self-contained local
service and check cleanup. For an existing deployment, choose a how-to guide:

| Execution    | Inline Python                                                                        | `airflow-config` YAML                                                                            |
| ------------ | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| Local worker | [Run a local service](docs/src/how-to.md#how-to-run-a-local-service-in-python)       | [Configure a local service](docs/src/how-to.md#how-to-run-a-local-service-with-airflow-config)   |
| SSH host     | [Run a service over SSH](docs/src/how-to.md#how-to-run-a-service-over-ssh-in-python) | [Configure an SSH service](docs/src/how-to.md#how-to-run-a-service-over-ssh-with-airflow-config) |

The [API reference](docs/src/api.md) describes scope, paths, monitoring defaults,
and DAG constraints. [Why Airflow owns the schedule](docs/src/explanation.md)
explains service ownership, user managers, remote paths, and restart policies.

Published documentation is available at
[airflow-laminar.github.io/airflow-systemd](https://airflow-laminar.github.io/airflow-systemd/).

## Ecosystem

- [systemd-pydantic](https://github.com/airflow-laminar/systemd-pydantic) supplies unit models and the systemctl client.
- [supervisor-pydantic](https://github.com/airflow-laminar/supervisor-pydantic) and [cron-pydantic](https://github.com/airflow-laminar/cron-pydantic) model alternative runtimes.
- [airflow-supervisor](https://github.com/airflow-laminar/airflow-supervisor) provides the analogous supervisord lifecycle.
- [airflow-cron](https://github.com/airflow-laminar/airflow-cron) converts cron jobs into ordinary Airflow tasks.
- [airflow-pydantic](https://github.com/airflow-laminar/airflow-pydantic) supplies declarative task and connection models.
- [airflow-config](https://github.com/airflow-laminar/airflow-config) produces YAML-driven DAGs.

> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
