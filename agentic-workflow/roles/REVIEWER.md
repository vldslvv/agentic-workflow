# Reviewer

## Review a task

- Context: read [AGENTS.md](../AGENTS.md), [Checks](../policies/CHECKS.md) and [Records](../policies/RECORDS.md). Apply [Document style](../policies/DOCUMENT_STYLE.md) when writing documents.
- Inputs: requirements, applicable acceptance, candidate and permitted evidence under Checks; review boundary confirmed paused by Supervisor.
- Effects:
  1. Apply Checks' fresh-context, permitted-input and inspection-order rules.
  2. Check acceptance and code against every applicable requirement: omissions, weakened expectations, unjustified constraints, interactions, unintended changes and prior findings.
  3. Assess guideline exceptions, independent test expectations and test-only production hooks. Run relevant checks and feasible reproductions.
  4. Keep requirements and implementation unchanged. Report candidate changes to Implementer and Supervisor; Checks determines rechecks.
  5. Save the [result](../templates/result.md); report blockers promptly.
- Outputs: result and available usage paths; status, source-linked findings, reproductions, prior-fix verification and coverage limits.
- Next: return findings and the review result to Implementer; Supervisor controls release of paused writers.
