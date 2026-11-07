"""Explicit JSON persistence boundary for the public task operations."""

import json
from dataclasses import asdict
from pathlib import Path

from . import domain
from .domain import Task

DEFAULT_TASKS_PATH = Path(__file__).resolve().parent.parent / "tasks.json"


def list_tasks(*, path: Path = DEFAULT_TASKS_PATH) -> list[Task]:
    """Read tasks in insertion order; a missing file represents an empty store."""
    try:
        contents = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    records = json.loads(contents)
    if not isinstance(records, list):
        raise ValueError("Task storage must contain a JSON list.")
    tasks = []
    ids = set()
    for record in records:
        if (
            not isinstance(record, dict)
            or set(record) != {"id", "title", "completed"}
            or type(record["id"]) is not int
            or record["id"] <= 0
            or record["id"] in ids
            or not isinstance(record["title"], str)
            or not record["title"].strip()
            or type(record["completed"]) is not bool
        ):
            raise ValueError("Task storage contains an invalid task record.")
        ids.add(record["id"])
        tasks.append(Task(**record))
    return tasks


def _save(tasks: list[Task], path: Path) -> None:
    path.write_text(
        json.dumps([asdict(task) for task in tasks], indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )


def create_task(title: str, *, path: Path = DEFAULT_TASKS_PATH) -> Task:
    tasks, created = domain.add(list_tasks(path=path), title)
    _save(tasks, path)
    return created


def delete_task(task_id: int, *, path: Path = DEFAULT_TASKS_PATH) -> None:
    tasks = domain.remove(list_tasks(path=path), task_id)
    _save(tasks, path)


def complete_task(task_id: int, *, path: Path = DEFAULT_TASKS_PATH) -> Task:
    tasks, completed = domain.complete(list_tasks(path=path), task_id)
    _save(tasks, path)
    return completed
