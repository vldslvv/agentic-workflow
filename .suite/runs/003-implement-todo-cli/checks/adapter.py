"""Frozen process adapter. No imports from candidate application code."""
import base64
import json
import os
from pathlib import Path
import subprocess


def snapshot(path):
    path = Path(path)
    if not path.exists():
        return {"exists": False}
    if path.is_dir():
        return {"exists": True, "directory": True}
    try:
        return {"exists": True, "base64": base64.b64encode(path.read_bytes()).decode()}
    except OSError as exc:
        return {"exists": True, "unreadable": str(exc)}


class Adapter:
    def __init__(self, app, evidence):
        self.app = Path(app).resolve()
        self.evidence = Path(evidence).resolve()
        self.evidence.mkdir(parents=True, exist_ok=True)
        self.records = []

    def execute(self, args, cwd, path=None, offline_namespace=False, raw=False):
        command = list(args) if raw else [
            "uv", "run", "--offline", "--no-sync", "--project", str(self.app), "todo", *args
        ]
        if offline_namespace:
            command = ["unshare", "-Urn", "--", *command]
        before = snapshot(path) if path else None
        env = dict(os.environ, NO_COLOR="1", UV_NO_PROGRESS="1", PYTHONUTF8="1")
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, timeout=45)
        record = {
            "command": command, "cwd": str(cwd), "exit_code": result.returncode,
            "stdout": result.stdout.decode("utf-8", "replace"),
            "stderr": result.stderr.decode("utf-8", "replace"),
            "stdout_base64": base64.b64encode(result.stdout).decode(),
            "stderr_base64": base64.b64encode(result.stderr).decode(),
            "before": before, "after": snapshot(path) if path else None,
        }
        self.records.append(record)
        (self.evidence / "commands.json").write_text(json.dumps(self.records, indent=2) + "\n")
        return result
