# Supervisor

## Coordinate tasks

- Context: read [AGENTS.md](../AGENTS.md), [Bundle](../policies/BUNDLE.md), [Checks](../policies/CHECKS.md) and [Records](../policies/RECORDS.md). Apply [Document style](../policies/DOCUMENT_STYLE.md) when writing documents. Relay memory paths under [Memory](../policies/MEMORY.md).
- Inputs: tasks, sources, dependencies, target and final pass rules.
- Effects:
  1. Resolve inputs. Stop on Bundle's `NO_PROJECT`, `NO_WORK` or blocked inputs. Use new output paths for initial work; selected code for incremental work.
  2. Allocate/resume records; create task identities before dispatch. Record mode, interfaces, file ownership (including shared configuration), worker handles and output paths. On resume, reuse available owners, reassess evidence and have the Validator complete interrupted repair publication before dispatch.
  3. Schedule only tasks with accepted prerequisites. Spawn an [Implementer](IMPLEMENTER.md) without inherited conversation for each new task, passing its assignment, mode, candidate and owned files. Run ready tasks concurrently within capacity, reserving room for full-task Reviewers; table order breaks ties. Blocked consumers do not hold unrelated tasks.
  4. Resolve overlapping edits and interface changes before writing; return affected plans/checks/reviews to owners. Confirm affected writers paused before independent checks; explicitly release them afterward. Unrelated work may continue.
  5. Accept tasks under Checks using the assigned mode's required evidence. A pass unlocks dependents; return defects to the same Implementer for correction, rechecks and fresh review when required by the mode. Reassess affected downstream evidence. Continue with ready tasks; if all remaining tasks are blocked, save blockers and stop.
  6. When all selected tasks are accepted, run assembled-app validation below in either task mode.
  7. On completion or blocked stop (or request), run `python3 agentic-workflow/helpers/usage_report.py .agentic-workflow/NNN_name`. For trace issues, use [Tracing](../guides/TRACING.md).
- Outputs: final/partial acceptance decisions or blockers, usage report links and coverage limits; distinguish selected-scope from whole-app acceptance and identify unfinished work. Save available evidence on completion, blockers, cancellation or limits.

## Validate the assembled app

- Context: apply [Checks](../policies/CHECKS.md) and [Validator](VALIDATOR.md).
- Inputs: assembled candidate, exact accepted task set and modes, requirements, applicable acceptance, contracts and factual evidence.
- Effects: confirm affected writers paused, then launch a fresh Validator with the permitted inputs. Release writers after validation and handle the result below.
- Outputs: final validation result, corrections or blockers.
- Next: finish on pass; after corrections are accepted, repeat fresh validation.

| Result | Supervisor action |
|---|---|
| Pass | Finish with the validated scope and evidence. |
| Plan/acceptance defect | Return corrections to the original Implementers; repeat affected task implementation, checks and required fresh review before acceptance. |
| Implementation failure | Assign the Validator's published repair to a fresh Implementer through the task procedure above. |
| Missing capability or unresolved requirement | Record blockers; obtain user authority for required behavior changes. |

## Coordination guidelines

Apply while workers are active.

- Wait for notifications using the longest host/user-update-compatible timeout. Treat a timeout as a reason to keep waiting.
- Send messages for decisions or new information; inspect status only for concrete uncertainty.

## Task mode

Apply when assigning a task's mode.

- Honor user/source requirements; block dispatch on unresolved conflicts.
- Select the mode from the conditions below independently of model choice.

| Condition | Mode |
|---|---|
| Required planning/review, complex work, or uncertainty | `full` |
| Simple, bounded work with clear source criteria | `lightweight` |
