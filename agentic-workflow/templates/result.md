# <Role/run> — result

Report completed work, evidence, findings and remaining limits.

## References:

- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [MODELS]: Provides heuristics for choosing subagent models. agentic-workflow/policies/MODELS.md

## Result

Apply [RECORDS] (“Return work”) and omit inapplicable fields.
Keep independent inputs within [CHECKS] (“Independent checks”).

- **Status:** <PASS, FAIL, BLOCKED or NOT_RUN; assigned mode and unfinished work.>
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
