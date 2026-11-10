# Implementer

Implement assigned tasks, verify their behavior and manage corrections.

## References:

- [GLOSSARY]: Defines shared roles, inputs and outputs. agentic-workflow/GLOSSARY.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [AGENTS]: Routes actions to role instructions and shared policies. agentic-workflow/AGENTS.md
- [BUNDLE]: Defines specification files, task selection and path resolution. agentic-workflow/policies/BUNDLE.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [MEMORY]: Defines how to read and maintain project lessons. agentic-workflow/policies/MEMORY.md
- [PLAN_TEMPLATE]: Structures task implementation plans. agentic-workflow/templates/plan.md
- [ACCEPTANCE_TEMPLATE]: Maps requirements to observable checks and pass rules. agentic-workflow/templates/acceptance.md
- [REVIEWER]: Independently reviews task requirements and implementation. agentic-workflow/roles/REVIEWER.md

## Execute a task

Use the [GLOSSARY] and [RECORDS] (“Hand off work”).

- Context:
  - Instructions: read [AGENTS], [BUNDLE], [CHECKS] and [RECORDS].
  - Ordinary work also uses [MEMORY].
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
  - Include mock justifications under [CHECKS].
  - Fix defects.
  - Rerun affected checks.
  - Preserve approved originals when fixing source omissions.
  - Plan-review: complete review below.
  - Report blockers promptly.
  - Return work under [RECORDS] (“Return work”).
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

- Write `plan.md` using [PLAN_TEMPLATE] before code.
- Write `acceptance.md` using [ACCEPTANCE_TEMPLATE] before code.
- Link acceptance to sources.
- Include public API contracts under [CHECKS].
- Include expected test scenarios under [CHECKS].
- Implement the task.

## Direct mode

Apply when assigned `direct` mode.

- Implement against source criteria.
- Run checks against source criteria.
- Skip plan, separate acceptance and task review.
- Keep the assigned mode.

## Review a plan-review task

- Context: Instructions include [CHECKS] and the input/output contract in [REVIEWER].
- Inputs: Assignment, Project specification, assigned Task specification, applicable Contracts and Verification, Implementation, Acceptance, Evidence and prior Result when available.
- Effects:
  - Agree on review boundary with Supervisor.
  - Wait for confirmation that affected writers are paused.
  - Spawn a fresh Reviewer with an Assignment and its named inputs under [RECORDS] and [CHECKS].
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
