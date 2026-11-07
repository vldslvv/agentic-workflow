"""Task transformations and explicit JSON storage boundaries."""

import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path


TASKS_PATH = Path(__file__).resolve().parent.parent / "tasks.json"


@dataclass(frozen=True)
class Task:
    id: int
    text: str
    completed: bool = False


def create_task(tasks: list[Task], text: str) -> list[Task]:
    task_id = max((task.id for task in tasks), default=0) + 1
    return [*tasks, Task(task_id, text)]


def complete_task(tasks: list[Task], task_id: int) -> list[Task]:
    return [replace(task, completed=True) if task.id == task_id else task for task in tasks]


def delete_task(tasks: list[Task], task_id: int) -> list[Task]:
    return [task for task in tasks if task.id != task_id]


def load_tasks(path: Path = TASKS_PATH) -> list[Task]:
    if not path.exists():
        return []
    return [Task(**item) for item in json.loads(path.read_text(encoding="utf-8"))]


def save_tasks(tasks: list[Task], path: Path = TASKS_PATH) -> None:
    path.write_text(
        json.dumps([asdict(task) for task in tasks], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
