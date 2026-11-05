---
id: TODO-CLI
version: "0.1"
status: draft
title: Local TODO CLI
depends_on: []
shared_contracts: []
---

# Acceptance — todo-cli

**Baseline commit:** `72be4307b03fbd80b5fd163d851b5c46f02b5a31`
**Approval:** Pending final document review; see [approval.json](approval.json).
This document specifies the future app. Saving it authorizes no app implementation or check execution.

## Goal and boundary

Provide a local, offline TODO CLI that manages an editable text checklist. Each task has a numeric ID, text, and completion status.

The supported target is Linux with Python 3.14, managed through uv. The project lives in `app/`; dependencies are declared in `pyproject.toml`, with a committed `uv.lock`. Application code uses the standard library. Internal module layout and build backend are delegated within the [target profile](../../../specs/targets/linux-python-uv.yaml).

Excluded: interactive menus, multiple-list management commands, dates, priorities, tags, subtasks, synchronization, concurrent writers, and additional output formats.

## Public interface

From `app/`:

```text
uv run todo --file PATH add "TEXT"
uv run todo --file PATH list [--status open|done|all]
uv run todo --file PATH complete ID
uv run todo --file PATH reopen ID
uv run todo --file PATH edit ID "TEXT"
uv run todo --file PATH delete ID
```

From the repository root, use `uv run --project app todo …`. Relative task-file paths resolve against the caller’s current directory, not the project directory.

Task operations require `--file PATH`. Help succeeds without a file and does not access task storage.

## File contract

Examples:

```text
1 [ ] Buy milk
2 [x] Call Sam
```

Each record contains a positive ASCII decimal ID without leading zeros, one space, `[ ]` or lowercase `[x]`, one space, and task text.

- IDs must be unique.
- Text must be nonempty after trimming surrounding whitespace. Preserve internal spacing and Unicode characters.
- Reject control characters in Unicode category `Cc`, and line separators U+2028/U+2029, in task text. Validate these before trimming.
- Accept UTF-8 files with LF or CRLF line endings and an optional final newline.
- Ignore whitespace-only lines. Comments and other record syntax are invalid.
- A successful state-changing operation rewrites records in file order using UTF-8, LF, no blank lines, and a final newline. An empty list is represented by a zero-byte file.
- Read-only commands, failed commands, and successful no-ops preserve existing file bytes.

Line terminators delimit records and are not task text. Whitespace-only lines are ignored before record validation; text in actual records remains subject to control-character validation.

## Requirements and prescribed verification

All checks below are future checks against the actual CLI, not executed results. Each uses isolated temporary directories, captures command arguments, exit codes, stdout, stderr, and relevant before/after file bytes, then removes its fixtures. A check passes only when every listed assertion holds. Persist captured evidence before cleanup under the future run directory registered by the manifest.

