# Acceptance specification: the reusable suite itself

ID: SUITE · Version: 0.1-draft

This document specifies the workflow tooling Codex is being asked to implement. It does not specify the user's future application. `SUITE-*` IDs refer to the tooling, not project capabilities. The assignment authorizes implementation of this brief; material behavior changes must be proposed explicitly.

## Goal and scope

Provide a lightweight, project-agnostic interface to Define, Implement, and Generate. The initial implementation may combine deterministic helper scripts with agent skills and manual handoff. It must report honestly which parts are automated.

Support file-based manifests and evidence, a serial DAG scheduler, pluggable workers and project verification adapters, fresh-session review, resume, and isolated-generation preparation. Do not build a hosted platform or prepopulate application requirements.

## Logical interface

Expose these operations through a documented CLI or library. Names below are logical operations, not commands already installed by this package.

| Operation | Minimum behavior |
|---|---|
| `define` | Prepare/import/revise specs through the authoring skill; retain provenance and unresolved questions |
| `validate` | Validate manifest, spec metadata, references, acceptance mappings, and dependency structure |
| `prepare` | Resolve selected work and export a job/bundle with content digests, without executing it |
| `implement` | Execute the selected spec workflow, including independent review and acceptance |
| `generate` | Schedule the selected graph using initial, incremental, regenerate, or cross-target mode |
| `verify` | Invoke the trusted project verifier against an identified candidate |
| `status` | Report input-scoped completion, failures, blocked work, and resume eligibility |

Support `resume`, `only`, `start-after`, `skip-completed`, and `max-items` semantics where relevant. These are scope controls, not permission to bypass prerequisites. Capabilities may first be provided as explicit manual jobs; state the limitation in output.

## Requirements and acceptance

| ID | Requirement | Acceptance evidence |
|---|---|---|
| SUITE-001 | Separate suite behavior from project content | An empty installation contains no product spec, chosen app stack, or generated application. Generate returns NO_PROJECT. |
| SUITE-002 | Import and validate generic specs | A well-formed synthetic spec is accepted structurally; duplicate IDs, unknown references, unresolved required fields, and missing acceptance mappings yield precise errors. Structural validity alone does not grant owner approval. |
| SUITE-003 | Derive the DAG from canonical spec dependencies | A chain and a fork produce valid ready-node sets. A cycle and an unknown prerequisite block execution. No duplicate hand-maintained graph is required. |
| SUITE-004 | Honor authority and frozen inputs | Workers cannot grant their own approvals. An approval is bound to a content digest; changing the approved content invalidates it. |
| SUITE-005 | Dispatch bounded, scoped worker jobs | Each job contains selected spec/requirement IDs, owned output paths, relevant dependencies, target, and budget. Worker identity, context, and result are recorded. |
| SUITE-006 | Request genuine fresh review | A review job has a distinct session and neutral contract-based context. A missing fresh session is reported; same-session self-review never counts as the independent gate. |
| SUITE-007 | Use verifier evidence, not worker self-report | A worker success response paired with a failing verifier yields FAIL. Missing checks or zero required checks executed cannot yield acceptance. Manual criteria are distinctly recorded. |
| SUITE-008 | Preserve baseline integrity | A worker attempt to modify protected specs/verifier assets is prevented by configured controls, or detected and invalidates the run. No unprotected deployment may be labeled enforced. |
| SUITE-009 | Persist evidence outside worker memory | Restarting the supervisor preserves request IDs, attempts, requirement dispositions, prompts, per-item logs, and artifact references. No conversation reconstruction is required for status. |
| SUITE-010 | Resume only when evidence still applies | Identical input and artifact digests allow reuse. Changed spec, dependency, target, verifier, suite/prompt, retained input, or missing/changed candidate artifacts invalidates relevant reuse. |
| SUITE-011 | Export only allowed regeneration inputs | Export contains approved inputs and excludes sentinel prior-source/history/transcript/build files. Traversal and symlink escapes are rejected. The final export has a file digest inventory. |
| SUITE-012 | Declare actual isolation limits | A procedural/manual environment is labeled procedural. Only tested controls for the declared boundary can produce enforced isolation. Known leakage yields CLEAN_ROOM_INVALID. |
| SUITE-013 | Distinguish all generation modes | Incremental work may use existing code; clean-room modes cannot seed selected scope from prior outputs. Cross-target mode changes target while preserving the behavior baseline. |
| SUITE-014 | Integrate before whole-scope acceptance | Passing individual nodes followed by failing combined acceptance produces a failed scope, not a successful project. Partial-scope claims name retained dependencies. |
| SUITE-015 | Handle stops and retries without falsifying results | Timeout, cancellation, missing dependencies, exhausted budget, and infrastructure failure produce explicit outcomes; attempts are retained and first-attempt results survive repair. |
| SUITE-016 | Support worker and project adapters | Demonstrate manual and stub worker adapters and at least one configurable real-worker adapter interface. A synthetic project adapter supplies candidate invocation/check behavior without hard-coded application assumptions. A real external worker need not be installed for structural tests to run. |
| SUITE-017 | Keep controls and execution safe | Jobs run only in explicitly authorized workspaces; no working source tree is deleted for regeneration. Credentials are not serialized in logs. Commands are explicit argument vectors or validated adapter operations, not untrusted shell interpolation. |
| SUITE-018 | Make scope controls truthful | `only`, `start-after`, `skip-completed`, and `max-items` never skip unmet prerequisites or fabricate completion. A selected no-op produces NO_WORK, distinct from project acceptance. |

