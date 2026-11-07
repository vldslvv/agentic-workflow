"""Command-line boundary for the public TODO operations."""

import argparse
import sys

from todolist import complete_task, create_task, delete_task, list_tasks


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage your TODO tasks.")
    commands = parser.add_subparsers(dest="command")
    add = commands.add_parser("add", help="add TITLE: create a task")
    add.add_argument("title", metavar="TITLE", help="task title (quote multiple words)")
    delete = commands.add_parser("delete", help="delete ID: remove a task")
    delete.add_argument("id", type=int, metavar="ID", help="task ID from list")
    complete = commands.add_parser("complete", help="complete ID: mark a task done")
    complete.add_argument("id", type=int, metavar="ID", help="task ID from list")
    commands.add_parser("list", help="show task IDs, titles and completion states")
    commands.add_parser("help", help="show this help")
    args = parser.parse_args()

    try:
        if args.command == "add":
            task = create_task(args.title)
            print(f"Added task {task.id}: {task.title}")
        elif args.command == "delete":
            delete_task(args.id)
            print(f"Deleted task {args.id}.")
        elif args.command == "complete":
            task = complete_task(args.id)
            print(f"Completed task {task.id}: {task.title}")
        elif args.command == "list":
            tasks = list_tasks()
            for task in tasks:
                status = "complete" if task.completed else "pending"
                print(f"{task.id} [{status}] {task.title}")
            if not tasks:
                print("No tasks.")
        else:
            parser.print_help()
    except (ValueError, OSError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0
