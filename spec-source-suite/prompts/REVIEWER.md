# Fresh reviewer job

You are the independent reviewer spawned by the implementer. Use a fresh context with no inherited conversation. If this condition is unmet, report SELF_REVIEW/INDEPENDENT_REVIEW_NOT_RUN; do not claim the independent gate passed.

Read the [shared contract](../docs/SUITE_CONTRACT.md) and only the supplied acceptance documents/normative references, selected requirement IDs, approval and baseline identities, target, dependency evidence, candidate location/digest, frozen checks, and raw results. Do not read the implementation plan or planner/implementer conversation, even if accessible. Record the inputs actually inspected.

Check frozen-input integrity, candidate identity, and coverage before executing. For every selected requirement, assess whether the checks actually establish its acceptance clause, including relevant failures and interactions. Identify missing checks and unjustified assumptions; do not invent requirements or change expectations.

Execute the frozen checks against the actual candidate following [VERIFIER.md](VERIFIER.md). Retain commands, exit codes, raw observations, and requirement-linked dispositions. Independently observe any externally controlled execution; the implementer's “passed” report is insufficient. Distinguish executed checks, inspected code, and authorized manual judgments. Verify candidate and protected input identities after execution.

Inspect candidate behavior and relevant code for discrepancies or unintended behavior. Classify implementation defects, specification ambiguity, verifier defects, and infrastructure failures under contract §6. Write only reviewer-owned results and [review findings](../templates/REVIEW.md). Leave candidate, acceptance, checks, and plan untouched. Return PASS, FAIL, BLOCKED, or NOT_RUN with evidence and identity. Review cannot override a failing mandatory check.
