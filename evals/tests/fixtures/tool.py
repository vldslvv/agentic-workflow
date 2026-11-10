"""Controlled external-process stand-ins; never used by a real eval run."""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

mode = os.environ.get("EVAL_FIXTURE", "pass")
tool = Path(sys.argv[0]).name
if tool == "codex" and sys.argv[1:] == ["login", "status"]:
    if mode == "launch_error":
        # Auth works, but the executable disappears before the generation launch.
        Path(sys.argv[0]).unlink()
    sys.exit(1 if mode == "unauthenticated" else 0)
root = Path.cwd() if tool == "codex" else Path.cwd().parents[1]
results = root / ".agentic-workflow/evals/todolist"


def hang() -> None:
    # The descendant ignores TERM, so merely killing/waiting for its parent is
    # insufficient. It would leave a marker if group termination were broken.
    child_code = """
import pathlib, signal, time
signal.signal(signal.SIGTERM, signal.SIG_IGN)
pathlib.Path('child-ready').touch()
time.sleep(1.5)
pathlib.Path('leaked-child').touch()
time.sleep(30)
"""
    subprocess.Popen([sys.executable, "-c", child_code], cwd=results)
    while not (results / "child-ready").exists():
        time.sleep(0.01)
    (results / "ready").touch()
    time.sleep(30)


if tool == "uv":
    if sys.argv[1:3] != ["run", "todo"]:
        sys.exit(8)
    if mode == "cli_timeout":
        hang()
    os.execv(sys.executable, [sys.executable, "todo.py", *sys.argv[3:]])

(results / "received.json").write_text(json.dumps(sys.argv[1:]))
(results / "fixture-source.txt").write_text((root / "source.txt").read_text())
print('{"fixture": "agent event"}', flush=True)
print("fixture stderr", file=sys.stderr, flush=True)
if mode in ("agent_timeout", "interrupt"):
    hang()
app = root / "apps/todolist"
app.mkdir(parents=True)
shutil.copyfile(Path(__file__).with_name("todo.py"), app / "todo.py")
if mode != "no_generation_data":
    (app / "tasks.json").write_text("generation data to preserve\n")
implementation = root / ".agentic-workflow/records/001_todolist"
reports = implementation / "reports"
reports.mkdir(parents=True)
for name in ("usage.json", "usage.md", "timeline.json"):
    if mode != "missing_artifacts":
        (reports / name).touch()
native = implementation / "native/session"
native.mkdir(parents=True)
if mode != "missing_artifacts":
    (native / "turn.jsonl").touch()
if mode == "artifact_directory":
    (reports / "usage.json").unlink()
    (reports / "usage.json").mkdir()
if mode == "multiple_implementations":
    (root / ".agentic-workflow/records/002_other").mkdir()
if mode == "no_implementation":
    shutil.rmtree(implementation)
if mode == "unexpected_changes":
    (root / "source.txt").write_text("unexpected tracked modification\n")
    (root / "unrelated").touch()
final = Path(sys.argv[sys.argv.index("--output-last-message") + 1])
final.write_text("fixture final response\n")
sys.exit(9 if mode == "agent_nonzero" else 0)
