# Verification

Task checks cover the business operations and initial JSON persistence, CLI command behavior against that interface, and Postgres storage against the same accepted contract. Final validation runs the assembled CLI with real Docker-hosted Postgres.

## Scenario — commands and persistence across invocations

**Task/source clauses:** [business logic](tasks/01_business_logic.md), [CLI](tasks/02_cli.md), [database schema](tasks/03_database.md), [integration](tasks/04_integration.md).
**Setup and inputs:** Start the supplied Docker database with an isolated empty database and configure the assembled CLI to connect to it.
**Actions:** Invoke help; add two distinct tasks in separate processes; list them in a new process; complete one and list again; delete/remove the other and list again. Inspect the persisted database records and invoke the CLI again after restarting its process.
**Pass rule:** Help describes the required commands. Added tasks survive separate invocations with distinct sequential integer IDs and their descriptions. Completion and deletion/removal remain observable on subsequent invocations according to the accepted operation contract. Stored fields satisfy the specified schema, with added/update timestamps and New, Completed and Deleted statuses reflecting the operations. Postgres holds the persisted state; the assembled CLI does not rely on tasks.json. Every successful command has a live database connection.
**Cleanup:** Remove the isolated database/container and temporary resources.
**Evidence:** Record CLI commands, exit statuses, outputs and database observations, including the separate invocations.

## Scenario — unavailable database connection

**Task/source clause:** [integration](tasks/04_integration.md), requiring a live database connection on every CLI invocation.
**Setup and inputs:** Use the same assembled application with the configured database stopped or unreachable.
**Actions:** Invoke each required command (add, delete, complete, list and help) with otherwise valid arguments. Restore the database and repeat a normal add/list sequence.
**Pass rule:** Every invocation while the connection is unavailable reports the failure and exits unsuccessfully, without a success response or JSON fallback. After the connection is restored, commands succeed and persist changes across invocations.
**Cleanup:** Remove the isolated database/container and temporary resources.
**Evidence:** Record database availability, commands, exit statuses, outputs and restored-operation results. Unavailable required Docker/Postgres execution blocks acceptance.

