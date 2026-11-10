# Execution records

Use the [shared vocabulary](../GLOSSARY.md) for Assignments and Results.

## Allocate or resume

- Context: apply the [record guidelines](#record-guidelines) when saving, handing off or resuming work.
- Inputs:
  - New work: Assignment and applicable specifications; Memory only where permitted.
  - Resumed work: Assignment, prior Results and Execution state when available.
- Effects:
  - For new work, run `python3 agentic-workflow/helpers/records.py allocate NAME` before starting tasks.
  - Look up resumed task IDs only in that implementation's immediate `tasks/` directory.
  - Ask when the implementation, task or resume scope is missing or unclear.
  - For resumed work, run `python3 agentic-workflow/helpers/records.py resolve IMPLEMENTATION TASK`.
  - Use complete records, findings and current files for that work.
  - Recheck outdated or missing evidence.
- Outputs: implementation root and task ID.
- Next: reuse the root for resumed work and repairs.

`allocate` reserves `.agentic-workflow/records/<NNN>_<name>/` under a local directory lock.
It attempts to capture session metadata and the current native turn.
`resolve` finds the task and attempts the same capture.
Codex supplies its thread identity directly; OpenCode 2.2.6 supplies
[native shell identity](../guides/TRACING.md#enable-opencode-capture).
Capture failures appear on stderr without blocking allocation or resolution.

## Recover originals

- Context: use when approved original documents are missing.
- Inputs: known task sources or conversations, and the missing document paths.
- Effects:
  - Recover originals from known sources.
  - Do not recreate originals from summaries.
  - Ask for unavailable originals with a list of checked locations.
  - Give independent workers recovered sources or acceptance criteria without recovery conversations.
  - In Plan mode, present full drafts without saving.
  - Once editing is available, save approved text before implementation or handoff.
- Outputs: recovered approved originals or a report of what is still missing.

## Hand off work

- Context: apply [Checks](CHECKS.md) and [Memory](MEMORY.md) when choosing what a recipient may read.
- Inputs: Assignment, Instructions and the recipient role’s named inputs.
- Effects:
  - Have each output owner create its record directories before saving outputs, including direct tasks and validation.
  - Pass the implementation directory path as `IMPLEMENTATION` for `resolve`, rather than its name.
  - Pass absolute paths or paths relative to a stated root.
  - Pass paths rather than document copies.
  - State the Assignment and pass the recipient’s named inputs, marking conditional inputs explicitly.
  - Link role instructions for procedure and the selected model policy for routing.
  - Include Plan and Memory only when the recipient’s role allows them.
  - Have recipients read Instructions and assigned inputs before planning, editing or checking.
  - Search only for inputs still missing.
  - Keep worker handles and output paths for return handoffs.
  - Send implementation corrections through [Supervisor](../roles/SUPERVISOR.md).
  - Send document corrections to their author.
  - Give an unavailable owner's replacement only allowed saved inputs.
  - Report owner replacements.
  - Include the assignment line below.
  - Have recipients repeat the assignment line in their own commentary.
- Outputs: Assignment with allowed input paths and assignment line.

Keep recipient handles and output paths in Execution state when coordinating tasks.

## Return work

Apply when a worker finishes, pauses for review or stops with unfinished work.

- Save one Result using the [result template](../templates/result.md).
- Include applicable Memory and usage paths.
- Filter Results and Evidence for independent recipients under [Checks](CHECKS.md#independent-checks).
- Return status, Result path and any decision or blocker in one short message.
- Link changed files, check evidence and findings from the saved result.
- Keep detailed command output in evidence files when needed.
- Report only new facts in follow-up messages.
- Preserve required evidence and unresolved findings when shortening results.

## Record guidelines

Apply to task documents, handoffs and results.

- Read files at their exact paths, even when someone else supplied the paths.
- Start new work from current authorized inputs without searching earlier tasks or conversations.
- Stop searching once the sources that govern the work are known.
- Store records in the locations below.
- Use source filenames without extensions as task IDs.
- Reserve `orchestration` for Supervisor activity and `validation` for final validation.
- Follow the assigned [Implementer mode](../roles/IMPLEMENTER.md) to decide which documents are required.
- Use `plan.md` and `acceptance.md` for required task documents.
- Follow the [plan](../templates/plan.md), [acceptance](../templates/acceptance.md) and [result](../templates/result.md) templates.
- Preserve approved originals and their history in place.
- Follow [Return work](#return-work) for saved results and completion messages.
- Link extra evidence and usage reports.
- Keep failure and repair history.
- Avoid routine manifests, checksum lists, duplicate summaries and repeated hash scans.
- Keep useful hashes for identity, deduplication or regression checks.
- Keep native logs local.
- Give independent workers usage measurements and metadata in JSON or Markdown.
- Exclude `events.json`, `timeline.json` and dashboard evidence from independent inputs because they contain conversations by default.
- Report missing telemetry as a reporting limit.
- Do not block app acceptance for missing telemetry.
- Leave unknown values unavailable.
- Apply [Tracing](../guides/TRACING.md) for capture throughout execution, usage reports and assignment recovery.

| Record | Location under the implementation root |
|---|---|
| Task IDs and documents | `tasks/<task-id>/` |
| Results and evidence | `runs/<task-id>/<agent-run-id>/` |
| Native turns | `native/<session-id>/<turn-id>.jsonl` (Codex) or `.json` (OpenCode) |
| Reports | `reports/` |

## Assignment format

Apply to the assignment line sent during handoff.

- Fill in the implementation name, source task ID and recipient role.
- Put the assignment marker at the start of its own line.
- Use the optional `purpose` field to describe the assignment.
- Keep the assignment for follow-ups unless explicitly retagged.
- Keep replacement workers' native identities separate.
- Use `supervisor` / `orchestration` for Supervisor turns and `validator` / `validation` for final validation.
- Emit your own assignment line in commentary after allocation or resume.

```text
AGENTIC_WORKFLOW {"implementation":"001_todolist","task":"01_business_logic","role":"implementer"}
```
