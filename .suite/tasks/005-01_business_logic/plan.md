# Plan — 01_business_logic

Request: Implement specs/todolist. This direct request authorizes derived records and implementation.
Sources: specs/todolist/project.md, task_order.md, tasks/01_business_logic.md, verification.md.
Acceptance: .suite/tasks/005-01_business_logic/acceptance.md.
Prerequisites: none. Selected order is 01_business_logic then 02_cli; unique IDs, no additional dependencies or cycles.

Build a small standard-library Python package in apps/todolist with uv and pyproject.toml. Expose TaskStore with create(title), list(), delete(id), complete(id), using positive integer IDs, nonblank titles and a completed boolean. Save a JSON list at apps/todolist/tasks.json by default regardless of cwd; allow an explicit path for other consumers. Missing file means an empty list. Reject invalid input and malformed storage without overwriting it; report missing IDs. Persist mutations with an atomic replacement. No database, server or concurrency guarantees.

Use unittest public-interface tests with real temporary JSON files to verify lifecycle, reloading, identifiers, invalid input, and malformed storage. No mocks or test-only production hooks. Run uv sync and uv run python -m unittest discover -s tests -v from apps/todolist. Save results in .suite/runs/005-01_business_logic. No project memory exists. Dispatch a fresh implementer and require a separate fresh review before accepting task 1 and preparing task 2.

Final assembled scenarios: from an unrelated temporary working directory use actual CLI processes to request help, list empty tasks, add two titles, list persisted tasks, complete one, delete the other, list final state and inspect app-root tasks.json. Remove the final task and confirm empty list. Check unknown ID and missing arguments fail clearly. Preserve any preexisting tasks.json during verification. Task 2 will add subprocess coverage for CLI transport and cwd behavior; business tests own detailed storage validation.
