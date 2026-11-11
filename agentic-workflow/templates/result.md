# <Role/run> — result

Report completed work, evidence, findings and remaining limits.

## References:

- [WORK_RESULT]: Defines WorkResult fields. agentic-workflow/contracts/WorkResult.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [MODELS]: Provides heuristics for choosing subagent models. agentic-workflow/policies/MODELS.md

## Result

Apply [RECORDS] (“Return work”) and omit inapplicable fields.
Return the concise [WORK_RESULT] after saving this record.
Keep independent inputs within [CHECKS] (“Independent checks”).

- **Status:** <PASS, FAIL, BLOCKED or NOT_RUN; assigned mode and unfinished work.>
- **Artifacts:** <Produced document, implementation, memory and other output paths.>
- **Self-review:** <When performed: scope, findings and resolutions; separate from independent review.>
- **Scope:** <Source and acceptance paths; candidate location/revision; changed files or checked boundary.>
- **Checks:** <Requirement coverage, command/method, working directory, outcome and evidence path.>
- **Findings:** <Source-linked expected/observed behavior, reproduction and resolution; remaining blockers or coverage gaps.>
- **Independent result:** <Required review or validation result path; acceptance remains with Supervisor.>
- **Routing:** <Model choice and reason under [MODELS]; requested and observed settings, with unknown observations unavailable.>
- **Limits:** <Skipped or substitute checks, guideline exceptions, cleanup errors and unavailable telemetry.>
- **Repair:** <Published or reserved repair path, dependencies and unfinished publication.>
- **Reconstruction:** <Allowed inputs, isolation controls, exclusions/leakage and limits when applicable.>

Document-only results report document validity and generation readiness separately.
Link available usage reports instead of copying measurements.
