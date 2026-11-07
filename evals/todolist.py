#!/usr/bin/env python3
"""One local generation trial, exact CLI checks, and presence-only trace checks."""

import argparse
import json
import math
import os
from pathlib import Path
import shutil
import signal
import stat
import subprocess
import sys
import time


PROMPT = "Implement specs/todolist"
APP = Path("apps/todolist")
RESULTS = Path(".evals/todolist")
OUTPUTS = (APP, RESULTS)
CLI_CASES = (
    (("list",), "No tasks.\n"),
    (("add", "Buy milk"), "Added task 1: Buy milk\n"),
    (("add", "Write tests"), "Added task 2: Write tests\n"),
    (("list",), "1 [ ] Buy milk\n2 [ ] Write tests\n"),
    (("complete", "1"), "Completed task 1\n"),
    (("list",), "1 [x] Buy milk\n2 [ ] Write tests\n"),
    (("delete", "1"), "Deleted task 1\n"),
    (("list",), "2 [ ] Write tests\n"),
    (("delete", "2"), "Deleted task 2\n"),
    (("list",), "No tasks.\n"),
    (("help",), "Usage: todo <command>\nCommands:\n  add <text>\n  list\n"
     "  complete <id>\n  delete <id>\n  help\n"),
)


class RunnerError(Exception):
    pass


class Interrupted(Exception):
    def __init__(self, signum):
        self.signum = signum


def interrupt(signum, frame):
    raise Interrupted(signum)


def git(root, *args):
    result = subprocess.run(
        ["git", "-C", str(root), *args], stdin=subprocess.DEVNULL,
        capture_output=True, timeout=60,
    )
    if result.returncode:
        raise RunnerError(result.stderr.decode(errors="replace").strip())
    return result.stdout.decode(errors="surrogateescape")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n")


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
            raise RunnerError(f"Refusing symlink path: {path}")
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
                raise RunnerError(f"Malformed model configuration row: {line}")
            table = tables.setdefault(section, {})
            if row[0] in table:
                raise RunnerError(f"Duplicate model configuration row: {row[0]}")
            table[row[0]] = row[1:]
    try:
        profile = tables["Role routes"][role][0]
        model, reasoning = tables["Profiles"][profile]
    except KeyError as exc:
        raise RunnerError(f"Missing {role} default route or profile in MODELS.md") from exc
    return {"profile": profile, "model": model, "reasoning": reasoning}


def preflight(root, allow_dirty):
    dirty = git(root, "status", "--porcelain=v1", "--untracked-files=all")
    if dirty and not allow_dirty:
        raise RunnerError(f"Clean checkout required; preserve or resolve these changes manually:\n{dirty}")
    for relative in OUTPUTS:
        if safe_path(root, relative).exists():
            raise RunnerError(f"Required absent path already exists: {relative}")
    if git(root, "ls-files", "--", *(str(p) for p in OUTPUTS)):
        raise RunnerError("Eval output paths contain tracked files")
    if subprocess.run(
        ["git", "-C", str(root), "check-ignore", "-q", str(RESULTS / "run.json")],
        stdin=subprocess.DEVNULL, timeout=60,
    ).returncode != 0:
        raise RunnerError(".evals/todolist/ must be ignored by Git")
    for name in ("uv", "codex"):
        if not shutil.which(name):
            raise RunnerError(f"Required executable unavailable: {name}")
    auth = subprocess.run(
        ["codex", "login", "status"], stdin=subprocess.DEVNULL,
        capture_output=True, timeout=60,
    )
    if auth.returncode:
        raise RunnerError("Codex is not authenticated; run codex login first")
    override = root / ".agentic-workflow/MODELS.md"
    routing = override if override.exists() else root / "agentic-workflow/policies/MODELS.md"
    return git(root, "rev-parse", "HEAD").strip(), role_settings(routing, "Supervisor"), dirty


def terminate_group(process):
    # Ignore repeated interrupts while reaping the leader and killing descendants,
    # including a child that ignores SIGTERM after its parent exits.
    previous = {s: signal.signal(s, signal.SIG_IGN) for s in (signal.SIGINT, signal.SIGTERM)}
    try:
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(process.pid, sig)
            except ProcessLookupError:
                break
            if sig == signal.SIGTERM:
                try:
                    process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    pass
        process.wait()
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def execute(command, cwd, timeout, stdout, stderr):
    started = time.monotonic()
    outcome = {"command": command, "status": "RUNNER_ERROR", "returncode": None}
    process = None
    try:
        with stdout.open("wb") as out, stderr.open("wb") as err:
            process = subprocess.Popen(
                command, cwd=cwd, stdin=subprocess.DEVNULL, stdout=out, stderr=err,
                start_new_session=True,
            )
            outcome["returncode"] = process.wait(timeout=timeout)
            outcome["status"] = "PASS" if process.returncode == 0 else "FAIL"
    except subprocess.TimeoutExpired:
        outcome["status"] = "TIMEOUT"
    except Interrupted as exc:
        outcome.update(status="INTERRUPTED", signal=exc.signum)
    except OSError as exc:
        outcome["error"] = str(exc)
    finally:
        if process is not None and outcome["status"] in ("TIMEOUT", "INTERRUPTED", "RUNNER_ERROR"):
            terminate_group(process)
            outcome["returncode"] = process.returncode
        outcome["elapsed_seconds"] = time.monotonic() - started
    return outcome


