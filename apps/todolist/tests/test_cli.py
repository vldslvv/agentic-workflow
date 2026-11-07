"""Exercise the installed command against disposable real application storage."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest


@pytest.fixture
def app(tmp_path):
    source = Path(__file__).resolve().parents[1]
    root = tmp_path / "app"
    root.mkdir()
    shutil.copytree(source / "todolist", root / "todolist")
    for filename in ("pyproject.toml", "uv.lock"):
        shutil.copy2(source / filename, root / filename)
    env = {key: value for key, value in os.environ.items()
           if key not in {"PYTHONPATH", "VIRTUAL_ENV"}}
    subprocess.run(
        ["uv", "sync", "--locked", "--no-dev", "--python", sys.executable],
        cwd=root, env=env, capture_output=True, text=True, check=True,
    )

    def run(*args):
        return subprocess.run(
            [str(root / ".venv" / "bin" / "todolist"), *args],
            cwd=tmp_path, env=env, capture_output=True, text=True,
        )

    return run, root / "tasks.json", tmp_path


def test_cli_help_and_lifecycle_across_processes(app):
    run, store, working_directory = app
    for args in (("--help",), ("help",), ()):
        result = run(*args)
        assert result.returncode == 0, result.stderr
        assert all(word in result.stdout for word in
                   ("add", "delete", "complete", "list", "help", "TITLE", "ID"))
        assert not store.exists()
    empty = run("list")
    assert empty.returncode == 0 and "No tasks" in empty.stdout
    assert not store.exists()

    first = run("add", "Buy café beans")
    second = run("add", "Read a book")
    assert first.returncode == second.returncode == 0
    initial = json.loads(store.read_text(encoding="utf-8"))
    first_id, second_id = (task["id"] for task in initial)
    assert first_id > 0 and second_id > 0 and first_id != second_id
    assert str(first_id) in first.stdout and str(second_id) in second.stdout
    assert initial == [
        {"id": first_id, "title": "Buy café beans", "completed": False},
        {"id": second_id, "title": "Read a book", "completed": False},
    ]
    before = store.read_bytes()
    listed = run("list")
    assert listed.returncode == 0
    assert listed.stdout.splitlines() == [
        f"{first_id} [pending] Buy café beans", f"{second_id} [pending] Read a book",
    ]
    assert store.read_bytes() == before

    for _ in range(2):
        completed = run("complete", str(first_id))
        assert completed.returncode == 0 and str(first_id) in completed.stdout
    after_completion = run("list")
    assert after_completion.returncode == 0
    assert after_completion.stdout.splitlines() == [
        f"{first_id} [complete] Buy café beans", f"{second_id} [pending] Read a book",
    ]
    assert json.loads(store.read_text(encoding="utf-8")) == [
        {"id": first_id, "title": "Buy café beans", "completed": True}, initial[1],
    ]
    deleted = run("delete", str(first_id))
    assert deleted.returncode == 0 and str(first_id) in deleted.stdout
    survivor = run("list")
    assert survivor.returncode == 0
    assert survivor.stdout.strip() == f"{second_id} [pending] Read a book"
    assert json.loads(store.read_text(encoding="utf-8")) == [initial[1]]
    assert run("delete", str(second_id)).returncode == 0
    final = run("list")
    assert final.returncode == 0 and "No tasks" in final.stdout
    assert json.loads(store.read_text(encoding="utf-8")) == []
    assert not (working_directory / "tasks.json").exists()


def test_cli_rejected_commands_report_errors_and_preserve_storage(app):
    run, store, _ = app
    assert run("add", "Keep me").returncode == 0
    before = store.read_bytes()
    for args in (
        ("unknown",), ("add",), ("delete",), ("complete",),
        ("delete", "not-an-id"), ("complete", "not-an-id"),
        ("add", "   "), ("delete", "999"), ("complete", "999"),
    ):
        result = run(*args)
        assert result.returncode != 0, args
        assert "error" in result.stderr.lower(), args
        assert "Traceback" not in result.stderr, args
        assert store.read_bytes() == before, args


def test_cli_invalid_json_is_readable_and_preserved(app):
    run, store, _ = app
    store.write_text("{broken", encoding="utf-8")
    for args in (("list",), ("add", "New")):
        result = run(*args)
        assert result.returncode != 0
        assert "error" in result.stderr.lower()
        assert "Traceback" not in result.stderr
        assert store.read_text(encoding="utf-8") == "{broken"


def test_cli_filesystem_failure_is_readable(app):
    run, store, _ = app
    store.mkdir()
    result = run("add", "Cannot save")
    assert result.returncode != 0
    assert "error" in result.stderr.lower()
    assert "Traceback" not in result.stderr
    assert store.is_dir()
