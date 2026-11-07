"""Command-line interface for the persistent TODO app."""

import sys

from todolist.business import (
    complete_task,
    create_task,
    delete_task,
    load_tasks,
    save_tasks,
)


HELP = """Usage: todo <command>
Commands:
  add <text>
  list
  complete <id>
  delete <id>
  help"""


def main() -> None:
    args = sys.argv[1:]
    if not args or args[0] == "help":
        print(HELP)
        return

    command = args[0]
    tasks = load_tasks()

    if command == "list":
        if not tasks:
            print("No tasks.")
        for task in tasks:
            marker = "x" if task.completed else " "
            print(f"{task.id} [{marker}] {task.text}")
    elif command == "add":
        tasks = create_task(tasks, args[1])
        save_tasks(tasks)
        task = tasks[-1]
        print(f"Added task {task.id}: {task.text}")
    elif command == "complete":
        task_id = int(args[1])
        save_tasks(complete_task(tasks, task_id))
        print(f"Completed task {task_id}")
    elif command == "delete":
        task_id = int(args[1])
        save_tasks(delete_task(tasks, task_id))
        print(f"Deleted task {task_id}")
    else:
        raise SystemExit(f"Unknown command: {command}")
