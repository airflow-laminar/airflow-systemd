# airflow_systemd.ServiceConfiguration

### *pydantic model* airflow_systemd.ServiceConfiguration

Bases: `_Section`

Process supervision settings from a systemd `[Service]` section.

#### section_name *: ClassVar[str]* *= 'Service'*

#### directives *: ClassVar[dict[str, str]]* *= {'bus_name': 'BusName', 'environment': 'Environment', 'environment_file': 'EnvironmentFile', 'exec_condition': 'ExecCondition', 'exec_reload': 'ExecReload', 'exec_start': 'ExecStart', 'exec_start_post': 'ExecStartPost', 'exec_start_pre': 'ExecStartPre', 'exec_stop': 'ExecStop', 'exec_stop_post': 'ExecStopPost', 'group': 'Group', 'guess_main_pid': 'GuessMainPID', 'kill_mode': 'KillMode', 'kill_signal': 'KillSignal', 'pid_file': 'PIDFile', 'remain_after_exit': 'RemainAfterExit', 'restart': 'Restart', 'restart_force_exit_status': 'RestartForceExitStatus', 'restart_max_delay_sec': 'RestartMaxDelaySec', 'restart_prevent_exit_status': 'RestartPreventExitStatus', 'restart_randomized_delay_sec': 'RestartRandomizedDelaySec', 'restart_sec': 'RestartSec', 'restart_steps': 'RestartSteps', 'runtime_max_sec': 'RuntimeMaxSec', 'send_sigkill': 'SendSIGKILL', 'standard_error': 'StandardError', 'standard_output': 'StandardOutput', 'success_exit_status': 'SuccessExitStatus', 'supplementary_groups': 'SupplementaryGroups', 'timeout_start_sec': 'TimeoutStartSec', 'timeout_stop_sec': 'TimeoutStopSec', 'type': 'Type', 'umask': 'UMask', 'user': 'User', 'watchdog_sec': 'WatchdogSec', 'working_directory': 'WorkingDirectory'}*

#### repeated *: ClassVar[frozenset[str]]* *= frozenset({'environment_file', 'exec_condition', 'exec_reload', 'exec_start', 'exec_start_post', 'exec_start_pre', 'exec_stop', 'exec_stop_post'})*

#### space_separated *: ClassVar[frozenset[str]]* *= frozenset({'restart_force_exit_status', 'restart_prevent_exit_status', 'success_exit_status', 'supplementary_groups'})*

#### *field* type *: ServiceType | None* *= None*

#### *field* exec_condition *: list[str]* *[Optional]*

#### *field* exec_start_pre *: list[str]* *[Optional]*

#### *field* exec_start *: list[str]* *[Optional]*

#### *field* exec_start_post *: list[str]* *[Optional]*

#### *field* exec_reload *: list[str]* *[Optional]*

#### *field* exec_stop *: list[str]* *[Optional]*

#### *field* exec_stop_post *: list[str]* *[Optional]*

#### *field* restart *: RestartPolicy | None* *= None*

#### *field* restart_sec *: TimeSpan | None* *= None*

#### *field* restart_steps *: int | None* *= None*

#### *field* restart_max_delay_sec *: TimeSpan | None* *= None*

#### *field* restart_randomized_delay_sec *: TimeSpan | None* *= None*

#### *field* timeout_start_sec *: TimeSpan | Literal['infinity'] | None* *= None*

#### *field* timeout_stop_sec *: TimeSpan | Literal['infinity'] | None* *= None*

#### *field* runtime_max_sec *: TimeSpan | Literal['infinity'] | None* *= None*

#### *field* watchdog_sec *: TimeSpan | None* *= None*

#### *field* remain_after_exit *: bool | None* *= None*

#### *field* guess_main_pid *: bool | None* *= None*

#### *field* pid_file *: Path | None* *= None*

#### *field* bus_name *: str | None* *= None*

#### *field* user *: str | None* *= None*

#### *field* group *: str | None* *= None*

#### *field* supplementary_groups *: list[str]* *[Optional]*

#### *field* working_directory *: Path | str | None* *= None*

#### *field* environment *: dict[str, str]* *[Optional]*

#### *field* environment_file *: list[Path | str]* *[Optional]*

#### *field* umask *: str | None* *= None*

#### *field* standard_output *: str | None* *= None*

#### *field* standard_error *: str | None* *= None*

#### *field* kill_mode *: KillMode | None* *= None*

#### *field* kill_signal *: str | None* *= None*

#### *field* send_sigkill *: bool | None* *= None*

#### *field* success_exit_status *: list[int | str]* *[Optional]*

#### *field* restart_prevent_exit_status *: list[int | str]* *[Optional]*

#### *field* restart_force_exit_status *: list[int | str]* *[Optional]*
