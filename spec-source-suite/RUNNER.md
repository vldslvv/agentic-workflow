# Optional future automated runner

Read only when runner implementation is requested. This assignment is not an app specification or a claim that automation exists. Ordinary role startup needs only [AGENTS.md](AGENTS.md) and its role routine.

## Assignment

1. Inspect repository conventions and available worker tools. Build a small bundle reader/validator, dependency scheduler following the shared bundle rules and Supervisor coordination procedure, role/review adapters, project check adapter and durable result store.
2. Support document authoring, single-task execution, whole-app generation, status/resume, incremental work and reconstruction with existing bundle/task/run locations. Keep the supervisor orchestration-only; dispatch a fresh planner when prerequisites pass and retain it for corrections. Retain implementers through their fresh-review loops. Run fresh final validators and schedule their recorded repair tasks through new planners/implementers, without duplicate repair creation on resume.
3. Capture all five roles' session/turn references and use the retained usage helper. Missing counters remain explicit and separate from acceptance.
4. Exercise acceptance with abstract fixtures, stub/manual adapters and explicit failures. Record manual fallback origin; never claim fresh review or execution that did not occur.
5. Report implemented capabilities, actual checks and blockers separately from live generation experiments. Do not invent an app, choose its stack or add a hosted control plane. Verify installed help before relying on worker flags. Avoid mandatory manifests, frozen checks or approval receipts.

## Acceptance

| ID | Required behavior and evidence |
|---|---|
| SUITE-001 | Empty installation contains no selected app/stack; generation without intent returns NO_PROJECT. |
| SUITE-002 | Read the existing Markdown bundle; report missing files, duplicate IDs, unknown references, cycles and missing acceptance mappings. |
| SUITE-003 | Schedule tasks from the explicit dependency table under the shared bundle rules and Supervisor coordination procedure. |
| SUITE-004 | Save full plans and source-linked acceptance before implementation; preserve explicit requirements and approved text. Resolve ordinary choices autonomously. |
| SUITE-005 | Dispatch a fresh planner per ready task, retain task planners for corrections and implementers through repairs, and have implementers request fresh reviewers excluding plans, conversations and memory. Missing fresh review blocks acceptance. |
| SUITE-006 | Use actual check results and adequate coverage; worker success with failed checks cannot pass. Record required manual checks and unavailable capabilities. |
| SUITE-007 | Resume from saved records, findings and current artifacts; reassess affected evidence when sources, dependencies or implementation change. Preserve history. |
| SUITE-008 | Carry relevant project memory between ordinary tasks and save supported lessons, without imposing a metadata schema. |
| SUITE-009 | Reconstruct in a new workspace using approved inputs; exclude prior implementation/history and memory, including traversal/symlink escapes. Preserve required behavior across targets and report tested isolation limits. |
| SUITE-010 | Fresh independent final validation excludes plans, conversations and memory. Assembly failure prevents whole-app acceptance; validator-generated, requirement-grounded repair tasks extend the bundle once per failed pass, resume without duplication, use new planners/implementers and fresh reviews, then repeat fresh final validation. |
| SUITE-011 | Cancellation, limits and unavailable infrastructure retain results/blockers; source workspaces are preserved and credentials kept out of logs. |
| SUITE-012 | Support worker and project adapters without app assumptions. Test stub/manual paths and unavailable tools honestly. |
| SUITE-013 | Capture supervisor, planner, implementer, reviewer and validator session/turn references, including repair and blocked work; link compatible usage totals, per-role/session statistics, known subtotals and limitations even for blocked runs. Missing telemetry never blocks app acceptance. |

Use synthetic dependency graphs, inert artifacts, fake failures and excluded sentinel files to test mechanics. Map results to these IDs and distinguish implemented automation, documentation walkthroughs and real app experiments. Successful fixtures alone do not establish successful app generation or reconstruction.
