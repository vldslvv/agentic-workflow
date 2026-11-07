#!/usr/bin/env python3
"""Evaluate committed HEAD in a clean worktree, archive evidence, and remove it."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile

import todolist


def archive_evidence(worktree, destination):
    results = todolist.safe_path(worktree, todolist.RESULTS)
    if results.is_dir():
        shutil.copytree(results, destination, dirs_exist_ok=True, symlinks=True)
    app = todolist.safe_path(worktree, todolist.APP)
    if app.is_dir():
        shutil.copytree(app, destination / "app", symlinks=True,
                        ignore=shutil.ignore_patterns(".venv", "__pycache__"))
    result_path = todolist.safe_path(destination, Path("result.json"))
    if result_path.is_file():
        report = json.loads(result_path.read_text())
        for name in report.get("records_created", []):
            if not isinstance(name, str) or name in ("", ".", "..") or Path(name).name != name:
                raise todolist.RunnerError("Invalid records path in eval result")
            source = todolist.safe_path(worktree, Path(".agentic-workflow") / name)
            if source.is_dir():
                shutil.copytree(source, destination / "records" / name, symlinks=True)


def evaluate(root, agent_timeout, command_timeout):
    commit = todolist.git(root, "rev-parse", "HEAD").strip()
    archive_root = todolist.safe_path(root, Path(".evals/todolist-worktrees"))
    archive_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-")
    destination = Path(tempfile.mkdtemp(prefix=stamp, dir=archive_root))
    temporary = Path(tempfile.mkdtemp(prefix="todolist-eval-"))
    worktree = temporary / "checkout"
    summary = {"source_commit": commit, "source_root": str(root), "worktree": str(worktree),
               "status": "RUNNER_ERROR", "exit_code": 2, "worktree_removed": False}
    try:
        todolist.git(root, "worktree", "add", "--detach", str(worktree), commit)
        dirty = todolist.git(worktree, "status", "--porcelain=v1", "--untracked-files=all")
        if dirty:
            raise todolist.RunnerError(f"New worktree is not clean:\n{dirty}")
        print(f"Evaluating committed HEAD {commit} in clean worktree {worktree}", flush=True)
        code = todolist.run(worktree, agent_timeout, command_timeout, allow_dirty=False)
        summary.update(exit_code=code, status={0: "PASS", 1: "FAIL", 2: "RUNNER_ERROR",
                                             124: "TIMEOUT"}.get(code, "INTERRUPTED"))
    except todolist.Interrupted as exc:
        summary.update(status="INTERRUPTED", exit_code=128 + exc.signum)
    except (OSError, ValueError, todolist.RunnerError, subprocess.SubprocessError) as exc:
        summary["error"] = str(exc)
    finally:
        # Finish evidence preservation and removal even if another interrupt arrives.
        previous = {sig: signal.signal(sig, signal.SIG_IGN) for sig in (signal.SIGINT, signal.SIGTERM)}
        try:
            if worktree.exists():
                # A failed archive leaves the worktree available for manual recovery.
                archive_evidence(worktree, destination)
                todolist.git(root, "worktree", "remove", "--force", str(worktree))
            temporary.rmdir()
            summary["worktree_removed"] = True
        except (OSError, ValueError, todolist.RunnerError, subprocess.SubprocessError) as exc:
            summary.update(status="RUNNER_ERROR", exit_code=2, cleanup_error=str(exc))
        finally:
            todolist.write_json(destination / "worktree.json", summary)
            for sig, handler in previous.items():
                signal.signal(sig, handler)
    print(f"Eval: {summary['status']}")
    print(f"Saved report and evidence: {destination}")
    if summary["worktree_removed"]:
        print("Temporary worktree removed.")
    else:
        print(f"Worktree retained for recovery: {worktree}")
    for key in ("error", "cleanup_error"):
        if key in summary:
            print(f"RUNNER_ERROR: {summary[key]}", file=sys.stderr)
    return summary["exit_code"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent-timeout", type=todolist.positive_seconds, default=1800)
    parser.add_argument("--command-timeout", type=todolist.positive_seconds, default=60)
    args = parser.parse_args()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, todolist.interrupt)
    try:
        if sys.platform == "win32":
            raise todolist.RunnerError("This local runner requires POSIX process groups")
        root = Path(todolist.git(Path.cwd(), "rev-parse", "--show-toplevel").strip()).resolve()
        return evaluate(root, args.agent_timeout, args.command_timeout)
    except todolist.Interrupted as exc:
        return 128 + exc.signum
    except (OSError, ValueError, todolist.RunnerError, subprocess.SubprocessError) as exc:
        print(f"RUNNER_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
