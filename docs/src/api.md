# API reference

## Airflow lifecycle

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

## Re-exported systemd models

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
