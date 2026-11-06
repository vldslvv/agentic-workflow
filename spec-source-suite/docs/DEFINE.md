# Define — documents and ready-task planning

Read [shared contract](SUITE_CONTRACT.md), [planning records](PLANNING.md) and [bundle format](MARKDOWN_BUNDLES.md). For app execution the supervisor performs this procedure for each ready task in its existing context. Scope determines the completion gate; writing future implementation steps does not execute them.

## D1. Resolve authority and scope

Use current user intent/selected sources and accepted dependency contracts. Preserve source provenance and explicit constraints; resolve unspecified implementation choices with simple recorded defaults under contract §1. Material contradictions require a decision. Keep discovery within current scope and stop when authoritative inputs are resolved.

For ordinary planning, select relevant notes through [project memory — starting inputs](PROJECT_MEMORY.md#starting-and-retaining-inputs); regeneration planning follows its exclusion boundary.

## D2. Define acceptance and boundaries

For new authorized authoring use the [bundle templates](../templates/bundle/project.md); preserve existing approved bundles in place. Map current task clauses/digests to stable requirement IDs and prerequisites using [acceptance](../templates/ACCEPTANCE.md). Cover applicable normal, boundary, error and interaction behavior. Shared constraints belong in project.md, shared/final scenarios in verification.md. Validate references and the derived graph.

## D3. Prepare scoped plan/checks

Use [plan](../templates/PLAN.md) for implementation approach, interfaces, dependency identities, ownership and integration. For documentation-only scope describe future checks without creating app environments/executables. For authorized handoff scope author task checks, declared regression set and applicable manual criteria with explicit pass rules. Reference shared scenarios instead of copying them; final scenarios stay separate. Freeze executable checks and all normative inputs before implementation.

## D4. Persist and hand off

Apply [planning-record](PLANNING.md) authority/persistence rules. Derived handoffs under a supplied implementation request need no extra approval prompt; exact explicitly approved text stays unchanged. Record a compact [receipt](../templates/RECEIPT.json) with paths/digests, readiness and unresolved decisions; return it when planning was delegated. Supply separate implementer/reviewer manifests, retaining reviewer exclusions.

Retain selected [memory inputs](PROJECT_MEMORY.md#starting-and-retaining-inputs) before freezing handoffs. When this completes the requested task, apply [memory maintenance](PROJECT_MEMORY.md#completing-and-maintaining).

**Document-completion gate:** requested documents saved/authorized with baseline and digests; consistency, coverage, references, graph and verification descriptions validated. No app candidate, execution or implementation review is required. Report generation readiness separately.

**Implementation-handoff gate:** document gate plus all prescribed available executable/manual checks and frozen inventory. Implementation must be authorized; an existing direct implementation request already supplies authority. Changes follow [CHANGE](../templates/CHANGE.md). Later reviewer reproductions follow contract §4's additive revision policy.
