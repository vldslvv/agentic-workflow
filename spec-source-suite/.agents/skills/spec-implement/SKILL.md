---
name: spec-implement
description: Implement selected approved project specifications and demonstrate acceptance alignment through fresh review and independent checks. Use for scoped implementation, not for inventing requirements or claiming clean-room generation.
---

# Implement and align

Read the repository `AGENTS.md`, [shared contract](../../../docs/SUITE_CONTRACT.md), and [Implement workflow](../../../docs/IMPLEMENT.md).

## Inputs

Require selected approved specs/requirement IDs, accepted prerequisites, target constraints, writable workspace boundaries, verification baseline, and a run budget. Missing inputs block the corresponding gate.

## Procedure

1. Validate readiness and freeze the relevant input identities. Keep scheduling and resume state in the supervisor or an explicit external run record.
2. Prepare a transient plan covering requirement IDs, integration points, and useful implementation-level tests.
3. Implement the selected behavior within owned paths. Do not modify approved specs, reference fixtures, or protected acceptance checks to fit the candidate.
4. Execute local checks and preserve actual outputs. Report missing execution honestly.
5. Request a fresh reviewer session using [REVIEWER.md](../../../prompts/REVIEWER.md). When unavailable, report the independent gate not run; do not role-play its completion in the same session.
6. Invoke the independent verifier against the actual candidate. Review opinions and unit tests do not substitute for mandatory behavioral checks.
7. Repair implementation defects within budget. Return ambiguities and verifier conflicts to their approval process. Preserve failed attempts.
8. Integrate and rerun the required combined-scope checks. Record evidence against the final candidate digest, not a previous version.

## Outputs

Produce the implementation artifacts, local check results, [review report](../../../templates/REVIEW.md), acceptance evidence, and [run report](../../../templates/RUN_REPORT.md). Acceptance requires every mandatory scoped gate; otherwise return explicit partial or failed status.
