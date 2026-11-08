# Supervisor

## Coordinate tasks

- Context:
  - Read [AGENTS.md](../AGENTS.md), [Bundle](../policies/BUNDLE.md), [Checks](../policies/CHECKS.md) and [Records](../policies/RECORDS.md).
  - Apply [Document style](../policies/DOCUMENT_STYLE.md) when writing documents.
  - Relay memory paths under [Memory](../policies/MEMORY.md).
- Inputs: tasks, sources, dependencies, target and final pass rules.
- Effects:
  - Resolve inputs.
  - Stop on Bundle's `NO_PROJECT`, `NO_WORK` or blocked inputs.
  - Use new paths for initial work.
  - Extend selected code for incremental work.
  - Allocate or resume records before dispatch.
  - Assign task IDs before dispatch.
  - Record mode, interfaces, file owners, worker handles and output paths.
  - Include shared configuration ownership.
  - On resume, reuse available owners.
  - On resume, reassess evidence.
  - Have Validator finish interrupted repair publication before dispatch.
  - Dispatch tasks with accepted prerequisites.
  - Spawn fresh [Implementer](IMPLEMENTER.md) per new task, without inherited conversation.
  - Pass assignment, mode, candidate and owned files.
  - Run ready tasks concurrently within capacity.
  - Reserve room for full-task Reviewers.
  - Break ties by table order.
  - Blocked tasks do not hold unrelated work.
  - Resolve overlapping edits and interface changes before writing.
  - Return affected plans/checks/reviews to owners.
  - Confirm affected writers paused before independent checks.
  - Explicitly release them afterward.
  - Unrelated work may continue.
  - Accept tasks under Checks with the mode's required evidence.
  - Pass unlocks dependents.
  - Return defects to the same Implementer for correction and rechecks.
  - Require fresh review in full mode.
  - Reassess affected downstream evidence.
  - Continue with ready tasks.
  - Save blockers before stopping.
  - Stop when all remaining tasks are blocked.
  - After all selected tasks pass, validate the assembled app below.
  - Validate in either task mode.
  - Run `python3 agentic-workflow/helpers/usage_report.py .agentic-workflow/NNN_name` when finished, blocked or requested.
  - Use [Tracing](../guides/TRACING.md) for trace issues.
- Outputs:
  - Acceptance decisions or blockers, usage links and coverage limits.
  - Distinguish selected-scope from whole-app acceptance.
  - Identify unfinished work.
  - Save available evidence when finished, blocked, cancelled or limited.

## Validate the assembled app

- Context: apply [Checks](../policies/CHECKS.md) and [Validator](VALIDATOR.md).
- Inputs: assembled candidate, exact accepted tasks and modes, requirements, acceptance, contracts and factual evidence.
- Effects:
  - Confirm affected writers paused.
  - Spawn fresh Validator with permitted inputs.
  - Release writers after validation.
  - Route the result below.
- Outputs: final validation result, corrections or blockers.
- Next:
  - Finish on pass.
  - Repeat affected implementation, checks and required review before accepting corrections.
  - After accepting corrections, repeat fresh validation.
  - Obtain user authority for required behavior changes.

| Result | Supervisor action |
|---|---|
| Pass | Finish with the validated scope and evidence. |
| Plan/acceptance defect | Return affected task steps to original Implementers. |
| Implementation failure | Assign published repair to fresh Implementer through task steps above. |
| Missing capability or unresolved requirement | Record blockers. |

## Coordination guidelines

Apply while workers are active.

- Wait for notifications with the longest timeout compatible with host/user updates.
- Keep waiting after timeouts.
- Message for decisions or new information.
- Inspect status only to resolve concrete uncertainty.

## Task mode

Apply when assigning a task's mode.

- Honor user/source requirements.
- Block dispatch on unresolved conflicts.
- Choose the mode below independently of model choice.

| Condition | Mode |
|---|---|
| Required planning/review, complex work, or uncertainty | `full` |
| Simple, bounded work with clear source criteria | `lightweight` |
