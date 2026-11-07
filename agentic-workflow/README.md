# Agentic Workflow

Agentic Workflow is a copy-in package of instructions, templates and local helpers
for specification-driven implementation. The workflow, role boundaries and
acceptance rules start at [AGENTS.md](AGENTS.md). Installing it selects no app,
stack or automated runner.

## Install

Copy the entire `agentic-workflow/` directory into an existing project's root.
No installer, Git history or source-repository Makefile is needed. Merge this block
into the project's root `AGENTS.md`, retaining its existing instructions. Keep the
markers so integration checks inspect only this block.

```markdown
<!-- agentic-workflow:start -->
# Agentic Workflow

- Before planning, changing or reviewing code, tests or tooling, read
  [Engineering guidelines](agentic-workflow/GUIDELINES.md).
- For specification implementation, read
  [Workflow entry points](agentic-workflow/AGENTS.md) and act as Supervisor.
- For document authoring or workflow maintenance, read those entry points
  and act as Planner.
- Ordinary planning and implementation follows
  [Project memory](agentic-workflow/MEMORY.md); implement ordinary work directly.
- Keep project inputs, application code, memory and execution evidence
  outside `agentic-workflow/`.
<!-- agentic-workflow:end -->
```

Optionally copy any of these directories from the source repository into the same
path in your project. Each wrapper uses the package's authoritative documents:

- `.agents/skills/agentic-workflow-planner/`
- `.agents/skills/agentic-workflow-supervisor/`
- `.agents/skills/agentic-workflow-acceptance/`

Invoke them explicitly with `$agentic-workflow-planner`,
`$agentic-workflow-supervisor` or `$agentic-workflow-acceptance`. Skills remain
optional; direct role-file routing works without them. Use an agent host that
supports the required worker isolation and settings, or report unsupported
capabilities under [model routing](MODELS.md) and [Checks](CHECKS.md).

## Ownership and updates

The shipped version is in [VERSION](VERSION). Replace `agentic-workflow/` in full
when updating, then refresh each installed skill wrapper and check the root block.
Keep customizations in project-owned files outside the package:

| Location | Owner and purpose |
|---|---|
| Root `AGENTS.md` | Project instructions plus the entry-point block |
| `specs/` | Project specification bundles |
| Application directories | Project code and dependencies |
| `.agents/memory/` | Project lessons under [Memory](MEMORY.md) |
| `.agentic-workflow/MODELS.md` | Optional complete project routing replacement |
| `.agentic-workflow/NNN_name/` | Task documents, runs, native traces and reports |

To customize routing, copy [MODELS.md](MODELS.md) to
`.agentic-workflow/MODELS.md` and edit the complete policy and tables there.
Agents and the eval launcher use that file when present, otherwise the packaged
default. Package replacement preserves the override and execution records.

The source repository's evals, example specifications, generated apps, research,
Makefile and integration tests are development assets; they are outside the copy
boundary. Historical artifacts stay unchanged. No old-name aliases, record
conversion or legacy assignment-tag readers are provided.

In the source repository, run `python3 -m unittest discover -s tests -v` for
copy-in integration checks and `python3 -m unittest discover -s evals/tests -v`
for the eval launcher. Root Makefile targets are development conveniences;
`make trace IMPL=PATH` requires an explicit implementation path.

## Requirements and portable commands

Helpers require Python 3.10+ and a local POSIX filesystem with `fcntl`/`flock`.
They use the standard library. A browser is useful for the local trace viewer;
only its optional Perfetto UI needs internet. Native telemetry availability and
pinned formats are described in [Tracing](helpers/TRACING.md). Missing telemetry
limits reports but does not block allocation or app acceptance. Windows support,
a package-manager installer, plugin publication and an automated runner are
outside this distribution.

Run these from the consuming project's root; quote paths containing spaces:

```sh
python3 agentic-workflow/helpers/check_package.py
python3 agentic-workflow/helpers/check_package.py --integration-root .
python3 -m unittest discover -s agentic-workflow/tests -v
python3 agentic-workflow/helpers/records.py allocate example
python3 agentic-workflow/helpers/usage_report.py .agentic-workflow/001_example
python3 agentic-workflow/helpers/trace_view.py .agentic-workflow/001_example --interval 5
```

Use the actual path printed by allocation; its numeric prefix advances with each
implementation. The viewer runs until `Ctrl+C`. Allocation accepts
`--records-root "path with spaces"` for a different records location. To resume an
existing task, use `records.py resolve IMPLEMENTATION TASK`; the task must exist
under that implementation's `tasks/`. Task and assignment conventions are in
[Records](RECORDS.md). Assignments use the `AGENTIC_WORKFLOW` tag prefix.

The default checker validates only the copied package and its local links. The
integration option also validates the marked root block and whichever of the
three optional skills are installed. It ignores other host instructions and
skills. Package tests run without a root Makefile; optional real-browser and
Perfetto processor checks report skips when their tools are unavailable.

## Example use

Ask the agent to author a specification bundle using
[the project template](templates/project.md), then request `Implement specs/example`
for authorized execution through [Supervisor](SUPERVISOR.md). Ordinary changes
can be implemented directly under [Guidelines](GUIDELINES.md) and
[Memory](MEMORY.md). Explicit plan-only or approval requirements still apply.

## Distribution license

A public release needs an owner-selected distribution license. This package does
not select one on the owner's behalf; include it before publishing a release.
