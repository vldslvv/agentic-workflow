"""Task values and pure state transitions."""

from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Task:
    id: int
    title: str
    completed: bool = False


def add(tasks: list[Task], title: str) -> tuple[list[Task], Task]:
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Task title must not be blank.")
    task = Task(max((task.id for task in tasks), default=0) + 1, title.strip())
    return [*tasks, task], task


def remove(tasks: list[Task], task_id: int) -> list[Task]:
    find(tasks, task_id)
    return [task for task in tasks if task.id != task_id]


def complete(tasks: list[Task], task_id: int) -> tuple[list[Task], Task]:
    completed = replace(find(tasks, task_id), completed=True)
    return [completed if task.id == task_id else task for task in tasks], completed


def find(tasks: list[Task], task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task
    raise ValueError(f"Task {task_id} does not exist.")
