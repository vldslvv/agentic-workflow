Connect the CLI and business layer to the Postgres storage implementation through the accepted storage interface. The assembled application uses the Docker-hosted Postgres database instead of tasks.json.

When executing the CLI, ensure that the database connection is alive, otherwise fail. This applies to every invocation, including help. Report the connection failure and exit unsuccessfully; do not silently fall back to JSON storage or report a successful command.

Preserve all required CLI commands and database schema behavior. Verify the assembled application against real Postgres using the [shared scenarios](../verification.md), including persistence across separate CLI invocations and failure when the database connection is unavailable.
