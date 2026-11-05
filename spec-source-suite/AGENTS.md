# Agent instructions — Spec Source Suite

This directory is reusable guidance, not an app specification. Keep project inputs, implementation, and run evidence outside it.

Read [the shared contract](docs/SUITE_CONTRACT.md) first. It is the single authority for approvals, task persistence, roles, frozen checks, DAG readiness, repair limits, isolation, and completion.

- Author app documents or define/revise behavior: read [spec-define](.agents/skills/spec-define/SKILL.md) and [Define](docs/DEFINE.md).
- Implement an approved app capability or assess an app candidate: read [spec-implement](.agents/skills/spec-implement/SKILL.md) and [Implement](docs/IMPLEMENT.md).
- Generate initial/incremental work: read [spec-generate](.agents/skills/spec-generate/SKILL.md), [Generate](docs/GENERATE.md), and Implement.
- Regenerate or change targets through reconstruction: additionally read [Regeneration](docs/REGENERATION.md).
- Apply required enforced isolation: read [Strong isolation](docs/STRONG_ISOLATION.md).
- Build automated suite tooling only when explicitly requested: read [CODEX_START](CODEX_START.md) and [BUILD_THE_SUITE](docs/BUILD_THE_SUITE.md).

Route by deliverable: executing a documentation plan stays in Define. Use its document-completion gate; app execution and its candidate-review gates require their own authorization.

For suite guidance changes, follow the user's approved task acceptance, preserve existing repository instructions, and validate references, metadata, and package checksums. Report procedural walkthroughs separately from actual app-generation experiments.
