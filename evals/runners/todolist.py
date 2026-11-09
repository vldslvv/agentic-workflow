"""One local generation trial, exact CLI checks, and presence-only trace checks."""

import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
import time

from . import runtime
from . import todolist_cli


PROMPT_PATH = Path(__file__).resolve().parents[1] / "prompts" / "todolist-generation.md"
APP = Path("apps/todolist")
RESULTS = Path(".agentic-workflow/evals/todolist")
OUTPUTS = (APP, RESULTS)


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args], stdin=subprocess.DEVNULL,
        capture_output=True, timeout=60,
    )
    if result.returncode:
        raise runtime.RunnerError(result.stderr.decode(errors="replace").strip())
    return result.stdout.decode(errors="surrogateescape")


def real_file(path):
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except FileNotFoundError:
        return False


def safe_path(root, relative):
    """Never read, grade, or remove an owned path through a symlink."""
    path = root
    for part in relative.parts:
        path /= part
        if path.is_symlink():
            raise runtime.RunnerError(f"Refusing symlink path: {path}")
    return path


def role_settings(path, role):
    tables = {}
    section = None
    for line in path.read_text().splitlines():
        if line.startswith("## "):
            section = line[3:].strip()
        if line.startswith("|") and section in ("Profiles", "Role routes"):
            row = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
            if len(row) != 3 or not all(row):
                raise runtime.RunnerError(f"Malformed model configuration row: {line}")
            table = tables.setdefault(section, {})
            if row[0] in table:
                raise runtime.RunnerError(f"Duplicate model configuration row: {row[0]}")
            table[row[0]] = row[1:]
    try:
        profile = tables["Role routes"][role][0]
        model, reasoning = tables["Profiles"][profile]
    except KeyError as exc:
        raise runtime.RunnerError(f"Missing {role} default route or profile in MODELS.md") from exc
    return {"profile": profile, "model": model, "reasoning": reasoning}


def preflight(root, allow_dirty):
    dirty = git(root, "status", "--porcelain=v1", "--untracked-files=all")
    if dirty and not allow_dirty:
        raise runtime.RunnerError(f"Clean checkout required; preserve or resolve these changes manually:\n{dirty}")
    for relative in OUTPUTS:
        if safe_path(root, relative).exists():
            raise runtime.RunnerError(f"Required absent path already exists: {relative}")
    if git(root, "ls-files", "--", *(str(p) for p in OUTPUTS)):
        raise runtime.RunnerError("Eval output paths contain tracked files")
    if subprocess.run(
        ["git", "-C", str(root), "check-ignore", "-q", str(RESULTS / "run.json")],
        stdin=subprocess.DEVNULL, timeout=60,
    ).returncode != 0:
        raise runtime.RunnerError(".agentic-workflow/evals/todolist/ must be ignored by Git")
    for name in ("uv", "codex"):
        if not shutil.which(name):
            raise runtime.RunnerError(f"Required executable unavailable: {name}")
    auth = subprocess.run(
        ["codex", "login", "status"], stdin=subprocess.DEVNULL,
        capture_output=True, timeout=60,
    )
    if auth.returncode:
        raise runtime.RunnerError("Codex is not authenticated; run codex login first")
    override = root / ".agentic-workflow/config/MODELS.md"
    routing = override if override.exists() else root / "agentic-workflow/policies/MODELS.md"
    return git(root, "rev-parse", "HEAD").strip(), role_settings(routing, "Supervisor"), dirty


def records_entries(root):
    records = safe_path(root, Path(".agentic-workflow/records"))
    return {p.name: p for p in records.iterdir()} if records.exists() else {}


def new_implementations(root, before):
    return sorted(name for name, path in records_entries(root).items()
                  if name not in before and path.is_dir() and not path.is_symlink())


