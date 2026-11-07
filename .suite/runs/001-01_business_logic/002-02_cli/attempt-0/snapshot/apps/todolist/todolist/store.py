"""Task operations backed by a JSON file."""

import json
import os
import tempfile
from pathlib import Path


class TaskStore:
    """Read current tasks for each operation and save mutations atomically."""

    def __init__(self, path: str | Path | None = None):
        self.path = (
            Path(path) if path is not None
            else Path(__file__).resolve().parents[1] / "tasks.json"
        )

    def list_tasks(self) -> list[dict]:
        """Return tasks in creation order, or an empty list for a new store."""
        try:
            raw = self.path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return []
        try:
            tasks = json.loads(raw)
        except json.JSONDecodeError as error:
            raise ValueError("Task storage is not valid JSON") from error
        if not isinstance(tasks, list):
            raise ValueError("Task storage must be a JSON array")
        ids = set()
        for task in tasks:
            if (
                not isinstance(task, dict)
                or set(task) != {"id", "title", "completed"}
                or type(task["id"]) is not int
                or task["id"] <= 0
                or task["id"] in ids
                or not isinstance(task["title"], str)
                or not task["title"].strip()
                or type(task["completed"]) is not bool
            ):
                raise ValueError("Task storage contains an invalid task")
            ids.add(task["id"])
        return tasks

    def create_task(self, title: str) -> dict:
        """Create a task with a trimmed title and an unused positive ID."""
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Task title must not be empty")
        tasks = self.list_tasks()
        task = {
            "id": max((item["id"] for item in tasks), default=0) + 1,
            "title": title.strip(),
            "completed": False,
        }
        tasks.append(task)
        self._save(tasks)
        return task

    def delete_task(self, task_id: int) -> None:
        """Delete a task, raising ValueError when the ID does not exist."""
        tasks = self.list_tasks()
        task = self._find(tasks, task_id)
        tasks.remove(task)
        self._save(tasks)

    def complete_task(self, task_id: int) -> None:
        """Mark a task complete; completing it again succeeds."""
        tasks = self.list_tasks()
        task = self._find(tasks, task_id)
        if not task["completed"]:
            task["completed"] = True
            self._save(tasks)

    @staticmethod
    def _find(tasks: list[dict], task_id: int) -> dict:
        if type(task_id) is not int or task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        for task in tasks:
            if task["id"] == task_id:
                return task
        raise ValueError(f"Task {task_id} does not exist")

    def _save(self, tasks: list[dict]) -> None:
        temporary_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.path.parent,
                prefix=".tasks-", suffix=".tmp", delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)
                json.dump(tasks, temporary, ensure_ascii=False, indent=2)
                temporary.write("\n")
            os.replace(temporary_path, self.path)
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
