"""Preserve generated application and trial evidence before removing a checkout."""

import json
import shutil
from pathlib import Path

from . import runtime, trial


def archive_evidence(worktree: Path, destination: Path) -> None:
    results = trial.safe_path(worktree, trial.RESULTS)
    if results.is_dir():
        shutil.copytree(
            results,
            destination,
            dirs_exist_ok=True,
            symlinks=True,
            ignore=shutil.ignore_patterns("uv-cache"),
        )
    app = trial.safe_path(worktree, trial.APP)
    if app.is_dir():
        shutil.copytree(
            app,
            destination / "app",
            symlinks=True,
            ignore=shutil.ignore_patterns(".venv", "__pycache__"),
        )
    result_path = trial.safe_path(destination, Path("result.json"))
    if result_path.is_file():
        report = json.loads(result_path.read_text())
        for name in report.get("records_created", []):
            if not isinstance(name, str) or name in ("", ".", "..") or Path(name).name != name:
                raise runtime.RunnerError("Invalid records path in eval result")
            source = trial.safe_path(worktree, Path(".agentic-workflow/records") / name)
            if source.is_dir():
                shutil.copytree(source, destination / "records" / name, symlinks=True)
