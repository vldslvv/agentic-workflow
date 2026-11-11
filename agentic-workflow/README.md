# Agentic Workflow

Copy-in instructions, templates and local helpers for specification-driven
implementation.

## References:

- [AGENTS]: Routes actions to role instructions and shared policies. agentic-workflow/AGENTS.md
- [MODELS]: Provides heuristics for choosing subagent models. agentic-workflow/policies/MODELS.md
- [CHECKS]: Defines acceptance criteria, independent checks and evidence rules. agentic-workflow/policies/CHECKS.md
- [TRACING]: Explains native capture, trace inspection and usage reporting. agentic-workflow/guides/TRACING.md
- [MEMORY]: Defines how to read and maintain project lessons. agentic-workflow/policies/MEMORY.md
- [RECORDS]: Defines execution records, assignments and handoffs. agentic-workflow/policies/RECORDS.md
- [PROJECT_TEMPLATE]: Structures project intent, constraints and output paths. agentic-workflow/templates/project.md
- [SUPERVISOR]: Coordinates implementation, recovery and acceptance. agentic-workflow/roles/SUPERVISOR.md
- [GUIDELINES]: Defines engineering rules for code, tests and tooling. agentic-workflow/policies/GUIDELINES.md

## Install

Start at [AGENTS] for roles and acceptance rules.

Copy the complete `agentic-workflow/` directory into an existing project root.
Merge this block into the root `AGENTS.md`, preserving existing instructions and
both markers; integration checks inspect only the marked block.

```markdown
<!-- agentic-workflow:start -->
# Agentic Workflow

Apply shared engineering and workflow instructions to project work.

## References:

- [GUIDELINES]: Defines engineering rules for code, tests and tooling. agentic-workflow/policies/GUIDELINES.md
- [AGENTS]: Routes actions to role instructions and shared policies. agentic-workflow/AGENTS.md
- [DOCUMENT_STYLE]: Defines document structure and reference conventions. agentic-workflow/policies/DOCUMENT_STYLE.md
- [MEMORY]: Defines how to read and maintain project lessons. agentic-workflow/policies/MEMORY.md

## Instructions

- Before planning, changing or reviewing code, tests or tooling, read
  [GUIDELINES].
- For specification implementation, read
  [AGENTS] and act as Supervisor.
- For document authoring or workflow maintenance, read those entry points
  and act as Planner.
- Before authoring or editing project documents,
  read [DOCUMENT_STYLE], regardless of role.
- Ordinary planning and implementation follows
  [MEMORY]; implement ordinary work directly.
- Keep project inputs, application code, memory and execution evidence
  outside `agentic-workflow/`.
<!-- agentic-workflow:end -->
```

Optionally copy these source-repository directories to the same project paths
and invoke the wrappers explicitly:

| Directory | Invocation |
|---|---|
| `.agents/skills/agentic-workflow-planner/` | `$agentic-workflow-planner` |
| `.agents/skills/agentic-workflow-supervisor/` | `$agentic-workflow-supervisor` |
| `.agents/skills/agentic-workflow-acceptance/` | `$agentic-workflow-acceptance` |

