# Shared suite contract

Version: 0.1-draft. This document is normative for all three workflows. MUST denotes a gate; SHOULD denotes a default that can be overridden with a recorded reason.

## 1. The suite and the project are separate

The suite supplies methods, templates, worker instructions, scheduling, review, verification dispatch, and generation controls. A project supplies behavior, acceptance criteria, dependency relationships, required assets/data, and approved target constraints.

A capability specification is also its acceptance document. It MUST define observable outcomes and how each mandatory requirement can be assessed. A separate verifier may contain executable code, but its checks MUST trace to approved requirements. A prose spec and an untraceable test suite are not two interchangeable authorities.

The durable reconstruction input is therefore a **specification bundle**, not necessarily only prose. It can include approved schemas, public fixtures, formal models, required assets, or other explicitly retained inputs. Record each retained item. Do not claim “all code deleted” when executable verification or intentionally retained runtime components survive; describe the actual boundary.

## 2. Authority and changes

Approved behavioral specs and explicitly normative referenced contracts define requirements. Target profiles add implementation/environment constraints but cannot override behavior. Plans and task lists are transient proposals. Historical implementation is evidence of behavior, not automatically the desired specification.

If normative artifacts conflict, stop the affected work and record SPEC_CONFLICT. Do not choose whichever interpretation makes implementation easier. A failing protected test is an acceptance blocker; it is not proof that the test is correct. Route spec/verifier disagreements to their designated owner and resume only after a versioned resolution.

Any externally visible implementation discovery MUST be classified as required behavior, an allowed choice, or a proposed requirement change. Preserve required decisions in the specification. Do not preserve source-code trivia merely because it arose during implementation.

An approval records the exact artifact digest and approving authority. A literal `status: approved` written by an implementation agent is not approval. The authority may be the user or a previously delegated policy; the worker cannot grant itself that authority.

## 3. Minimum project input

Before implementation, the project MUST provide:

| Input | Meaning |
|---|---|
| Registered specs | Nonempty set of capability documents with stable spec and requirement IDs |
| Observable boundary | Public inputs/outputs, side effects, errors, and allowed variation that matter for the project |
| Dependencies | Explicit required capabilities or shared contracts, with resolvable references |
| Acceptance design | Requirement-linked checks/evals, pass rules, and treatment of nonautomated criteria |
| Target profile | Selected execution constraints and delivery type, without assumed application choices |
| Verification arrangement | An independent verifier or declared manual authority; automation gaps are visible |
| Output ownership | The paths/resources a worker may create or modify |

A project manifest indexes these inputs. It does not restate requirement semantics. The supplied templates are not a project until filled and approved.

Required data and assets must be supplied or reproducibly obtainable under the declared policy. Keep credentials out of specs and logs. Credentials needed during testing are injected by the trusted environment and recorded by reference, never by secret value.

## 4. Dependency and work graphs

`depends_on` in each spec is the canonical capability dependency declaration. The supervisor derives the project DAG from these declarations and the registered spec paths. Do not maintain a second hand-edited graph with divergent semantics.

Use an edge only for a real prerequisite. A semantic cross-reference need not be an execution dependency. If implementation prerequisites form a cycle, resolve it by extracting a shared contract or treating the mutually dependent behavior as one acceptance unit. Do not arbitrarily remove an edge just to make topological sorting succeed.

The conservative default is that a dependency must be accepted at the required revision before its consumer runs. A project may explicitly permit contract-first parallel work, but integration then has its own mandatory acceptance gate. A stub does not establish acceptance against the real dependency.

A work item can reference one or more specs but MUST identify exact requirement IDs and scope. One capability can need multiple transient implementation tasks; the spec does not have to mirror classes or files.

## 5. Roles and separation

The **spec author/owner** defines and approves behavior. The **implementation worker** produces code and implementation-level tests. The **reviewer** evaluates the candidate against the approved spec in a fresh session. The **verifier** executes or oversees acceptance checks. The **supervisor** owns orchestration, persisted state, retries, scope, and evidence.