| ID | Required behavior | Check and concrete scenarios |
|---|---|---|
| TODO-R001 | Provide the documented uv entry point and six subcommands on Linux/Python 3.14. Require an explicit file path for task operations. Prepared task operations work offline. | **C01:** Prepare the locked project; invoke help and all subcommands. Verify missing `--file` fails. Run operations without network access. Invoke from another working directory and verify relative paths select files there. |
| TODO-R002 | Parse the file contract exactly. One invalid record invalidates the entire file. | **C02:** Accept empty files, blank lines, Unicode text, LF/CRLF, and missing final newline. Reject malformed markers/separators, nonpositive or leading-zero IDs, duplicate IDs, empty text, forbidden controls, and invalid UTF-8. Errors identify the problem and line where applicable; no command partially processes or rewrites invalid data. |
| TODO-R003 | Add an open task at the end of file order. Assign one greater than the largest existing ID, or 1 for an empty list. Duplicate descriptions are allowed. | **C03:** Add to empty and populated files, including manually reordered and nonconsecutive IDs. Verify text normalization, status, position, persistence, duplicate descriptions, and reuse after deleting the highest ID. |
| TODO-R004 | List all tasks by default, in file order. Filter by `open`, `done`, or `all`. | **C04:** List mixed statuses and reordered IDs under every filter. Assert canonical checklist output, empty stdout for no matches, and unchanged file bytes. |
| TODO-R005 | Complete and reopen the selected ID, preserving its text, ID, and position. Repeating the current state succeeds without rewriting. | **C05:** Complete an open task and reopen a completed task. Repeat both operations against files containing noncanonical permitted formatting; assert successful no-ops preserve bytes. |
| TODO-R006 | Edit only the selected task’s text, preserving its status, ID, and position. Editing to the same normalized text is a successful no-op. | **C06:** Edit open and completed tasks, including Unicode and internal spaces. Verify unaffected task values and order. Reject invalid text without changing bytes; verify same-text edits preserve bytes. |
| TODO-R007 | Delete only the selected ID without confirmation or renumbering remaining tasks. | **C07:** Delete first, middle, highest-ID, and last remaining tasks. Verify retained IDs and order, output of the removed record, and a zero-byte file after the final deletion. |
| TODO-R008 | A missing file behaves as an empty list. Only add creates it, and its parent directory must already exist. | **C08:** List a missing file successfully without creating it. Fail mutations targeting absent IDs without creating it. Add creates the file; add with a missing parent fails without creating directories. |
| TODO-R009 | Unknown IDs fail. Invalid command syntax, IDs, status filters, or text are usage errors. | **C09:** Exercise unknown IDs for complete, reopen, edit, and delete; malformed CLI IDs; missing/extra arguments; unsupported commands/statuses; empty, multiline, and control-containing CLI text. Verify expected error class and unchanged storage. |
| TODO-R010 | List prints only matching canonical record lines. Successful mutations—including no-ops—print the affected record; delete prints the removed record. Success exits 0. | **C10:** Assert exact record output and trailing newlines for every operation, with no headings, colors, prompts, or summaries. Successful operations produce no application error output. |
| TODO-R011 | Data/filesystem errors exit 1; usage errors exit 2. Errors go to stderr, with no task output or traceback. Failed mutations leave existing task-file bytes unchanged. | **C11:** Test malformed data, unknown IDs, unreadable files, directory paths, and unwritable storage locations. Assert exit class, empty stdout, useful diagnostics, and byte preservation. Error wording may vary; diagnostics identify the offending argument, ID, or path, and malformed record line where applicable. |
| TODO-R012 | Persist state across independent processes using atomic replacement for state-changing writes. Assume one writer at a time. | **C12:** Run the complete lifecycle in separate invocations, interleave valid manual file edits, and verify subsequent commands observe them. Exercise write failure with an existing file and verify preservation. The independent reviewer also verifies atomic replacement on the actual candidate. |

Invalid text supplied as a CLI argument is a usage error; invalid text read from a file is a data error. CLI IDs follow the same positive-decimal syntax as stored IDs. Duplicate descriptions are distinct tasks identified by their IDs.

## Verification and project acceptance

- C01–C12 are mandatory. C12 is also the assembled-app lifecycle check: add, edit, complete, filtered list, reopen, delete, manual edits, and reading persisted state through fresh processes.
- Automated assertions determine observable behavior. Independent review additionally checks coverage and the atomic-write mechanism.
- Filesystem-failure checks require an environment that can enforce access restrictions. Offline checks require an arrangement that can demonstrate network unavailability. An unavailable required mechanism is a blocked check, not a pass.
- The reviewer executes checks independently against the identified candidate and records requirement-linked evidence. Frozen inputs must remain intact.
- Every mandatory check, independent-review finding, assembled-app gate, and frozen-input integrity check must pass. Unexecuted or blocked checks cannot be reported as accepted.
- No manual app criterion is required. A later user walkthrough assesses the workflow separately.

## Dependencies, retained inputs, and readiness

There are no subsystem prerequisites, external services, or retained user assets. Future checks create disposable task files. There is one subsystem and no dependency edges.

The target and future frozen checks must implement this contract without adding behavior requirements. The implementation sequence and ownership are documented in [implementation-order.md](../../../specs/implementation-order.md).

**Open behavior decisions:** None proposed. Final document approval remains pending.

**Generation readiness:** BLOCKED. Executable checks, execution adapters, and the full frozen handoff inventory are intentionally absent from this documentation-only task. The documentation inventory is not a frozen executable verifier. App checks and independent implementation review are NOT_RUN.

Approval lives in the adjacent digest-bound record, not this status field. Later behavioral changes require a revised approval under the [suite contract](../../../spec-source-suite/docs/SUITE_CONTRACT.md).
