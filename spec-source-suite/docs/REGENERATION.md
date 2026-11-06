# Branch — regeneration and cross-target reconstruction

Read this only for `regenerate` or `cross-target` mode, together with [Generate](GENERATE.md). The [shared contract](SUITE_CONTRACT.md) continues to govern acceptance and attempts.

## R1. Fix the experiment boundary

`regenerate` reconstructs a selected scope without its prior implementation. `cross-target` does so on a different target with the same approved behavior. Changing technology with access to old implementation is porting, not clean-room reconstruction. Record scoped prerequisites and retained services, binaries, assets, data, and schemas; they are retained inputs, not reconstructed outputs.

Keep behavior, acceptance thresholds, and approved fixtures fixed. A target-specific build/invocation adapter may change only with independent validation and an approved revision; it cannot normalize away contractual differences. A changed verifier means a changed-baseline comparison, not an unchanged-verifier experiment. Define persistence compatibility, state restoration, or migration checks only where required by the project.

## R2. Export to a new workspace

Never delete the working implementation. Export only explicitly allowlisted approved behavior, contracts, public examples, retained assets/data, relevant suite guidance, and target constraints. Exclude prior scoped source, build products, repository history, old plans, prompts/transcripts, implementation-derived caches, and leaked acceptance answers. Prepare any new task plan from allowed inputs inside the experiment; the current plan still stays out of reviewer context.

Apply [project-memory exclusions](PROJECT_MEMORY.md#excluded-contexts) to exports and every regeneration handoff, including planning contexts and retained note copies. Declare their paths in each worker's `forbidden_paths`.

Resolve export paths safely and reject traversal or symlink escapes. Hash the actual final exported files and inspect them for forbidden/sentinel artifacts. Keep audit records outside the exported inputs. Credentials must not enter the export.

## R3. Record actual separation

Account for agent memories, parent directories, home/mounted files, history, caches, remotes, and network. For required enforcement use [STRONG_ISOLATION.md](STRONG_ISOLATION.md); unavailable required controls block execution. Procedural regeneration may proceed only under an explicit procedural policy and supports a weaker claim. A fresh directory with access to prior code is not an enforced clean room.

Report actual isolation as `enforced`, `procedural`, or `none` (prior access permitted/untracked). Known prior-code leakage yields CLEAN_ROOM_INVALID and invalidates reconstruction claims; retain ordinary conformance evidence separately. Test doubles do not establish compatibility with real retained dependencies: run the integration gate at the actual boundary.

## R4. Execute and report

Resume Generate at G2. Never seed selected scope from prior implementation outputs. Resume only outputs produced inside this recorded experiment with matching provenance and identities; label it resumed, not a fresh trial. Apply the same frozen acceptance to the final candidate, including declared errors, ordering, state, and operational limits.

Report original and changed target/adapter identities, export inventory, retained boundaries, isolation controls/limits, first-attempt and repaired outcomes, and any baseline changes. Finite checks establish scoped conformance, not universal behavioral equivalence. Repeated reliability trials require retaining every trial and its conditions; one success does not estimate reconstruction reliability.
