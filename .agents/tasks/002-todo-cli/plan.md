# Prepare the TODO CLI generation documents

## Goal

Produce an approved documentation bundle that a later generation task can use to build the TODO CLI through spec-source-suite.

This task creates documents only. It does not create application code, executable tests, environments, or generation-run evidence.

## Documents to produce

- **Task documents** under `.agents/tasks/002-todo-cli/`: this documentation-only `plan.md`, the authoritative app `acceptance.md`, and an approval record binding their exact contents to the user’s approval and repository baseline.
- **Project bundle** under `specs/`: a concise brief, `project.yaml`, a target profile, and an implementation-order document. The manifest must reference the task’s acceptance document directly, without duplicating requirements.
- Record the current Git baseline and the working-guidance digests, preserving existing staged changes.

## Specification content

Carry forward the agreed TODO contract into acceptance requirements with stable IDs:

- Six noninteractive subcommands: add, list, complete, reopen, edit, and delete. Every task operation requires an explicit file path.
- An editable UTF-8 checklist containing unique positive numeric IDs, task text, and completion markers. Preserve the agreed syntax, text validation, newline handling, and malformed-file rejection rules.
- Allocate IDs from the current maximum plus one. Preserve file order and support listing by completion status.
- Treat missing files as empty; only add creates a file, and parent directories must already exist.
- Make repeated state changes successful no-ops. Preserve existing bytes on errors and no-ops; normalize formatting on actual changes.
- Use the agreed plain output and exit-code conventions. Require atomic persistence under a single-writer assumption.
- Target Linux and Python 3.14 through uv, with dependencies declared in `pyproject.toml`, a locked project in `app/`, and offline task operations after preparation.

For each requirement, document concrete verification inputs, expected outputs and side effects, failure cases, cleanup, and required evidence. Describe checks without implementing or executing them.

## Future implementation order

Document one subsystem, `TODO-CLI`, with no dependencies, and the following future sequence:

1. Prepare executable acceptance checks from the approved requirements and freeze the complete handoff inputs.
2. Generate the uv application within its authorized output paths.
3. Execute acceptance checks and obtain fresh-context independent review.
4. Apply the suite’s bounded repair process when necessary.
5. Complete assembled-app acceptance and report actual evidence.
6. Conduct the separate user walkthrough and propose workflow improvements from the trial.

This sequence is documentation for later work; none of its execution steps is authorized by this task.

## Document validation and completion

Review the bundle for consistent terminology, complete behavioral coverage, valid references, target compatibility, and an acyclic dependency graph. Confirm that every agreed requirement has a documented verification method.

Present the complete documents for approval. Save approved text exactly when editing is available, with digest-bound approval records. Leave suite guidance unchanged.

The task is complete when the documentation is approved, saved, and internally consistent. **Generation readiness remains blocked until executable checks are prepared and frozen in a separately authorized phase.** Do not claim the suite’s full Define handoff or app acceptance has completed.
