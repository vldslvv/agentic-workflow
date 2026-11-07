# Business layer acceptance

Authority: `specs/todolist/project.md`, `specs/todolist/tasks/01_business_logic.md`, `specs/todolist/verification.md`; engineering constraints: repository `guidelines.md`.

| ID | Source requirement | Observable check and pass rule |
| --- | --- | --- |
| B1 | task: create tasks | Public service creates a task with a stable integer ID, title and incomplete state; listing returns it. |
| B2 | task: list tasks | Empty storage lists empty; multiple tasks list with their individual titles/IDs/state. |
| B3 | task: complete tasks | Completing an ID changes that task to complete and persists across a new service instance. |
| B4 | task: delete tasks | Deleting an ID removes that task, preserves remaining tasks and persists across a new instance. |
| B5 | task: preserve in root tasks.json | Default service path equals `apps/todolist/tasks.json`; a real default-path lifecycle writes/readbacks JSON and restores original file or removes newly created storage afterward. Temporary-path tests independently check restart persistence. |
| B6 | project: uv/pyproject; simple implementation | `uv run python -m unittest discover -s tests -v` from app succeeds; inspect pyproject and production modules for cohesive functional domain rules and explicit storage boundary. |
| B7 | shared verification: adding/removing/deleting end-to-end | Business-layer lifecycle covered now; assembled CLI end-to-end scenarios deferred to successor task and final validation. |

Chosen contract checks: blank title -> ValueError without write; unknown complete/delete ID -> KeyError without write; malformed JSON -> read failure without data replacement. These are ordinary API choices, not new source requirements.

Coverage: tests use real local JSON storage, no mocks. CLI is outside this task. Finite local tests do not prove behavior under concurrent writers or unexpected filesystem failure; neither behavior is required.
