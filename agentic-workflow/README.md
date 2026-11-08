# Agentic Workflow

Agentic Workflow is a copy-in package of instructions, templates and local helpers
for specification-driven implementation. The workflow, role boundaries and
acceptance rules start at [AGENTS.md](AGENTS.md). Installing it selects no app,
stack or automated runner.

## Install

- Context: start at [AGENTS.md](AGENTS.md) for role boundaries and acceptance rules.
- Inputs: an existing project and the complete `agentic-workflow/` directory; no installer, Git history or source-repository Makefile is needed.
- Effects: copy the package into the project's root. Merge the block below into the project's root `AGENTS.md`, retaining its existing instructions and the markers so integration checks inspect only this block. Optionally install the skill wrappers listed below.
- Outputs: an installed package and root entry points, with any selected optional skills.
- Next: run the [portable checks](#requirements-and-portable-commands).

```markdown
<!-- agentic-workflow:start -->
# Agentic Workflow

- Before planning, changing or reviewing code, tests or tooling, read
  [Engineering guidelines](agentic-workflow/policies/GUIDELINES.md).
- For specification implementation, read
  [Workflow entry points](agentic-workflow/AGENTS.md) and act as Supervisor.
- For document authoring or workflow maintenance, read those entry points
  and act as Planner.
- Before authoring or editing documents,
  read [Document style](agentic-workflow/policies/DOCUMENT_STYLE.md), regardless of role.
- Ordinary planning and implementation follows
  [Project memory](agentic-workflow/policies/MEMORY.md); implement ordinary work directly.
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
capabilities under [model routing](policies/MODELS.md) and [Checks](policies/CHECKS.md).

## Update the package

- Context: use the ownership boundary below.
- Inputs: replacement package and installed optional wrappers.
- Effects: replace `agentic-workflow/` in full, refresh each installed skill wrapper and check the root block.
- Outputs: updated package and wrappers, preserving project-owned customizations and execution records.
- Next: run the [portable checks](#requirements-and-portable-commands).

## Ownership

Apply when installing, customizing or updating the package.

- Keep customizations in project-owned files outside the package, using the locations below.
- Keep `AGENTS.md`, `WORKFLOW.md` and `README.md` at the package root; use `roles/` for local role procedures, `policies/` for shared rules and `guides/` for operations. Retain `templates/`, `helpers/` and `tests/`.
- Preserve historical artifacts. Provide no old-name aliases, record conversion or legacy assignment-tag readers.

| Location | Owner and purpose |
|---|---|
| Root `AGENTS.md` | Project instructions plus the entry-point block |
| `specs/` | Project specification bundles |
| Application directories | Project code and dependencies |
| `.agents/memory/` | Project lessons under [Memory](policies/MEMORY.md) |
| `.agentic-workflow/MODELS.md` | Optional complete project routing replacement |
| `.agentic-workflow/NNN_name/` | Task documents, runs, native traces and reports |

To customize routing, copy [MODELS.md](policies/MODELS.md) to
`.agentic-workflow/MODELS.md` and edit the complete policy and tables there.
Apply its [routing-source policy](policies/MODELS.md#routing-source).

The source repository's evals, example specifications, generated apps, research,
Makefile and integration tests are development assets outside the copy boundary.

## Requirements and portable commands

Helpers require Python 3.10+ and a local POSIX filesystem with `fcntl`/`flock`.
They use the standard library. A browser is useful for the local trace viewer;
only its optional Perfetto UI needs internet. Capture, import and reporting workflows
are described in [Tracing](guides/TRACING.md). Missing telemetry
limits reports but does not block allocation or app acceptance. Windows support,
a package-manager installer, plugin publication and an automated runner are
outside this distribution.

### Check and operate

- Context: apply [Records](policies/RECORDS.md) for task/assignment conventions and [Tracing](guides/TRACING.md) for telemetry operation.
- Inputs: consuming project root and, for record operations, an implementation name or identified implementation/task. Quote paths containing spaces.
- Effects: run the applicable commands below from the project root. Use the actual path printed by allocation; its numeric prefix advances with each implementation. Stop the viewer with `Ctrl+C`.
- Outputs: package/link results, test evidence, allocated records or generated usage reports/dashboard, according to the selected command.

```sh
python3 agentic-workflow/helpers/check_package.py
python3 agentic-workflow/helpers/check_package.py --integration-root .
python3 -m unittest discover -s agentic-workflow/tests -v
python3 agentic-workflow/helpers/records.py allocate example
python3 agentic-workflow/helpers/usage_report.py .agentic-workflow/001_example
python3 agentic-workflow/helpers/trace_view.py .agentic-workflow/001_example --interval 5
```

Allocation accepts `--records-root "path with spaces"` for a different records location. To resume an
existing task, use `records.py resolve IMPLEMENTATION TASK`; the task must exist
under that implementation's `tasks/`.

The default checker validates only the copied package and its local links. The
integration option also validates the marked root block and whichever of the
three optional skills are installed. It ignores other host instructions and
skills. Package tests run without a root Makefile; optional real-browser and
Perfetto processor checks report skips when their tools are unavailable.

### Source-repository checks

- Context: use these development conveniences in the source repository; package tests also run without its Makefile.
- Inputs: source checkout, installed tools and the changes to verify.
- Effects: run `python3 -m unittest discover -s tests -v` for copy-in integration checks and `python3 -m unittest discover -s evals/tests -v` for the eval launcher. Use `make trace IMPL=PATH` only with an explicit implementation path.
- Outputs: integration and eval fixture results, with any unavailable checks disclosed.

## Example use

- Context: follow [workflow entry points](AGENTS.md); explicit plan-only or approval requirements still apply.
- Inputs: project brief or ordinary change request.
- Effects: ask the agent to author a specification bundle using [the project template](templates/project.md), then request `Implement specs/example` for authorized execution through [Supervisor](roles/SUPERVISOR.md). Implement ordinary changes directly under [Guidelines](policies/GUIDELINES.md) and [Memory](policies/MEMORY.md).
- Outputs: authored documents or authorized implementation results.

## Distribution license

A public release needs an owner-selected distribution license. This package does
not select one on the owner's behalf; include it before publishing a release.
