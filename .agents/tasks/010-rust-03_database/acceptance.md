# Acceptance — 03_database

Baseline: `07fd1484a33826b53c9e669b7490175bce1bd11a`. Source: `specs/todolist_rust/tasks/03_database.md`; shared normative sources are project.md, task_order.md and verification.md in that bundle. SHA256 identities are bound in approval.json and the frozen inventory.

Prerequisite: 02_cli, accepted at its recorded candidate identity before implementation. Selected scope: all source clauses. Rust app root: `apps/todolist_rust`. Final task intentionally supersedes JSON storage.

| ID | Source clause | Observable check |
|---|---|---|
| D1 | instead of text file, use a docker container that spawns Postgres database | Docker Compose provisions PostgreSQL with persistent volume and healthcheck. Runtime persistence uses PostgreSQL only; no tasks.json writes. DATABASE_URL selects database, with documented local default. |
| D2 | When executing the CLI ... connection is alive, otherwise fail | Every invocation, including help and no arguments, attempts a real connection before command handling. Unreachable database fails within 10 seconds, nonzero exit and explanatory stderr. |
| D3 | id: int -- unique and sequential; description: string; added: datetime; update: datetime; status: enum | Public tasks table has PostgreSQL integer generated sequential primary key id, text description, timestamp added and quoted update fields, and a PostgreSQL enum status with exactly New/Completed/Deleted. IDs increase and are never reused; sequence gaps after rollback are allowed. added is immutable, update reflects mutations. Fresh database schema initializes automatically. |
| D4 | status: enum -- reflects the status: Completed/New/Deleted | Add starts New, complete becomes Completed, delete soft-deletes to Deleted; normal list excludes Deleted. Missing/deleted ids fail on mutation; repeat completion is idempotent. |
| D5 | verification.md: Run end-to-end scenarios such as adding tasks, removing, deleting | Run add/list/complete/delete through separate CLI processes against real Docker Postgres; inspect persisted schema/status/timestamps, restart container and verify persistence, test unreachable DB and invalid inputs. Earlier operation requirements remain; JSON persistence is explicitly superseded. |

## Execution

Frozen command: `python3 .suite/runs/008-todolist-rust/checks/verify.py database --evidence <owned-evidence-directory>`. Setup/inputs/assertions/cleanup are executable in the check. Business checks compile an external consumer of the production library; CLI checks invoke the built binary in fresh processes, preserving preexisting data. Database checks use an isolated Compose project/port/volume and clean up only that project. All assertions and subprocesses must pass; failures retain stdout, stderr and exit codes. Database checks require Docker access.

CLI listing: tab-separated id/status/description header and rows, no extra preamble. Descriptions with tabs/newlines are escaped in display. Case-sensitive statuses New/Completed/Deleted. Errors use stderr and nonzero exit. No manual gate. Check coverage review and independent fresh-context execution are mandatory; source inspection verifies simple Rust implementation and schema configuration alongside assertions.

Retained inputs: none. Sources and preexisting repository files protected. Owned candidate path: apps/todolist_rust. Approval: sibling approval.json, derived under the direct implementation request, not separately user-reviewed.
