# Future automated runner

- Read only when runner implementation is requested. This is an automation assignment, not an app specification or a claim that automation exists.
- Inspect repository conventions and installed worker help. Build a bundle reader/validator, dependency scheduler, role/review adapters, project-check adapter and durable result store using the contracts below.
- Support document authoring, single-task execution, whole-app generation, status/resume, incremental work and reconstruction with existing bundle/task/run locations. Follow [workflow entry points](AGENTS.md) and the [Workflow contract](WORKFLOW.md); add no separate orchestration policy.
- Keep the runner app/stack-neutral. Add no hosted control plane, mandatory manifests, frozen checks or approval receipts. Record manual fallback origins and unavailable capabilities honestly.
- Verify mechanics with synthetic dependency graphs, inert artifacts, stub/manual adapters, explicit failures and excluded sentinel files. Map evidence to these IDs; report implemented automation, documentation walkthroughs and live app experiments separately. Fixtures alone do not establish successful generation or reconstruction.

| ID | Required behavior and evidence |
|---|---|
| AGENTIC_WORKFLOW-001 | Empty installation has no selected app/stack; no intent returns `NO_PROJECT`. |
| AGENTIC_WORKFLOW-002 | Read [Bundle](BUNDLE.md); report missing files, duplicate IDs, unknown references, cycles and missing required acceptance mappings. |
| AGENTIC_WORKFLOW-003 | Schedule tasks using [Supervisor](SUPERVISOR.md) prerequisites, capacity and mode rules. |
| AGENTIC_WORKFLOW-004 | Execute [Workflow task steps](WORKFLOW.md#spawn-implementer--per-task) and [Implementer](IMPLEMENTER.md) procedures for the assigned mode, preserving explicit requirements and approved text while resolving ordinary choices autonomously. |
| AGENTIC_WORKFLOW-005 | Dispatch and retain role contexts through Workflow; keep document-only work with [Planner](PLANNER.md). Verify required independent checks under [Checks](CHECKS.md). |
| AGENTIC_WORKFLOW-006 | Apply Checks using actual outcomes, adequate coverage, required manual checks and explicit unavailable capabilities. |
| AGENTIC_WORKFLOW-007 | Resume from [Records](RECORDS.md); preserve history and reassess evidence after relevant changes. |
| AGENTIC_WORKFLOW-008 | Carry and maintain useful lessons under [Memory](MEMORY.md). |
| AGENTIC_WORKFLOW-009 | Apply [Reconstruction](RECONSTRUCTION.md), including allowed inputs, cross-target behavior and tested separation limits. |
| AGENTIC_WORKFLOW-010 | Run [Validator](VALIDATOR.md); exercise failed assembly, repair creation, interrupted repair recovery and subsequent validation through the Supervisor. |
| AGENTIC_WORKFLOW-011 | Preserve results/blockers on cancellation, limits or missing infrastructure; preserve source workspaces and keep credentials out of logs. |
| AGENTIC_WORKFLOW-012 | Support worker/project adapters without app assumptions; test stub/manual paths and unavailable tools honestly. |
| AGENTIC_WORKFLOW-013 | Capture all five roles' native session/turn references, including repairs and blocked work; use the existing [usage helper](helpers/usage_report.py). Link compatible totals, role/session statistics, known subtotals and limits. Missing telemetry never blocks app acceptance. |
