Implement a business layer for a TODO app.

It should:
 - create tasks
 - list tasks
 - delete tasks
 - complete tasks

The tasks are preserved at tasks.json at the root of the project.

Establish a storage interface used by the business layer, with JSON persistence as its initial implementation. Its accepted contract must cover the operations, task data and errors required by the [CLI](02_cli.md) and [Postgres storage](03_database.md), including the database specification's fields and statuses. Define observable operation results and storage-failure behavior so both implementations can satisfy the same contract and the CLI can use either without changing its command behavior.

