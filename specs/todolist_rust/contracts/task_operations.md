# Task operations and storage

- **Participants:** The [business layer](../tasks/01_business_logic.md) serves the [CLI](../tasks/02_cli.md) through an interchangeable storage interface.
- **Providers:** Initial JSON storage and [Postgres storage](../tasks/03_database.md) implement the same storage contract.
- **Sources:** [Project requirements](../project.md).
- **Interface:** Create, list, delete and complete tasks through the business layer and its storage interface.
- **Semantics:** Both storage implementations provide the same task data, operation results and storage-failure behavior.
- **Guarantees:** Switching storage preserves CLI command behavior.

## Task data

| Field | Type | Requirement |
|---|---|---|
| `id` | Integer | Unique and sequential. |
| `description` | String | Task description. |
| `added` | Datetime | Addition timestamp. |
| `update` | Datetime | Update timestamp. |
| `status` | Enum | `New`, `Completed` or `Deleted`, reflecting task operations. |

## Behavior

- Preserve task data across process invocations.
- Reflect creation, completion and deletion in the task status and timestamps.
- Expose observable results for creating, listing, completing and deleting tasks.
- Establish concrete operation results and storage-failure behavior in the [business-layer task](../tasks/01_business_logic.md).
- Record those agreed interfaces here before dependent tasks begin.

## Examples

| Interaction | Observable outcome |
|---|---|
| Create two distinct tasks and reload state | Descriptions persist with distinct sequential integer IDs and `New` statuses. |
| Complete a task and reload state | The `Completed` status and required timestamps persist. |
| Delete a task and reload state | Deletion remains observable under the agreed operation contract and `Deleted` status. |
| A storage operation fails | The agreed storage-failure behavior is exposed. |

## Rust interface

- Use the `todolist_rust` library with public `Task`, `Status`, `Error`, `Storage`, `add`, `list`, `complete` and `delete` exports.
- Represent task IDs as `i64`, timestamps as `chrono::DateTime<chrono::Utc>`, and statuses as `Status::{New, Completed, Deleted}`.
- Serialize task field names exactly as listed above, including `update`, and serialize statuses using their enum names.
- Implement `Storage::create_task(&mut self, description: String, now: DateTime<Utc>) -> Result<Task, Error>`, `Storage::list_tasks(&mut self) -> Result<Vec<Task>, Error>` and `Storage::change_status(&mut self, id: i64, status: Status, now: DateTime<Utc>) -> Result<Task, Error>`.
- Call `add(&mut impl Storage, &str)`, `list(&mut impl Storage)`, `complete(&mut impl Storage, i64)` and `delete(&mut impl Storage, i64)` through the business layer.
- Return `Result<Task, Error>` from mutations and `Result<Vec<Task>, Error>` from listing.
- Expose `Error::{InvalidDescription, NotFound(i64), Deleted(i64), Storage(String)}` with human-readable `Display` messages.

## Operation semantics

- Reject blank descriptions with `InvalidDescription` and preserve nonblank descriptions exactly.
- Assign the first ID as 1 and each later ID as the previous maximum plus 1, retaining deleted tasks.
- Set `added` and `update` to the supplied creation time and status to `New`.
- List every task, including completed and deleted tasks, in ascending ID order.
- Complete a new task by changing its status to `Completed` and its `update` timestamp to the supplied time.
- Delete a new or completed task by changing its status to `Deleted` and its `update` timestamp to the supplied time.
- Preserve task data and timestamps when completing an already completed task or deleting an already deleted task.
- Return `Deleted(id)` when completing a deleted task and `NotFound(id)` for an unknown identifier.
- Preserve descriptions, identifiers and addition timestamps during status changes.
- Return `Storage(message)` for persistence, connection, parsing or identifier exhaustion failures without reporting success.
- Require status changes to persist successfully before returning a changed task.

## JSON storage

- Export `json::JsonStorage::new(path)` and `json::JsonStorage::default()`.
- Use the compiled app root's `tasks.json` path for the default JSON store, independent of the caller's working directory.
- Treat a missing JSON file as empty storage and reject malformed existing JSON as a storage error.
- Store a JSON array of tasks and replace the file through a temporary sibling file after successful serialization.
