# airflow_systemd.TimerUnitConfiguration

### *pydantic model* airflow_systemd.TimerUnitConfiguration

Bases: `_SystemdConfiguration`

#### section_order *: ClassVar[tuple[str, ...]]* *= ('unit', 'timer', 'install')*

#### *field* unit *: UnitConfiguration | None* *= None*

#### *field* timer *: [TimerConfiguration](airflow_systemd.TimerConfiguration.md#airflow_systemd.TimerConfiguration)* *[Required]*

#### *field* install *: InstallConfiguration | None* *= None*
