"""Command-line interface for the TODO app."""

import argparse
import sys

from . import TaskStore


def main() -> int:
    parser = argparse.ArgumentParser(prog="todo", description="Manage your TODO tasks.")
    commands = parser.add_subparsers(dest="command")
    add = commands.add_parser("add", help="Add a task (quote multiword titles)")
    add.add_argument("title", metavar="TITLE", help="Task title")
    for command, description in (
        ("delete", "Delete a task"),
        ("complete", "Mark a task complete"),
    ):
        subparser = commands.add_parser(command, help=description)
        subparser.add_argument("id", metavar="ID", type=int, help="Task ID from list")
    commands.add_parser("list", help="List tasks and their completion state")
    commands.add_parser("help", help="Show this help")
    args = parser.parse_args()

    if args.command in (None, "help"):
        parser.print_help()
        return 0

    store = TaskStore()
    try:
        if args.command == "add":
            task = store.create_task(args.title)
            print(f"Added task {task['id']}: {task['title']}")
        elif args.command == "delete":
            store.delete_task(args.id)
            print(f"Deleted task {args.id}.")
        elif args.command == "complete":
            store.complete_task(args.id)
            print(f"Completed task {args.id}.")
        elif args.command == "list":
            tasks = store.list_tasks()
            if not tasks:
                print("No tasks.")
            for task in tasks:
                marker = "x" if task["completed"] else " "
                print(f"{task['id']} [{marker}] {task['title']}")
    except (ValueError, OSError) as error:
        print(f"todo: error: {error}", file=sys.stderr)
        return 1
    return 0
