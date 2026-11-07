# Supervisor

Read [AGENTS.md](AGENTS.md), [Workflow](WORKFLOW.md), [Bundle](BUNDLE.md), [Checks](CHECKS.md) and [Records](RECORDS.md). Coordinate through concise results; workers own detailed planning. Relay memory paths under [Memory](MEMORY.md).

1. Resolve the W1 inputs and record locations. Use new output paths for initial work and selected code for incremental work.
2. Assign each task's mode using the table below and record it in the handoff. Dispatch through W2 and Records, supplying resolved guideline paths and the role's permitted inputs.
3. Maintain the coordination state in S2, including ownership of shared configuration. Explain file conflicts, review delays or capacity limits; use the workflow's pause/release procedure for independent checks.
4. Collect results under W5. Assess each task against its assigned [Implementer procedures](IMPLEMENTER.md) and Checks; identify affected downstream evidence when returning findings.
5. Coordinate final validation and correction routing through W6–W8. Use [Validator](VALIDATOR.md) for final scenarios and repair publication/recovery.
6. Use native waits/notifications for the longest duration allowed by host and user-update limits. Timeouts alone mean keep waiting. Avoid status prompts, short polling, sleep monitoring and repeated agent-list checks; use a status snapshot only for concrete uncertainty. Message workers for inputs, decisions, changes, blockers or repairs; keep user updates brief and factual.
7. Report outcomes under W8. At overall completion or a blocked stop, or earlier on request, run `python3 agentic-workflow/helpers/usage_report.py .agentic-workflow/NNN_name`. Link reports and coverage limits. For the dashboard or tracing troubleshooting, read [Tracing](helpers/TRACING.md).

## Task mode

Honor source and user requirements; resolve conflicting instructions before dispatch. Unresolved requirements block either mode. Model profiles do not determine task mode.

| Task conditions | Assigned mode |
|---|---|
| Planning or independent task review is required, or work is complex | `full` |
| Work is simple and bounded, with clear source criteria | `lightweight` |
| Uncertain which applies | `full` |
