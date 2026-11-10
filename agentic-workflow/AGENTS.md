# Agentic Workflow

Use this index to locate context needed for the current task.
A reference alone does not require reading its target.
Open documents when their context is needed or an applicable instruction explicitly requires them.

Routes workflow actions to role instructions and shared policies.

## References:

- [SUPERVISOR]: Enter as Supervisor to implement specifications (including one task) or coordinate tasks; to update or repair an existing app against revised specifications, use “Reconcile an existing implementation”. agentic-workflow/roles/SUPERVISOR.md
- [PLANNER]: Plan or edit documents/workflow. agentic-workflow/roles/PLANNER.md
- [IMPLEMENTER]: Implement a task. agentic-workflow/roles/IMPLEMENTER.md
- [REVIEWER]: Review a task. agentic-workflow/roles/REVIEWER.md
- [VALIDATOR]: Validate the app. agentic-workflow/roles/VALIDATOR.md
- [GLOSSARY]: Interpret roles, inputs and outputs. agentic-workflow/GLOSSARY.md
- [BUNDLE]: Resolve specifications. agentic-workflow/policies/BUNDLE.md
- [CHECKS]: Define or assess checks. agentic-workflow/policies/CHECKS.md
- [RECORDS]: Hand off, save or resume work. agentic-workflow/policies/RECORDS.md
- [MEMORY]: Carry out ordinary planning or implementation. agentic-workflow/policies/MEMORY.md
- [RECONSTRUCTION]: Rebuild without prior implementation, reading before any role starts. agentic-workflow/policies/RECONSTRUCTION.md
- [WORKFLOW_REVIEW]: Review workflow documents. agentic-workflow/guides/WORKFLOW_REVIEW.md
- [README]: Install or check the package/optional skills. agentic-workflow/README.md
- [TRACING]: Inspect traces or usage. agentic-workflow/guides/TRACING.md
- [GUIDELINES]: Plan, change or review code, tests or tooling. agentic-workflow/policies/GUIDELINES.md
- [MODELS]: Choose subagents and their models. agentic-workflow/policies/MODELS.md
- [DOCUMENT_STYLE]: Author or edit project documents. agentic-workflow/policies/DOCUMENT_STYLE.md
- [PLAN_TEMPLATE]: Write a task implementation Plan. agentic-workflow/templates/plan.md
- [ACCEPTANCE_TEMPLATE]: Write Acceptance criteria and checks. agentic-workflow/templates/acceptance.md
- [RESULT_TEMPLATE]: Record a Result with status, evidence, findings and limits. agentic-workflow/templates/result.md

## Shared instructions

Every role reads [GUIDELINES] and applies its context documents.
When choosing subagents and their models, use `.agentic-workflow/config/MODELS.md`
if present, otherwise [MODELS].
Follow conditional references when applicable.
Before authoring or editing project documents,
read and apply [DOCUMENT_STYLE], regardless of role.
Keep project inputs, code, memory and execution evidence outside this package.

Find specification templates in [BUNDLE]; use [PLAN_TEMPLATE], [ACCEPTANCE_TEMPLATE] and [RESULT_TEMPLATE] for execution documents.
