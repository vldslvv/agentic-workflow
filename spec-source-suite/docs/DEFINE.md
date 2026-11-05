# Define — prepare approved task inputs

Read the [shared contract](SUITE_CONTRACT.md). Define is the planner's procedure for new intent, imported specs, explicitly authorized observations of existing behavior, or changes to approved behavior.

**Inputs:** user intent or an existing bundle, approval authority, repository baseline, and known constraints. **Output:** approved task documents, registered subsystem specs, manifest/target references, and frozen requirement-linked checks. Missing intent yields NO_PROJECT; unresolved normative choices remain proposed.

## D1. Establish scope and boundaries

Identify observable operations, outputs, errors, side effects, persisted state, allowed variation, and exclusions. Preserve source provenance. Observed behavior is a proposal until approved. Use concise prose and tables; add schemas or models only where needed. Resolve material gaps with the user and leave delegated internal choices open.

## D2. Define subsystems and acceptance

Choose independently assessable subsystems, defaulting to one per task. Use [SPEC.md](../templates/SPEC.md) for each task's `acceptance.md`; retain existing authoritative formats when possible. Register its path in [project.yaml](../templates/project.yaml). Put shared semantics in normative references. Validate the derived DAG under contract §5.

Each mandatory requirement needs observable normal, boundary, failure, and interaction outcomes as applicable, with concrete checks. Define project-level assembled-app checks too. Keep project metadata and [target constraints](../templates/target.yaml) outside the suite. Select technology only from supplied or delegated choices.

## D3. Prepare plan and checks

Write the complete implementation approach using [PLAN.md](../templates/PLAN.md), including requirement scope, dependency inputs, owned paths, integration points, and check commands. Prepare requirement-linked executable checks and authorized manual criteria under contract §4. Use [VERIFICATION.md](../templates/VERIFICATION.md) only if acceptance needs a separate mapping. Missing required check execution mechanisms block the implementation handoff.

## D4. Review, approve, persist, and freeze

Check contradictions, coverage, references, prerequisite cycles, and retained inputs. Present both complete documents for approval. Follow contract §2 for exact persistence, Plan-mode deferral, baseline commit, approval digests, and later changes. Freeze the approved checks and normative input inventory before implementation. If checks reveal a contract gap, resolve and approve it before freezing.

**Completion gate:** documents are saved and approved, all selected requirements have available prescribed checks, graph and references are valid, and the handoff inventory is frozen. Planning approval does not start implementation. On a separate implementation instruction, hand off both documents and the contract §3 inputs. Behavior changes follow [CHANGE.md](../templates/CHANGE.md) and invalidate affected evidence.