def artifact_grade(root, created):
    implementations = [root / ".agentic-workflow/records" / name for name in created]
    grade = {"status": "FAIL", "implementations": [p.name for p in implementations], "missing": []}
    if len(implementations) != 1:
        grade["error"] = "Expected one new implementation directory under .agentic-workflow/records"
        return grade
    implementation = implementations[0]
    for name in ("usage.json", "usage.md", "timeline.json"):
        relative = (implementation / "reports" / name).relative_to(root)
        if not real_file(safe_path(root, relative)):
            grade["missing"].append(str(relative))
    traces = [p for p in implementation.glob("native/*/*.jsonl")
              if real_file(safe_path(root, p.relative_to(root)))]
    grade["native_files"] = [str(p.relative_to(root)) for p in sorted(traces)]
    if not traces:
        grade["missing"].append(str(implementation.relative_to(root) / "native/*/*.jsonl"))
    grade["status"] = "FAIL" if grade["missing"] else "PASS"
    return grade


def run(root, agent_timeout, command_timeout, allow_dirty):
    commit, settings, dirty = preflight(root, allow_dirty)
    before = sorted(records_entries(root))
    results = root / RESULTS
    command = ["codex", "exec", "--json", "--color", "never", "--sandbox", "workspace-write",
               "--enable", "multi_agent", "-c", 'approval_policy="never"',
               "-c", "sandbox_workspace_write.network_access=true", "--model", settings["model"],
               "--output-last-message", str(results / "final-response.txt")]
    if settings["reasoning"] != "default":
        command += ["-c", f'model_reasoning_effort={json.dumps(settings["reasoning"])}']
    prompt = PROMPT_PATH.read_text()
    command.append(prompt)
    results.mkdir(parents=True)
    (results / "prompt.txt").write_text(prompt)
    runtime.write_json(results / "run.json", {
        "eval": "todolist", "root": str(root), "source_commit": commit,
        "prompt": prompt, "prompt_path": "prompt.txt", "command": command, "supervisor": settings,
        "agent_timeout_seconds": agent_timeout, "command_timeout_seconds": command_timeout,
        "persistent_sessions": True, "started_at_unix": time.time(),
        "records_entries_before": before,
        "allow_dirty": allow_dirty, "git_status_before": dirty,
    })
    started = time.monotonic()
    report = {"status": "RUNNER_ERROR", "generation": {"status": "NOT_RUN"},
              "cli": {"status": "NOT_RUN"}, "artifacts": {"status": "NOT_RUN"}}
    try:
        print(f"Launching one Codex trial ({settings['model']}, {settings['reasoning']}); logs: {results}", flush=True)
        report["generation"] = runtime.execute(command, root, agent_timeout, results / "events.jsonl", results / "agent.stderr")
        report["records_created"] = new_implementations(root, before)
        # Presence and CLI grades are independent of the generation exit status.
        try:
            report["artifacts"] = artifact_grade(root, report["records_created"])
        except (OSError, runtime.RunnerError) as exc:
            report["artifacts"] = {"status": "RUNNER_ERROR", "error": str(exc)}
        if report["generation"]["status"] != "INTERRUPTED":
            try:
                app = safe_path(root, APP)
                safe_path(root, APP / "tasks.json")
                report["cli"] = todolist_cli.grade(app, results, command_timeout)
            except (OSError, runtime.RunnerError) as exc:
                report["cli"] = {"status": "RUNNER_ERROR", "error": str(exc)}
        runtime.write_json(results / "cli.json", report["cli"])
        statuses = [report[key]["status"] for key in ("generation", "cli", "artifacts")]
        report["status"] = next((s for s in ("INTERRUPTED", "RUNNER_ERROR", "TIMEOUT") if s in statuses),
                                 "PASS" if all(s == "PASS" for s in statuses) else "FAIL")
    except runtime.Interrupted as exc:
        report.update(status="INTERRUPTED", signal=exc.signum)
    except (OSError, runtime.RunnerError, subprocess.SubprocessError) as exc:
        report.update(status="RUNNER_ERROR", error=str(exc))
    finally:
        report["elapsed_seconds"] = time.monotonic() - started
        try:
            if "records_created" not in report:
                report["records_created"] = new_implementations(root, before)
            report["git_status"] = git(root, "status", "--porcelain=v1", "--untracked-files=all")
            report["unexpected_changes"] = git(
                root, "status", "--porcelain=v1", "--untracked-files=all", "--", ".",
                *(f":(exclude,literal){p}" for p in OUTPUTS),
                *(f":(exclude,literal).agentic-workflow/records/{name}" for name in report["records_created"]),
            )
        except (OSError, runtime.RunnerError, subprocess.SubprocessError) as exc:
            report.update(status="RUNNER_ERROR", error=str(exc))
        runtime.write_json(results / "result.json", report)
    for key in ("generation", "cli", "artifacts", "status"):
        print(f"{key}: {report[key]['status'] if isinstance(report[key], dict) else report[key]}")
    print(f"Results: {results / 'result.json'}")
    print("Generated files retained until explicit cleanup.")
    if report.get("unexpected_changes"):
        print(f"Unexpected changes retained for manual handling:\n{report['unexpected_changes']}")
    if report["status"] == "INTERRUPTED":
        return 128 + report.get("signal", report["cli"].get("signal", report["generation"].get("signal", signal.SIGINT)))
    return {"PASS": 0, "FAIL": 1, "RUNNER_ERROR": 2, "TIMEOUT": 124}[report["status"]]


