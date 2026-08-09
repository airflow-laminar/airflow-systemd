# airflow_systemd.TimerConfiguration

### *pydantic model* airflow_systemd.TimerConfiguration[[source]](../../../_modules/systemd_pydantic/models.html.md#TimerConfiguration)

Bases: `_Section`

Activation settings from a systemd `[Timer]` section.

#### section_name *: ClassVar[str]* *= 'Timer'*

#### directives *: ClassVar[dict[str, str]]* *= {'accuracy_sec': 'AccuracySec', 'defer_reactivation': 'DeferReactivation', 'fixed_random_delay': 'FixedRandomDelay', 'on_active_sec': 'OnActiveSec', 'on_boot_sec': 'OnBootSec', 'on_calendar': 'OnCalendar', 'on_clock_change': 'OnClockChange', 'on_startup_sec': 'OnStartupSec', 'on_timezone_change': 'OnTimezoneChange', 'on_unit_active_sec': 'OnUnitActiveSec', 'on_unit_inactive_sec': 'OnUnitInactiveSec', 'persistent': 'Persistent', 'randomized_delay_sec': 'RandomizedDelaySec', 'randomized_offset_sec': 'RandomizedOffsetSec', 'remain_after_elapse': 'RemainAfterElapse', 'unit': 'Unit', 'wake_system': 'WakeSystem'}*

#### repeated *: ClassVar[frozenset[str]]* *= frozenset({'on_active_sec', 'on_boot_sec', 'on_calendar', 'on_startup_sec', 'on_unit_active_sec', 'on_unit_inactive_sec'})*

#### *field* on_active_sec *: list[TimeSpan]* *[Optional]*

#### *field* on_boot_sec *: list[TimeSpan]* *[Optional]*

#### *field* on_startup_sec *: list[TimeSpan]* *[Optional]*

#### *field* on_unit_active_sec *: list[TimeSpan]* *[Optional]*

#### *field* on_unit_inactive_sec *: list[TimeSpan]* *[Optional]*

#### *field* on_calendar *: list[str]* *[Optional]*

#### *field* accuracy_sec *: TimeSpan | None* *= None*

#### *field* randomized_delay_sec *: TimeSpan | None* *= None*

#### *field* fixed_random_delay *: bool | None* *= None*

#### *field* randomized_offset_sec *: TimeSpan | None* *= None*

#### *field* defer_reactivation *: bool | None* *= None*

#### *field* on_clock_change *: bool | None* *= None*

#### *field* on_timezone_change *: bool | None* *= None*

#### *field* unit *: str | None* *= None*

#### *field* persistent *: bool | None* *= None*

#### *field* wake_system *: bool | None* *= None*

#### *field* remain_after_elapse *: bool | None* *= None*
