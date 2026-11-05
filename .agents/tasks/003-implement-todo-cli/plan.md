# Implement the specified TODO CLI

Implement the user's request, “Implement the specifications for this app here: specs”, against the exact existing TODO-CLI specification. This operational plan records the authorized work; it does not alter behavior or replace the earlier documentation plan.

## Scope and approach

- Select TODO-R001–TODO-R012 from `.agents/tasks/002-todo-cli/acceptance.md`, version 0.1. One subsystem, no dependency edges, retained inputs, services, or assets.
- Use the specified Linux / CPython 3.14 / uv target. Create the application in `app/`, using standard-library application code, a declared console entry point, and a versioned `uv.lock`. Internal module layout and build backend are delegated by the existing target.
- Implement strict argument and checklist parsing, immutable task values, six command operations, and atomic same-directory replacement. Preserve file bytes on read-only operations, failures, and no-ops. Keep storage paths relative to caller cwd.
- Prepare executable black-box checks C01–C12 before implementation. Exercise the installed console script through uv, fresh processes, isolated disposable fixtures, real permission failures, and network namespaces. Freeze their content and all normative inputs. C12 also tests the assembled application.
- Dispatch a fresh implementer with candidate ownership limited to `app/` and its logs. The implementer spawns a fresh reviewer without this plan or conversation, as required by the suite. The reviewer executes all checks, inspects coverage and atomic replacement, and owns review evidence.
- Allow candidate 0 plus at most two implementation repairs. Escalate specification/verifier/infrastructure issues instead of altering frozen expectations. Accept only after mandatory checks, independent review, assembled C12, and input/candidate integrity pass.

## Ownership and execution

Planner/supervisor owns this task, the manifest/target execution registrations, frozen checks and inventory, and the top-level run report. Original task 002 documents remain byte-for-byte intact. Implementation owns `app/` and `.suite/runs/003-implement-todo-cli/implementer/`. Reviewers own their numbered reviewer directories. Isolation is procedural, not an enforced write sandbox.

Prepare with `uv sync --locked --project app`. Run checks with `python3 .suite/runs/003-implement-todo-cli/checks/acceptance.py --app app --evidence <owned-output-directory>`; use `--only C12` for separate assembled-app execution. Checks invoke `uv run --offline --no-sync --project <absolute-app> todo ...`. C01 additionally uses `unshare -Urn` and proves external networking is unavailable. Fixtures are removed after raw command, output, and byte evidence is saved.

Initial baseline: `3650ded7aaadf073631a091eadf37cfefc3e81c0`. The current implementation instruction authorizes preparing the missing handoff and app generation. No domain, stack, deployment, or behavior choices beyond the supplied bundle are introduced.
