# Acceptance — 01_business_logic
Baseline: e63405b4205b0f965879f37e739e3a161ab7f47a
Authority: user request “Implement specs/todolist”; derived criteria under contract §1.
Sources: specs/todolist/project.md, task_order.md, tasks/01_business_logic.md, verification.md; SHA-256 identities in approval.json and frozen-v1.json.
Prerequisites: none. Source order validated: 01_business_logic -> 02_cli; unique existing task IDs, no other declared edges or cycles.

| ID | Source clause and observable criterion | Check |
|---|---|---|
| BL-CREATE | 01_business_logic “create tasks”: accept nonempty trimmed title, assign positive integer ID unique among stored tasks, return id/title/completed=false | business.py lifecycle and rejected operations |
| BL-LIST | “list tasks”: empty store is [], otherwise creation order with ID, title, completion state | business.py lifecycle |
| BL-DELETE | “delete tasks”: remove specified ID, preserve others; absent ID raises ValueError without writes | business.py lifecycle/rejected operations |
| BL-COMPLETE | “complete tasks”: set specified task completed=true; repeated completion succeeds; missing ID raises ValueError | business.py lifecycle/rejected operations |
| BL-STORE | “preserved at tasks.json at the root of the project”: JSON array in apps/todolist/tasks.json by default; data survives new instances/processes; malformed JSON or invalid structure raises ValueError without overwrite | business.py lifecycle/corruption; final.py default-path integration |
| PROJECT-UV | project.md “use uv + pyproject.toml” and “implemented at apps/todolist”: Python standard library runtime; uv sync succeeds; pyproject and lockfile retained | setup execution; independent source inspection |

Chosen public boundary: `from todolist import TaskStore`; TaskStore(path=None), create_task(title)->dict, list_tasks()->list[dict], delete_task(id), complete_task(id). Explicit path is normal business-layer configuration, used by callers embedding the layer. Default resolves to app root independent of cwd. Root of project means declared generated project apps/todolist. No concurrency/multiuser guarantee requested.

Checks use temporary directories and clean them. All assertions must pass, with mandatory errors leaving original bytes intact. Task checks: checks/task-v1.json. Initial regression set: none (no accepted capabilities yet). Final assembled scenarios: specs/todolist/verification.md concretized in checks/final.py, frozen now and executed only after CLI acceptance. Manual gate: reviewer inspects simple design, pyproject/uv and default-path resolution. No external service needed. Coverage, execution and review are separate gates. No retained memory (project does not exist yet). No unresolved decisions.
Approval: approval.json. Inventory: frozen-v1.json.