def records_entries(root):
    records = safe_path(root, Path(".agentic-workflow"))
    return {p.name: p for p in records.iterdir()} if records.exists() else {}


def new_implementations(root, before):
    return sorted(name for name, path in records_entries(root).items()
                  if name not in before and path.is_dir() and not path.is_symlink())


def artifact_grade(root, created):
    implementations = [root / ".agentic-workflow" / name for name in created]
    grade = {"status": "FAIL", "implementations": [p.name for p in implementations], "missing": []}
    if len(implementations) != 1:
        grade["error"] = "Expected one new implementation directory under .agentic-workflow"
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


def cli_grade(root, results, timeout):
    app = safe_path(root, APP)
    grade = {"status": "FAIL", "commands": []}
    if not app.is_dir():
        grade["error"] = f"Missing app directory: {APP}"
        return grade
    data = safe_path(root, APP / "tasks.json")
    if data.exists():
        if not real_file(data):
            grade["error"] = "tasks.json is not a regular file"
            return grade
        shutil.copyfile(data, results / "generation-tasks.json")
        data.unlink()
    for index, (args, expected) in enumerate(CLI_CASES, 1):
        stdout = results / f"cli-{index:02d}.stdout"
        stderr = results / f"cli-{index:02d}.stderr"
        observed = execute(["uv", "run", "todo", *args], app, timeout, stdout, stderr)
        observed.update(expected_stdout=expected, stdout=stdout.read_bytes().decode(errors="replace"),
                        stderr=stderr.read_bytes().decode(errors="replace"))
        if observed["status"] == "PASS" and stdout.read_bytes() != expected.encode():
            observed["status"] = "FAIL"
        if args[0] == "add":
            observed["tasks_json_created"] = real_file(data)
            if not observed["tasks_json_created"] and observed["status"] == "PASS":
                observed["status"] = "FAIL"
        grade["commands"].append(observed)
        write_json(results / "cli.json", grade)
        if observed["status"] in ("TIMEOUT", "INTERRUPTED", "RUNNER_ERROR"):
            grade["status"] = observed["status"]
            if "signal" in observed:
                grade["signal"] = observed["signal"]
            return grade
    grade["status"] = "PASS" if all(c["status"] == "PASS" for c in grade["commands"]) else "FAIL"
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
    command.append(PROMPT)
    results.mkdir(parents=True)
    write_json(results / "run.json", {
        "eval": "todolist", "root": str(root), "source_commit": commit,
        "prompt": PROMPT, "command": command, "supervisor": settings,
        "agent_timeout_seconds": agent_timeout, "command_timeout_seconds": command_timeout,
        "persistent_sessions": True, "started_at_unix": time.time(),
        "records_entries_before": before,
        "allow_dirty": allow_dirty, "git_status_before": dirty,
    })
    started = time.monotonic()
    report = {"overall": "RUNNER_ERROR", "agent": {"status": "NOT_RUN"},
              "cli": {"status": "NOT_RUN"}, "artifacts": {"status": "NOT_RUN"}}
    try:
        print(f"Launching one Codex trial ({settings['model']}, {settings['reasoning']}); logs: {results}", flush=True)
        report["agent"] = execute(command, root, agent_timeout, results / "events.jsonl", results / "agent.stderr")
        report["records_created"] = new_implementations(root, before)
        # These checks never synthesize or repair traces after Codex exits.
        for name, check in (("artifacts", lambda: artifact_grade(root, report["records_created"])),
                            ("cli", lambda: cli_grade(root, results, command_timeout))):
            if report["agent"]["status"] == "INTERRUPTED" and name == "cli":
                continue
            try:
                report[name] = check()
            except (OSError, RunnerError) as exc:
                report[name] = {"status": "RUNNER_ERROR", "error": str(exc)}
            if name == "cli":
                write_json(results / "cli.json", report[name])
        statuses = [report[key]["status"] for key in ("agent", "cli", "artifacts")]
        report["overall"] = next((s for s in ("INTERRUPTED", "RUNNER_ERROR", "TIMEOUT") if s in statuses),
                                 "PASS" if all(s == "PASS" for s in statuses) else "FAIL")
    except Interrupted as exc:
        report.update(overall="INTERRUPTED", signal=exc.signum)
    except (OSError, RunnerError, subprocess.SubprocessError) as exc:
        report.update(overall="RUNNER_ERROR", error=str(exc))
    finally:
        report["elapsed_seconds"] = time.monotonic() - started
        try:
            if "records_created" not in report:
                report["records_created"] = new_implementations(root, before)
            report["git_status"] = git(root, "status", "--porcelain=v1", "--untracked-files=all")
            report["unexpected_changes"] = git(
                root, "status", "--porcelain=v1", "--untracked-files=all", "--", ".",
                *(f":(exclude,literal){p}" for p in OUTPUTS),
                *(f":(exclude,literal).agentic-workflow/{name}" for name in report["records_created"]),
            )
        except (OSError, RunnerError, subprocess.SubprocessError) as exc:
            report.update(overall="RUNNER_ERROR", error=str(exc))
        write_json(results / "result.json", report)
    for key in ("agent", "cli", "artifacts", "overall"):
        print(f"{key}: {report[key]['status'] if isinstance(report[key], dict) else report[key]}")
    print(f"Results: {results / 'result.json'}")
    print("Generated files retained until explicit cleanup.")
    if report.get("unexpected_changes"):
        print(f"Unexpected changes retained for manual handling:\n{report['unexpected_changes']}")
    if report["overall"] == "INTERRUPTED":
        return 128 + report.get("signal", report["cli"].get("signal", report["agent"].get("signal", signal.SIGINT)))
    return {"PASS": 0, "FAIL": 1, "RUNNER_ERROR": 2, "TIMEOUT": 124}[report["overall"]]


