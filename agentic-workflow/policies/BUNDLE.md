# Specification bundle

Apply when resolving or authoring project specifications and task selections.

- Use the selected bundle. Otherwise look outside the package for the files below; ask if multiple bundles fit. New authorized authoring uses `specs/`; preserve existing locations.
- Return `NO_PROJECT` without project intent; block generation on missing required inputs. Treat compatibility assessment alone as insufficient authorization for generation.
- Use the bundle and its normative references as behavior authority over plans and memory. Preserve explicit requirements, complete approved text and history.
- Treat a direct implementation request as authorization for derived records and ordinary choices. Obtain user authority for required behavior changes and material conflicts; require execution authorization beyond document approval alone.
- Use ordinary Markdown without required frontmatter. Keep shared constraints in `project.md`, shared/final scenarios in `verification.md`, and task behavior and interfaces in task files.

| File | Purpose | Template |
|---|---|---|
| `project.md` | Intent, constraints, target and output paths | [Project](../templates/project.md) |
| `task_order.md` | Task filenames and dependencies | [Task order](../templates/task_order.md) |
| `tasks/*.md` | Required behavior and interface contracts | [Task](../templates/tasks/task.md) |
| `verification.md` | Shared checks and assembled-app scenarios | [Verification](../templates/verification.md) |

- Declare scheduling dependencies only in the `Task | Depends on` table in `task_order.md`. List each task once; use `None` or comma-separated task filenames for dependencies. Names and row order add no dependencies.
- Use unique filename stems as task IDs. Resolve bare task filenames under `tasks/`, task paths/links from the bundle root, and normative links from their containing document. Reject missing files, unlisted dependencies, unknown references and cycles, including self-dependencies.
- Select listed tasks with their prerequisites and normative inputs. Include unmet prerequisites or leave the selection blocked; accepted prerequisites require valid evidence. An empty selection yields `NO_WORK`. [Supervisor](../roles/SUPERVISOR.md) schedules the selection.
- Resolve repository-relative output paths from the repository root. Material ambiguity blocks execution. Clarify broad scenarios' pass rules before execution without changing requirements; checks can develop during implementation without frozen inventories or approval receipts. Format validity and app acceptance are separate conclusions.
