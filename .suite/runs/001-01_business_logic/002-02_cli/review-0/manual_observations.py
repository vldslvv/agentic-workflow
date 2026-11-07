"""Capture the prescribed reviewer readability and entry-point observations."""
import datetime
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parents[5]
OUTPUT = Path(__file__).resolve().parent / "manual-observations.json"
records = []


def observe(argv, cwd, label):
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    clock = time.monotonic()
    result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=120)
    records.append({"label": label, "argv": argv, "cwd": str(cwd),
                    "started_at": started, "duration_seconds": time.monotonic() - clock,
                    "exit_code": result.returncode, "stdout": result.stdout,
                    "stderr": result.stderr, "timeout": False})
    OUTPUT.write_text(json.dumps(records, indent=2) + "\n")


observe(["uv", "--version"], ROOT, "environment")
observe(["uv", "run", "--project", "apps/todolist", "todo", "--help"], ROOT,
        "documented uv run entry point and root help")
with tempfile.TemporaryDirectory() as directory:
    temporary = Path(directory)
    app = temporary / "app"
    shutil.copytree(ROOT / "apps/todolist", app,
                    ignore=shutil.ignore_patterns(".venv", "__pycache__", "*.egg-info", "tasks.json", ".agents"))
    command = ["uv", "run", "--project", str(app), "todo"]
    observe(command + ["list"], temporary, "empty-list readability")
    (app / "tasks.json").write_text(json.dumps([
        {"id": 1, "title": "Buy café supplies", "completed": False},
        {"id": 2, "title": "Read book", "completed": True},
    ]), encoding="utf-8")
    observe(command + ["list"], temporary, "mixed-list readability")
    observe(command + ["complete", "abc"], temporary, "syntax-error readability")
    observe(command + ["delete", "999"], temporary, "unknown-ID readability")
    observe(command + ["add", " "], temporary, "empty-title readability")
    (app / "tasks.json").write_text("{damaged", encoding="utf-8")
    observe(command + ["list"], temporary, "corrupt-storage readability")
    (app / "tasks.json").unlink()
    (app / "tasks.json").mkdir()
    observe(command + ["list"], temporary, "unreadable-storage readability")
print(OUTPUT.read_text())
