# Verification

Task checks cover business operations, initial JSON persistence, CLI behavior and Postgres conformance to the [shared contract](contracts/task_operations.md).
Final validation runs the assembled CLI with real Docker-hosted Postgres.

## Scenario — commands and persistence across invocations

- **Task/source clauses:** [Task operations and schema](contracts/task_operations.md), [CLI commands](tasks/02_cli.md) and [integration](tasks/04_integration.md).
- **Setup and inputs:** Start an isolated empty database with the supplied Docker setup and configure the assembled CLI to connect to it.
- **Actions:** Invoke help, add two distinct tasks, list them, complete one, list again, delete the other and list again, using separate processes.
- **Pass rule:** Match the shared operation and schema contract, required help output and integration requirements across invocations.
- **Cleanup:** Remove the isolated database/container and temporary resources.
- **Evidence:** Record CLI commands, exit statuses, outputs and persisted database fields and statuses, including observations after restarting the CLI process.

## Scenario — unavailable database connection

- **Task/source clauses:** [Integration](tasks/04_integration.md), requiring a live database connection on every CLI invocation.
- **Setup and inputs:** Use the assembled application with the configured database stopped or unreachable.
- **Actions:** Invoke every required command with valid arguments, then restore the database and repeat an add/list sequence in separate processes.
- **Pass rule:** Unavailable connections produce the specified failures for every command, while restored connections permit successful commands and persistent changes.
- **Cleanup:** Remove the isolated database/container and temporary resources.
- **Evidence:** Record database availability, commands, exit statuses, outputs and restored-operation results.

Unavailable required Docker/Postgres execution blocks acceptance.

