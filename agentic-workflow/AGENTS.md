# Agentic Workflow

Routes workflow actions to role instructions and shared policies.

## References:

- [SUPERVISOR]: Coordinates implementation, recovery and acceptance. agentic-workflow/roles/SUPERVISOR.md
- [PLANNER]: Authors project documents and maintains workflow instructions. agentic-workflow/roles/PLANNER.md
- [IMPLEMENTER]: Implements assigned tasks and manages corrections. agentic-workflow/roles/IMPLEMENTER.md
- [REVIEWER]: Independently reviews task requirements and implementation. agentic-workflow/roles/REVIEWER.md
- [VALIDATOR]: Validates the assembled app and publishes repair tasks. agentic-workflow/roles/VALIDATOR.md
- [GLOSSARY]: Defines shared roles, inputs and outputs. agentic-workflow/GLOSSARY.md
- [BUNDLE]: Defines specification files, task selection and path resolution. agentic-workflow/policies/BUNDLE.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [MEMORY]: Defines how to read and maintain project lessons. agentic-workflow/policies/MEMORY.md
- [RECONSTRUCTION]: Defines rebuilding from allowed inputs without prior implementation. agentic-workflow/policies/RECONSTRUCTION.md
- [WORKFLOW_REVIEW]: Defines requested workflow conformance reviews. agentic-workflow/guides/WORKFLOW_REVIEW.md
- [README]: Explains installation, package ownership and portable commands. agentic-workflow/README.md
- [TRACING]: Explains native capture, trace inspection and usage reporting. agentic-workflow/guides/TRACING.md
- [GUIDELINES]: Defines engineering rules for code, tests and tooling. agentic-workflow/policies/GUIDELINES.md
- [MODELS]: Provides heuristics for choosing subagent models. agentic-workflow/policies/MODELS.md
- [DOCUMENT_STYLE]: Defines document structure and reference conventions. agentic-workflow/policies/DOCUMENT_STYLE.md
- [PLAN_TEMPLATE]: Structures task implementation plans. agentic-workflow/templates/plan.md
- [ACCEPTANCE_TEMPLATE]: Maps requirements to observable checks and pass rules. agentic-workflow/templates/acceptance.md
- [RESULT_TEMPLATE]: Records completion status, evidence, findings and limits. agentic-workflow/templates/result.md

## Entry points

Read the context for your action:

| Action | Context |
|---|---|
| Implement specifications, including one task | [SUPERVISOR], enter as Supervisor |
| Update or repair an existing app against revised specifications | [SUPERVISOR] (“Reconcile an existing implementation”) |
| Coordinate tasks | [SUPERVISOR] |
| Plan or edit documents/workflow | [PLANNER] |
| Implement a task | [IMPLEMENTER] |
| Review a task | [REVIEWER] |
| Validate the app | [VALIDATOR] |
| Interpret role inputs and outputs | [GLOSSARY] |
| Resolve specifications | [BUNDLE] |
| Define or assess checks | [CHECKS] |
| Hand off, save or resume work | [RECORDS] |
| Ordinary planning/implementation | [MEMORY] |
| Rebuild without prior implementation | [RECONSTRUCTION], before any role starts |
| Review workflow documents | [WORKFLOW_REVIEW] |
| Install or check the package/optional skills | [README] |
| Inspect traces or usage | [TRACING] |

Every role reads [GUIDELINES] and applies its context documents.
When choosing subagents and their models, use `.agentic-workflow/config/MODELS.md`
if present, otherwise [MODELS].
Follow conditional references when applicable.
Before authoring or editing project documents,
read and apply [DOCUMENT_STYLE], regardless of role.
Keep project inputs, code, memory and execution evidence outside this package.

Find specification templates in [BUNDLE]; use [PLAN_TEMPLATE], [ACCEPTANCE_TEMPLATE] and [RESULT_TEMPLATE] for execution documents.
