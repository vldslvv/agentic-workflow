import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from todolist import (
    DEFAULT_TASKS_PATH,
    Task,
    complete_task,
    create_task,
    delete_task,
    list_tasks,
)


def test_task_lifecycle_survives_another_process(tmp_path):
    path = tmp_path / "tasks.json"
    assert list_tasks(path=path) == []
    assert not path.exists()

    first = create_task("  Buy café beans  ", path=path)
    second = create_task("Read book", path=path)
    assert first.title == "Buy café beans"
    assert second.title == "Read book"
    assert first.id > 0 and second.id > 0 and first.id != second.id
    assert not first.completed and not second.completed
    original = path.read_bytes()
    assert list_tasks(path=path) == [first, second]
    assert list_tasks(path=path) == [first, second]
    assert path.read_bytes() == original

    completed = complete_task(first.id, path=path)
    assert completed == Task(first.id, "Buy café beans", True)
    assert list_tasks(path=path) == [completed, second]
    assert complete_task(first.id, path=path) == completed
    delete_task(second.id, path=path)

    result = subprocess.run(
        [sys.executable, "-c", """
import json, sys
from dataclasses import asdict
from pathlib import Path
from todolist import list_tasks
print(json.dumps([asdict(task) for task in list_tasks(path=Path(sys.argv[1]))]))
""", str(path)],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    )
    expected = [{"id": first.id, "title": "Buy café beans", "completed": True}]
    assert json.loads(result.stdout) == expected
    assert json.loads(path.read_text(encoding="utf-8")) == expected

    # Removing a lower ID must never renumber a surviving task or cause collision.
    third = create_task("Third", path=path)
    delete_task(first.id, path=path)
    fourth = create_task("Fourth", path=path)
    assert list_tasks(path=path) == [third, fourth]
    assert fourth.id != third.id


@pytest.mark.parametrize("operation", [
    lambda path: create_task(" \t\n", path=path),
    lambda path: delete_task(999, path=path),
    lambda path: complete_task(999, path=path),
])
def test_rejected_changes_preserve_store(tmp_path, operation):
    path = tmp_path / "tasks.json"
    create_task("Keep", path=path)
    original = path.read_bytes()
    with pytest.raises(ValueError):
        operation(path)
    assert path.read_bytes() == original


@pytest.mark.parametrize("contents", [
    "{broken",
    "{}",
    '[{"id": 1, "title": "Missing status"}]',
    '[{"id": true, "title": "Bad ID", "completed": false}]',
    '[{"id": 0, "title": "Bad ID", "completed": false}]',
    '[{"id": 1, "title": " ", "completed": false}]',
    '[{"id": 1, "title": "Bad status", "completed": "false"}]',
    '[{"id": 1, "title": "A", "completed": false},'
    ' {"id": 1, "title": "B", "completed": true}]',
])
def test_invalid_storage_is_rejected_without_overwrite(tmp_path, contents):
    path = tmp_path / "tasks.json"
    path.write_text(contents, encoding="utf-8")
    for operation in (
        lambda: list_tasks(path=path),
        lambda: create_task("New", path=path),
        lambda: complete_task(1, path=path),
        lambda: delete_task(1, path=path),
    ):
        with pytest.raises(ValueError):
            operation()
        assert path.read_text(encoding="utf-8") == contents


def test_filesystem_errors_surface(tmp_path):
    with pytest.raises(OSError):
        list_tasks(path=tmp_path)
    with pytest.raises(OSError):
        create_task("Cannot save", path=tmp_path / "missing" / "tasks.json")


def test_default_store_is_project_relative_from_another_directory(tmp_path):
    expected = Path(__file__).resolve().parents[1] / "tasks.json"
    assert DEFAULT_TASKS_PATH == expected
    result = subprocess.run(
        [sys.executable, "-c",
         "from todolist import DEFAULT_TASKS_PATH; print(DEFAULT_TASKS_PATH)"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
        env={key: value for key, value in os.environ.items() if key != "PYTHONPATH"},
    )
    assert Path(result.stdout.strip()) == expected
