# Execution records

Read when saving work, handing it off or resuming it. Use exact paths; a supplied path still requires reading its contents.

1. Allocate before task work: `python3 agentic-workflow/helpers/records.py allocate NAME`. It reserves a new `.agentic-workflow/<NNN>_<name>/` under a local directory lock and captures session metadata and the active native turn. Resumes and repairs reuse that root.
2. Store task identities and documents under `tasks/<task-id>/`, results/evidence under `runs/<task-id>/<agent-run-id>/`, native turns under `native/<session-id>/<turn-id>.jsonl`, and reports under `reports/`. Use source filename stems as task IDs. Reserve `orchestration` for Supervisor activity and `validation` for final validation.
3. Use the assigned [Implementer mode](IMPLEMENTER.md) for document requirements. Store required documents as `plan.md` and `acceptance.md`; use the [plan](templates/plan.md), [acceptance](templates/acceptance.md) and [result](templates/result.md) templates. Preserve approved originals and history in place.
4. For fresh work, use the current brief/bundle and permitted memory; do not search earlier tasks or conversations. For continuation, use identified paths or execution references. Resolve a bare task ID only under the identified implementation's immediate `tasks/`; ask if the implementation/task is absent, ambiguous or continuation is unclear. Stop discovery once authority is resolved.
5. On resume, run `python3 agentic-workflow/helpers/records.py resolve IMPLEMENTATION TASK` to resolve the task and capture this turn. Use complete identified records, findings and current artifacts; reassess stale/missing evidence and preserve useful failures and resolutions.
6. Recover missing approved originals from the task's known source/conversation. If unavailable, report locations checked and request originals instead of inventing them from summaries. Independent workers receive recovered sources or acceptance, never the recovery conversation. In Plan mode present full drafts and defer saving; save approved text before implementation or handoff once editing is available.
7. Hand off the implementation root, task ID, assigned mode and exact paths to entry/role guidance, resolved guidelines, allowed sources, candidate and evidence. Use absolute paths or paths relative to an explicit root, not copied documents. Include accepted contracts, agreed interfaces/ownership, relevant prior findings and an output path. Include plans/memory only for permitted roles under [Checks](CHECKS.md) and [Memory](MEMORY.md). Discover only unresolved inputs.
8. Retain role handles and artifact paths. Route implementation corrections through [Workflow](WORKFLOW.md); return document corrections to their author. Replace unavailable owners from permitted saved inputs and disclose the replacement.
9. Add the assignment line below to handoffs; recipients also emit it in local commentary. Substitute the implementation name, source task ID and recipient role; optional `purpose` describes the assignment. Follow-ups inherit it unless retagged; replacements keep distinct native identities. Supervisor turns use `supervisor` / `orchestration`; final validation uses `validator` / `validation`.

```text
AGENTIC_WORKFLOW {"implementation":"001_todolist","task":"01_business_logic","role":"implementer"}
```

10. Save one concise [result](templates/result.md) per role/run; link extra evidence and derived usage reports. Keep failures and repair history. Omit routine manifests, checksum lists, duplicate summaries and repeated hash sweeps; functional identity, deduplication and regression hashes remain valid.

- Keep native logs local. Usage JSON/Markdown contain measurements and metadata; content exports (`events.json`, `timeline.json`) and the dashboard contain recorded conversations by default. Independent workers may receive usage reports, never content exports or dashboard evidence.
- Native capture continues throughout work; adapters calculate usage. Keep no trace inventories or manual token totals. Missing telemetry limits reporting, not app acceptance; unknown values stay unavailable. Missing tags leave task/role unavailable without discarding measured usage. For collection and assignment recovery, read [Tracing](helpers/TRACING.md).
