# Execution records

Allocate execution records, dispatch role contracts and save results for continuation.

## References:

- [WORK_RESULT]: Defines the worker's return message. agentic-workflow/contracts/WorkResult.md
- [TRACING]: Defines native capture, provider detection and usage reporting. agentic-workflow/guides/TRACING.md
- [CHECKS]: Restricts independent inputs and defines evidence rules. agentic-workflow/policies/CHECKS.md
- [RESULT_TEMPLATE]: Structures saved Results and evidence references. agentic-workflow/templates/result.md

## Allocate or resume

Apply before starting tasks or continuing identified work.

- Run `python3 agentic-workflow/helpers/records.py allocate NAME` for new work.
- Run `python3 agentic-workflow/helpers/records.py resolve IMPLEMENTATION TASK` for resumed work, passing the implementation path.
- Resolve scope from authorized inputs and identified records, searching task IDs only in that implementation's immediate `tasks/` directory.
- Report missing or ambiguous scope as a blocker without prompting.
- Reuse the implementation root for continuations and repairs, rechecking missing or outdated evidence under [CHECKS].
- Apply [TRACING] for capture, provider detection, usage reports and assignment recovery.

| Record | Location under the allocated implementation root |
|---|---|
| Task documents | `tasks/<task-id>/` |
| Results and evidence | `runs/<task-id>/<agent-run-id>/` |
| Native turns | `native/<session-id>/<turn-id>.jsonl` (Codex) or `.json` (OpenCode) |
| Reports | `reports/` |

## Recover originals

Apply when approved original documents are missing.

- Recover approved originals from known sources rather than summaries, reporting unavailable originals and checked locations as blockers without prompting.
- Present full unsaved drafts in Plan mode and save approved text before implementation or handoff once editing is available.
- Give independent workers permitted recovered documents without recovery conversations under [CHECKS].

## Hand off work

Apply when dispatching or replacing a worker.

- Send the recipient's declared input contract with role instructions, the selected model policy and the assignment line below.
- Use artifact paths relative to a stated root or absolute paths, reading each exact path before work.
- Start from current authorized inputs and search only for missing governing sources.
- Filter independent handoffs under [CHECKS] (“Independent checks”).
- Keep worker handles and output paths for continuation, giving replacements only permitted saved inputs and reporting replacements.
- Route implementation corrections through Supervisor and document corrections to their author.

## Return work

Apply when finishing, pausing for review or stopping with unfinished work.

- Create output directories and save one Result using [RESULT_TEMPLATE] before returning [WORK_RESULT].
- Link required evidence and unresolved findings, retaining failure and repair history when shortening records.
- Keep detailed command output in linked evidence files when needed and report only new facts in follow-ups.
- Keep native logs local and report unavailable telemetry as a limit without blocking application acceptance.

## Assignment format

Apply when tagging work for tracing and handoffs.

- Emit the assignment marker at the start of its own commentary line after allocation or resume, and have recipients repeat their assigned line.
- Fill in the implementation name, source task ID and recipient role, adding optional `purpose` when useful.
- Reserve `supervisor` / `orchestration` and `validator` / `validation` for coordination and final validation.
- Keep the assignment for follow-ups unless explicitly retagged, retaining separate native identities for replacement workers.

```text
AGENTIC_WORKFLOW {"implementation":"001_todolist","task":"01_business_logic","role":"implementer"}
```
