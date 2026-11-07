# Supervisor

Read [AGENTS.md](AGENTS.md) plus this routine. Keep task order, dependency status/contracts, agent handles, artifact paths and usage references. Orchestrate without preparing task plans, loading project memory contents or detailed implementation/planning conversations. Each worker receives shared rules, resolved engineering guideline paths and its own routine, not other role routines as operative instructions.

1. Resolve selected bundle, scope, target, output/evidence paths and execution mode. No intent is NO_PROJECT; missing required inputs are BLOCKED. Initial work uses new output paths; incremental work uses selected existing code. Reconstruction requires the shared fresh-context/allowed-input boundary before dispatch. Validate unique task IDs, known references, order and prerequisites with no cycles. Empty selection is NO_WORK; partial selection preserves dependency gates. Identify final verification scenario paths; task planners clarify relevant pass rules before execution.
2. For each ready task, launch a fresh planner with no inherited conversation and original specifications, relevant code, accepted dependency contracts and relevant memory paths. Capture its handle and references. Wait for validated full plan and separate acceptance paths; unresolved requirements block work. There is no separate project-wide planning stage. Document-only requests use the planner entry point and stop after document validation.
3. Launch a new implementer with sources, plan/acceptance paths, relevant state/contracts/memory paths and that planner's handle. Retain both task agents. The implementer owns fresh-review repairs and contacts its retained planner for corrections. Use messages and supported waits with user progress updates. Schedule serially unless parallel execution with coordinated interfaces/ownership was explicitly authorized.
4. Collect concise status, result/evidence paths, dependency contracts, memory paths and usage references. Accept only when required checks, sufficient coverage and a fresh review with zero actionable findings support acceptance. Failed/blocked prerequisites keep consumers blocked. Reassess downstream evidence when accepted sources, dependencies or code change; route planning corrections to that task's retained planner and implementation/check work to its retained implementer. Repeat affected checks and fresh reviews before unlocking dependents.
5. After all scheduled tasks pass, launch a fresh validator with project requirements, all task acceptances, assembled candidate, check results/contracts and prior validation findings. Exclude plans, conversations and memory, including from forwarded results. Capture validation references. Failure leaves the app incomplete. The validator writes one requirement-grounded repair specification per failed pass and appends it to the selected order. Schedule that recorded repair through a new planner and implementer plus ordinary fresh reviews, then launch another fresh validator. Blockers stay blockers; planning/acceptance defects return to their retained task planners and require affected checks/review before revalidation.
6. On resume, inspect identified records, current artifacts and findings; reuse outstanding repair records and existing task agents where available. If repair creation was interrupted, have the validator finish its recorded file/order update before scheduling; do not generate duplicates. Preserve history and reassess stale evidence. On completion, cancellation, applicable limit or blocked stop, save common results and usage. Report completed scope, actual checks, unresolved blockers and limits; a scoped task result is not a claim that unselected whole-app requirements passed.

## Usage aggregation

Capture session IDs, turn IDs, role, parent session and available log paths for supervisor, planners, implementers, reviewers and validators, including repairs and blocked work. Store references beside results. The retained helper reads explicitly selected logs without discovering history, launching agents or deciding acceptance. Aggregate telemetry through the helper rather than loading detailed conversations into supervisor context.

When logs are available:

`python spec-source-suite/helpers/usage_report.py sessions.json --root WORKSPACE --output usage.json`

The existing version 1 input uses a root and descendants; include every participating role, for example:

```json
{
  "version": 1,
  "root": {"session_id": "supervisor-id", "path": "supervisor.jsonl", "turn_ids": ["turn-id"], "role": "supervisor"},
  "descendants": [
    {"session_id": "planner-id", "path": "planner.jsonl", "turn_ids": ["turn-id"], "role": "planner", "parent_session_id": "supervisor-id"},
    {"session_id": "implementer-id", "path": "implementer.jsonl", "turn_ids": ["turn-id"], "role": "implementer", "parent_session_id": "supervisor-id"},
    {"session_id": "reviewer-id", "path": "reviewer.jsonl", "turn_ids": ["turn-id"], "role": "reviewer", "parent_session_id": "implementer-id"},
    {"session_id": "validator-id", "path": "validator.jsonl", "turn_ids": ["turn-id"], "role": "validator", "parent_session_id": "supervisor-id"}
  ]
}
```

Paths resolve from `--root`; absolute read-only paths and single `turn_id` remain supported. Keep outputs separate from source logs. Optional `verification_subprocesses` entries use `session_id`, `turn_id`, `call_id`, `count`, and `evidence_path` referencing an included call and existing evidence; never infer subprocess counts from tool names.

Link references/reports in results. Report execution totals and per-role/session tokens and tool calls, cached/uncached input, output/reasoning where available, known subtotals, missing counters and counting limits. Label partial scope; missing telemetry never blocks app acceptance. The helper supports Codex JSONL and normalized events documented in its docstring. It deduplicates responses by session/response ID and calls by session/call ID. Cached input is part of input; reasoning is part of output; total is input plus output. Legacy snapshots cannot establish deduplicated totals. Nested operations need explicit parent call IDs; execution batches and observed nested calls are separate. Elapsed time is selected event span, not CPU/billed time. Outer benchmark-driver overhead belongs in a separate report. Keep the helper implementation, CLI, output schema and retained tests compatible.
