# Specification bundle

Apply when finding or writing project specifications and selecting tasks. A bundle is the set of project files listed below.

- Use the selected bundle. If none is selected, look outside the package for these files. Ask when more than one bundle fits.
- Put new specifications in `specs/` when authoring is authorized. Keep existing specifications in their current locations.
- Return `NO_PROJECT` when no project has been requested. Block generation when required inputs are missing.
- Treat a compatibility assessment as a request to assess, not permission to generate an app.
- Follow the bundle and the requirements it links to when they disagree with plans or memory.
- Preserve explicit requirements, the full approved text and its history.
- Make ordinary implementation choices and create needed records when the user requests implementation.
- Ask the user to resolve significant requirement conflicts or authorize changes to required behaviour.
- Require permission to implement; approval of a document alone does not provide it.
- Use ordinary Markdown. No frontmatter is required.
- Keep shared constraints in `project.md`, shared and final scenarios in `verification.md`, and task behaviour and interfaces in task files.

| File | Purpose | Template |
|---|---|---|
| `project.md` | Intent, constraints, target and output paths | [Project](../templates/project.md) |
| `task_order.md` | Task filenames and dependencies | [Task order](../templates/task_order.md) |
| `tasks/*.md` | Required behavior and interface contracts | [Task](../templates/tasks/task.md) |
| `verification.md` | Shared checks and assembled-app scenarios | [Verification](../templates/verification.md) |

## Select tasks and resolve paths

Apply before scheduling work. The [Supervisor](../roles/SUPERVISOR.md) schedules the selected tasks.

- Declare dependencies only in the `Task | Depends on` table in `task_order.md`.
- List each task once. Use `None` or comma-separated task filenames for dependencies. Do not infer dependencies from names or row order.
- Use unique filenames without extensions as task IDs.
- Resolve bare task filenames under `tasks/` and task paths or links from the bundle root. Resolve links to requirements from the document containing the link.
- Reject missing files, unlisted dependencies, unknown references and dependency cycles, including tasks that depend on themselves.
- Select listed tasks together with their prerequisites and required source documents.
- Include unfinished prerequisites in the selection or leave it blocked. Require valid evidence for prerequisites already accepted.
- Return `NO_WORK` for an empty selection.
- Resolve repository-relative output paths from the repository root. Stop execution when ambiguity could affect the work.
- Clarify how broad scenarios pass before execution, without changing their requirements.
- Allow checks to develop during implementation. Do not require a fixed check inventory or approval receipt.
- Report valid document format separately from whether the app meets its requirements.
