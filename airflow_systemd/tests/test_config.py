from datetime import timedelta

from airflow_systemd import SystemdAirflowConfiguration


def test_airflow_configuration_defaults(systemd_airflow_configuration: SystemdAirflowConfiguration):
    assert systemd_airflow_configuration.check_interval == timedelta(seconds=5)
    assert systemd_airflow_configuration.check_timeout == timedelta(hours=8)
    assert systemd_airflow_configuration.stop_on_exit is True
    assert systemd_airflow_configuration.cleanup is True


def test_airflow_configuration_roundtrip(systemd_airflow_configuration: SystemdAirflowConfiguration):
    value = SystemdAirflowConfiguration.model_validate_json(systemd_airflow_configuration.model_dump_json())

    assert value == systemd_airflow_configuration
    assert value._pydantic_path == systemd_airflow_configuration._pydantic_path
