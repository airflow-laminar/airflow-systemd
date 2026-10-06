# Why Airflow owns the schedule

Airflow coordinates workflows; systemd owns service processes, their children,
and their resource groups. `airflow-systemd` connects those responsibilities by
creating service units and starting them within an Airflow DAG run.

Systemd can also schedule work through timer units. A timer that starts the same
service independently of Airflow gives both schedulers control over its lifetime.
Airflow could then monitor or stop a service started outside its own run. This
integration starts service units directly, so the DAG schedule remains the
workload’s scheduling policy. Timer models are re-exported from
`systemd-pydantic`, but the Airflow lifecycle does not start or enable timers.

## Why worker placement and scope matter

A systemd manager belongs to a host. A user manager also belongs to a Unix user.
A local lifecycle therefore needs every task to reach the same manager and
configuration files. Sharing a directory between workers does not share their
service managers. Routing the tasks to one worker host preserves that ownership.

The system manager and user managers have separate unit directories and
permissions. A user manager lets an application account manage its own services
without writing system-wide unit files. Its D-Bus session must be reachable from
the worker or SSH session. Lingering keeps that manager available after logout,
which matters for services that remain active between DAG runs.

System scope fits units managed as part of host administration. The account
configuring those units needs both filesystem permissions and authorization to
control the system manager. A service’s `User=` setting controls the workload’s
identity separately from the account that writes and manages its unit.

## Why SSH configuration needs explicit remote paths

Configuration models are constructed when Airflow parses a DAG. Their default
home directory, temporary directory, and username come from that parsing
process. Those defaults may describe the scheduler rather than the SSH account.
Explicit remote paths give configuration commands and later task processes the
same unit files and saved state on the target host.

`SystemdSSH` uses Airflow SSH operators to write and remove configuration.
Service control and status checks use a `SystemdClient` with an
`AirflowSSHCommandRunner` backed by the same connection. All of those operations
run on the remote host. The shell prefix applies to both paths, so environment
setup for a virtual environment or user bus is consistent across the lifecycle.

## Why monitoring and service restart are separate

The monitor maps service state to `airflow-ha` results. Successful completion
ends monitoring. Running or otherwise healthy services continue. Failed checks
take the restart and retrigger path. Airflow polling follows the workflow’s
monitoring window, while systemd retains ownership of the process.

Systemd’s `Restart=` policy can restart a service while Airflow is between
checks or DAG runs. Airflow’s restart flags control startup within the DAG
lifecycle. These policies serve different intervals and can be configured
independently. Finite batch jobs normally use the default `Restart=no` so their
completion remains visible to the workflow.

A persistent service may never complete. Its Airflow monitoring window needs an
end condition, and stop and cleanup must be disabled if the service should
remain available for the next run. Cleanup normally removes generated unit
files and saved configuration; journald owns the service’s logs separately.

## Python and airflow-config describe the same lifecycle

Inline Python constructs `Systemd` or `SystemdSSH` with a typed configuration.
It keeps the definition beside other Airflow code and works without
`airflow-config`.

YAML loads into `SystemdTask` or `SystemdSSHTask`, which construct the same
lifecycle classes. `airflow-config` adds Hydra composition and configuration
loading to the DAG parsing environment. Execution location remains a separate
choice: either configuration format can target a local or remote manager.

## Systemd and supervisord

[airflow-supervisor](https://github.com/airflow-laminar/airflow-supervisor) creates
a dedicated supervisord instance with its own PID, logs, and control endpoint.
`airflow-systemd` uses the target host’s existing manager and journald. Systemd
fits deployments where services already belong in host administration;
supervisord fits applications that need a separate process manager installed
with their dependencies.
