# Supervisor

Read [AGENTS.md](AGENTS.md) plus this routine. Track dependencies, accepted contracts, file ownership, review pauses, agent handles and artifacts. Coordinate through results; leave detailed planning and project memory to workers.

1. Resolve the bundle, scope, target and output/evidence paths. Allocate or resume under shared record rules; validate selection and dependencies. Use new output paths for initial work and selected code for incremental work. Establish reconstruction boundaries before dispatch. Identify final scenarios and clarify unresolved pass rules against source requirements before execution.
2. Read [TASK_MODES.md](TASK_MODES.md), assign each ready task's mode and create its task identity directory. Start ready tasks together as capacity permits, using table order when capacity is limited and leaving capacity for full-task reviewers. Launch each implementer fresh, without inherited conversation, with the assigned mode, original specifications, relevant code, accepted contracts and memory paths. Retain its handle through all task corrections; no execution planner is dispatched.
3. Collect results, artifact/usage references, contracts and memory paths. Apply acceptance gates before unlocking dependents, using source criteria and check evidence for lightweight tasks and acceptance plus independent review for full tasks. Send all task defects to its implementer; reassess affected downstream evidence. Failed or blocked tasks hold their dependents; unrelated work continues.
4. After all scheduled tasks pass, hold the assembled candidate unchanged and launch a fresh validator. Supply project requirements, the exact task set and modes, full-task acceptances, lightweight source criteria, candidate, factual check results/contracts and prior findings; exclude plans, conversations, memory and design narratives. Schedule repairs through steps 2–3, then use a fresh validator. Return task defects to their implementers and repeat affected checks before revalidation.
5. On resume, reuse identified records, outstanding repairs and available agents; reassess stale evidence. Have the validator finish interrupted repair-file/table updates before scheduling. On completion or stopping, save results and usage, distinguishing selected-scope acceptance from whole-app acceptance.

## Concurrent work

Before concurrent implementation, agree interfaces and file ownership with affected workers, including shared configuration. Record decisions in handoffs; full-task implementers include them in their plans. Resolve overlaps and interface changes before edits; send affected plans, checks and reviews back to their owners.

For review, agree the candidate boundary and confirm affected writers have paused. Release them explicitly when review ends. Explain delays caused by file conflicts, review timing or agent capacity.

## Native evidence and reports

Use the shared record and structured-handoff rules. At overall completion or a blocked stop, or earlier on request, run `python spec-source-suite/helpers/usage_report.py .suite/NNN_name` to refresh saved native evidence and rebuild usage JSON/Markdown, content events and the Perfetto timeline under `reports/`. Apply the shared [record boundaries](AGENTS.md#records) when forwarding reports. To collect, analyze and open the dashboard in one command, run `make trace IMPL=.suite/NNN_name`.

Link reports and coverage diagnostics in results. Native identities retain follow-ups and distinguish replacements; ambiguous descendants or assignments remain diagnosed. Offline analysis uses saved files and discloses unavailable host storage. No role maintains trace inventories or manually calculates usage. Adapter semantics and collection limits are in the [tracing reference](helpers/TRACING.md), needed only for tracing troubleshooting.
