# App generation

- `spec-source-suite/` is reusable guidance. Change it only for requested workflow/tooling work; keep app inputs, code and evidence outside it.
- For any spec implementation, including `Implement specs/todolist`, read the [suite entry points](spec-source-suite/AGENTS.md) and act as [Supervisor](spec-source-suite/SUPERVISOR.md). Named skills are optional.
- For ordinary work, implement directly or briefly plan first; apply engineering guidelines, run relevant checks, inspect the diff and report results. Formal workflow artifacts and roles are optional unless requested. Plan-only requests stop at the plan; preserve explicit approval requirements.
- For suite maintenance or explicit suite roles/skills, follow the applicable suite guidance. Use the paths below directly and batch independent reads; search only for unresolved inputs.
- For fresh or continuing suite work, follow [Records](spec-source-suite/RECORDS.md). Ordinary planners/implementers must follow [Memory](spec-source-suite/MEMORY.md). Advice/tooling work uses requested files and relevant references without task-history discovery.
- Resolve spec inputs and authority through [Bundle](spec-source-suite/BUNDLE.md). Use [Planner](spec-source-suite/PLANNER.md) for document-only authoring and suite maintenance. Future-runner requirements are not app requirements.

| Read when | Path |
|---|---|
| Before planning, writing, changing or reviewing code/tests/tooling | [Engineering guidelines](spec-source-suite/GUIDELINES.md) |
| Suite work: role and reference entry points | [Suite entry points](spec-source-suite/AGENTS.md) |
| Entering a role or selecting worker settings | [Model routing](spec-source-suite/MODELS.md) |
| Coordinating spec implementation | [Supervisor](spec-source-suite/SUPERVISOR.md) |
| Authoring or maintaining documents | [Planner](spec-source-suite/PLANNER.md) |
| Executing an assigned task | [Implementer](spec-source-suite/IMPLEMENTER.md) |
| Assigned independent task review | [Reviewer](spec-source-suite/REVIEWER.md) |
| Assigned final app validation | [Validator](spec-source-suite/VALIDATOR.md) |
| Resolving specification inputs | [Bundle](spec-source-suite/BUNDLE.md) |
| Preparing or assessing verification | [Checks](spec-source-suite/CHECKS.md) |
| Saving, handing off or resuming work | [Records](spec-source-suite/RECORDS.md) |
| Ordinary planning or implementation | [Memory](spec-source-suite/MEMORY.md) |
| Rebuilding without prior implementation | [Reconstruction](spec-source-suite/RECONSTRUCTION.md) |
| Authoring project inputs | [Project](spec-source-suite/templates/project.md), [task order](spec-source-suite/templates/task_order.md), [task](spec-source-suite/templates/tasks/task.md), [verification](spec-source-suite/templates/verification.md) |
| Authoring task records | [Plan](spec-source-suite/templates/plan.md), [acceptance](spec-source-suite/templates/acceptance.md), [result](spec-source-suite/templates/result.md) |
| Checking suite changes | [Package checker](spec-source-suite/helpers/check_package.py) |
| Allocating implementations or resuming tasks | [Records helper](spec-source-suite/helpers/records.py) |
| Aggregating execution usage | [Usage helper](spec-source-suite/helpers/usage_report.py) |
| Operating or troubleshooting tracing | [Tracing](spec-source-suite/helpers/TRACING.md) |
| Requested automated-runner work | [Future runner](spec-source-suite/RUNNER.md) |
| Running or maintaining the todolist eval | [Eval guide](evals/README.md) |
