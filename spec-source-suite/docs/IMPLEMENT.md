# Implement — one task's planner, implementer, reviewer cycle

Read the [shared contract](SUITE_CONTRACT.md); its authority, roles, integrity, attempt limits, and acceptance rules apply here. [Generate](GENERATE.md) schedules this procedure across subsystems.

**Inputs:** a separately authorized implementation task with the planner's complete approved documents, baseline/approval record, frozen checks, accepted dependency evidence, target, and owned paths. **Outputs:** candidate, raw check results, independent review, and run record tied to exact identities.

## I1. Validate the planner handoff

Confirm [Define](DEFINE.md)'s implementation-handoff gate completed and contract §§1–5 readiness holds. Its document-completion gate alone does not satisfy this precondition. The planner has already prepared the implementation plan and checks; the implementer reads them rather than replacing them. Record the input inventory and ownership in the run directory. Missing inputs yield BLOCKED before implementation. Significant plan deviations follow contract §6.

## I2. Implement and check the candidate

Build within owned paths, including approved integration work. Add useful local tests where they establish behavior; they supplement the frozen acceptance checks. Run build/local checks, retaining actual commands, output, and exit codes. Compare protected input digests and inspect scope changes before presenting a candidate. Record its revision or content digest, including uncommitted output when relevant.

## I3. Spawn independent review and acceptance execution

The implementer spawns a fresh reviewer using [REVIEWER.md](../prompts/REVIEWER.md) and contract §3's restricted input handoff. Exclude the plan and conversation. The reviewer assesses check coverage and executes the frozen acceptance checks against that candidate, using [VERIFIER.md](../prompts/VERIFIER.md) for execution guidance. It owns its raw results and [review record](../templates/REVIEW.md). Recheck candidate and baseline identities after execution; results for a moving candidate are invalid.

**Gate:** every prescribed acceptance check was assessed and a genuine independent review exists. Missing execution or fresh context blocks acceptance; a local pass alone is insufficient.

## I4. Repair or escalate

Apply the exact routing and initial-plus-two-repairs limit in contract §6. Return requirement-linked implementation defects to the implementer; preserve prior attempts. Each repaired candidate returns to I2 and a new fresh review/acceptance run at I3. Specification, verifier, infrastructure, and significant-plan problems go immediately to the supervisor, not through speculative implementation repairs.

## I5. Integrate and request acceptance

Integrate through the authorized repository procedure and run the declared real-dependency/regression checks on the combined candidate. If integration changes reviewed behavior, repeat the affected review and acceptance before requesting acceptance. Preserve evidence against the actual integrated identity.

The supervisor applies contract §7 and records the result using [RUN_REPORT.md](../templates/RUN_REPORT.md). A subsystem pass can unlock dependents; only Generate's assembled-app gate can establish project acceptance. A blocked or failed gate remains explicit and preserves partial evidence.
