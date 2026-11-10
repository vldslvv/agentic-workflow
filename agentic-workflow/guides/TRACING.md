# Tracing workflows

Capture, inspect and report workflow execution traces and usage.

## References:

- [OPENCODE_RELEASE]: Identifies the checked OpenCode release. https://github.com/anomalyco/opencode/releases/tag/v2.2.6
- [OPENCODE_SHELL]: Defines native agent shell identity. https://github.com/anomalyco/opencode/blob/v2.2.6/packages/core/src/tool/plugin/shell.ts
- [OPENCODE_SUBAGENT]: Defines prompt delivery and child session reuse. https://github.com/anomalyco/opencode/blob/v2.2.6/packages/core/src/tool/plugin/subagent.ts
- [OPENCODE_COMPLETION]: Defines background child completion notifications. https://github.com/anomalyco/opencode/blob/v2.2.6/packages/core/src/session/subagent-completion.ts
- [OPENCODE_EXPORT]: Defines settled-message export behavior. https://github.com/anomalyco/opencode/blob/v2.2.6/packages/core/src/session/transfer.ts
- [OPENCODE_MESSAGES]: Defines exported session messages. https://github.com/anomalyco/opencode/blob/v2.2.6/packages/schema/src/session-message.ts
- [OPENCODE_TOKENS]: Defines native token accounting. https://github.com/anomalyco/opencode/blob/v2.2.6/packages/schema/src/token-usage.ts
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md

## Automatic tracing provider detection

Apply when capturing, viewing or reporting native evidence.

- Use the implementation directory containing `native/` and `reports/` as the directory argument.
- Expect reporting and viewing to detect the agent host from saved native evidence.
- Expect missing, unreadable, invalid or mixed-provider evidence to stop the command before writes or viewer startup.
- Capture or import supported native traces before starting a report or viewer.
- Keep each implementation's native evidence limited to one tracing provider.
- Expect each refresh to route explicitly to the detected provider internally.
- Read `tracing_provider` in normalized reports separately from the model's `provider` field.

Reporting and viewing have no provider option and do not use the current shell's
agent identity for detection. They inspect the saved native formats without
accessing host storage or executables, then refresh only the detected provider.
The viewer retains that provider for every refresh and reports it in its status.

Allocation and task resolution detect the host automatically from `CODEX_THREAD_ID`
or `OPENCODE_SESSION_ID`. Exactly one nonempty identity selects that provider.
Conflicting identities fail before creating records, locks or captures and name
both providers; run the command in a shell with only the active host's identity.
With neither identity, allocation and resolution still work and warn that capture
is unavailable. A selected provider's capture failure preserves saved evidence
and never falls back to another provider. Capture has no provider override.

## Enable OpenCode capture

- Context: use OpenCode 2.2.6 for workflow execution.
- Inputs: the installed CLI and its native `OPENCODE_SESSION_ID` environment variable.
- Effects:
  1. Allocate or resolve records from the agent's shell.
  2. Start live capture below and keep it running through completion.
- Outputs: selected native turns, background continuations and proven subagent dispatches.
- Next: inspect capture diagnostics and the generated reports.

No plugin is required. The helpers invoke `opencode session export SESSION_ID`
using `PATH`, or the standard `~/.opencode/bin/opencode` installation.
The V1 plugin previously provided here must be removed from
`.opencode/plugins/agentic-workflow.js` when updating an existing installation.

Allocation and resolution select the current turn using native idle boundaries;
steered prompts before an idle marker remain in that turn. A turn starts with a
user prompt or synthetic wake-up and ends at idle. Refresh follows returned child
session IDs with matching parent identities and a unique delivered prompt match,
including steering messages and the native fresh-child prefix. Dispatch start
bounds delivery; tool completion does not, because delivery can appear later.
Missing delivery is retried on refresh, and repeated matches remain ambiguous.

Refresh also follows synthetic notifications identifying children or shells
dispatched in selected turns, then follows dispatches in those continuations.
Automatic continuation selection stops at a new user-initiated turn after idle;
use `records.py resolve` to explicitly join that work to the implementation.
Assignments carry across selected turns in the same session; quoted child
notification text does not identify the supervisor's assignment.
Sessions are never selected by working directory or recency.

OpenCode exports only settled assistant messages, so running tools and model
steps appear after settlement. Keep capture running until the final idle marker
is saved; an unfinished-turn diagnostic means completion has not been observed.
Canonical captures use `native/<session-id>/<initiating-message-id>.json`.
Keep manual exports at other paths under `native/` so they remain unchanged.
Missing CLI access or ambiguous dispatches produce coverage diagnostics while
preserving saved evidence. Existing V1 saved exports remain readable; live
capture targets V2. The checked release and native contracts are
[OPENCODE_RELEASE], [OPENCODE_SHELL], [OPENCODE_MESSAGES], [OPENCODE_TOKENS],
[OPENCODE_SUBAGENT], [OPENCODE_COMPLETION] and [OPENCODE_EXPORT]. Export polling
remains eventually consistent; it cannot expose unsettled assistant activity.

