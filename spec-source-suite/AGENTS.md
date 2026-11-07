# Suite entry points

- This suite provides reusable instructions, templates and local helpers. Keep app inputs, code, memory and evidence outside it; no app or automated runner is selected by installing it.
- For any role, read [engineering guidelines](GUIDELINES.md), [model routing](MODELS.md) and the role below. Follow its linked references when their stated conditions apply.
- For specification implementation, including one task, enter through [Supervisor](SUPERVISOR.md). For document-only work or suite maintenance, use [Planner](PLANNER.md).
- Load role files directly. The explicit `spec-planner` and `spec-supervisor` skills in `.agents/skills/` are optional entry points.
- When adopting the suite, merge repository instructions and verify host capabilities. Worker flags, setting controls and isolation depend on the host.

| Read when | Document |
|---|---|
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
