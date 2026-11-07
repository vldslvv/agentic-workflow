# Future automated runner

- Read only when runner implementation is requested. This is an automation assignment, not an app specification or a claim that automation exists.
- Inspect repository conventions and installed worker help. Build a bundle reader/validator, dependency scheduler, role/review adapters, project-check adapter and durable result store using the contracts below.
- Support document authoring, single-task execution, whole-app generation, status/resume, incremental work and reconstruction with existing bundle/task/run locations. Follow [suite entry points](AGENTS.md); add no separate orchestration policy.
- Keep the runner app/stack-neutral. Add no hosted control plane, mandatory manifests, frozen checks or approval receipts. Record manual fallback origins and unavailable capabilities honestly.
- Verify mechanics with synthetic dependency graphs, inert artifacts, stub/manual adapters, explicit failures and excluded sentinel files. Map evidence to these IDs; report implemented automation, documentation walkthroughs and live app experiments separately. Fixtures alone do not establish successful generation or reconstruction.

| ID | Required behavior and evidence |
|---|---|
| SUITE-001 | Empty installation has no selected app/stack; no intent returns `NO_PROJECT`. |
| SUITE-002 | Read [Bundle](BUNDLE.md); report missing files, duplicate IDs, unknown references, cycles and missing required acceptance mappings. |
| SUITE-003 | Schedule from the dependency table using [Supervisor](SUPERVISOR.md), including its task-mode decisions. |
| SUITE-004 | Follow [Implementer](IMPLEMENTER.md) document requirements for the assigned mode, preserving explicit requirements and approved text while resolving ordinary choices autonomously. |
| SUITE-005 | Dispatch and retain role contexts through the current Supervisor/Implementer workflows; keep document-only work with [Planner](PLANNER.md). Verify required independent checks under [Checks](CHECKS.md). |
| SUITE-006 | Apply Checks using actual outcomes, adequate coverage, required manual checks and explicit unavailable capabilities. |
| SUITE-007 | Resume from [Records](RECORDS.md); preserve history and reassess evidence after relevant changes. |
| SUITE-008 | Carry and maintain useful lessons under [Memory](MEMORY.md). |
| SUITE-009 | Apply [Reconstruction](RECONSTRUCTION.md), including allowed inputs, cross-target behavior and tested separation limits. |
| SUITE-010 | Run [Validator](VALIDATOR.md); exercise failed assembly, repair creation, interrupted repair recovery and subsequent validation through the Supervisor. |
| SUITE-011 | Preserve results/blockers on cancellation, limits or missing infrastructure; preserve source workspaces and keep credentials out of logs. |
| SUITE-012 | Support worker/project adapters without app assumptions; test stub/manual paths and unavailable tools honestly. |
| SUITE-013 | Capture all five roles' native session/turn references, including repairs and blocked work; use the existing [usage helper](helpers/usage_report.py). Link compatible totals, role/session statistics, known subtotals and limits. Missing telemetry never blocks app acceptance. |
