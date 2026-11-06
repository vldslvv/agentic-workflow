# Acceptance — 01_business_logic

Baseline: `07fd1484a33826b53c9e669b7490175bce1bd11a`. Source: `specs/todolist_rust/tasks/01_business_logic.md`; shared normative sources are project.md, task_order.md and verification.md in that bundle. SHA256 identities are bound in approval.json and the frozen inventory.

Prerequisite: none, accepted at its recorded candidate identity before implementation. Selected scope: all source clauses. Rust app root: `apps/todolist_rust`. Final task intentionally supersedes JSON storage.

| ID | Source clause | Observable check |
|---|---|---|
| B1 | create tasks | Store::open(path) opens or creates a JSON store; add(description) returns a Task with positive increasing id and New status. Trim descriptions and reject blank input. |
| B2 | list tasks | list() returns active tasks in increasing id order, including Completed tasks. |
| B3 | delete tasks | delete(id) removes task from active listing; unknown ids fail without altering existing tasks. |
| B4 | complete tasks | complete(id) sets Completed; unknown ids fail without altering existing tasks; repeated completion is idempotent. |
| B5 | tasks.json at the root of the project | JSON persists between Store instances. Default app data root is apps/todolist_rust, regardless of working directory. Corrupt JSON fails without overwriting it. This storage mechanism is superseded by task 03. |

## Execution

Frozen command: `python3 .suite/runs/008-todolist-rust/checks/verify.py business --evidence <owned-evidence-directory>`. Setup/inputs/assertions/cleanup are executable in the check. Business checks compile an external consumer of the production library; CLI checks invoke the built binary in fresh processes, preserving preexisting data. Database checks use an isolated Compose project/port/volume and clean up only that project. All assertions and subprocesses must pass; failures retain stdout, stderr and exit codes. Database checks require Docker access.

CLI listing: tab-separated id/status/description header and rows, no extra preamble. Descriptions with tabs/newlines are escaped in display. Case-sensitive statuses New/Completed/Deleted. Errors use stderr and nonzero exit. No manual gate. Check coverage review and independent fresh-context execution are mandatory; source inspection verifies simple Rust implementation and schema configuration alongside assertions.

Retained inputs: none. Sources and preexisting repository files protected. Owned candidate path: apps/todolist_rust. Approval: sibling approval.json, derived under the direct implementation request, not separately user-reviewed.