## Minimal architecture

Use a manifest/spec reader, validator, DAG scheduler, context packager, worker adapter, review adapter, verifier adapter, workspace/isolation adapter, and file-backed run store. They can be small modules in one process. Keep the state machine deterministic outside the agent wherever possible.

The supervisor accepts worker artifacts as untrusted candidates. Only trusted verification and the completion policy determine acceptance. External workers must not be able to overwrite trusted run conclusions or the protected verifier through shared writable mounts.

A worker adapter consumes a scoped job and returns execution status, session identity when available, artifact locations, logs, and failure information. A manual adapter emits the job and waits for an explicitly imported result. Imported manual evidence retains its origin and does not prove automation or strong isolation.

A project adapter defines applicable build/prepare/invoke/check/cleanup operations. A library, CLI, service, UI, data pipeline, or other artifact can implement different subsets. No universal HTTP service, container deployment, or database is assumed.

An isolation adapter reports controls it actually applied: mounted paths, allowed network sources, permitted credentials, session/memory policy, and verifier boundary. If enforcement is unavailable, keep ordinary workflows usable and downgrade the isolation claim.

## Test design without inventing a product

Use small synthetic fixtures: abstract capability IDs, dependency edges, inert output files, stub worker responses, artificial verifier PASS/FAIL records, and sentinel strings that must not enter exported inputs. These fixtures test the suite's behavior. They must not become a default user project.

Test adapter failure, partial files, unexpected return codes, malformed evidence, cancellation, restart, stale hashes, and integration failure. Add a few targeted property checks for DAG ordering and resume invalidation when useful; do not generate redundant unit tests for every trivial helper.

Map every SUITE requirement to actual executed evidence. Report unimplemented or untested requirements plainly. A successful fixture test demonstrates the supervisor's mechanics, not the quality of generated applications.

## Definition of done for the initial generic suite

The three workflows are usable; the manifest, templates, and skills agree; structural fixtures cover the required gates; missing inputs and unavailable capabilities are honest; and a new project can be inserted without changing core workflow code.

The final report must distinguish instruction-only capability, implemented automation, executed mechanical tests, and any real agent/project experiments. Do not claim real regeneration until the user supplies an actual project and such an experiment runs.
