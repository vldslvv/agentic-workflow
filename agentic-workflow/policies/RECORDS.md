# Execution records

## Allocate or resume

- Context: read when saving work, handing it off or resuming it; apply the [record guidelines](#record-guidelines).
- Inputs: current brief/bundle and permitted memory for fresh work, or identified continuation paths/execution references.
- Effects: for fresh work, allocate before task work with `python3 agentic-workflow/helpers/records.py allocate NAME`. It reserves a new `.agentic-workflow/<NNN>_<name>/` under a local directory lock and captures session metadata and the active native turn. For continuation, resolve a bare task ID only under the identified implementation's immediate `tasks/`; ask if the implementation/task is absent, ambiguous or continuation is unclear. Run `python3 agentic-workflow/helpers/records.py resolve IMPLEMENTATION TASK` to resolve the task and capture this turn. Use complete identified records, findings and current artifacts; reassess stale/missing evidence and preserve useful failures and resolutions.
- Outputs: implementation root and task identity; resumes and repairs reuse that root.

## Recover originals

- Context: apply when approved originals are missing.
- Inputs: the task's known source/conversation and missing document paths.
- Effects: recover originals from those sources; if unavailable, report locations checked and request originals instead of inventing them from summaries. Give independent workers recovered sources or acceptance, never the recovery conversation. In Plan mode present full drafts and defer saving; save approved text before implementation or handoff once editing is available.
- Outputs: recovered approved originals or explicit blockers.

## Hand off work

- Context: apply [Checks](CHECKS.md) and [Memory](MEMORY.md) to recipient inputs.
- Inputs: implementation root, task ID, assigned mode, exact paths to entry/role guidance, resolved guidelines, allowed sources, candidate and evidence; accepted contracts, agreed interfaces/ownership, relevant prior findings and an output path.
- Effects: pass absolute paths or paths relative to an explicit root, not copied documents. Include plans/memory only for permitted roles; discover only unresolved inputs. Retain role handles and artifact paths. Route implementation corrections through [Supervisor](../roles/SUPERVISOR.md); return document corrections to their author. Replace unavailable owners from permitted saved inputs and disclose the replacement. Add the assignment line below; recipients also emit it in local commentary.
- Outputs: permitted handoff inputs, recipient handle and assignment identity.

## Record guidelines

Apply to task documents, handoffs and results.

- Use exact paths and read their contents even when supplied.
- Use current authorized inputs for fresh work without searching earlier tasks or conversations. Stop discovery once authority is resolved.
- Store task identities and documents under `tasks/<task-id>/`, results/evidence under `runs/<task-id>/<agent-run-id>/`, native turns under `native/<session-id>/<turn-id>.jsonl`, and reports under `reports/`. Use source filename stems as task IDs; reserve `orchestration` for Supervisor activity and `validation` for final validation.
- Use the assigned [Implementer mode](../roles/IMPLEMENTER.md) for document requirements. Store required documents as `plan.md` and `acceptance.md`; use the [plan](../templates/plan.md), [acceptance](../templates/acceptance.md) and [result](../templates/result.md) templates. Preserve approved originals and history in place.
- Save one concise result per role/run; link extra evidence and derived usage reports. Keep failures and repair history. Omit routine manifests, checksum lists, duplicate summaries and repeated hash sweeps; retain functional identity, deduplication and regression hashes where useful.
- Keep native logs local. Give independent workers usage JSON/Markdown measurements and metadata, never content exports (`events.json`, `timeline.json`) or dashboard evidence, which contain recorded conversations by default.
- Keep native capture running throughout work and use adapters to calculate usage without trace inventories or manual token totals. Treat missing telemetry as a reporting limit, not an app acceptance blocker; keep unknown values unavailable. Leave task/role unavailable for missing tags without discarding measured usage. For collection and assignment recovery, read [Tracing](../guides/TRACING.md).

## Assignment format

Apply to the assignment line emitted during handoff.

- Substitute the implementation name, source task ID and recipient role; use optional `purpose` to describe the assignment.
- Inherit the assignment on follow-ups unless retagged; keep distinct native identities for replacements.
- Use `supervisor` / `orchestration` for Supervisor turns and `validator` / `validation` for final validation.

```text
AGENTIC_WORKFLOW {"implementation":"001_todolist","task":"01_business_logic","role":"implementer"}
```