## Capture live work

- Context: apply [RECORDS] when starting or resuming execution.
- Inputs: allocated implementation path, saved native evidence and available native host storage, with [OpenCode capture](#enable-opencode-capture) configured when applicable.
- Effects:
  1. Run `python3 agentic-workflow/helpers/trace_view.py IMPLEMENTATION --interval 5`.
  2. Keep the process running during execution.
  3. Rerun the command to replace a viewer for the same implementation and provider and apply the requested interval.
- Outputs: captured native turns, refreshed reports and a local dashboard.
- Next: inspect progress or report final usage before stopping capture with `Ctrl+C`.

Codex and OpenCode use the same foreground viewer lifecycle. Each successful
invocation owns its viewer until stopped. Viewers from before automatic replacement
support must be stopped manually once before restarting. A different provider,
another implementation or an unrelated port occupant is rejected.

## Import saved traces

- Context: use when analyzing saved Codex records or OpenCode exports.
- Inputs: implementation path and native records for the intended work.
- Effects:
  - Copy selected Codex records with their metadata into `IMPLEMENTATION/native/`.
  - For OpenCode, save `opencode session export SESSION_ID` JSON under `IMPLEMENTATION/native/`.
  - Include only intended turns, excluding unrelated work and inherited fork history.
  - Preserve original records when preparing imports.
- Outputs: saved native evidence under the implementation root.
- Next: [generate usage reports](#report-usage) or [open the viewer](#inspect-traces).

## Inspect traces

- Context: use when inspecting execution, recorded content or timing.
- Inputs: implementation path and captured or imported traces.
- Effects:
  1. Open the running dashboard or launch `python3 agentic-workflow/helpers/trace_view.py IMPLEMENTATION`.
  2. Open the printed URL if the browser does not launch.
  3. Use **Group by** and search to find relevant tasks, agents or tools.
  4. Inspect **Recorded content** for messages and tool activity.
  5. Use **Open timeline in Perfetto** when timing details are needed.
- Outputs: execution observations and identified evidence gaps.
- Perfetto shows one bar per native agent/session from its earliest selected start to its latest selected completion, including waits between turns.
- Agent bars show elapsed observed spans, not continuous model activity or proof of process liveness.
- Span details include contributing turn IDs and individual turn evidence; events and usage totals retain separate turns and measurements.
- Keep an agent bar unfinished when any selected turn lacks an observed end.
- Unfinished agent bars indicate an observed start without an observed end, including interrupted captures, and do not establish process liveness or a measured duration.
- Parallel Perfetto tracks preserve overlapping operations without asserting call nesting between tracks.
- Perfetto lists sessions by earliest recorded time, keeps each session's parallel tracks together, and places untimed sessions last.
- Model variant labels describe the host's selected variant separately from observed reasoning effort.
- Next:
  - Reopen Perfetto for updated timing snapshots.
  - [Recover assignments](#recover-assignments) when task or role attribution is missing.

## Recover assignments

- Context: apply [RECORDS] when reports lack assignments for opaque handoffs.
- Inputs: selected session/turn IDs and saved evidence of task/role assignments.
- Effects:
  1. Verify missing assignments against saved evidence.
  2. Add verified assignments to `IMPLEMENTATION/assignment-annotations.json` using the format below.
  3. Reference existing evidence files inside the implementation.
  4. Resolve duplicate or conflicting annotations before refreshing reports.
- Outputs: annotations for missing assignments on exact selected turns.
- Next: [regenerate reports](#report-usage), leaving unsupported assignments unknown.

```json
{
  "version": 1,
  "assignments": [{
    "adapter": "codex",
    "session_id": "SESSION",
    "turn_id": "TURN",
    "task": "01_business_logic",
    "role": "implementer",
    "purpose": "Implement business logic",
    "evidence": ["runs/01_business_logic/build/result.md"]
  }]
}
```

## Report usage

- Context: apply [RECORDS] when work finishes, is blocked or needs a usage report.
- Inputs: implementation path, saved native evidence and any assignment annotations.
- Effects:
  1. Run `python3 agentic-workflow/helpers/usage_report.py IMPLEMENTATION`.
  2. Read usage totals and coverage diagnostics.
  3. Report measured usage with missing or ambiguous evidence identified.
  4. Link permitted reports in the role's result under [RECORDS]' disclosure rules.
- Outputs:
  - Usage reports: `reports/usage.json` and `reports/usage.md`.
  - Content and timing exports: `reports/events.json` and `reports/timeline.json`.
