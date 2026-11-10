#!/usr/bin/env python3
"""Start a new implementation with allocate; resume a task with resolve.

Choose a subcommand; read its --help for arguments and restrictions.

Allocates directories or resolves an existing task and attempts native capture;
starts no service. Detection reads CODEX_THREAD_ID and OPENCODE_SESSION_ID.
Conflicting nonempty identities fail before any writes; absent identities warn
and retain allocation/resolution behavior. There is no provider override.

Prints the selected path; capture diagnostics go to stderr. Exit 0 means
success, not complete telemetry; exit 2 means invalid input or an operation
error (stderr).

Retain the returned path for later commands.

Examples:
  python3 agentic-workflow/helpers/records.py allocate example
  python3 agentic-workflow/helpers/records.py resolve .agentic-workflow/records/001_example 01_task
"""

import argparse
import os
import re
import sys
from pathlib import Path

from tracing.registry import capture_current, detect_current
from tracing.shared.files import identifier, locked
from tracing.shared.types import Diagnostic


def report_capture(diagnostics: list[Diagnostic]) -> None:
    for diagnostic in diagnostics:
        print("records: " + diagnostic["code"], file=sys.stderr)
        if diagnostic["code"] == "current_session_unavailable":
            print(
                "records: capture unavailable; use CODEX_THREAD_ID or OPENCODE_SESSION_ID in the active agent shell; see "
                "agentic-workflow/guides/TRACING.md#automatic-tracing-provider-detection",
                file=sys.stderr,
            )
        elif diagnostic["code"] == "opencode_export_unavailable":
            print(
                "records: check opencode session export SESSION_ID and the selected session; "
                "saved evidence is retained",
                file=sys.stderr,
            )


def allocate(records_root: Path, name: str) -> Path:
    identifier(name)
    detected = detect_current(os.environ)
    records_root = Path(records_root)
    records_root.mkdir(parents=True, exist_ok=True)
    with locked(records_root):
        numbers = [
            int(match[1])
            for p in records_root.iterdir()
            if p.is_dir() and (match := re.fullmatch(r"(\d{3,})_.+", p.name))
        ]
        root = records_root / f"{max(numbers, default=0) + 1:03d}_{name}"
        root.mkdir()  # Reserve before writing; an interrupted allocation is not reused.
        for directory in ("tasks", "runs", "reports"):
            (root / directory).mkdir()
        with locked(root / ".records.lock"):
            capture_diagnostics = capture_current(root, detected)
        report_capture(capture_diagnostics)
    return root


def resolve_task(root: Path, task: str) -> Path:
    detected = detect_current(os.environ)
    root = Path(root)
    target = root / "tasks" / identifier(task)
    if not target.is_dir() or not target.resolve().is_relative_to(root.resolve()):
        raise ValueError("task absent from identified implementation")
    with locked(root / ".records.lock"):
        report_capture(capture_current(root, detected))
    return target


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    commands = parser.add_subparsers(dest="command", required=True)
    allocate_parser = commands.add_parser(
        "allocate",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Start new work; every call creates a new implementation, even for the same
name.

name starts with an ASCII letter/digit and contains only ASCII letters, digits,
_, . or -; --records-root defaults to .agentic-workflow/records in the cwd.

Creates --records-root/<NNN>_<name>/ with tasks/, runs/, reports/ and
.records.lock; NNN is the next numeric prefix (at least three digits). Attempts
to save the current native turn and session metadata under
<NNN>_<name>/native/<session-id>/<turn-id>.jsonl (Codex) or .json (OpenCode);
OpenCode 2.2.6 supplies OPENCODE_SESSION_ID in agent shells. CODEX_THREAD_ID
identifies Codex. Both nonempty identities fail before writes. With neither
identity, allocation continues with a warning. There is no provider override.
Starts no service.

Prints the implementation path. Exit 0 means allocation succeeded, not complete
telemetry; best-effort capture diagnostics go to stderr. Exit 2 means invalid
input or an operation error (stderr).

Retain and reuse the printed path for tasks, reports and repairs; use resolve
to resume an existing task instead of allocating again.

Example: python3 agentic-workflow/helpers/records.py allocate example
""",
    )
    allocate_parser.add_argument("name", help="implementation name (safe identifier)")
    allocate_parser.add_argument(
        "--records-root",
        type=Path,
        default=Path(".agentic-workflow/records"),
        help="records directory (default: .agentic-workflow/records)",
    )
    resolve_parser = commands.add_parser(
        "resolve",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""Resume a known task in an existing implementation.

implementation is the allocated implementation path; task is an existing
directory name under implementation/tasks/. task starts with an ASCII
letter/digit and contains only ASCII letters, digits, _, . or -.

Requires implementation/tasks/<task>/ to exist within implementation; creates
no task. Creates/uses implementation/.records.lock and attempts to save the
current native turn and session metadata to implementation/native/<session-
id>/<turn-id>.jsonl (Codex) or .json (OpenCode); OpenCode 2.2.6 supplies
OPENCODE_SESSION_ID in agent shells. CODEX_THREAD_ID identifies Codex. Both
nonempty identities fail before writes. With neither identity, resolution
continues with a warning.
There is no provider override. Starts no service.

Prints the task path. Exit 0 means resolution succeeded, not complete
telemetry; best-effort capture diagnostics go to stderr. Exit 2 means invalid
input, absent task or an operation error (stderr).

Use the returned task path and retain implementation for reports/repairs.

Example: python3 agentic-workflow/helpers/records.py resolve .agentic-workflow/records/001_example 01_task
""",
    )
    resolve_parser.add_argument(
        "implementation", type=Path, help="existing implementation directory"
    )
    resolve_parser.add_argument("task", help="existing task directory name (safe identifier)")
    args = parser.parse_args()
    try:
        if args.command == "allocate":
            print(allocate(args.records_root, args.name))
        else:
            print(resolve_task(args.implementation, args.task))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f"records: {exc}\n")


if __name__ == "__main__":
    main()
