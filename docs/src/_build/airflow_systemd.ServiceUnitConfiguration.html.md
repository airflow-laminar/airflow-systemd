# airflow_systemd.ServiceUnitConfiguration

### *pydantic model* airflow_systemd.ServiceUnitConfiguration[[source]](../../../_modules/systemd_pydantic/models.html.md#ServiceUnitConfiguration)

Bases: `_SystemdConfiguration`

#### section_order *: ClassVar[tuple[str, ...]]* *= ('unit', 'service', 'install')*

#### *field* unit *: UnitConfiguration | None* *= None*

#### *field* service *: [ServiceConfiguration](airflow_systemd.ServiceConfiguration.html.md#airflow_systemd.ServiceConfiguration)* *[Required]*

#### *field* install *: InstallConfiguration | None* *= None*