Roles need not be different vendors or models. Fresh context is a procedural separation, not proof of statistically independent reasoning. A same-session review MUST be labeled SELF_REVIEW and cannot fulfill a required independent-review gate.

Implementation workers MUST NOT edit protected acceptance assertions, reference fixtures, or approved spec snapshots. Proposed checks and changes can be submitted separately. The verifying authority reviews and versions those changes before use.

Held-out test cases are optional. Independent ownership and immutability matter even when all tests are visible. Held-out cases MUST test disclosed requirements; they must not impose secret behavior. Record the visible-versus-held-out policy and the feedback allowed during repair.

## 6. Evidence and completion

Spec state is `draft`, `proposed`, `approved`, or `superseded`. Implementation and regeneration status belong to **run evidence**, not a mutable `done` flag in the spec.

Each selected mandatory requirement has one of PASS, FAIL, BLOCKED, or NOT_RUN, with evidence and a check type. Manual criteria must name the approving reviewer and inspected artifact. A manual judgment is not an automated test result.

A run is accepted only when all required gates for its declared scope pass and none are unaccounted for. Report automated conformance separately from full acceptance whenever manual criteria are present. Exclusions and nonapplicability must be approved before execution, not invented after a failure. Empty selection or zero executed mandatory checks cannot yield an acceptance pass.

Keep distinct evidence for:

- **Implemented and accepted:** this candidate met the scoped requirements under the recorded conditions.
- **Regenerated and accepted:** a newly generated candidate met the same baseline after starting without the scoped prior implementation, subject to the recorded isolation limits.
- **Cross-target regenerated and accepted:** the same behavior baseline passed on the selected alternative target.

These are scope- and revision-specific observations. A test suite demonstrates only what it exercises; no run establishes universal equivalence over unspecified behavior.

## 7. Run identity, resume, and accounting

Record at least: project/spec bundle digest, selected requirement IDs, dependency revisions, suite/prompt revisions, target digest, verifier revision/digest, retained input manifest, environment/tool versions, worker/reviewer identities and session IDs when available, candidate artifact digest, executed checks, timestamps, budgets, and outcomes.

Use `.suite/runs/<run-id>/` or a project-configured equivalent for `run.log`, append-only `results.jsonl`, rendered prompts, per-item logs, review records, and verification reports. Audit artifacts MUST NOT be automatically exported into a clean-room input bundle.

A resume operation can reuse completion only when relevant input identities still match and referenced outputs and evidence still exist and match their digests. Reverify after any candidate modification. Do not skip a node because an old log said “done.” A scope restriction, skip, or start-after option cannot bypass an unmet dependency or acceptance gate.

Distinguish the first-attempt result from eventual acceptance after repair. Record failed attempts, repair counts, timeout/infra errors, cost when available, and human interventions. Do not erase failed attempts from success-rate reporting.

## 8. Failure routing

| Finding | Required action |
|---|---|
| Missing, ambiguous, or contradictory behavior | Return to Define; hold affected work |
| Candidate violates an approved requirement | Repair implementation within the run budget |
| Acceptance check contradicts its referenced requirement | Raise verifier/spec issue; do not weaken checks in the implementation branch |
| Environment or dependency unavailable | Record infrastructure failure or BLOCKED; do not count as behavioral failure or pass |
| Target cannot satisfy a requirement | Report incompatible target; seek an explicit choice, not a silent requirement downgrade |
| Prior-code leakage or unverified isolation | Invalidate the clean-room claim; preserve any ordinary conformance evidence separately |
| Budget exhausted | Stop with partial evidence and resumable state |

## 9. Minimalism

Begin with Markdown, a manifest, file-based evidence, one worker per task, one fresh reviewer, and a serial scheduler. Add schemas, formal models, parallelism, or heavier isolation when the project's risks and experiment goals require them. Test counts and agent counts are not measures of completeness.
