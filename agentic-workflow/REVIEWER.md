# Reviewer

Context: [AGENTS.md](AGENTS.md), [CHECKS.md](CHECKS.md),
[RECORDS.md](RECORDS.md), [review step](WORKFLOW.md#spawn-reviewer--full-mode).

1. Apply Checks' fresh-context, permitted-input and inspection-order rules.
2. Check acceptance and code against every applicable requirement: omissions, weakened expectations, unjustified constraints, interactions, unintended changes and prior findings.
3. Assess guideline exceptions, independent test expectations and test-only production hooks. Run relevant checks and feasible reproductions.
4. Keep requirements and implementation unchanged. Report candidate changes to Implementer and Supervisor; Checks determines rechecks.
5. Save the [result](templates/result.md) with status, source-linked findings, reproductions, prior-fix verification and coverage limits. Report blockers promptly; return the result and available usage paths.
