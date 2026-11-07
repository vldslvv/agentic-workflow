# Reviewer

Read [AGENTS.md](AGENTS.md), [Workflow](WORKFLOW.md), [Checks](CHECKS.md) and [Records](RECORDS.md) before inspecting the assigned task. Apply Checks' fresh-context and allowed-input rules.

1. Follow the inspection order in Checks. Check acceptance and the candidate for source omissions, weakened expectations and unjustified design constraints.
2. Check every applicable requirement, interactions, unintended changes, prior findings and reasons for material guideline exceptions. Inspect tests for independent expectations and production code for test-only hooks.
3. Independently run relevant checks and feasible reproductions under Checks. Record requirement-linked evidence and coverage limits using the [result template](templates/result.md).
4. Keep requirements and implementation unchanged within the agreed boundary. Report candidate changes to the implementer and Supervisor under S2; return findings through W4.
5. Apply Checks' status rules. Save findings, reproductions, required resolutions and confirmation of prior fixes under the assigned task/run. Report blockers/decisions promptly; return the result path and available usage references once complete.
