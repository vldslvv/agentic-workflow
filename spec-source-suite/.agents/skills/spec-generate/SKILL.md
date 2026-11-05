---
name: spec-generate
description: Generate a project from approved specifications, update it incrementally, or run same-target or cross-target regeneration. Use only for an explicitly requested generation scope; never delete working source or invent project specs.
---

# Generate from specifications

Read the repository `AGENTS.md`, [shared contract](../../../docs/SUITE_CONTRACT.md), and [Generate workflow](../../../docs/GENERATE.md). Use `spec-implement` for the scoped worker loop rather than creating a second implementation procedure.

## Inputs

Require a filled project manifest, approved spec bundle, target profile, verification baseline, selected scope/mode, retained input policy, and authorized workspace. No project specs means NO_PROJECT.

## Procedure

1. Resolve the requested mode: initial, incremental, regenerate, or cross-target. Distinguish ordinary porting with old-code access from clean-room generation.
2. Freeze behavior/acceptance and input identities. Resolve prerequisite closure, retained boundaries, and downstream integration checks.
3. Prepare a new workspace where the mode requires it. Export only allowlisted inputs and record actual content digests. Do not delete or copy the old implementation into a clean-room scope.
4. Apply available filesystem, history, session/memory, network, and verifier controls. If controls cannot be enforced, label the run procedural or blocked according to its required policy.
5. Schedule ready spec nodes, serially by default. Use fresh implementation/review sessions and external run state. Respect prerequisites even when applying resume or scope controls.
6. Run project-level acceptance through the protected verifier. Keep the behavior baseline fixed on a technology switch; separately approve and validate any adapter change.
7. Preserve first-attempt results and any repairs. Report actual conformance, scope, retained dependencies, and isolation separately.

## Outputs

Produce a generated workspace, input manifest, node-level evidence, combined acceptance results, and [run report](../../../templates/RUN_REPORT.md). Do not claim enforced clean-room regeneration from prompts alone or real regeneration from stub-worker tests.
