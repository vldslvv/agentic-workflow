# Tracing workflows

## Capture live work

- Context: apply [Records](../policies/RECORDS.md) when starting or resuming execution.
- Inputs: allocated implementation path and available native host storage.
- Effects:
  1. Run `python3 agentic-workflow/helpers/trace_view.py IMPLEMENTATION --interval 5`.
  2. Keep the process running during execution.
- Outputs: captured native turns, refreshed reports and a local dashboard.
- Next: inspect progress or report final usage before stopping capture with `Ctrl+C`.

## Import saved traces

- Context: use when analyzing saved Codex records or OpenCode exports.
- Inputs: implementation path and native records for the intended work.
- Effects:
  - Copy selected Codex records with their metadata into `IMPLEMENTATION/native/`.
  - For OpenCode, save `opencode export SESSION_ID` JSON under `IMPLEMENTATION/native/`.
  - Include only intended turns, excluding unrelated work and inherited fork history.
  - Preserve original records when preparing imports.
- Outputs: saved native evidence under the implementation root.
- Next: [generate usage reports](#report-usage) or [open the viewer](#inspect-traces).

## Inspect traces

- Context: use when inspecting execution, recorded content or timing.
- Inputs: implementation path with captured or imported traces.
- Effects:
  1. Open the running dashboard or launch `python3 agentic-workflow/helpers/trace_view.py IMPLEMENTATION`.
  2. Open the printed URL if the browser does not launch.
  3. Use **Group by** and search to find relevant tasks, agents or tools.
  4. Inspect **Recorded content** for messages and tool activity.
  5. Use **Open timeline in Perfetto** when timing details are needed.
- Outputs: execution observations and identified evidence gaps.
- Next:
  - Reopen Perfetto for updated timing snapshots.
  - [Recover assignments](#recover-assignments) when task or role attribution is missing.

## Recover assignments

- Context: apply [Records](../policies/RECORDS.md) when reports lack assignments for opaque handoffs.
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

- Context: apply [Records](../policies/RECORDS.md) when work finishes, is blocked or needs a usage report.
- Inputs: implementation path with saved native evidence and any assignment annotations.
- Effects:
  1. Run `python3 agentic-workflow/helpers/usage_report.py IMPLEMENTATION`.
  2. Read usage totals and coverage diagnostics.
  3. Report measured usage with missing or ambiguous evidence identified.
  4. Link permitted reports in the role's result under Records' disclosure rules.
- Outputs:
  - Usage reports: `reports/usage.json` and `reports/usage.md`.
  - Content and timing exports: `reports/events.json` and `reports/timeline.json`.
