# airflow_systemd.UnitInfo

### *pydantic model* airflow_systemd.UnitInfo

Bases: `BaseModel`

#### *field* name *: str* *[Required]*

#### *field* load_state *: str* *= ''*

#### *field* active_state *: str* *= ''*

#### *field* sub_state *: str* *= ''*

#### *field* result *: str* *= ''*

#### *field* exec_main_code *: str* *= ''*

#### *field* exec_main_status *: int | None* *= None*

#### running() → bool

#### stopped() → bool

#### done(ok_exitstatuses: list[int | str] | None = None) → bool

#### ok(ok_exitstatuses: list[int | str] | None = None) → bool

#### bad(ok_exitstatuses: list[int | str] | None = None) → bool
