"""Small independent persistent CLI used only to exercise the evaluator."""

import json
import os
from pathlib import Path
import sys


mode = os.environ.get("EVAL_FIXTURE", "pass")
path = Path("other.json" if mode == "wrong_storage" else "tasks.json")
tasks = json.loads(path.read_text()) if path.exists() else []
command, *args = sys.argv[1:]
if command == "list":
    output = "\n".join(f"{t['id']} [{'x' if t['done'] else ' '}] {t['text']}" for t in tasks) or "No tasks."
elif command == "help":
    output = "Usage: todo <command>\nCommands:\n  add <text>\n  list\n  complete <id>\n  delete <id>\n  help"
else:
    if command == "add":
        task = {"id": max((t["id"] for t in tasks), default=0) + 1, "text": args[0], "done": False}
        tasks.append(task)
        output = f"Added task {task['id']}: {task['text']}"
    else:
        task_id = int(args[0])
        if command == "complete":
            next(t for t in tasks if t["id"] == task_id)["done"] = True
            output = f"Completed task {task_id}"
        else:
            tasks = [t for t in tasks if t["id"] != task_id]
            output = f"Deleted task {task_id}"
    path.write_text(json.dumps(tasks))
ending = "" if mode == "no_newline" else "\r\n" if mode == "crlf" else "\n"
sys.stdout.write(("Wrong output" if mode == "wrong_output" else output) + ending)
if mode == "cli_nonzero":
    sys.exit(7)
