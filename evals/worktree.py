#!/usr/bin/env python3
"""Evaluate committed HEAD in a clean worktree, archive evidence, and remove it."""

import argparse
import signal
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import cast

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from evals import todolist
from evals.support import runtime, trial
from evals.support.archive import archive_evidence
from evals.support.models import Status, WorktreeResult


def run(root: Path, agent_timeout: float, command_timeout: float) -> WorktreeResult:
    commit = trial.git(root, "rev-parse", "HEAD").strip()
    archive_root = trial.safe_path(root, Path(".agentic-workflow/evals/todolist-worktrees"))
    archive_root.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-")
    destination = Path(tempfile.mkdtemp(prefix=stamp, dir=archive_root))
    worktrees = trial.safe_path(root, Path(".agentic-workflow/tmp/worktrees"))
    worktrees.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix="todolist-eval-", dir=worktrees))
    worktree = temporary / "checkout"
    summary: WorktreeResult = {
        "source_commit": commit,
        "source_root": str(root),
        "worktree": str(worktree),
        "status": "RUNNER_ERROR",
        "exit_code": 2,
        "worktree_removed": False,
    }
    try:
        trial.git(root, "worktree", "add", "--detach", str(worktree), commit)
        dirty = trial.git(worktree, "status", "--porcelain=v1", "--untracked-files=all")
        if dirty:
            raise runtime.RunnerError(f"New worktree is not clean:\n{dirty}")
        print(f"Evaluating committed HEAD {commit} in clean worktree {worktree}", flush=True)
        result = todolist.run(worktree, agent_timeout, command_timeout, allow_dirty=False)
        code = todolist.exit_code(result)
        summary.update(
            {
                "exit_code": code,
                "status": cast(
                    Status,
                    {0: "PASS", 1: "FAIL", 2: "RUNNER_ERROR", 124: "TIMEOUT"}.get(
                        code, "INTERRUPTED"
                    ),
                ),
            }
        )
    except runtime.Interrupted as exc:
        summary.update({"status": "INTERRUPTED", "exit_code": 128 + exc.signum})
    except (OSError, ValueError, runtime.RunnerError, subprocess.SubprocessError) as exc:
        summary["error"] = str(exc)
    finally:
        # Finish evidence preservation and removal even if another interrupt arrives.
        previous = {
            sig: signal.signal(sig, signal.SIG_IGN) for sig in (signal.SIGINT, signal.SIGTERM)
        }
        try:
            if worktree.exists():
                # A failed archive leaves the worktree available for manual recovery.
                archive_evidence(worktree, destination)
                trial.git(root, "worktree", "remove", "--force", str(worktree))
            temporary.rmdir()
            summary["worktree_removed"] = True
        except (OSError, ValueError, runtime.RunnerError, subprocess.SubprocessError) as exc:
            summary.update({"status": "RUNNER_ERROR", "exit_code": 2, "cleanup_error": str(exc)})
        finally:
            runtime.write_json(destination / "worktree.json", summary)
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
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent-timeout", type=runtime.positive_seconds, default=1800)
    parser.add_argument("--command-timeout", type=runtime.positive_seconds, default=60)
    args = parser.parse_args()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, runtime.interrupt)
    try:
        if sys.platform == "win32":
            raise runtime.RunnerError("This local runner requires POSIX process groups")
        root = Path(trial.git(Path.cwd(), "rev-parse", "--show-toplevel").strip()).resolve()
        return run(root, args.agent_timeout, args.command_timeout)["exit_code"]
    except runtime.Interrupted as exc:
        return 128 + exc.signum
    except (OSError, ValueError, runtime.RunnerError, subprocess.SubprocessError) as exc:
        print(f"RUNNER_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
