# Execution records

## Allocate or resume

- Context: read when saving, handing off or resuming work. Apply the [record guidelines](#record-guidelines).
- Inputs: the current brief or bundle and allowed memory for new work; identified record paths for resumed work.
- Effects:
  1. For new work, run `python3 agentic-workflow/helpers/records.py allocate NAME` before starting tasks. It reserves `.agentic-workflow/<NNN>_<name>/` under a local directory lock and captures session metadata and the current native turn.
  2. For resumed work, look up bare task IDs only in that implementation's immediate `tasks/` directory. Ask if the implementation or task is missing or ambiguous, or it is unclear what to resume.
  3. When resuming, run `python3 agentic-workflow/helpers/records.py resolve IMPLEMENTATION TASK` to find the task and capture the current turn.
  4. Use the complete records, findings and current files for that work. Recheck outdated or missing evidence and keep useful failure and repair history.
- Outputs: the implementation root and task ID. Reuse that root for resumed work and repairs.

## Recover originals

- Context: use when approved original documents are missing.
- Inputs: known task sources or conversations, and the missing document paths.
- Effects:
  1. Recover originals from those sources. If they are unavailable, list the locations checked and ask for the originals. Do not recreate them from summaries.
  2. Give independent workers recovered sources or acceptance criteria, without the conversation used to recover them.
  3. In Plan mode, present full drafts without saving. Once editing is available, save approved text before implementation or handoff.
- Outputs: recovered approved originals or a report of what is still missing.

## Hand off work

- Context: apply [Checks](CHECKS.md) and [Memory](MEMORY.md) when choosing what a recipient may read.
- Inputs: implementation root, task ID and mode; entry points, role instructions and guideline paths; allowed sources, work to check and evidence; accepted contracts, agreed interfaces, file owners, prior findings and an output path.
- Effects:
  1. Pass absolute paths or paths relative to a stated root. Pass paths rather than document copies.
  2. Include plans and memory only when the recipient's role allows them. Search only for inputs still missing.
  3. Keep worker handles and output paths so work can return to its owner.
  4. Send implementation corrections through [Supervisor](../roles/SUPERVISOR.md). Send document corrections to their author.
  5. If an owner is unavailable, give the replacement only allowed saved inputs and report the replacement.
  6. Include the assignment line below. Have the recipient repeat it in its own commentary.
- Outputs: allowed input paths, recipient handle and assignment line.

## Record guidelines

Apply to task documents, handoffs and results.

- Read files at their exact paths, even when someone else supplied the paths.
- Start new work from current authorized inputs without searching earlier tasks or conversations.
- Stop searching once the sources that govern the work are known.
- Store records in the locations below. Use source filenames without extensions as task IDs.
- Reserve `orchestration` for Supervisor activity and `validation` for final validation.
- Follow the assigned [Implementer mode](../roles/IMPLEMENTER.md) to decide which documents are required.
- Use `plan.md` and `acceptance.md` for required task documents. Follow the [plan](../templates/plan.md), [acceptance](../templates/acceptance.md) and [result](../templates/result.md) templates.
- Preserve approved originals and their history in place.
- Save one short result per role and run. Link extra evidence and usage reports; keep failure and repair history.
- Avoid routine manifests, checksum lists, duplicate summaries and repeated hash scans. Keep hashes used for identity, deduplication or regression checks when useful.
- Keep native logs local. Give independent workers usage measurements and metadata in JSON or Markdown.
- Do not give independent workers `events.json`, `timeline.json` or dashboard evidence. These contain recorded conversations by default.
- Keep native capture running throughout the work. Use adapters to calculate usage; do not create trace inventories or count tokens manually.
- Report missing telemetry as a reporting limit. It does not block app acceptance.
- Leave unknown values unavailable. When assignment tags are missing, leave task and role unavailable but keep measured usage.
- Read [Tracing](../guides/TRACING.md) when collecting traces or recovering assignments.

| Record | Location under the implementation root |
|---|---|
| Task IDs and documents | `tasks/<task-id>/` |
| Results and evidence | `runs/<task-id>/<agent-run-id>/` |
| Native turns | `native/<session-id>/<turn-id>.jsonl` |
| Reports | `reports/` |

## Assignment format

Apply to the assignment line sent during handoff.

- Fill in the implementation name, source task ID and recipient role. Use the optional `purpose` field to describe the assignment.
- Keep the assignment for follow-ups unless it is explicitly retagged. Keep replacement workers' native identities separate.
- Use `supervisor` / `orchestration` for Supervisor turns and `validator` / `validation` for final validation.

```text
AGENTIC_WORKFLOW {"implementation":"001_todolist","task":"01_business_logic","role":"implementer"}
```
