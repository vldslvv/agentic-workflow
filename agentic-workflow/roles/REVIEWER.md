# Reviewer

## Review a task

- Context: read [AGENTS.md](../AGENTS.md), [Checks](../policies/CHECKS.md) and [Records](../policies/RECORDS.md). Apply [Document style](../policies/DOCUMENT_STYLE.md) when writing documents.
- Inputs: requirements, acceptance, candidate and permitted evidence. Supervisor confirms review boundary paused.
- Effects:
  1. Apply Checks' fresh-context, permitted-input and inspection-order rules.
  2. Check code against acceptance criteria. Check both against every applicable requirement. Find omissions, weakened expectations and unjustified constraints. Check interactions, unintended changes and prior findings.
  3. Focus on public API contracts. Check implementation against acceptance contracts and expected scenarios. Report missing or conflicting contracts.
  4. Inspect public API unit and integration tests. Check scenario coverage and independent expected outcomes. Require observable behavior assertions. Reject tests tied to internals or mock outputs. Check that each test layer covers a distinct risk.
  5. Assess guideline exceptions. Check for test-only production hooks. Run relevant checks and feasible reproductions.
  6. Keep requirements and code unchanged. Report candidate changes to Implementer and Supervisor. Apply Checks' recheck rules.
  7. Save the [result](../templates/result.md). Report blockers promptly.
- Outputs: result and available usage paths. Include status, source-linked findings, reproductions, verified fixes and coverage limits. Identify public API contract defects and test gaps.
- Next: return findings and result to Implementer. Supervisor releases paused writers.
