# Acceptance — 02_cli

Baseline: `07fd1484a33826b53c9e669b7490175bce1bd11a`. Source: `specs/todolist_rust/tasks/02_cli.md`; shared normative sources are project.md, task_order.md and verification.md in that bundle. SHA256 identities are bound in approval.json and the frozen inventory.

Prerequisite: 01_business_logic, accepted at its recorded candidate identity before implementation. Selected scope: all source clauses. Rust app root: `apps/todolist_rust`. Final task intentionally supersedes JSON storage.

| ID | Source clause | Observable check |
|---|---|---|
| C1 | add tasks | todolist add DESCRIPTION accepts quoted text, reports id, rejects blank descriptions. |
| C2 | delete tasks | todolist delete ID removes from active listing; invalid and unknown ids produce nonzero exit. |
| C3 | complete tasks | todolist complete ID changes status and reports success. |
| C4 | list tasks | todolist list prints a tab-separated header id/status/description and rows in id order; an empty list succeeds. |
| C5 | help | todolist help, --help and no arguments show usage; malformed commands fail with explanatory stderr. JSON-stage CLI always uses app-root tasks.json. |

## Execution

Frozen command: `python3 .suite/runs/008-todolist-rust/checks/verify.py cli --evidence <owned-evidence-directory>`. Setup/inputs/assertions/cleanup are executable in the check. Business checks compile an external consumer of the production library; CLI checks invoke the built binary in fresh processes, preserving preexisting data. Database checks use an isolated Compose project/port/volume and clean up only that project. All assertions and subprocesses must pass; failures retain stdout, stderr and exit codes. Database checks require Docker access.

CLI listing: tab-separated id/status/description header and rows, no extra preamble. Descriptions with tabs/newlines are escaped in display. Case-sensitive statuses New/Completed/Deleted. Errors use stderr and nonzero exit. No manual gate. Check coverage review and independent fresh-context execution are mandatory; source inspection verifies simple Rust implementation and schema configuration alongside assertions.

Retained inputs: none. Sources and preexisting repository files protected. Owned candidate path: apps/todolist_rust. Approval: sibling approval.json, derived under the direct implementation request, not separately user-reviewed.
