# Implementer

Use the [shared vocabulary](../GLOSSARY.md) and [Assignment and Result handling](../policies/RECORDS.md#hand-off-work).

## Execute a task

- Context:
  - Instructions: read [AGENTS.md](../AGENTS.md), [Bundle](../policies/BUNDLE.md), [Checks](../policies/CHECKS.md) and [Records](../policies/RECORDS.md).
  - Ordinary work also uses [Memory](../policies/MEMORY.md).
- Inputs:
  - Assignment, Project specification, assigned Task specification, applicable Contracts and Verification, Implementation.
  - When continuing: prior Result and any existing Plan and Acceptance.
  - Ordinary work: Memory.
- Effects:
  - Read Instructions and assigned inputs before planning or editing.
  - Agree on scope and file ownership with Supervisor before concurrent edits.
  - Follow the assigned mode below.
  - Check requirements and regressions.
  - Inspect the diff.
  - Record check evidence.
  - Include mock justifications under Checks.
  - Fix defects.
  - Rerun affected checks.
  - Preserve approved originals when fixing source omissions.
  - Plan-review: complete review below.
  - Report blockers promptly.
  - Return work under [Records](../policies/RECORDS.md#return-work).
- Outputs:
  - Implementation, Evidence, Result.
  - Plan-review mode: Plan and Acceptance.
  - When useful lessons are saved: Memory.
- Next:
  - Return result to Supervisor for acceptance.
  - Keep this context for corrections.
  - Repeat affected task steps.

## Plan-review mode

Apply when assigned `plan-review` mode.

- Write [plan.md](../templates/plan.md) before code.
- Write [acceptance.md](../templates/acceptance.md) before code.
- Link acceptance to sources.
- Include public API contracts under Checks.
- Include expected test scenarios under Checks.
- Implement the task.

## Direct mode

Apply when assigned `direct` mode.

- Implement against source criteria.
- Run checks against source criteria.
- Skip plan, separate acceptance and task review.
- Keep the assigned mode.

## Review a plan-review task

- Context: Instructions include [Checks](../policies/CHECKS.md) and the [Reviewer input/output contract](REVIEWER.md).
- Inputs: Assignment, Project specification, assigned Task specification, applicable Contracts and Verification, Implementation, Acceptance, Evidence and prior Result when available.
- Effects:
  - Agree on review boundary with Supervisor.
  - Wait for confirmation that affected writers are paused.
  - Spawn a fresh Reviewer with an Assignment and its named inputs under Records and Checks.
  - Pass mock justifications with check evidence.
  - Report review completion to Supervisor.
  - Wait for explicit release before writing.
  - Fix actionable findings.
  - Rerun affected checks.
  - Repeat with fresh Reviewer.
  - Keep task ownership through corrections.
- Outputs: Implementation, Evidence and Result, including the Reviewer Result reference.
- Next:
  - After review passes, return task result to Supervisor.
