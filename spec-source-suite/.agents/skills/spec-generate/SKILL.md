---
name: spec-generate
description: Generate initial or incremental app work from an approved subsystem DAG; use explicit branches for regeneration and cross-target reconstruction.
---

# Generate

Read the repository AGENTS.md, [shared contract](../../../docs/SUITE_CONTRACT.md), [Generate](../../../docs/GENERATE.md), [Implement skill](../spec-implement/SKILL.md), and [Implement workflow](../../../docs/IMPLEMENT.md). Follow G1–G5 as supervisor.

Use the manifest's registered acceptance documents and canonical depends_on declarations. Validate ready tasks, obtain planner handoffs, and dispatch Implement serially. Maintain evidence outside worker memory and require assembled-app checks before project acceptance.

Load [Regeneration](../../../docs/REGENERATION.md) only for regeneration/cross-target scope and [Strong isolation](../../../docs/STRONG_ISOLATION.md) when enforcement is required. Return the generated candidate and scoped run evidence with actual isolation and unresolved gates.
