# Implement — produce code and demonstrate alignment

Read [SUITE_CONTRACT](SUITE_CONTRACT.md) first. This workflow handles a selected accepted unit of work; [GENERATE](GENERATE.md) schedules it across a project.

## Inputs

Require an approved spec snapshot, selected requirement IDs, dependency evidence, a target profile, declared writable output paths, and an acceptance baseline. The supervisor records a run and supplies only relevant context to the worker.

Existing code may be used for normal implementation and incremental work. That permission does not carry into a clean-room generation run.

## I1. Check readiness

Validate approval, references, scope, and prerequisites. Record what will be checked locally and what must be checked after integration. An approved dependency contract can support parallel development only under an explicitly chosen contract-first policy; acceptance against a stub is not integration acceptance.

If a required acceptance mechanism is unavailable, report that before implementation. Useful implementation may proceed when authorized, but it cannot be labeled accepted until the gate exists and passes.

## I2. Make a transient plan

The worker maps the selected requirements to implementation work and implementation-level tests. It chooses internal architecture within the target constraints. The plan must identify integration points, relevant failure cases, and the verification commands or adapter operations it expects to use.

The plan is not an alternative specification. Any externally visible ambiguity returns to Define. Any permitted implementation choice stays in the plan unless it becomes a necessary operational contract.

## I3. Implement in an owned workspace

Build only the selected scope and unavoidable integration changes. Write useful unit and integration tests. Do not modify approved specifications, golden references, verifier assertions, or acceptance thresholds in the implementation branch.

Report newly discovered contract gaps using a change proposal. Additional test ideas can be submitted to the verifier owner, but the worker cannot silently promote its own assumptions into acceptance rules.

Prefer a fresh worker session per task. Supply approved context and scoped dependency contracts rather than an unbounded history of earlier agent conversations.

## I4. Run local checks

Execute build checks and implementation-level tests through the chosen project adapter. Record actual results, commands, exit codes, and artifacts. Missing tooling, skipped execution, and timeouts remain explicit. A worker's statement that the code “should pass” is not evidence.

Unit tests are implementation-specific and may be discarded on a technology change. They complement, but do not replace, durable behavioral acceptance checks.

## I5. Review in a fresh context

Start a new reviewer session using [REVIEWER.md](../prompts/REVIEWER.md). Provide the approved contract, selected IDs, candidate revision, allowed inspection context, and raw execution evidence. Do not supply the implementation agent's persuasive narrative as the basis of review.

The reviewer inspects requirement coverage, unintended behavior, errors, integration boundaries, and missing evidence. It must cite requirement IDs and concrete findings. See [REVIEW.md](../templates/REVIEW.md) for the report.

If a fresh session cannot be obtained, record INDEPENDENT_REVIEW_NOT_RUN. A useful self-review can still be kept, but cannot be relabeled independent.

## I6. Execute independent acceptance

The trusted verifier runs the protected acceptance baseline against the candidate. Adapt the execution boundary to the project: a library can use a neutral driver, a CLI can be invoked as a process, a service can be deployed in isolation, and other artifacts can use their declared evaluation protocol. Deployment is not required when the artifact has no deployment lifecycle.

Run system-level interaction checks after combining independently developed capabilities. Preserve outputs, required state observations, side effects, and failure evidence. The verifier must observe the actual candidate rather than trust a worker-authored “passed” report.

Review and execution provide different evidence. Full acceptance requires both when the project policy makes both mandatory. A code review cannot override a failing mandatory check.

## I7. Repair or escalate

For implementation defects, return requirement-linked findings to a repair worker and rerun the affected checks plus the declared regression set. Re-review material changes. Hash each candidate so results cannot be reused after the code changes.

For a specification or verifier defect, stop the affected acceptance run. Resolve and approve a versioned change, then begin evaluation against the new baseline. Preserve the old failure; do not edit history to make the original run appear successful.

Bound attempts and resources. Record first-attempt failure separately from eventual acceptance. Failure to complete within budget yields partial evidence, not a fabricated success.

## I8. Integrate and record

Integrate the candidate through the repository's approved mechanism. Run the integration gate on the actual combined revision; individual branch passes are not sufficient. Record the accepted revision, complete requirement dispositions, exact verification baseline, and any manual approval evidence.

The supervisor, not the worker, marks completion. Future resume/skip decisions must validate input and artifact identity. When a behavior change affects dependents, invalidate their old evidence until relevant checks are rerun.

## What successful alignment means

Every selected mandatory requirement has evidence from the prescribed method; all required integration checks pass; no blocking review findings remain; protected inputs match their approved versions; and results are tied to the actual candidate.

This workflow establishes scoped conformance of an implementation. Only a separate generation experiment can establish that the implementation was regenerated under declared isolation conditions.
