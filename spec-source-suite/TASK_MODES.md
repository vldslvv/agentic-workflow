# Task modes

Read this file when selecting a task's mode or applying its assigned workflow. The Supervisor selects the mode for each task before dispatch; the implementer follows that assignment.

## Selecting a mode

Honor source and user requirements. Resolve conflicting instructions before dispatch; unresolved requirements block either mode.

| Task conditions | Mode |
|---|---|
| Planning or independent task review is required, or the work is complex | `full` |
| Work is simple and bounded, with clear source criteria | `lightweight` |
| Uncertain which mode applies | `full` |

Record the selected mode in the assignment and result. Selection is a Supervisor judgment under these rules; model profiles do not select task modes.

## Execution

| Mode | Required task workflow |
|---|---|
| `lightweight` | One agent implements, runs relevant checks, reviews its own diff and reports the result. Use source requirements as acceptance criteria. No plan, separate acceptance document or independent task reviewer. |
| `full` | One agent writes the plan and source-linked acceptance before implementation, implements, checks and self-reviews. A fresh independent reviewer assesses the candidate; the original agent owns all corrections and repairs. |

The assigned mode defines the task flow; lightweight has no optional-review or automatic-escalation branch. Both modes follow the [shared engineering, acceptance, coordination and usage rules](AGENTS.md). Full-task documents use the [shared outlines](AGENTS.md#task-document-outlines).

Every spec implementation uses the [Supervisor's project workflow](SUPERVISOR.md), including dependency gates and final independent app validation, whichever task modes are selected. Project orchestration and the `full` task mode are separate decisions.
