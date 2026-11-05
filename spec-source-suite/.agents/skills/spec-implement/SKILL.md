---
name: spec-implement
description: Implement an approved task, spawn fresh independent acceptance review, and repair within the shared attempt limit.
---

# Implement

Read the repository AGENTS.md, [shared contract](../../../docs/SUITE_CONTRACT.md), and [Implement](../../../docs/IMPLEMENT.md). Follow I1–I5 with the persisted planner handoff.

Implement within owned paths; preserve protected inputs and actual check results. Spawn the reviewer with no inherited conversation using [REVIEWER.md](../../../prompts/REVIEWER.md), supplying acceptance and checks but excluding the plan and conversation. The reviewer assesses coverage and executes acceptance independently.

Apply contract §6 for repairs and immediate escalations. Return the candidate, raw results, review findings, and [run report](../../../templates/RUN_REPORT.md). The supervisor applies the acceptance gates; missing checks or independent review cannot pass.
