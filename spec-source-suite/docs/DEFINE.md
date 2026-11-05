# Define — prepare approved task inputs

Read the [shared contract](SUITE_CONTRACT.md). Define is the planner's procedure for new intent, imported specs, explicitly authorized observations of existing behavior, or changes to approved behavior.

**Inputs:** user intent or an existing bundle, approval authority, repository baseline, and known constraints. **Document output:** approved task documents, registered subsystem specs, manifest/target references, implementation order where requested, and requirement-linked verification descriptions. **Additional handoff output, when authorized:** executable checks and frozen normative inputs. Missing intent yields NO_PROJECT; unresolved normative choices remain proposed.

Select scope from the deliverable. Executing a documentation plan remains Define work; it does not invoke Implement or Generate. For a documents-only request, complete the document branch below and report future executable-check preparation and app execution as deferred.

## D1. Establish scope and boundaries

Identify observable operations, outputs, errors, side effects, persisted state, allowed variation, and exclusions. Preserve source provenance. Observed behavior is a proposal until approved. Use concise prose and tables; add schemas or models only where needed. Resolve material gaps with the user and leave delegated internal choices open.

## D2. Define subsystems and acceptance

Choose independently assessable subsystems, defaulting to one per task. Use [SPEC.md](../templates/SPEC.md) for each task's `acceptance.md`; retain existing authoritative formats when possible. Register its path in [project.yaml](../templates/project.yaml). Put shared semantics in normative references. Validate the derived DAG under contract §5.

Each mandatory requirement needs observable normal, boundary, failure, and interaction outcomes as applicable, with concrete checks. Define project-level assembled-app checks too. Keep project metadata and [target constraints](../templates/target.yaml) outside the suite. Select technology only from supplied or delegated choices.

## D3. Prepare plan and checks

For documentation-only work, preserve the approved documentation plan and describe future implementation order, interfaces, ownership, and verification scenarios at the requested level. Acceptance states the future app's required outcomes; those outcomes are not the completion criteria for writing the documents. Describe setup, inputs, assertions, cleanup, pass rules, and evidence without creating executable app checks or an app environment.

When implementation-handoff preparation is authorized, write its implementation approach using [PLAN.md](../templates/PLAN.md), including requirement scope, dependency inputs, owned paths, integration points, and check commands. Prepare requirement-linked executable checks and authorized manual criteria under contract §4. Use [VERIFICATION.md](../templates/VERIFICATION.md) only if acceptance needs a separate mapping. Missing execution mechanisms block that handoff, not the documentation-only deliverable.

## D4. Review, approve, persist, and freeze

Check contradictions, coverage, references, prerequisite cycles, and retained inputs. Present both complete documents for approval. Follow contract §2 for exact persistence, Plan-mode deferral, baseline commit, approval digests, and later changes. For document scope, record document identities and defer executable-check freezing. For authorized handoff preparation, freeze the approved checks and normative input inventory before implementation. If checks reveal a contract gap, resolve and approve it before freezing.

**Document-completion gate:** requested documents are saved and approved, requirements have concrete verification descriptions, and consistency, coverage, graph, references, and approval identities are validated. This gate requires no app candidate, app-check execution, independent implementation review, or generation run. Report document completion separately from generation readiness.

**Implementation-handoff gate:** the document gate passes, all selected requirements have available prescribed executable/manual checks, and the handoff inventory is frozen. Planning approval does not start implementation. On a separate implementation instruction, hand off both documents and the contract §3 inputs. Behavior changes follow [CHANGE.md](../templates/CHANGE.md) and invalidate affected evidence.
