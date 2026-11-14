# Implementer

Author documents, maintain workflow instructions, plan and implement assigned work, check results and manage corrections.

## References:

- [WORK_INPUT]: Defines WorkInput fields. agentic-workflow/contracts/WORK_INPUT.md
- [WORK_RESULT]: Defines WorkResult fields. agentic-workflow/contracts/WORK_RESULT.md
- [GLOSSARY]: Defines shared roles, inputs and outputs. agentic-workflow/GLOSSARY.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [AGENTS]: Routes actions to role instructions and shared policies. agentic-workflow/AGENTS.md
- [BUNDLE]: Defines specification files, task selection and path resolution. agentic-workflow/policies/BUNDLE.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [MEMORY]: Defines how to read and maintain project lessons. agentic-workflow/policies/MEMORY.md
- [DOCUMENT_STYLE]: Defines document structure and reference conventions. agentic-workflow/policies/DOCUMENT_STYLE.md
- [PLAN_TEMPLATE]: Structures task implementation plans. agentic-workflow/templates/PLAN.md
- [ACCEPTANCE_TEMPLATE]: Maps requirements to observable checks and pass rules. agentic-workflow/templates/ACCEPTANCE.md
- [README]: Explains installation, package ownership and portable commands. agentic-workflow/README.md
- [WORKFLOW_REVIEW]: Defines requested workflow conformance reviews. agentic-workflow/guides/WORKFLOW_REVIEW.md

## Contracts

- Provides: `execute_work(input: WorkInput) -> WorkResult` using [WORK_INPUT] and [WORK_RESULT].

## Execute work

- Context:
  - Instructions: read [AGENTS], [BUNDLE], [CHECKS] and [RECORDS].
  - Ordinary work also uses [MEMORY].
  - Document authoring applies [DOCUMENT_STYLE].
- Inputs: [WORK_INPUT].
- Effects:
  1. Read description and sources to resolve the authorized work, mode, ownership, output paths and current execution phase.
  2. Agree on scope and file ownership with Supervisor before concurrent edits.
  3. Reuse applicable existing documents and Results when resuming unfinished work or addressing assigned findings.
  4. Confirm explicit Supervisor release before editing after independent checking.
  5. Author requested documents through [Author documents](#author-documents).
  6. For authorized implementation, follow the assigned [plan-review](#plan-review-mode) or [direct](#direct-mode) procedure.
  7. Check requirements and regressions under [CHECKS] and inspect the diff.
  8. Record evidence and mock justifications under [CHECKS] and [RECORDS].
  9. Fix defects and rerun affected checks.
  10. Report blockers promptly.
  11. For a completed plan-review candidate, return through [Hand off for review](#hand-off-for-review).
  12. For other work, save the Result and return under [RECORDS] (“Return work”).
- Outputs: [WORK_RESULT].
- Next:
  - End the turn at the review handoff.
  - Return direct work to Supervisor for acceptance.
  - Stop document-only or plan-only work at the authorized documents.
  - Repeat affected steps when Supervisor assigns corrections through [WORK_INPUT].

## Author documents

- Context: apply when the description authorizes document authoring or corrections.
- Inputs: [WORK_INPUT].
- Effects:
  1. Resolve governing sources and authorized destinations from the assignment.
  2. Write authorized documents using templates from [BUNDLE], [PLAN_TEMPLATE] or [ACCEPTANCE_TEMPLATE].
  3. Apply [CHECKS] (“Prepare acceptance”) when authoring or correcting Acceptance.
  4. Check source coverage, consistency, component boundaries, contract alignment, links and dependencies.
  5. Check that pass rules are observable.
  6. Report unresolved requirements and unavailable checks.
- Outputs: [WORK_RESULT], saved by [Execute work](#execute-work).
- Next: proceed to application implementation only when separately authorized under [BUNDLE].

## Hand off for review

- Context: apply in plan-review mode after implementation or review corrections.
- Inputs: [WORK_INPUT].
- Effects:
  1. Complete assigned findings and affected rechecks before handing off again.
  2. Record readiness for review in the Result and mark independent review `NOT_RUN`.
  3. Save the Result under [RECORDS] (“Return work”) before returning [WORK_RESULT].
- Outputs: [WORK_RESULT] with review readiness.
- Next: end the turn and wait for Supervisor release before further edits.

## Plan-review mode

Apply when assigned `plan-review` mode for authorized implementation.

- Before application implementation, write or reuse an applicable `plan.md` using [PLAN_TEMPLATE].
- Before application implementation, write or reuse an applicable `acceptance.md` using [ACCEPTANCE_TEMPLATE] and [CHECKS] (“Prepare acceptance”).
- Implement the task after both documents are ready and any explicit approval requirement is satisfied.

## Direct mode

Apply when assigned `direct` mode for authorized implementation.

- Implement and check source criteria under [CHECKS] (“Prepare checks”).
- Skip Plan, separate Acceptance and task review.
- Keep the assigned mode.

## Workflow maintenance

Apply when changing workflow instructions or tooling.

- Index referenced documents under [DOCUMENT_STYLE] with explicit read conditions.
- Exclude transient execution artifacts.
- Keep indexes within existing role permissions.
- Check preserved behavior and complete role reading paths.
- Run package checks and relevant tests from [README] (“Requirements and portable commands”).
- Include the integration check for root or skill changes.
- Use [WORKFLOW_REVIEW] for requested document conformance reviews.
- Report documentation checks separately from live app experiments.
