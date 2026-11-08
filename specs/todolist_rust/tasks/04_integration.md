# Application wiring — CLI with Postgres

## Context

- **Responsibility:** Assemble the CLI, business layer and Postgres storage.
- **Boundary:** Own backend selection and connection checks for every CLI invocation.
- **Sources:** [Project requirements](../project.md) and [CLI commands](02_cli.md).

## Contracts

- **Consumes:** [Task operations and storage](../contracts/task_operations.md), implemented by the business layer and Postgres component.
- **Provides:** The required CLI commands backed by Docker-hosted Postgres.

## Behavior

- **Inputs:** Every CLI invocation, including `help`.
- **Effects:** Check the database connection and use Postgres for task persistence.
- **Outputs:** Command results preserving the required CLI behavior and database schema.
- **Failures:** Report an unavailable connection and exit unsuccessfully without a success response or JSON fallback.

## Constraints

- Use the accepted storage interface to connect the business layer to Postgres.
- Require a live database connection for every CLI invocation.
- Use Postgres instead of `tasks.json` in the assembled application.

## Acceptance

| Scenario | Observable pass condition |
|---|---|
| Commands with real Postgres | Satisfy [commands and persistence](../verification.md#scenario--commands-and-persistence-across-invocations) across separate CLI invocations. |
| Unavailable database and recovery | Satisfy the [connection failure scenario](../verification.md#scenario--unavailable-database-connection) for every command, including help. |
