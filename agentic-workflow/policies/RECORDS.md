# Execution records

Allocate execution records, hand off declared input contracts and save results for continuation.

## References:

- [WORK_RESULT]: Defines the worker's return message. agentic-workflow/contracts/WORK_RESULT.md
- [TRACING]: Defines native capture, provider detection and usage reporting. agentic-workflow/guides/TRACING.md
- [RESULT_TEMPLATE]: Structures saved Results and evidence references. agentic-workflow/templates/RESULT.md

## Allocate or resume

Apply before starting tasks or continuing identified work.

- Run `python3 agentic-workflow/helpers/records.py allocate NAME` for new work.
- Run `python3 agentic-workflow/helpers/records.py resolve IMPLEMENTATION TASK` for resumed work, passing the implementation path.
- Resolve scope from authorized inputs and identified records, searching task IDs only in that implementation's immediate `tasks/` directory.
- Report missing or ambiguous scope as a blocker without prompting.
- Reuse the implementation root for continuations and repairs, reassessing missing or outdated evidence before reuse.
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
- Give independent workers permitted recovered documents without recovery conversations.

## Hand off work

Apply when dispatching or replacing a worker.

- Send the declared input contract with applicable Instructions and an assignment marker under [TRACING] (“Assignment format”).
- Use artifact paths relative to a stated root or absolute paths, reading each exact path before work.
- Start from current authorized inputs and search only for missing governing sources.
- Filter independent handoffs and recovered documents using the independent input restrictions below.
- Keep worker handles and output paths for continuation, giving replacements only permitted saved inputs and reporting replacements.

## Independent inputs

Apply to independent review and validation, including handoffs and recovered documents.

- Start in fresh contexts without inherited conversation.
- Admit only the declared input contract and applicable Instructions.
- Limit supplied Results and Evidence to facts, prior findings and focused guideline or mock justifications.
- Exclude plans, implementation suggestions, conversations, memory, design explanations and correctness claims, including copies in other files.
- Exclude native logs, events, timelines and dashboard evidence; allow usage measurements and metadata in JSON or Markdown.

## Return work

Apply when finishing, pausing for review or stopping with unfinished work.

- Create output directories and save one Result using [RESULT_TEMPLATE] before returning [WORK_RESULT].
- Link required evidence and unresolved findings, retaining failure and repair history when shortening records.
- Keep detailed command output in linked evidence files when needed and report only new facts in follow-ups.
- Keep native logs local and report unavailable telemetry as a limit without blocking application acceptance.

## Tag work

Apply when tagging work for tracing and handoffs.

- Use [TRACING] (“Assignment format”) after allocation or resume and for handoffs and follow-ups.
