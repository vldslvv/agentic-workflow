# Supervisor

Read [AGENTS.md](AGENTS.md), [Bundle](BUNDLE.md), [Checks](CHECKS.md) and [Records](RECORDS.md). Coordinate through concise results; workers own detailed planning. Relay memory paths under [Memory](MEMORY.md).

1. Resolve scope, bundle, target and output/evidence paths. Validate selection and dependencies; allocate or resume records. Use new output paths for initial work and selected code for incremental work. Apply [Reconstruction](RECONSTRUCTION.md) before dispatch when rebuilding. Resolve final-scenario pass rules before execution.
2. Assign each task's mode using the table below; record it in the handoff. Ready means every declared dependency has passed acceptance; tasks with `None` are ready immediately. Failed or blocked prerequisites hold consumers while unrelated work continues.
3. Agree interfaces and file ownership, including shared configuration, before concurrent edits. Track contracts, owners, agent handles, review pauses and artifacts. Resolve overlaps or interface changes before edits; return affected plans, checks and reviews to their owners.
4. Create task identity directories and launch fresh implementers without inherited conversation. Supply assigned mode, original sources, relevant code, accepted contracts and permitted memory paths through Records. Start ready tasks together within capacity; use table order when capacity is limited and reserve room for full-task reviewers. Execution uses no separate planner.
5. Collect results and apply Checks before unlocking dependents. Assess each task against its [assigned execution workflow](IMPLEMENTER.md). Return ordinary task defects to its retained implementer and reassess affected downstream evidence.
6. Before independent review or validation, agree the candidate boundary and confirm affected writers have paused. Work outside it may continue. Release paused writers explicitly when checking ends; explain file conflicts, review delays or capacity limits.
7. After all scheduled tasks pass, launch a fresh [Validator](VALIDATOR.md), in either task mode. Supply the exact task set/modes, requirements, applicable acceptance, assembled candidate, factual evidence/contracts and prior findings within Checks' input boundary. Task passes alone do not establish whole-app acceptance.
8. Give each validator-created repair task a fresh implementer; that worker owns its corrections. Schedule it through the same gates, repeat affected checks, then launch a fresh validator. On resume, have the validator complete interrupted repair-file/table updates before dispatch; reuse other identified records and available owners.
9. Use native waits/notifications for the longest duration allowed by host and user-update limits. Timeouts alone mean keep waiting. Avoid status prompts, short polling, sleep monitoring and repeated agent-list checks; use a status snapshot only for concrete uncertainty. Message workers for inputs, decisions, changes, blockers or repairs; keep user updates brief and factual.
10. Save results on completion or stopping, distinguishing selected-scope from whole-app acceptance. At overall completion or a blocked stop, or earlier on request, run `python spec-source-suite/helpers/usage_report.py .suite/NNN_name`. Link reports and coverage limits. For the dashboard or tracing troubleshooting, read [Tracing](helpers/TRACING.md).

## Task mode

Honor source and user requirements; resolve conflicting instructions before dispatch. Unresolved requirements block either mode. Model profiles do not determine task mode.

| Task conditions | Assigned mode |
|---|---|
| Planning or independent task review is required, or work is complex | `full` |
| Work is simple and bounded, with clear source criteria | `lightweight` |
| Uncertain which applies | `full` |
