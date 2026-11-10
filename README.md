# Agentic Workflow

A minimal and opinionated agentic workflow.

This repository provides copy-in instructions, specification templates and local
helpers for agents working on software projects. The workflow connects component
specifications to implementation, independent review and assembled-app validation.

## Structure

The portable package lives in [`agentic-workflow/`](agentic-workflow/README.md).

| Path | Purpose |
|---|---|
| [`AGENTS.md`](agentic-workflow/AGENTS.md) | Entry points and required context for each action |
| [`WORKFLOW.md`](agentic-workflow/WORKFLOW.md) | Authoritative workflow behavior and outcomes |
| [`roles/`](agentic-workflow/roles/) | Responsibilities and procedures for each role |
| [`policies/`](agentic-workflow/policies/) | Shared rules for specifications, engineering, checks, records and model routing |
| [`guides/`](agentic-workflow/guides/) | Workflow document review and trace inspection |
| [`templates/`](agentic-workflow/templates/) | Specification and execution document formats |
| [`helpers/`](agentic-workflow/helpers/) | Package checks, record allocation, trace capture and usage reports |
| [`tests/`](agentic-workflow/tests/) | Portable package tests |

The repository also contains optional role wrappers in `.agents/skills/`, example
bundles in `specs/`, applications in `apps/`, evaluation tooling in `evals/` and
integration tests in `tests/`.

## Roles

Each role has a focused responsibility within the [workflow](agentic-workflow/WORKFLOW.md).

| Role | Responsibility | Output |
|---|---|---|
| [Planner](agentic-workflow/roles/PLANNER.md) | Author requested documents and check their consistency | Documents, validity assessment and generation readiness |
| [Supervisor](agentic-workflow/roles/SUPERVISOR.md) | Resolve specifications, coordinate tasks and accept results | Execution state, accepted work or blockers |
| [Implementer](agentic-workflow/roles/IMPLEMENTER.md) | Implement an assigned task and check its behavior | Candidate implementation, evidence and task result |
| [Reviewer](agentic-workflow/roles/REVIEWER.md) | Independently assess a task against requirements and acceptance | Findings and review result |
| [Validator](agentic-workflow/roles/VALIDATOR.md) | Check assembled-app scenarios and interactions | Final validation result and repair specifications when needed |

