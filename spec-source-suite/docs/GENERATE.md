# Generate — construct a project from its specification bundle

Read [SUITE_CONTRACT](SUITE_CONTRACT.md) first. Generate prepares the inputs and environment, schedules the dependency graph, invokes [IMPLEMENT](IMPLEMENT.md), and collects project-level evidence.

## Modes

| Mode | Existing project implementation visible? | Claim available after successful acceptance |
|---|---|---|
| `initial` | None exists for the selected project scope | A first implementation was generated from the supplied bundle |
| `incremental` | Yes, within the declared workspace | An existing implementation was updated and accepted |
| `regenerate` | Prior implementation of the selected scope is excluded | A new scoped implementation passed the same behavior baseline under the reported isolation conditions |
| `cross-target` | Prior implementation of the selected scope is excluded; target changes | A new target implementation passed the same behavior baseline under the reported isolation conditions |

Changing the target in place while letting the worker read the old implementation is a porting experiment, not a clean-room cross-target regeneration experiment. Keep that distinction in reporting.

## G1. Select scope and freeze the baseline

Select one capability, an explicit subgraph, or the full project. Resolve prerequisites before starting. For partial scope, either include prerequisite capabilities in the generation closure or provide declared boundary dependencies. Record which path is used.

Do not confuse prerequisite closure with impact analysis: upstream prerequisites support generation; downstream consumers determine what integration/regression checks may be affected. A full-system claim requires the full-system boundary and acceptance gate.

Freeze approved spec and requirement IDs, dependency revisions, verifier revision, target profile, suite/prompt revision, required inputs, budgets, and feedback policy. The project must supply nonempty specs. A target incompatible with immutable behavior must be rejected or explicitly renegotiated, not accommodated by quietly relaxing requirements.

## G2. Prepare a new workspace when required

For `initial`, `regenerate`, and `cross-target`, create a new output workspace. For regeneration, export only approved inputs from an allowlist. Never test the idea by deleting the user's working repository.

An export may contain approved behavior documents, schemas, public acceptance examples, retained assets/data, relevant suite instructions, and target/environment constraints. It must not contain prior scoped source code, copied build outputs, repository history, old implementation plans, old prompts/transcripts, implementation-derived caches, or leaked acceptance answers.

The environment must account for persistent agent memories, parent directory instructions, home directories, filesystem mounts, repository remotes, and network access. A clean directory with unrestricted access to the old repository is not an enforced clean room. Restrict those channels through the available runner/sandbox, or downgrade the isolation claim.

Export checks MUST resolve paths safely and reject traversal and symlink escapes. Hash the final exported files, not just the requested path names. Scan for prohibited paths and sentinel artifacts where applicable. Do not embed secrets in export manifests.

## G3. Declare retained boundaries

Some projects need external services, binaries, datasets, model weights, schemas, UI assets, or existing state. Declare which survive and why. A retained component is part of the experiment boundary, not evidence that it can be regenerated.

For partial regeneration, record whether dependencies are real services/binaries, approved contracts, or test doubles. Tests against a double must be labeled; test integration with the real boundary before claiming compatibility.

Code reconstruction is distinct from state restoration or data migration. Require those checks only when the project declares them, and report them separately. Cross-target persistence compatibility must specify the preserved observable data semantics, not assume identical storage internals.

## G4. Dispatch the DAG

Default to topological serial execution. For each ready node, prepare a fresh task context and invoke Implement. Scheduling, retry limits, run state, and dependency completion belong to the supervisor.

Parallelize only ready nodes with isolated writes or explicit resource coordination. After combining results, run integration acceptance on the combined candidate. A generation run cannot pass merely because every node emitted a “done” message.

An incremental mode may reuse matching accepted outputs. A clean-room mode cannot seed the selected scope from outputs of the previous implementation. It may resume outputs produced **inside the same recorded experiment** if their provenance and input identities remain valid; label the run resumed rather than a fresh independent trial.

## G5. Keep the verifier outside the implementation's authority

Run acceptance from a separately controlled process/environment. Protect its assertions, reference data, and results. A directory name or agent instruction is not sufficient protection if the worker can still write those files.

Tests may all be public; secrecy is optional. For held-out tests, disclose the behavioral contract but not the cases, and define what failure feedback can be returned during repair. Preserve a one-shot first-attempt result even when repair is allowed.

The acceptance oracle should remain technology-independent. A target-specific invocation/build adapter may change, but it must not normalize away contractual differences or change expected outcomes. Record and independently validate adapter revisions before comparative acceptance. If an entire new verifier is necessary, mark the run as a changed-baseline comparison rather than claiming an unchanged verifier.

## G6. Evaluate at project scope

Run the same frozen behavioral baseline against the generated system, including cross-capability behavior and declared operational limits. Measure only within the specified environment and sampling design.

For nondeterministic outputs, apply the approved rubric, statistical protocol, or semantic comparison. Do not introduce ad hoc tolerances after seeing failures. For a technology switch, check public errors, ordering, data semantics, and relevant concurrency/recovery behavior where the project requires them.

A new implementation that passes finite acceptance tests provides evidence of specified conformance, not a proof of all conceivable behavioral equivalence.

## G7. Report the experiment precisely

Use [RUN_REPORT.md](../templates/RUN_REPORT.md). Report mode, exact scope, baseline, target, retained boundaries, visible inputs, candidate digest, first-attempt result, repaired result, failed requirements, manual interventions, resources, and evidence paths.

Report isolation as one of:

- `enforced`: required controls were applied and evidenced for the declared threat model.
- `procedural`: the workflow requested separation, but the environment did not enforce every required boundary.
- `none`: prior implementation access was permitted or untracked.

Only the first level supports the suite's enforced clean-room claim. Procedural regeneration can still provide useful weaker evidence. Any discovered leakage invalidates the clean-room claim for that run, even if conformance passes.

Run repeated trials only when evaluating reliability; record all attempts and their varying factors. One successful run is a successful run, not an established probability of future reconstruction success.

## Failure behavior

Missing specs: NO_PROJECT. Missing approvals or required assets: BLOCKED. Invalid DAG: BLOCKED. Incompatible target: BLOCKED. Acceptance mismatch: FAIL. Infrastructure failure: INFRA_ERROR. Suspected or detected input leakage: CLEAN_ROOM_INVALID. Preserve partial results and never replace these outcomes with a pass because a worker exited successfully.
