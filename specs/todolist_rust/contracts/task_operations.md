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
