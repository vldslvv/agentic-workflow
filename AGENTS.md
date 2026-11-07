# App generation

`spec-source-suite/` is reusable guidance; change it only for requested workflow/tooling work. Keep app inputs, code and evidence outside it.

Spec implementation (for example, `Implement specs/todolist`) always uses the project workflow: read [shared rules](spec-source-suite/AGENTS.md) and act as [Supervisor](spec-source-suite/SUPERVISOR.md), even without a named skill. Individual [task modes](spec-source-suite/TASK_MODES.md) operate within that workflow.

For other ordinary work, implement directly or briefly plan first; follow engineering guidelines, run relevant checks, inspect the diff and report results. Formal workflow artifacts and roles are optional unless requested. Plan-only requests stop at the plan; honor explicit review/approval requirements. Explicit suite skills/roles and suite maintenance follow the suite's applicable guidance.

Use the paths below directly and batch independent reads. Search for paths only when the request, this map or the handoff leaves them unresolved. Read only entries applicable to the work.

| Read when | Path |
|---|---|
| Before planning, writing, changing or reviewing code, tests or tooling | [engineering guidelines](spec-source-suite/GUIDELINES.md) |
| Suite app work or suite maintenance: shared rules | [spec-source-suite/AGENTS.md](spec-source-suite/AGENTS.md) |
| Entering a role or selecting settings for a worker | [spec-source-suite/MODELS.md](spec-source-suite/MODELS.md) |
| Selecting full/lightweight task mode or applying an assigned workflow | [spec-source-suite/TASK_MODES.md](spec-source-suite/TASK_MODES.md) |
| Document-only suite authoring | [spec-source-suite/PLANNER.md](spec-source-suite/PLANNER.md) |
| Any spec implementation or app generation: orchestration | [spec-source-suite/SUPERVISOR.md](spec-source-suite/SUPERVISOR.md) |
| Assigned suite task execution, including full-mode planning | [spec-source-suite/IMPLEMENTER.md](spec-source-suite/IMPLEMENTER.md) |
| Assigned suite independent review | [spec-source-suite/REVIEWER.md](spec-source-suite/REVIEWER.md) |
| Assigned suite final validation | [spec-source-suite/VALIDATOR.md](spec-source-suite/VALIDATOR.md) |
| Authoring project inputs | [project](spec-source-suite/templates/project.md), [task order](spec-source-suite/templates/task_order.md), [task](spec-source-suite/templates/tasks/task.md), [verification](spec-source-suite/templates/verification.md) |
| Checking suite changes | [spec-source-suite/helpers/check_package.py](spec-source-suite/helpers/check_package.py) |
| Allocating implementations or resuming tasks | [records helper](spec-source-suite/helpers/records.py) |
| Aggregating execution usage | [spec-source-suite/helpers/usage_report.py](spec-source-suite/helpers/usage_report.py) |
| Requested automated-runner work only | [spec-source-suite/RUNNER.md](spec-source-suite/RUNNER.md) |
| Running or maintaining the local todolist eval | [evals/README.md](evals/README.md) |

Apply the engineering guidelines and include their resolved paths in delegated work; shared rules govern source resolution and handoff.

- Fresh work uses the current brief or selected bundle. Ordinary planners and implementers may consult [project memory](spec-source-suite/AGENTS.md#project-memory), without searching earlier tasks or conversations.
- Continuing work uses identified task paths or execution references. Resolve a bare task ID only under the identified `.suite/<NNN>_<name>/tasks/`; ask if the implementation or task is absent, ambiguous, or continuation itself is unclear. Stop discovery when authority is resolved.
- Advice/tooling work uses requested files and relevant references, without task-history discovery.

For spec implementation use the selected [Markdown bundle](spec-source-suite/AGENTS.md#markdown-bundle); otherwise look outside the suite for its four file types and ask if multiple bundles are plausible. New authorized authoring uses `specs/` and the bundle templates. Missing required inputs block generation; no project intent yields NO_PROJECT.

The explicit suite skills are `spec-planner` and `spec-supervisor`. A direct implementation request authorizes derived plans and acceptance without routine reapproval. Preserve explicit requirements, approved text and historical records. [Records](spec-source-suite/AGENTS.md#records) describes task storage and recovery.

Future-runner requirements are not app requirements. Suite guidance changes follow the requested scope, acceptance and [maintenance rules](spec-source-suite/AGENTS.md#workflow-maintenance).