The Supervisor selects each task's mode under the
[task-mode policy](agentic-workflow/roles/SUPERVISOR.md#task-mode).
Plan-review mode includes a plan, separate acceptance criteria and independent
task review; direct mode uses source criteria without those separate documents
or task review. Both modes lead to assembled-app validation.

## Policies

Shared rules have their authoritative homes in these documents.

| Policy | Scope |
|---|---|
| [Guidelines](agentic-workflow/policies/GUIDELINES.md) | Engineering and testing principles |
| [Document style](agentic-workflow/policies/DOCUMENT_STYLE.md) | Document structure and writing rules |
| [Bundle](agentic-workflow/policies/BUNDLE.md) | Specification files, task boundaries, dependencies and authority |
| [Checks](agentic-workflow/policies/CHECKS.md) | Acceptance criteria, evidence and independent checks |
| [Records](agentic-workflow/policies/RECORDS.md) | Execution artifacts, handoffs and resumable work |
| [Memory](agentic-workflow/policies/MEMORY.md) | Project lessons for ordinary work |
| [Models](agentic-workflow/policies/MODELS.md) | Role routing and host settings |
| [Reconstruction](agentic-workflow/policies/RECONSTRUCTION.md) | Rebuilding without prior implementation context |

## Specification format

A specification bundle describes the project, its components and observable
acceptance outcomes. The [bundle policy](agentic-workflow/policies/BUNDLE.md)
defines how these files are resolved and used.

```text
specs/example/
├── project.md
├── task_order.md
├── tasks/
│   └── component.md
├── contracts/          # Optional shared interaction contracts
│   └── interaction.md
└── verification.md
```

| File and template | Contents |
|---|---|
| [`project.md`](agentic-workflow/templates/project.md) | Intent, users, shared constraints, environment, output path, persistence and unresolved decisions |
| [`task_order.md`](agentic-workflow/templates/task_order.md) | A `Task \| Depends on` table linking task files and declaring prerequisites |
| [`tasks/*.md`](agentic-workflow/templates/tasks/task.md) | Component responsibility, boundary, sources, provided and consumed contracts, behavior, constraints and acceptance scenarios |
| [`contracts/*.md`](agentic-workflow/templates/contracts/contract.md) | Participants, interfaces, semantics, guarantees and interaction examples |
| [`verification.md`](agentic-workflow/templates/verification.md) | Shared and assembled-app scenarios with sources, setup, actions, pass rules, cleanup and evidence |

The task template describes behavior through inputs, effects, outputs, state,
failures and invariants. Its acceptance table pairs each scenario with an
observable pass condition. Optional sections hold implementation suggestions and
workflow requirements.

Execution documents use separate templates:
[`plan.md`](agentic-workflow/templates/plan.md) records the approach and checks,
[`acceptance.md`](agentic-workflow/templates/acceptance.md) maps source requirements
and contracts to check scenarios, and
[`result.md`](agentic-workflow/templates/result.md) records outcomes, evidence,
findings and limits. Their storage locations follow
[Records](agentic-workflow/policies/RECORDS.md).

## Use

For installation, updates and supported commands, follow the
[package guide](agentic-workflow/README.md).

1. Copy the package and merge its entry-point block using the [installation instructions](agentic-workflow/README.md#install).
2. Ask the agent to author a bundle such as `specs/example/` using the templates.
3. Request `Implement specs/example` to start execution through the Supervisor.

Ordinary changes use [Guidelines](agentic-workflow/policies/GUIDELINES.md) and
[Memory](agentic-workflow/policies/MEMORY.md) directly, as described in the root
[AGENTS.md](AGENTS.md).

## Evals

The source repository includes local evaluations for workflow documents,
specification bundles and end-to-end implementation. They use Python 3.11+ on
POSIX and an authenticated local Codex CLI; todolist trials also require Git and uv.

| Evaluation | Inputs | Command | Effect |
|---|---|---|---|
| [Workflow review](evals/README.md#review-and-repair-workflow-documents) | Current workflow documents and entry points, including uncommitted changes | `make eval-workflow` | Review a snapshot; opt into one Markdown repair with `WORKFLOW_REPAIR=1` |
| [Specification review](evals/README.md#review-specification-bundles) | Current bundles under `specs/`, templates and applicable policies | `make eval-specs` | Report findings and suggested corrections without editing specifications |
| [Todolist end-to-end](evals/README.md#todolist-end-to-end-eval) | Committed `HEAD` in a clean temporary worktree | `make eval` | Generate an app, grade agent completion, CLI behavior and artifact presence, then archive the trial |

Reports and evidence are saved under `.agentic-workflow/evals/`. Optional workflow repair
retains edits for inspection; its `PASS` result includes no independent re-review.
Todolist artifact presence does not establish trace quality or workflow compliance.

Follow the [eval guide](evals/README.md) for prerequisites, model and timeout
settings, selecting a specification bundle, current-checkout trials and cleanup.

## Development and checks

Source development uses Python 3.11+ and uv. Configuration and locked development
dependencies live in root `pyproject.toml`, `uv.lock` and `.pre-commit-config.yaml`.
Runtime dependencies are empty; the copied package needs only the standard library.

```sh
uv sync --locked --python 3.11
make check
make test
uv run pre-commit run --all-files
uv python install 3.11 3.15
make check-portability
```

`make check` runs strict mypy, Ruff linting, 100-column formatting checks and the
package/integration checker across helpers, evals, tests and fixtures. Generated
apps, execution evidence, temporary worktrees and caches are outside that scope.
Pre-commit runs the same checks; install the hook with `uv run pre-commit install`.

`make test` runs package, copy-in installation and eval behavior suites.
`make check-portability` runs the package checker and all three suites on Python
3.11 and 3.15, using interpreters resolved by uv. Install those interpreters before
running the matrix. Optional browser and Perfetto checks skip when unavailable.
Live model evaluations remain separate from these fixture-based checks.

Override `PYTHON` with an interpreter path, `UV` with a uv executable, or
`PORTABILITY_PYTHONS` with a space-separated version list. Commands also work from
another directory using `make -f /path/to/agentic-workflow/Makefile check`.
The [package guide](agentic-workflow/README.md#requirements-and-portable-commands)
lists commands available after copying only the package.
