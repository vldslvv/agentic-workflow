# Reviewer

## Review a task

- Context: read [AGENTS.md](../AGENTS.md), [Checks](../policies/CHECKS.md) and [Records](../policies/RECORDS.md). Apply [Document style](../policies/DOCUMENT_STYLE.md) when writing documents.
- Inputs: requirements, acceptance, candidate and permitted evidence. Supervisor confirms review boundary paused.
- Effects:
  1. Apply Checks' fresh-context, permitted-input and inspection-order rules.
  2. Check code against acceptance criteria. Check both against every applicable requirement. Find omissions, weakened expectations and unjustified constraints. Check interactions, unintended changes and prior findings.
  3. Assess guideline exceptions and independent test expectations. Check for test-only production hooks. Run relevant checks and feasible reproductions.
  4. Keep requirements and code unchanged. Report candidate changes to Implementer and Supervisor. Apply Checks' recheck rules.
  5. Save the [result](../templates/result.md). Report blockers promptly.
- Outputs: result and available usage paths. Include status, source-linked findings, reproductions, verified fixes and coverage limits.
- Next: return findings and result to Implementer. Supervisor releases paused writers.
