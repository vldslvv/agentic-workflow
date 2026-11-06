"""Task operations backed by a JSON file."""

import json
import os
import tempfile
from dataclasses import asdict, dataclass, replace
from pathlib import Path


class TodoError(Exception):
    """An invalid task operation or inaccessible task storage."""


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    completed: bool = False


class TaskStore:
    """Read current tasks on each operation and persist successful changes."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def list(self) -> list[Task]:
        try:
            raw = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return []
        except (OSError, UnicodeError) as error:
            raise TodoError(f"Cannot read tasks from {self.path}: {error}") from error

        try:
            records = json.loads(raw)
        except ValueError as error:
            raise TodoError(f"Invalid task data in {self.path}: {error}") from error
        if not isinstance(records, list):
            raise TodoError(f"Invalid task data in {self.path}: expected an array")

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
                or record["title"] != record["title"].strip()
                or type(record["completed"]) is not bool
            ):
                raise TodoError(f"Invalid task record in {self.path}")
            tasks.append(Task(**record))
            ids.add(record["id"])
        return tasks

    def create(self, title: str) -> Task:
        if not isinstance(title, str) or not title.strip():
            raise TodoError("Task title must not be blank")
        tasks = self.list()
        task = Task(max((task.id for task in tasks), default=0) + 1, title.strip())
        self._save([*tasks, task])
        return task

    def delete(self, task_id: int) -> None:
        tasks = self.list()
        index = self._find(tasks, task_id)
        del tasks[index]
        self._save(tasks)

    def complete(self, task_id: int) -> None:
        tasks = self.list()
        index = self._find(tasks, task_id)
        if not tasks[index].completed:
            tasks[index] = replace(tasks[index], completed=True)
            self._save(tasks)

    @staticmethod
    def _find(tasks: list[Task], task_id: int) -> int:
        if type(task_id) is int and task_id > 0:
            for index, task in enumerate(tasks):
                if task.id == task_id:
                    return index
        raise TodoError(f"Task {task_id} not found")

    def _save(self, tasks: list[Task]) -> None:
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.path.parent,
                prefix=f".{self.path.name}.", suffix=".tmp", delete=False,
            ) as stream:
                temporary = Path(stream.name)
                json.dump([asdict(task) for task in tasks], stream, ensure_ascii=False, indent=2)
                stream.write("\n")
            os.replace(temporary, self.path)
        except (OSError, UnicodeError) as error:
            raise TodoError(f"Cannot save tasks to {self.path}: {error}") from error
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
