# airflow_systemd.SystemdConfiguration

### *pydantic model* airflow_systemd.SystemdConfiguration

Bases: `BaseModel`

Named collection of systemd service and timer unit files.

#### *field* service *: dict[str, [ServiceUnitConfiguration](airflow_systemd.ServiceUnitConfiguration.md#airflow_systemd.ServiceUnitConfiguration)]* *[Required]*

#### *field* timer *: dict[str, [TimerUnitConfiguration](airflow_systemd.TimerUnitConfiguration.md#airflow_systemd.TimerUnitConfiguration)]* *[Optional]*

#### *field* unit_dir *: Path | None* *= None*

#### *field* working_dir *: Path | None* *= None*

#### *field* scope *: SystemdScope* *= 'system'*

#### to_cfg() → dict[str, str]

#### *property* service_names *: list[str]*

#### *property* timer_names *: list[str]*

#### *property* unit_paths *: list[Path]*

#### write() → list[Path]

#### rmdir() → None

#### *classmethod* load(config_dir: str = 'config', config_name: str = '', overrides: list[str] | None = None, , basepath: str = '', \_offset: int = 3) → Self

#### start() → dict[str, [UnitInfo](airflow_systemd.UnitInfo.md#airflow_systemd.UnitInfo)]

#### running() → bool

#### stop() → dict[str, [UnitInfo](airflow_systemd.UnitInfo.md#airflow_systemd.UnitInfo)]

#### kill() → dict[str, [UnitInfo](airflow_systemd.UnitInfo.md#airflow_systemd.UnitInfo)]
