"""Task operations backed by a JSON file in the application root."""

import json
import os
from pathlib import Path
import tempfile


class TaskStore:
    """Read current tasks on every operation and persist successful mutations.

    Tasks are dictionaries with integer ``id``, string ``title``, and boolean
    ``completed`` fields. Invalid input, malformed storage, and unknown IDs raise
    ValueError. Filesystem errors propagate as OSError. Concurrent writers are
    outside this small store's contract.
    """

    def __init__(self, path: str | Path | None = None):
        self.path = (
            Path(path) if path is not None
            else Path(__file__).resolve().parent.parent / "tasks.json"
        )

    def list(self) -> list[dict]:
        """Return all tasks, or an empty list if the file does not exist."""
        try:
            raw = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return []
        try:
            tasks = json.loads(raw)
        except (json.JSONDecodeError, UnicodeError) as exc:
            raise ValueError(f"Invalid task storage: {self.path}") from exc
        if not isinstance(tasks, list):
            raise ValueError("Invalid task storage: expected a JSON list")
        ids = set()
        for task in tasks:
            if (
                not isinstance(task, dict)
                or set(task) != {"id", "title", "completed"}
                or type(task["id"]) is not int
                or task["id"] <= 0
                or not isinstance(task["title"], str)
                or not task["title"].strip()
                or type(task["completed"]) is not bool
            ):
                raise ValueError("Invalid task storage: invalid task fields")
            if task["id"] in ids:
                raise ValueError("Invalid task storage: duplicate task ID")
            ids.add(task["id"])
        return tasks

    def create(self, title: str) -> dict:
        """Create an incomplete task with a positive ID and return it."""
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must not be blank")
        tasks = self.list()
        task = {
            "id": max((item["id"] for item in tasks), default=0) + 1,
            "title": title.strip(),
            "completed": False,
        }
        tasks.append(task)
        self._save(tasks)
        return task

    def complete(self, task_id: int) -> dict:
        """Mark a task complete and return it; repeated completion is harmless."""
        tasks, task = self._find(task_id)
        task["completed"] = True
        self._save(tasks)
        return task

    def delete(self, task_id: int) -> None:
        """Delete the selected task, reporting unknown IDs without mutation."""
        tasks, task = self._find(task_id)
        tasks.remove(task)
        self._save(tasks)

    def _find(self, task_id: int) -> tuple[list[dict], dict]:
        if type(task_id) is not int or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        tasks = self.list()
        for task in tasks:
            if task["id"] == task_id:
                return tasks, task
        raise ValueError(f"Task {task_id} not found")

    def _save(self, tasks: list[dict]) -> None:
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.path.parent,
                prefix=f".{self.path.name}.", suffix=".tmp", delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)
                json.dump(tasks, temporary, ensure_ascii=False, indent=2)
                temporary.write("\n")
            os.replace(temporary_path, self.path)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
