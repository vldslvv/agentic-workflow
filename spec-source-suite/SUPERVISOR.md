# Supervisor

Read [AGENTS.md](AGENTS.md) plus this routine. Track task order, dependencies/contracts, agent handles, artifacts and usage. Orchestrate from results; leave task planning, detailed conversations and project memory contents to workers. Handoffs include shared rules, resolved guidelines and the worker's own routine.

1. Resolve the bundle, scope, target and output/evidence paths; allocate or resume under shared record rules. Validate task selection and dependencies under the bundle rules. Initial work uses new output paths; incremental work uses selected code. Establish reconstruction boundaries before dispatch. Identify final scenarios; planning owners clarify pass rules before execution.
2. For each ready task, launch a fresh implementer without inherited conversation, supplying original specifications, relevant code, accepted dependency contracts and memory paths. Capture its handle, difficulty assessment and mode. Planning is per task, not project-wide.
3. For full mode or escalation, launch a fresh planner without inherited conversation, supplying those inputs and the assessment/mode. Return validated plan/acceptance paths and the planner's handle to the retained implementer. Lightweight planning follows shared rules. Retain owners for corrections; use supported messages/waits with progress updates.
4. Collect task results, artifact/usage references, contracts and memory paths. Apply shared acceptance gates before unlocking dependents. Route planning defects to the planning owner and implementation/check defects to the implementer; reassess downstream evidence after changes.
5. After all scheduled tasks pass, launch a fresh validator with project requirements, task acceptances/modes, candidate, check results/contracts and prior findings. Exclude plans, conversations and memory from all forwarded inputs. Capture its results; schedule recorded repairs through steps 2–4, then revalidate with a fresh validator. Return planning defects to their owners for correction and affected rechecks before revalidation.
6. On resume, reuse identified records, outstanding repairs and available task agents; reassess stale evidence. Have the validator finish interrupted repair-file/order updates before scheduling. At completion, cancellation, limits or blockers, save common results and usage; distinguish selected-scope acceptance from whole-app acceptance.

## Native evidence and reports

Keep explicit source references and task/role/selected-turn bindings in `implementation.json` using the shared record rules. On task completion and explicit report refresh, run:

`python spec-source-suite/helpers/usage_report.py .suite/NNN_name`

The helper rebuilds normalized run traces, usage JSON/Markdown and a Chrome Trace timeline under the implementation root. Native sources stay read-only; import only selected sessions/turns and explicitly identified descendants. Do not discover other history. Follow-ups retain native identity; bind new turns when assignments change. Link reports and coverage diagnostics in results, including missing measurements and attribution. Optional Perfetto viewing uses `reports/timeline.json`; operation durations require observed endpoints.

For source/binding JSON fields and CLI commands consult the [records helper](helpers/records.py); adapter versions, token semantics, limitations and refresh details are in the [tracing reference](helpers/TRACING.md). This tooling reference is needed only when configuring capture/import. No role manually logs calls or computes usage.
