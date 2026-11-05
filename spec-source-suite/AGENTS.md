# Agent instructions — Spec Source Suite

This repository defines a reusable development workflow. It is not a preselected application.

## Route the work

- To define or revise project behavior, use `spec-define` and `docs/DEFINE.md`.
- To implement an approved capability and assess alignment, use `spec-implement` and `docs/IMPLEMENT.md`.
- To generate a project, regenerate a scope, or switch technologies, use `spec-generate` and `docs/GENERATE.md`.
- To implement the suite itself, follow `CODEX_START.md` and `docs/BUILD_THE_SUITE.md`. Do not invent a demonstration product.

Read `docs/SUITE_CONTRACT.md` before a workflow. It defines common terms, authority, evidence, and failure handling.

## Non-negotiable boundaries

1. Project specs and their explicit acceptance clauses are authoritative. Tasks and implementation plans are not requirements.
2. Do not choose a project domain, technology stack, or deployment model when the user has not supplied or delegated it.
3. Missing project specifications yield NO_PROJECT. Missing execution inputs yield BLOCKED. Neither is a pass.
4. Do not change frozen requirements, fixtures, verifier assertions, or thresholds to make an implementation pass. Propose a change and obtain the designated approval first.
5. Keep acceptance evidence traceable to requirement IDs and actual executed checks. Never fabricate execution, another agent, review independence, isolation, or approval.
6. Use a fresh session for independent review. A role change inside the implementation conversation is self-review, not independent review.
7. Preserve a neutral boundary between workflow tooling and project adapters. Keep run state, scheduling, budget, retries, and resume decisions outside worker memory.
8. Default to serial execution. Parallelize only DAG-ready work with isolated writes and explicit integration gates.
9. Do not delete the working implementation to test regeneration. Use a new workspace and explicit input allowlist. Instructions alone do not enforce a sandbox.
10. Add tests that establish requirements or catch meaningful regressions; do not produce large numbers of overlapping tests without a verification purpose.
11. Do not treat this repository's templates as completed specs. Unresolved required values block approval or execution at the corresponding gate.
12. Retain required data, assets, schemas, and external contracts separately from disposable code. Regenerating code does not recreate lost production state or unavailable third-party services.

When merging these instructions into an existing project, preserve applicable existing guidance. Changes to the suite's own policy must be explicit; they must not be incidental side effects of implementing a project feature.
