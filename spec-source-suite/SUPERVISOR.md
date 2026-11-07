# Supervisor

Read [AGENTS.md](AGENTS.md) plus this routine. Track dependencies, accepted contracts, file ownership, review pauses, agent handles and artifacts. Coordinate through results; leave detailed planning and project memory to workers.

1. Resolve the bundle, scope, target and output/evidence paths. Allocate or resume under shared record rules; validate selection and dependencies. Use new output paths for initial work and selected code for incremental work. Establish reconstruction boundaries before dispatch. Identify final scenarios and have planning owners clarify pass rules before execution.
2. Start ready tasks together as capacity permits, using table order when capacity is limited. Leave room for planners and reviewers. Failed or blocked tasks hold their dependents; unrelated work continues. Launch each implementer fresh, without inherited conversation, with original specifications, relevant code, accepted contracts and memory paths. Record its handle, assessment and mode. Plan per task.
3. For full mode or escalation, launch a fresh planner without inherited conversation with the same inputs and assessment/mode. The implementer ends its assessment turn while planning proceeds. Once documents are validated and coordination decisions below are recorded, explicitly resume the retained implementer with plan/acceptance paths and the planner's handle. If resumption is unavailable, follow shared replacement rules. Lightweight planning follows shared rules and the same coordination procedure.
4. Collect results, artifact/usage references, contracts and memory paths. Apply acceptance gates before unlocking dependents. Send planning defects to the planning owner and implementation/check defects to the implementer; reassess affected downstream evidence.
5. After all scheduled tasks pass, hold the assembled candidate unchanged and launch a fresh validator. Supply project requirements, the exact task set being validated, acceptances/modes, candidate, check results/contracts and prior findings; exclude plans, conversations and memory. Schedule repairs through steps 2–4, then use a fresh validator. Return planning defects to their owners; repeat affected checks before revalidation.
6. On resume, reuse identified records, outstanding repairs and available agents; reassess stale evidence. Have the validator finish interrupted repair-file/table updates before scheduling. On completion or stopping, save results and usage, distinguishing selected-scope acceptance from whole-app acceptance.

## Concurrent work

Before concurrent implementation, agree interfaces and file ownership with affected workers, including shared configuration. Send decisions in handoffs for planning owners to record. Resolve overlaps and interface changes before edits; send affected plans, checks and reviews back to their owners.

For review, agree the candidate boundary and confirm affected writers have paused. Release them explicitly when review ends. Explain delays caused by file conflicts, review timing or agent capacity.

## Native evidence and reports

Use the shared record and structured-handoff rules. At overall completion or a blocked stop, or earlier on request, run `python spec-source-suite/helpers/usage_report.py .suite/NNN_name` to refresh saved native evidence and rebuild usage JSON/Markdown and the Perfetto timeline under `reports/`. To collect, analyze and open the dashboard in one command, run `make trace IMPL=.suite/NNN_name`.

Link reports and coverage diagnostics in results. Native identities retain follow-ups and distinguish replacements; ambiguous descendants or assignments remain diagnosed. Offline analysis uses saved files and discloses unavailable host storage. No role maintains trace inventories or manually calculates usage. Adapter semantics and collection limits are in the [tracing reference](helpers/TRACING.md), needed only for tracing troubleshooting.
