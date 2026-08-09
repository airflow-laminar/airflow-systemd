# airflow_systemd.SystemdConfiguration

### *pydantic model* airflow_systemd.SystemdConfiguration[[source]](../../../_modules/systemd_pydantic/config/systemd.html.md#SystemdConfiguration)

Bases: `BaseModel`

Named collection of systemd service and timer unit files.

#### *field* service *: dict[str, [ServiceUnitConfiguration](airflow_systemd.ServiceUnitConfiguration.html.md#airflow_systemd.ServiceUnitConfiguration)]* *[Required]*

#### *field* timer *: dict[str, [TimerUnitConfiguration](airflow_systemd.TimerUnitConfiguration.html.md#airflow_systemd.TimerUnitConfiguration)]* *[Optional]*

#### *field* unit_dir *: Path | None* *= None*

#### *field* working_dir *: Path | None* *= None*

#### *field* scope *: SystemdScope* *= 'system'*

#### to_cfg() → dict[str, str][[source]](../../../_modules/systemd_pydantic/config/systemd.html.md#SystemdConfiguration.to_cfg)

#### *property* service_names *: list[str]*

#### *property* timer_names *: list[str]*

#### *property* unit_paths *: list[Path]*

#### write() → list[Path][[source]](../../../_modules/systemd_pydantic/config/systemd.html.md#SystemdConfiguration.write)

#### rmdir() → None[[source]](../../../_modules/systemd_pydantic/config/systemd.html.md#SystemdConfiguration.rmdir)

#### *classmethod* load(config_dir: str = 'config', config_name: str = '', overrides: list[str] | None = None, , basepath: str = '', \_offset: int = 3) → Self[[source]](../../../_modules/systemd_pydantic/config/systemd.html.md#SystemdConfiguration.load)

#### start() → dict[str, [UnitInfo](airflow_systemd.UnitInfo.html.md#airflow_systemd.UnitInfo)][[source]](../../../_modules/systemd_pydantic/config/systemd.html.md#SystemdConfiguration.start)

#### running() → bool[[source]](../../../_modules/systemd_pydantic/config/systemd.html.md#SystemdConfiguration.running)

#### stop() → dict[str, [UnitInfo](airflow_systemd.UnitInfo.html.md#airflow_systemd.UnitInfo)][[source]](../../../_modules/systemd_pydantic/config/systemd.html.md#SystemdConfiguration.stop)

#### kill() → dict[str, [UnitInfo](airflow_systemd.UnitInfo.html.md#airflow_systemd.UnitInfo)][[source]](../../../_modules/systemd_pydantic/config/systemd.html.md#SystemdConfiguration.kill)
