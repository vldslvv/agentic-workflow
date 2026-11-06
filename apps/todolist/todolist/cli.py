"""Command-line interface for the project-local task store."""

import argparse
import sys
from pathlib import Path

from todolist.core import TaskStore, TodoError


def positive_id(value: str) -> int:
    try:
        task_id = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("task ID must be a positive integer") from None
    if task_id <= 0:
        raise argparse.ArgumentTypeError("task ID must be a positive integer")
    return task_id


def main() -> int:
    parser = argparse.ArgumentParser(prog="todo", description="Manage your tasks.")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="Add a task")
    add.add_argument("title", help="Task title (quote titles containing spaces)")
    for name, description in (("delete", "Delete a task"), ("complete", "Mark a task complete")):
        command = commands.add_parser(name, help=description)
        command.add_argument("id", type=positive_id, help="Task ID shown by list")
    commands.add_parser("list", help="List all tasks")
    commands.add_parser("help", help="Show this help message")
    args = parser.parse_args()

    if args.command == "help":
        parser.print_help()
        return 0

    store = TaskStore(Path(__file__).resolve().parent.parent / "tasks.json")
    try:
        if args.command == "add":
            task = store.create(args.title)
            print(f"Added task {task.id}: {task.title}")
        elif args.command == "delete":
            store.delete(args.id)
            print(f"Deleted task {args.id}.")
        elif args.command == "complete":
            store.complete(args.id)
            print(f"Completed task {args.id}.")
        elif args.command == "list":
            tasks = store.list()
            if not tasks:
                print("No tasks.")
            for task in tasks:
                marker = "[x]" if task.completed else "[ ]"
                print(f"{task.id} {marker} {task.title}")
    except TodoError as error:
        print(f"todo: {error}", file=sys.stderr)
        return 1
    return 0
