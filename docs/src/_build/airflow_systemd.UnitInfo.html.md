# airflow_systemd.UnitInfo

### *pydantic model* airflow_systemd.UnitInfo[[source]](../../../_modules/systemd_pydantic/client/systemctl.html.md#UnitInfo)

Bases: `BaseModel`

#### *field* name *: str* *[Required]*

#### *field* load_state *: str* *= ''*

#### *field* active_state *: str* *= ''*

#### *field* sub_state *: str* *= ''*

#### *field* result *: str* *= ''*

#### *field* exec_main_code *: str* *= ''*

#### *field* exec_main_status *: int | None* *= None*

#### running() → bool[[source]](../../../_modules/systemd_pydantic/client/systemctl.html.md#UnitInfo.running)

#### stopped() → bool[[source]](../../../_modules/systemd_pydantic/client/systemctl.html.md#UnitInfo.stopped)

#### done(ok_exitstatuses: list[int | str] | None = None) → bool[[source]](../../../_modules/systemd_pydantic/client/systemctl.html.md#UnitInfo.done)

#### ok(ok_exitstatuses: list[int | str] | None = None) → bool[[source]](../../../_modules/systemd_pydantic/client/systemctl.html.md#UnitInfo.ok)

#### bad(ok_exitstatuses: list[int | str] | None = None) → bool[[source]](../../../_modules/systemd_pydantic/client/systemctl.html.md#UnitInfo.bad)
