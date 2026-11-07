# Acceptance — 01_business_logic

Request: Implement specs/todolist.
Sources: specs/todolist/project.md; task_order.md; tasks/01_business_logic.md; verification.md.
Prerequisites: none. Target: apps/todolist; evidence: .suite/runs/005-01_business_logic.

| ID | Exact source clause and observable outcome | Check and pass rule |
|---|---|---|
| BL1 | tasks/01_business_logic.md: “create tasks” | Create nonblank tasks; distinct positive IDs and incomplete initial state survive reload. |
| BL2 | tasks/01_business_logic.md: “list tasks” | List an empty store and created tasks through public API. |
| BL3 | tasks/01_business_logic.md: “delete tasks” | Remove only selected task; deletion survives reload. |
| BL4 | tasks/01_business_logic.md: “complete tasks” | Mark selected task complete and preserve others; survives reload. |
| BL5 | tasks/01_business_logic.md: “tasks are preserved at tasks.json at the root of the project” | Real JSON persistence; default path apps/todolist/tasks.json independent of cwd. CLI assembled verification will also exercise actual default path. |
| SH1 | project.md: “use uv + pyproject.toml for dependency and venv management” | uv sync and uv run checks succeed with project manifest and lockfile. |
| SH2 | project.md: “project should be implemented at apps/todolist”; “do not overengineer, keep things simple” | Small Python package at specified path; no external runtime dependencies. |

Derived defaults: numeric IDs, title and completed fields; explicit path supported for reusable store. Blank titles and invalid/missing IDs fail without mutation; malformed storage is reported and preserved. Mutations use atomic replacement. Concurrency is outside scope. Shared verification: specs/todolist/verification.md, real files and final CLI lifecycle after task 2. No required manual dependencies or unavailable checks.
