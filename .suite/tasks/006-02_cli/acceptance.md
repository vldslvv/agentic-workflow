# Acceptance — 02_cli

Request: Implement specs/todolist.
Sources: specs/todolist/project.md; task_order.md; tasks/02_cli.md; verification.md.
Prerequisite: 01_business_logic accepted with .suite/runs/005-01_business_logic/review.md PASS. Dependency: TaskStore public contract in .suite/runs/005-01_business_logic/checks.md.
Target apps/todolist; evidence .suite/runs/006-02_cli.

| ID | Exact source clause and observable outcome | Check and pass rule |
|---|---|---|
| CLI1 | tasks/02_cli.md: “add tasks” | CLI add TITLE persists task through store and prints useful confirmation. Quoted multiword titles work. |
| CLI2 | tasks/02_cli.md: “delete tasks” | CLI delete ID removes selected task in a later process; useful confirmation. |
| CLI3 | tasks/02_cli.md: “complete tasks” | CLI complete ID persists completion; list visibly distinguishes completed tasks. |
| CLI4 | tasks/02_cli.md: “list tasks” | CLI list shows IDs, titles and statuses, or readable empty state. |
| CLI5 | tasks/02_cli.md: “help” | help and --help show all supported commands; no arguments show usage. |
| SH1 | project.md: “use uv + pyproject.toml for dependency and venv management” | uv sync and uv run python -m todolist work; tests pass under uv. |
| SH2 | project.md: “project should be implemented at apps/todolist”; “do not overengineer, keep things simple” | CLI uses accepted business API and standard argparse; README explains runnable commands. |
| E2E1 | verification.md: “Run end-to-end scenarios such as adding tasks, removing, deleting.” | Real assembled CLI processes add two tasks, complete one, delete the other, list persisted remaining completed task, then delete it and list empty. Check actual app-root tasks.json and independent cwd. Removing/deleting refer to the same delete capability. |

Derived defaults: uv run python -m todolist; add requires one quoted TITLE; complete/delete require numeric ID; errors print concise stderr and exit nonzero. Bad/missing arguments, unknown IDs, blank titles and corrupt storage must be readable failures without data loss. No-argument usage may exit zero. Shared regression: all business tests remain passing, business-layer acceptance remains valid. No network/runtime service or manual-only check required. Scope excludes concurrency and packaging a global command.
