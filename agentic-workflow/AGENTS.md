# Agentic Workflow entry points

- Agentic Workflow provides reusable instructions, templates and local helpers. Keep app inputs, code, memory and evidence outside it; no app or automated runner is selected by installing it.
- For any role, read [engineering guidelines](GUIDELINES.md), resolve model routing under [Models](MODELS.md#routing-source), and read the role below. Follow its linked references when their stated conditions apply.
- For specification implementation, including one task, read [Workflow](WORKFLOW.md) and enter through [Supervisor](SUPERVISOR.md). Every implementation role follows that contract. For document-only work or workflow maintenance, use [Planner](PLANNER.md).
- Load role files directly. The explicit `agentic-workflow-planner`, `agentic-workflow-supervisor` and `agentic-workflow-acceptance` skills in the project's `.agents/skills/` are optional entry points; installation is described in [README](README.md).
- When adopting the workflow, merge repository instructions and verify host capabilities. Worker flags, setting controls and isolation depend on the host.

| Read when | Document |
|---|---|
| Installing, updating or checking the package | [Installation and portable commands](README.md) |
| Entering a role or selecting worker settings | [Model routing](MODELS.md) |
| Implementing specifications or changing the implementation workflow | [Workflow contract](WORKFLOW.md) |
| Asked to review documents against the workflow | [Workflow document review](WORKFLOW_REVIEW.md) |
| Coordinating implementation | [Supervisor](SUPERVISOR.md) |
| Authoring or maintaining documents | [Planner](PLANNER.md) |
| Executing an assigned task | [Implementer](IMPLEMENTER.md) |
| Independently reviewing a task | [Reviewer](REVIEWER.md) |
| Independently validating the assembled app | [Validator](VALIDATOR.md) |
| Resolving specification inputs | [Bundle](BUNDLE.md) |
| Preparing, running or assessing checks | [Checks and acceptance](CHECKS.md) |
| Saving, handing off or resuming work | [Records](RECORDS.md) |
| Ordinary planning or implementation | [Project memory](MEMORY.md) |
| Rebuilding without prior implementation | [Reconstruction](RECONSTRUCTION.md) |
| Implementing a requested automated runner | [Future runner](RUNNER.md) |
| Operating or troubleshooting tracing | [Native trace reference](helpers/TRACING.md) |
| Authoring project inputs | [Project](templates/project.md), [task order](templates/task_order.md), [task](templates/tasks/task.md), [verification](templates/verification.md) |
| Authoring task records | [Plan](templates/plan.md), [acceptance](templates/acceptance.md), [result](templates/result.md) |
| Checking package changes | [Package checker](helpers/check_package.py) |
| Allocating implementations or resuming tasks | [Records helper](helpers/records.py) |
| Aggregating execution usage | [Usage helper](helpers/usage_report.py) |
