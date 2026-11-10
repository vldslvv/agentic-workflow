"""Independent persistent CLI fixture, with deliberate contract violations."""

import json
import os
import sys
from collections.abc import Iterator
from pathlib import Path
from typing import NotRequired, TypedDict


class Task(TypedDict):
    id: int
    text: str
    done: bool
    parent: int | None
    extra: NotRequired[str]


mode = os.environ.get("EVAL_FIXTURE", "pass")
path = Path("other.json" if mode == "wrong_storage" else "tasks.json")
tasks: list[Task] = json.loads(path.read_text()) if path.exists() else []
command, *args = sys.argv[1:]
if command == "list":

    def lines(parent: int | None = None, depth: int = 0) -> Iterator[str]:
        for task in sorted(tasks, key=lambda item: item["id"]):
            if task["parent"] == parent:
                yield f"{'  ' * depth}{task['id']} [{'x' if task['done'] else ' '}] {task['text']}"
                yield from lines(task["id"], depth + 1)

    output = "\n".join(lines()) or "No tasks."
    if mode == "wrong_order" and any(t["parent"] for t in tasks):
        output = "\n".join(reversed(output.splitlines()))
elif command == "help":
    output = "Usage: todo <command>\nCommands:\n  add <text> [--parent <id>]\n  list\n  complete <id>\n  delete <id>\n  help"
else:
    if command == "add":
        parents = [int(args[i + 1]) for i, arg in enumerate(args) if arg == "--parent"]
        if len(parents) > 1 or (parents and not any(t["id"] == parents[0] for t in tasks)):
            if mode == "invalid_mutation":
                tasks[0]["done"] = True
                path.write_text(json.dumps(tasks))
            elif mode == "invalid_metadata":
                tasks[0]["extra"] = "changed without changing the listing"
                path.write_text(json.dumps(tasks))
            elif mode == "invalid_reformat":
                path.write_text(json.dumps(tasks, indent=4))
            sys.exit(2)
        parent = parents[0] if parents and mode != "ignore_parent" else None
        task: Task = {
            "id": max((t["id"] for t in tasks), default=0) + 1,
            "text": args[0],
            "done": False,
            "parent": parent,
        }
        tasks.append(task)
        output = f"Added task {task['id']}: {task['text']}"
    else:
        task_id = int(args[0])
        if command == "complete":
            next(t for t in tasks if t["id"] == task_id)["done"] = True
            output = f"Completed task {task_id}"
        else:
            removed = {task_id}
            if mode != "keep_descendants":
                while True:
                    descendants = {t["id"] for t in tasks if t["parent"] in removed}
                    if descendants <= removed:
                        break
                    removed |= descendants
            tasks = [t for t in tasks if t["id"] not in removed]
            # Surface orphaned descendants so listing exposes incomplete deletion.
            if mode == "keep_descendants":
                for task in tasks:
                    if task["parent"] in removed:
                        task["parent"] = None
            output = f"Deleted task {task_id}"
    path.write_text(json.dumps(tasks))
ending = "" if mode == "no_newline" else "\r\n" if mode == "crlf" else "\n"
sys.stdout.write(("Wrong output" if mode == "wrong_output" else output) + ending)
if mode == "cli_nonzero":
    sys.exit(7)
