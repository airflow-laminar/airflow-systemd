from pathlib import Path

import pytest

from airflow_systemd import ServiceConfiguration, ServiceUnitConfiguration, SystemdAirflowConfiguration


@pytest.fixture
def systemd_airflow_configuration(tmp_path: Path) -> SystemdAirflowConfiguration:
    return SystemdAirflowConfiguration(
        service={
            "test": ServiceUnitConfiguration(
                service=ServiceConfiguration(type="exec", exec_start="/bin/echo hello"),
            )
        },
        unit_dir=tmp_path / "units",
        working_dir=tmp_path / "state",
        scope="user",
        pool="test-pool",
    )
