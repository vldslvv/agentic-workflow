Now instead of text file, use a docker container that spawns Postgres database.
When executing the CLI, you have to ensure that the database connection is alive, otherwise fail.

The schema should be the following:
id: int -- unique and sequential
description: string
added: datetime
update: datetime
status: enum -- reflects the status: Completed/New/Deleted

