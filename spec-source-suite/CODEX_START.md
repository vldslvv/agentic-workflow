# Codex assignment: implement a generic spec-source suite

## Objective

Build a reusable suite with three capabilities:

1. Define and maintain specification documents that also serve as acceptance documents.
2. Implement selected specifications, independently review alignment, and execute acceptance checks.
3. Generate or regenerate an implementation from the approved specification bundle, including a different target technology when requested.

The user will supply their own project specifications later. **Do not build a sample application. Do not select a business domain. Do not preselect the generated project's language, framework, database, or interface style.**

## Start here

Read `AGENTS.md`, `docs/SUITE_CONTRACT.md`, the three workflow documents, and `docs/BUILD_THE_SUITE.md`. Treat BUILD_THE_SUITE as the acceptance specification for the tooling you are building. Reuse the provided skills, prompts, and templates; improve their consistency through explicit edits rather than creating a competing methodology.

First inventory the existing repository and available worker execution tools. Reuse repository conventions. In an otherwise empty repository, choosing a lightweight language for the **suite's own tooling** is permitted; record that choice and do not propagate it as a generated-project requirement. Do not claim a particular external agent CLI supports a flag without checking its installed help or current official documentation.

## Delivery sequence

### Milestone 1 — Usable file-based workflows

Make Define, Implement, and Generate usable through the existing instruction-only skills and templates. Validate template metadata, required fields, references, and dependencies. Provide documented manual handoff when an external worker cannot be launched. Record manual operations as manual.

### Milestone 2 — Thin supervisor

Implement manifest loading, spec validation, ready-node calculation, job preparation, worker adapters, fresh review, verification dispatch, and evidence records. Start with serial execution. Make state and resume decisions independent of agent conversations. Every selected task must reference an approved specification and acceptance IDs.

### Milestone 3 — Generation and isolation boundary

Implement first-generation, incremental, same-target regeneration, and cross-target regeneration modes. Use a new workspace for clean-room modes, explicit input export, input digests, and a separate verifier interface. Report the actual isolation level. Do not claim enforced clean-room regeneration when using only instructions or manual copying.

### Milestone 4 — Generic suite acceptance

Execute the BUILD_THE_SUITE acceptance cases using synthetic structural fixtures, stub workers, and fake verifiers. Those fixtures may contain abstract identifiers and inert files; they are not an example product and do not select a project stack. Demonstrate a missing-project stop, dependency sequencing, genuine verification failures, safe resume, and exclusion of sentinel implementation artifacts.

## Keep the initial scope small

Do not add a web dashboard, hosted service, database-backed control plane, distributed queue, plugin marketplace, or multi-agent debate system. Do not require a particular specification DSL. Markdown plus a small manifest is the baseline. Use an adapter interface where project-specific build/run/check behavior belongs.

Do not assume an external paid API is available. Provide a worker adapter interface and an explicit manual fallback. A stub worker can test the supervisor, but cannot count as an actual agent reconstruction experiment.

## Required final report

Report which suite requirements pass, which are blocked, which are untested, and the evidence paths. State separately whether any real project was supplied and whether any real generation was attempted. A functioning supervisor with synthetic fixtures demonstrates workflow mechanics, not behavior-preserving reconstruction of a real project.

If no user project has been supplied, finish with a usable empty suite and instructions for adding one. Do not fill the empty project slots yourself.
