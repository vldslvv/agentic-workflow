"""Command-line interface for the TODO app."""

import argparse
import sys

from todolist import TaskStore


def main() -> int:
    parser = argparse.ArgumentParser(prog="todolist", description="Manage your TODO list.")
    commands = parser.add_subparsers(dest="command")
    add = commands.add_parser("add", help="Add a task")
    add.add_argument("title", help="Task title (quote titles containing spaces)")
    commands.add_parser("list", help="List tasks and their completion status")
    for command, description in (("complete", "Complete a task"), ("delete", "Delete a task")):
        subparser = commands.add_parser(command, help=description)
        subparser.add_argument("id", type=int, help="Task ID shown by list")
    commands.add_parser("help", help="Show this help message")
    args = parser.parse_args()

    if args.command in (None, "help"):
        parser.print_help()
        return 0

    store = TaskStore()
    try:
        if args.command == "add":
            task = store.create(args.title)
            print(f"Added task {task['id']}: {task['title']}")
        elif args.command == "list":
            tasks = store.list()
            if not tasks:
                print("No tasks yet.")
            for task in tasks:
                status = "completed" if task["completed"] else "pending"
                print(f"{task['id']} [{status}] {task['title']}")
        elif args.command == "complete":
            task = store.complete(args.id)
            print(f"Completed task {task['id']}: {task['title']}")
        elif args.command == "delete":
            store.delete(args.id)
            print(f"Deleted task {args.id}.")
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0
