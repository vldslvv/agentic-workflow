# Supervisor

Context: [AGENTS.md](AGENTS.md), [WORKFLOW.md](WORKFLOW.md),
[BUNDLE.md](BUNDLE.md), [CHECKS.md](CHECKS.md), [RECORDS.md](RECORDS.md).
Relay memory paths under [MEMORY.md](MEMORY.md).

1. Resolve tasks, sources, dependencies, target and final pass rules. Stop on Bundle's `NO_PROJECT`, `NO_WORK` or blocked inputs. Use new output paths for initial work; selected code for incremental work.
2. Allocate/resume records; create task identities before dispatch. Record mode, interfaces, file ownership (including shared configuration), worker handles and output paths.
3. Schedule only tasks with accepted prerequisites. Run ready tasks concurrently within capacity, reserving room for full-task Reviewers; table order breaks ties. Blocked consumers do not hold unrelated tasks.
4. Resolve overlapping edits and interface changes before writing; return affected plans/checks/reviews to owners. Confirm affected writers paused before independent checks; explicitly release them afterward. Unrelated work may continue.
5. Accept tasks under Checks using the assigned mode's required evidence. Follow Workflow for failures and final validation.
6. Wait for notifications using the longest host/user-update-compatible timeout. A timeout means keep waiting. Send messages for decisions or new information; inspect status only for concrete uncertainty.
7. On completion or blocked stop (or request), run `python3 agentic-workflow/helpers/usage_report.py .agentic-workflow/NNN_name`; link reports and coverage limits. For trace issues, use [TRACING.md](helpers/TRACING.md).

## Task mode

| Condition | Mode |
|---|---|
| Required planning/review, complex work, or uncertainty | `full` |
| Simple, bounded work with clear source criteria | `lightweight` |

Honor user/source requirements; unresolved conflicts block dispatch. Model choice does not determine mode.
