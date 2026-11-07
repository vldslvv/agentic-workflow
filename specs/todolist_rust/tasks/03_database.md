Implement Postgres storage against the business layer's accepted storage interface, providing the same operations, data and error behavior as the initial JSON implementation. Supply a Docker setup that starts the Postgres database. Verify storage behavior against that real database without requiring CLI changes; [integration](04_integration.md) makes Postgres the CLI's storage backend.

The schema should be the following:
id: int -- unique and sequential
description: string
added: datetime
update: datetime
status: enum -- reflects the status: Completed/New/Deleted

