from datetime import timedelta

from systemd_pydantic import SystemdConvenienceConfiguration

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


def test_systemd_json_excludes_airflow_fields(systemd_airflow_configuration: SystemdAirflowConfiguration):
    value = SystemdConvenienceConfiguration.model_validate_json(systemd_airflow_configuration.systemd_json())

    assert value.service == systemd_airflow_configuration.service
    assert "check_interval" not in systemd_airflow_configuration.systemd_json()
