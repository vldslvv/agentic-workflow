"""Supervisor verification of the actual assembled app; restores existing data."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
APP = ROOT / "apps/todolist"
STORAGE = APP / "tasks.json"
REPORT = Path(__file__).with_name("assembled.md")
previous = STORAGE.read_bytes() if STORAGE.exists() else None
lines = ["# Assembled app verification", "", "Actual app, separate CLI processes, real app-root storage, unrelated temporary cwd.", ""]
env = {**os.environ, "PYTHONPATH": str(APP)}


def run(cwd, *args, success=True):
    command = ["uv", "run", "--project", str(APP), "python", "-m", "todolist", *args]
    result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True)
    lines.extend([f"Command: `uv run --project apps/todolist python -m todolist {' '.join(args)}`", f"Exit: {result.returncode}", "```text", result.stdout + result.stderr, "```", ""])
    assert (result.returncode == 0) == success, result
    return result.stdout + result.stderr


try:
    STORAGE.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix="todolist-assembled-") as cwd:
        help_text = run(cwd, "help")
        assert all(command in help_text for command in ("add", "list", "complete", "delete", "help"))
        run(cwd, "--help")
        run(cwd, "list")
        run(cwd, "add", "Buy café beans")
        run(cwd, "add", "Write report")
        data = json.loads(STORAGE.read_text())
        assert len(data) == 2
        assert [task["title"] for task in data] == ["Buy café beans", "Write report"]
        assert all(task["completed"] is False for task in data)
        first, second = (task["id"] for task in data)
        listed = run(cwd, "list")
        assert "Buy café beans" in listed and "Write report" in listed
        run(cwd, "complete", str(first))
        run(cwd, "delete", str(second))
        listed = run(cwd, "list")
        assert "Buy café beans" in listed and "Write report" not in listed
        assert json.loads(STORAGE.read_text()) == [{"id": first, "title": "Buy café beans", "completed": True}]
        snapshot = STORAGE.read_bytes()
        run(cwd, "complete", "999999", success=False)
        run(cwd, "add", success=False)
        assert STORAGE.read_bytes() == snapshot
        run(cwd, "delete", str(first))
        run(cwd, "list")
        assert json.loads(STORAGE.read_text()) == []
        assert not (Path(cwd) / "tasks.json").exists()
    lines.append("PASS: help, cross-process lifecycle, errors without mutation, Unicode titles, app-root persistence, final empty state.")
except BaseException as exc:
    lines.append(f"FAIL: {type(exc).__name__}: {exc}")
    raise
finally:
    if previous is None:
        STORAGE.unlink(missing_ok=True)
    else:
        STORAGE.write_bytes(previous)
    lines.append("Cleanup: preexisting storage restored, or generated storage removed.")
    REPORT.write_text("\n".join(lines) + "\n")