def clean(root):
    marker = safe_path(root, RESULTS / "run.json")
    if not real_file(marker):
        raise RunnerError("No eval run exists; refusing cleanup")
    metadata = json.loads(marker.read_text())
    if (not isinstance(metadata, dict) or metadata.get("eval") != "todolist"
            or metadata.get("root") != str(root) or metadata.get("prompt") != PROMPT):
        raise RunnerError("Eval run marker does not identify this checkout")
    result_path = safe_path(root, RESULTS / "result.json")
    if not real_file(result_path):
        raise RunnerError("No completed eval inventory; preserve execution records and handle cleanup manually")
    report = json.loads(result_path.read_text())
    before = metadata.get("records_entries_before")
    created = report.get("records_created") if isinstance(report, dict) else None
    if (not isinstance(before, list) or not isinstance(created, list)
            or any(not isinstance(name, str) or not name or name in (".", "..")
                   or Path(name).name != name or name in before for name in created)):
        raise RunnerError("Invalid eval records inventory; refusing cleanup")
    owned = (APP, *(Path(".agentic-workflow") / name for name in created), RESULTS)
    paths = [safe_path(root, p) for p in owned]
    # Include HEAD so staging a deletion cannot make tracked data eligible for removal.
    pathspecs = [f":(literal){p}" for p in owned]
    tracked = git(root, "ls-files", "--", *pathspecs)
    tracked += git(root, "ls-tree", "-r", "--name-only", "HEAD", "--", *(str(p) for p in owned))
    if tracked:
        raise RunnerError(f"Refusing cleanup: eval paths contain tracked files:\n{tracked}")
    for path in paths:
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()
    print("Removed apps/todolist, this eval's records directories, and .evals/todolist.")
    remaining = git(root, "status", "--porcelain=v1", "--untracked-files=all")
    if remaining:
        print(f"Unexpected changes retained for manual handling:\n{remaining}")
    return 0


def positive_seconds(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("timeout must be a positive finite number")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    trial = commands.add_parser("run", help="run one generation trial in the current clean checkout")
    trial.add_argument("--agent-timeout", type=positive_seconds, default=1800)
    trial.add_argument("--command-timeout", type=positive_seconds, default=60)
    trial.add_argument("--allow-dirty", action="store_true",
                       help="allow uncommitted inputs; record initial Git status in run.json")
    commands.add_parser("clean", help="remove only this eval's untracked outputs")
    args = parser.parse_args()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, interrupt)
    try:
        if os.name != "posix":
            raise RunnerError("This local runner requires POSIX process groups")
        if not shutil.which("git"):
            raise RunnerError("Required executable unavailable: git")
        root = Path(git(Path.cwd(), "rev-parse", "--show-toplevel").strip()).resolve()
        return run(root, args.agent_timeout, args.command_timeout, args.allow_dirty) if args.action == "run" else clean(root)
    except Interrupted as exc:
        print("Interrupted", file=sys.stderr)
        return 128 + exc.signum
    except (OSError, RunnerError, ValueError, subprocess.SubprocessError) as exc:
        print(f"RUNNER_ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
