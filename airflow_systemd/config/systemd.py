from datetime import time, timedelta
from typing import Literal

from airflow_pydantic import Pool
from pydantic import Field
from systemd_pydantic import SystemdConvenienceConfiguration

__all__ = ("SystemdAirflowConfiguration", "load_airflow_config")


class SystemdAirflowConfiguration(SystemdConvenienceConfiguration):
    """Systemd configuration for an Airflow-managed job."""

    check_interval: timedelta = Field(default=timedelta(seconds=5), description="Interval between service status checks")
    check_timeout: timedelta = Field(default=timedelta(hours=8), description="Timeout for service status checks")

    runtime: timedelta | None = Field(default=None, description="Maximum runtime of the systemd job")
    endtime: time | None = Field(default=None, description="End time of the systemd job")
    maxretrigger: int | None = Field(default=None, description="Maximum number of service check retriggers")
    reference_date: Literal["start_date", "logical_date", "data_interval_end"] = Field(
        default="data_interval_end",
        description="Date used to evaluate runtime and endtime",
    )

    pool: str | Pool | None = Field(default=None, description="Airflow pool for systemd tasks")
    stop_on_exit: bool = Field(default=True, description="Stop services when the DAG finishes")
    cleanup: bool = Field(default=True, description="Remove generated unit files when the DAG finishes")
    restart_on_initial: bool = Field(default=False, description="Restart services on an initial Airflow run")
    restart_on_retrigger: bool = Field(default=False, description="Restart services when airflow-ha retriggers the job")


load_airflow_config = SystemdAirflowConfiguration.load