def clean(root):
    marker = safe_path(root, RESULTS / "run.json")
    if not real_file(marker):
        raise runtime.RunnerError("No eval run exists; refusing cleanup")
    metadata = json.loads(marker.read_text())
    if (not isinstance(metadata, dict) or metadata.get("eval") != "todolist"
            or metadata.get("root") != str(root)):
        raise runtime.RunnerError("Eval run marker does not identify this checkout")
    result_path = safe_path(root, RESULTS / "result.json")
    if not real_file(result_path):
        raise runtime.RunnerError("No completed eval inventory; preserve execution records and handle cleanup manually")
    report = json.loads(result_path.read_text())
    before = metadata.get("records_entries_before")
    created = report.get("records_created") if isinstance(report, dict) else None
    if (not isinstance(before, list) or not isinstance(created, list)
            or any(not isinstance(name, str) or not name or name in (".", "..")
                   or Path(name).name != name or name in before for name in created)):
        raise runtime.RunnerError("Invalid eval records inventory; refusing cleanup")
    owned = (APP, *(Path(".agentic-workflow/records") / name for name in created), RESULTS)
    paths = [safe_path(root, p) for p in owned]
    # Include HEAD so staging a deletion cannot make tracked data eligible for removal.
    pathspecs = [f":(literal){p}" for p in owned]
    tracked = git(root, "ls-files", "--", *pathspecs)
    tracked += git(root, "ls-tree", "-r", "--name-only", "HEAD", "--", *(str(p) for p in owned))
    if tracked:
        raise runtime.RunnerError(f"Refusing cleanup: eval paths contain tracked files:\n{tracked}")
    for path in paths:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()
    print("Removed apps/todolist, this eval's records directories, and .agentic-workflow/evals/todolist.")
    remaining = git(root, "status", "--porcelain=v1", "--untracked-files=all")
    if remaining:
        print(f"Unexpected changes retained for manual handling:\n{remaining}")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    trial = commands.add_parser("run", help="run one generation trial in the current clean checkout")
    trial.add_argument("--agent-timeout", type=runtime.positive_seconds, default=1800)
    trial.add_argument("--command-timeout", type=runtime.positive_seconds, default=60)
    trial.add_argument("--allow-dirty", action="store_true",
                       help="allow uncommitted inputs; record initial Git status in run.json")
    commands.add_parser("clean", help="remove only this eval's untracked outputs")
    args = parser.parse_args()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, runtime.interrupt)
    try:
        if os.name != "posix":
            raise runtime.RunnerError("This local runner requires POSIX process groups")
        if not shutil.which("git"):
            raise runtime.RunnerError("Required executable unavailable: git")
        root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").strip()).resolve()
        return run(root, args.agent_timeout, args.command_timeout, args.allow_dirty) if args.action == "run" else clean(root)
    except runtime.Interrupted as exc:
        print("Interrupted", file=sys.stderr)
        return 128 + exc.signum
    except (OSError, runtime.RunnerError, ValueError, subprocess.SubprocessError) as exc:
        print(f"RUNNER_ERROR: {exc}", file=sys.stderr)
        return 2

