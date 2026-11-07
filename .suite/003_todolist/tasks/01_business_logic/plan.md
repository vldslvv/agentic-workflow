# Business layer plan

- Authority: direct implementation of `specs/todolist`; sources: `specs/todolist/project.md`, `tasks/01_business_logic.md`, `task_order.md`, `verification.md`.
- Constraints: repository `guidelines.md`; use a functional core and explicit filesystem boundary, simple public API, uv and pyproject, output `apps/todolist`.
- Prerequisites: first task; no predecessor. No existing app or project memory.
- Assessment: simple task with four operations and local JSON persistence, no compatibility commitments or complex component interactions. Workflow: lightweight. Standard implementer route, requested gpt-6.1-sol/medium; observed host settings unavailable, retained host defaults.
- Approach: immutable task values, pure creation/completion/deletion helpers behind a small file-backed service. The service defaults to `apps/todolist/tasks.json`, independent of working directory. Integer IDs remain unique among active tasks. Blank titles raise ValueError, missing IDs raise KeyError. Missing files represent an empty list; invalid JSON is reported without overwriting it.
- Checks: stdlib unittest through uv, real temporary files, lifecycle/reload/default-path/error behavior; inspect app diff. Apply test-audit authoring gates. Its linked `/home/vv/docs/help/testing/writing-tests.md` is unavailable; use the skill's available authoring guidance.
- Destinations: acceptance in this directory; implementation `apps/todolist`; evidence/result `.suite/003_todolist/runs/01_business_logic/business/`.
- Review: optional independent review omitted because this is a small standalone business layer covered at its public storage boundary. Whole-app independent validation remains required.
