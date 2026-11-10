#!/usr/bin/env python3
"""One local generation trial, exact CLI checks, and presence-only trace checks."""

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from dataclasses import asdict
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


from evals.support import runtime, todolist_cli, trial
from evals.support.models import TrialResult

PROMPT_PATH = Path(__file__).resolve().parent / "prompts" / "todolist-generation.md"


def run(root: Path, agent_timeout: float, command_timeout: float, allow_dirty: bool) -> TrialResult:
    commit, settings, dirty = trial.preflight(root, allow_dirty)
    before = sorted(trial.records_entries(root))
    results = root / trial.RESULTS
    command = [
        "codex",
        "exec",
        "--json",
        "--color",
        "never",
        "--sandbox",
        "workspace-write",
        "--enable",
        "multi_agent",
        "-c",
        'approval_policy="never"',
        "-c",
        "sandbox_workspace_write.network_access=true",
        "--model",
        settings.model,
        "--output-last-message",
        str(results / "final-response.txt"),
    ]
    if settings.reasoning != "default":
        command += ["-c", f"model_reasoning_effort={json.dumps(settings.reasoning)}"]
    prompt = PROMPT_PATH.read_text()
    command.append(prompt)
    results.mkdir(parents=True)
    (results / "prompt.txt").write_text(prompt)
    runtime.write_json(
        results / "run.json",
        {
            "eval": "todolist",
            "root": str(root),
            "source_commit": commit,
            "prompt": prompt,
            "prompt_path": "prompt.txt",
            "command": command,
            "supervisor": asdict(settings),
            "agent_timeout_seconds": agent_timeout,
            "command_timeout_seconds": command_timeout,
            "persistent_sessions": True,
            "started_at_unix": time.time(),
            "records_entries_before": before,
            "allow_dirty": allow_dirty,
            "git_status_before": dirty,
        },
    )
    started = time.monotonic()
    report: TrialResult = {
        "status": "RUNNER_ERROR",
        "generation": {"status": "NOT_RUN"},
        "cli": {"status": "NOT_RUN"},
        "artifacts": {"status": "NOT_RUN"},
    }
    try:
        print(
            f"Launching one Codex trial ({settings.model}, {settings.reasoning}); logs: {results}",
            flush=True,
        )
        report["generation"] = runtime.execute(
            command,
            root,
            agent_timeout,
            results / "events.jsonl",
            results / "agent.stderr",
        )
        report["records_created"] = trial.new_implementations(root, before)
        # Presence and CLI grades are independent of the generation exit status.
        try:
            report["artifacts"] = trial.artifact_grade(root, report["records_created"])
        except (OSError, runtime.RunnerError) as exc:
            report["artifacts"] = {"status": "RUNNER_ERROR", "error": str(exc)}
        if report["generation"]["status"] != "INTERRUPTED":
            try:
                app = trial.safe_path(root, trial.APP)
                trial.safe_path(root, trial.APP / "tasks.json")
                report["cli"] = todolist_cli.grade(app, results, command_timeout)
            except (OSError, runtime.RunnerError) as exc:
                report["cli"] = {"status": "RUNNER_ERROR", "error": str(exc)}
        runtime.write_json(results / "cli.json", report["cli"])
        statuses = [report[key]["status"] for key in ("generation", "cli", "artifacts")]
        report["status"] = next(
            (s for s in ("INTERRUPTED", "RUNNER_ERROR", "TIMEOUT") if s in statuses),
            "PASS" if all(s == "PASS" for s in statuses) else "FAIL",
        )
    except runtime.Interrupted as exc:
        report.update({"status": "INTERRUPTED", "signal": exc.signum})
    except (OSError, runtime.RunnerError, subprocess.SubprocessError) as exc:
        report.update({"status": "RUNNER_ERROR", "error": str(exc)})
    finally:
        report["elapsed_seconds"] = time.monotonic() - started
        try:
            if "records_created" not in report:
                report["records_created"] = trial.new_implementations(root, before)
            report["git_status"] = trial.git(
                root, "status", "--porcelain=v1", "--untracked-files=all"
            )
            report["unexpected_changes"] = trial.git(
                root,
                "status",
                "--porcelain=v1",
                "--untracked-files=all",
                "--",
                ".",
                *(f":(exclude,literal){p}" for p in trial.OUTPUTS),
                *(
                    f":(exclude,literal).agentic-workflow/records/{name}"
                    for name in report["records_created"]
                ),
            )
        except (OSError, runtime.RunnerError, subprocess.SubprocessError) as exc:
            report.update({"status": "RUNNER_ERROR", "error": str(exc)})
        runtime.write_json(results / "result.json", report)
    for key in ("generation", "cli", "artifacts"):
        print(f"{key}: {report[key]['status']}")
    print(f"status: {report['status']}")
    print(f"Results: {results / 'result.json'}")
    print("Generated files retained until explicit cleanup.")
    if report.get("unexpected_changes"):
        print(f"Unexpected changes retained for manual handling:\n{report['unexpected_changes']}")
    return report


def exit_code(report: TrialResult) -> int:
    if report["status"] == "INTERRUPTED":
        return 128 + report.get(
            "signal", report["cli"].get("signal", report["generation"].get("signal", signal.SIGINT))
        )
    return {"PASS": 0, "FAIL": 1, "RUNNER_ERROR": 2, "TIMEOUT": 124}[report["status"]]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    trial_parser = commands.add_parser(
        "run", help="run one generation trial in the current clean checkout"
    )
    trial_parser.add_argument("--agent-timeout", type=runtime.positive_seconds, default=1800)
    trial_parser.add_argument("--command-timeout", type=runtime.positive_seconds, default=60)
    trial_parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="allow uncommitted inputs; record initial Git status in run.json",
    )
    commands.add_parser("clean", help="remove only this eval's untracked outputs")
    args = parser.parse_args()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, runtime.interrupt)
    try:
        if os.name != "posix":
            raise runtime.RunnerError("This local runner requires POSIX process groups")
        if not shutil.which("git"):
            raise runtime.RunnerError("Required executable unavailable: git")
        root = Path(trial.git(Path.cwd(), "rev-parse", "--show-toplevel").strip()).resolve()
        if args.action == "clean":
            return trial.clean(root)
        return exit_code(run(root, args.agent_timeout, args.command_timeout, args.allow_dirty))
    except runtime.Interrupted as exc:
        print("Interrupted", file=sys.stderr)
        return 128 + exc.signum
    except (OSError, runtime.RunnerError, ValueError, subprocess.SubprocessError) as exc:
        print(f"RUNNER_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
