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
  - Check requirements and regressions under [CHECKS].
  - Inspect the diff.
  - Record evidence and mock justifications under [CHECKS] and [RECORDS].
  - Fix defects and rerun affected checks.
  - Plan-review: follow [Hand off for review](#hand-off-for-review).
  - Report blockers promptly.
  - Return work under [RECORDS] (“Return work”).
- Outputs:
  - Implementation, Evidence, Result.
  - Plan-review mode: Plan and Acceptance.
  - When useful lessons are saved: Memory.
- Next:
  - Direct mode: return the Result to Supervisor for acceptance.
  - Repeat affected task steps when Supervisor assigns corrections.

## Hand off for review

- Context: apply in plan-review mode after implementation or review corrections.
- Inputs: Implementation, Acceptance and Evidence, plus Reviewer findings when assigned corrections.
- Effects:
  - When resuming after review, confirm explicit release from Supervisor before editing.
  - Fix assigned findings and rerun affected checks before handing off again.
  - Save the Result under [RECORDS] (“Return work”).
  - Record readiness for review in the Result and mark independent review `NOT_RUN`.
  - Return the Result path and indicate readiness for review in the final reply.
- Outputs: Implementation, Acceptance, Evidence and Result for Supervisor.
- Next: End the turn at the handoff.

## Plan-review mode

Apply when assigned `plan-review` mode.

- Before code, write `plan.md` using [PLAN_TEMPLATE].
- Before code, write `acceptance.md` using [ACCEPTANCE_TEMPLATE] and [CHECKS] (“Prepare acceptance”).
- Implement the task.

## Direct mode

Apply when assigned `direct` mode.

- Implement and check source criteria under [CHECKS] (“Prepare checks”).
- Skip plan, separate acceptance and task review.
- Keep the assigned mode.
