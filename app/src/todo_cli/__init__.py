"""Local checklist storage and command-line operations."""

import argparse
from dataclasses import dataclass, replace
import os
from pathlib import Path
import re
import sys
import tempfile
import unicodedata


class DataError(Exception):
    """An invalid checklist or an operation on an unknown task."""


@dataclass(frozen=True)
class Task:
    id: int
    done: bool
    text: str

    def record(self) -> str:
        return f"{self.id} [{'x' if self.done else ' '}] {self.text}\n"


def normalized_text(value: str) -> str:
    for character in value:
        if unicodedata.category(character) == "Cc" or character in "\u2028\u2029":
            raise ValueError(f"text contains forbidden character U+{ord(character):04X}")
    value = value.strip()
    if not value:
        raise ValueError("text must not be empty or whitespace-only")
    return value


def argument_text(value: str) -> str:
    try:
        return normalized_text(value)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error


def argument_id(value: str) -> int:
    if not re.fullmatch(r"[1-9][0-9]*", value):
        raise argparse.ArgumentTypeError(f"invalid ID {value!r}; expected a positive ASCII decimal without leading zeros")
    return int(value)


def read_tasks(path: Path) -> list[Task]:
    try:
        content = path.read_bytes()
    except FileNotFoundError:
        return []
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        line = content[:error.start].count(b"\n") + 1
        raise DataError(f"{path}: line {line}: invalid UTF-8") from error

    tasks = []
    seen = set()
    lines = text.split("\n")
    for number, line in enumerate(lines, 1):
        # Only CR directly before LF is a line terminator. Other controls in
        # actual records must reach text validation without being stripped.
        if number < len(lines) and line.endswith("\r"):
            line = line[:-1]
        if not line.strip():
            continue
        match = re.fullmatch(r"([1-9][0-9]*) \[( |x)\] (.*)", line)
        if match is None:
            raise DataError(f"{path}: line {number}: invalid checklist record")
        task_id = int(match[1])
        if task_id in seen:
            raise DataError(f"{path}: line {number}: duplicate ID {task_id}")
        try:
            description = normalized_text(match[3])
        except ValueError as error:
            raise DataError(f"{path}: line {number}: {error}") from error
        tasks.append(Task(task_id, match[2] == "x", description))
        seen.add(task_id)
    return tasks


def write_tasks(path: Path, tasks: list[Task]) -> None:
    """Finish a same-directory temporary file before atomically replacing storage."""
    content = "".join(task.record() for task in tasks).encode("utf-8")
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=path.parent, prefix=".todo-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(prog="todo", description="Manage an editable local text checklist.", allow_abbrev=False)
    result.add_argument("--file", type=Path, help="checklist path, relative to the current working directory")
    commands = result.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="append an open task", allow_abbrev=False)
    add.add_argument("text", type=argument_text, metavar="TEXT")
    listing = commands.add_parser("list", help="list tasks in file order", allow_abbrev=False)
    listing.add_argument("--status", choices=("open", "done", "all"), default="all")
    for name, help_text in (("complete", "mark a task complete"), ("reopen", "mark a task open"), ("edit", "change task text"), ("delete", "remove a task")):
        command = commands.add_parser(name, help=help_text, allow_abbrev=False)
        command.add_argument("id", type=argument_id, metavar="ID")
        if name == "edit":
            command.add_argument("text", type=argument_text, metavar="TEXT")
    return result


def execute(args: argparse.Namespace) -> str:
    tasks = read_tasks(args.file)
    if args.command == "list":
        return "".join(task.record() for task in tasks if args.status == "all" or task.done == (args.status == "done"))
    if args.command == "add":
        affected = Task(max((task.id for task in tasks), default=0) + 1, False, args.text)
        tasks.append(affected)
    else:
        index = next((index for index, task in enumerate(tasks) if task.id == args.id), None)
        if index is None:
            raise DataError(f"{args.file}: unknown task ID {args.id}")
        previous = tasks[index]
        if args.command == "delete":
            affected = tasks.pop(index)
        else:
            affected = replace(previous, text=args.text) if args.command == "edit" else replace(previous, done=args.command == "complete")
            if affected == previous:
                return affected.record()
            tasks[index] = affected
    write_tasks(args.file, tasks)
    return affected.record()


def main() -> int:
    # The file contract places no size limit on otherwise valid decimal IDs.
    sys.set_int_max_str_digits(0)
    cli = parser()
    args = cli.parse_args()
    if args.file is None:
        cli.error("--file PATH is required for task operations")
    try:
        output = execute(args)
    except (DataError, OSError) as error:
        print(f"todo: {args.file}: {error}" if isinstance(error, OSError) else f"todo: {error}", file=sys.stderr)
        return 1
    sys.stdout.write(output)
    return 0