Direct role-file routing works without wrappers. Report unsupported host worker
isolation or settings under [CHECKS]. Run the [portable checks](#requirements-and-portable-commands)
after installation.

OpenCode 2.2.6 uses native session capture under [TRACING] (“Enable OpenCode capture”)
without a plugin; follow the update note there to remove the old V1 wrapper.

## Update the package

Replace `agentic-workflow/` in full, refresh installed wrappers, check the root
block and rerun portable checks. Preserve project-owned files and execution
history; provide no old-name aliases, record conversion or legacy assignment-tag
readers.

## Ownership

Keep customizations outside the package:

| Location | Purpose |
|---|---|
| Root `AGENTS.md` | Project instructions and entry-point block |
| `specs/` | Project specification bundles |
| Application directories | Project code and dependencies |
| `.agentic-workflow/memory/` | Project lessons under [MEMORY] |
| `.agentic-workflow/config/MODELS.md` | Project model-selection overrides |
| `.agentic-workflow/records/NNN_name/` | Tasks, runs, native traces and reports |

To customize model choices, copy [MODELS] to the path above and edit its heuristics.

Retain the package layout: root `AGENTS.md`, `GLOSSARY.md`, `WORKFLOW.md` and `README.md`, plus
`roles/`, `contracts/`, `policies/`, `guides/`, `templates/`, `helpers/` and `tests/`.
Workflow data contracts describe handoff fields; application interface contracts remain in specification bundles.
Source-repository evals, example specs, generated apps, research, Makefile and
integration tests stay outside the copy boundary.

Tracing code lives under `helpers/tracing/`: `registry.py` selects providers,
`codex/` and `opencode/` own native capture and interpretation, and `shared/`
contains normalized types, filesystem utilities, assignments, enrichment,
accounting, timelines and presentation. Commands use this package; providers
import only their own modules and shared utilities, and shared modules never
import providers or commands. The package checker enforces these boundaries.

## Requirements and portable commands

Helpers use the Python 3.11+ standard library and require a local POSIX filesystem
with `fcntl`/`flock`. Copy-in use needs no uv, pip, repository configuration or
third-party typing libraries. The trace viewer uses a browser; only its optional Perfetto
UI needs internet. The package includes no app stack, automated runner, Windows
support, package-manager installer or plugin publication.

### Check and operate

Run from the consuming project root. Consult command `--help`, including
`records.py allocate --help` and `records.py resolve --help`, for usage and
lifecycle instructions. Follow [RECORDS] for task conventions
and [TRACING] for capture, imports and reports.

```sh
python3 agentic-workflow/helpers/check_package.py
python3 agentic-workflow/helpers/check_package.py --integration-root .
python3 -m unittest discover -s agentic-workflow/tests -v
python3 agentic-workflow/helpers/records.py allocate example
python3 agentic-workflow/helpers/usage_report.py .agentic-workflow/records/001_example
python3 agentic-workflow/helpers/trace_view.py .agentic-workflow/records/001_example --interval 5
```

Use the actual path printed by allocation; each call advances the numeric prefix.
Quote paths containing spaces. Stop the viewer with `Ctrl+C`. Missing telemetry
limits reports but does not block allocation or app acceptance. Conflicting
native session identities fail before writes; see [TRACING] for detection.
Reporting and viewing detect the tracing provider from saved native evidence,
independently of the current agent shell, and route explicitly to it internally.
There is no provider option. Missing, unreadable, invalid or mixed-provider evidence
fails before writes or viewer startup. Only the detected provider's evidence is
refreshed; report filenames stay the same.

The checker validates the package, local links and every Python import, including
conditional, function-local and literal dynamic imports. Imports must resolve to
the standard library or copied package modules; computed import targets fail.
Run it with the interpreter that will execute the helpers. `--integration-root` adds the
marked root block and installed workflow wrappers, ignoring other host
instructions and skills. Tests need no source Makefile; optional browser and
Perfetto checks skip when their tools are unavailable.

### Source-repository checks

```sh
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s evals/tests -v
make trace IMPL=PATH
```

These run copy-in integration checks, eval fixtures and a viewer for an explicit
implementation, respectively. The source repository also provides `make check`,
`make test` and `make check-portability`; the latter checks the package and all
behavior suites on Python 3.11 and 3.15. Development configuration stays at the
repository root and is not part of the copied package.

## Example use

Ask the agent to author a specification bundle using the
[PROJECT_TEMPLATE], then request `Implement specs/example`
for execution through [SUPERVISOR]. Ordinary changes follow
[GUIDELINES] and [MEMORY] directly.
Preserve explicit plan-only and approval requirements.

## Distribution license

Include an owner-selected distribution license before a public release.
