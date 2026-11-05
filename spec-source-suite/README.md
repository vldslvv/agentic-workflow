# Spec Source Suite

**Reusable workflows for defining specifications, implementing against acceptance criteria, and generating a project from those specifications.**

Version: 0.1-draft · Prepared: 2026-11-05

This package is a generic workflow suite, not a sample application. It contains instruction-only agent skills, operating documents, blank project templates, and an acceptance specification for optional automation. It contains no application implementation, selected business domain, language, framework, database, or deployment stack.

## The three capabilities

| Capability | Input | Output | Workflow |
|---|---|---|---|
| **Define** | Your intent, existing specifications, or explicitly authorized behavior observations | Reviewed specification/acceptance documents, requirement IDs, verification design, and a dependency DAG | [DEFINE](docs/DEFINE.md) |
| **Implement and align** | Approved specs, a target profile, and an implementation workspace | An implementation with requirement-linked review and acceptance evidence | [IMPLEMENT](docs/IMPLEMENT.md) |
| **Generate** | An approved project specification bundle, target profile, and scope | A new implementation plus evidence of conformance; optionally a clean-room or cross-technology regeneration result | [GENERATE](docs/GENERATE.md) |

**Define decides what must be built. Implement handles one accepted unit of work. Generate orchestrates Implement across a project or selected subgraph.** Regeneration is a controlled mode of Generate, not a second implementation methodology.

Each capability specification is also its acceptance document. Acceptance tests operationalize that document; they do not become an undocumented alternative source of requirements.

## Two ways to use this package

### Use the workflows with agents now

Keep this package intact in a repository. Start with [AGENTS.md](AGENTS.md), the shared [suite contract](docs/SUITE_CONTRACT.md), and the workflow you need. The three instruction-only skills are under `.agents/skills/`.

In Codex, invoke them explicitly:

```text
$spec-define Help me turn the project description I provide into specifications.
$spec-implement Implement the approved specification I select and verify alignment.
$spec-generate Generate the project from the approved specification bundle and target I select.
```

These are skill invocations, not installed shell commands. The skills coordinate work through available tools; they do not themselves provide a supervisor, sandbox, or verifier. Missing execution capabilities must be reported rather than simulated.

The folder and invocation conventions follow the official Codex documentation; see [sources](docs/SOURCES.md). When merging into an existing repository, preserve existing instructions and merge deliberately; do not overwrite an existing `AGENTS.md` or same-named skill.

### Have Codex implement the reusable tooling first

Give Codex [CODEX_START.md](CODEX_START.md). The implementation assignment is to build the generic suite, using [BUILD_THE_SUITE.md](docs/BUILD_THE_SUITE.md) as its acceptance specification. It is explicitly not an assignment to invent an application.

Start with file-based artifacts, a serial scheduler, fresh worker sessions, and manual execution fallback. Add automation only where repeatable execution or enforcement is needed. A workflow usable through files and agents is a valid first milestone.

## Insert your project later

Copy and complete [PROJECT.md](templates/PROJECT.md), [project.yaml](templates/project.yaml), and one or more [SPEC.md](templates/SPEC.md) files. Register their paths in the project manifest. Select a [target profile](templates/target.yaml) only when preparing implementation or generation. Define the independent verification arrangement with [VERIFICATION.md](templates/VERIFICATION.md).

A minimal project can have one capability specification. Add shared contracts, state models, schemas, data, or other artifacts only when its behavior requires them. Do not manufacture a DAG with unnecessary nodes merely to use the suite.

Templates deliberately contain unresolved values. They are scaffolding, not an approved project. No specifications means **NO_PROJECT**, not a successful empty generation run.

## What is durable, and what is replaceable?

Durable inputs are approved specifications, referenced contracts and required data/assets, acceptance definitions and verifier revisions, generation policy, and approved target constraints. Plans, source code, local unit tests, and build products are replaceable. Evidence and logs are retained for audit but are not automatically inputs to later clean-room generation.

Changing technologies may replace an implementation-specific test adapter, but must not silently change externally required behavior or acceptance thresholds.

## Reading order

Read the [shared contract](docs/SUITE_CONTRACT.md), then the selected workflow. Use the templates when creating project artifacts. Read the automation implementation brief only when building the suite's tooling.

No generation, application test, or clean-room experiment has been executed by this package. Its own structural validation is reported in `PACKAGE_CHECKS.json`.
