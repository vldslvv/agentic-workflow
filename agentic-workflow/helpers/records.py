#!/usr/bin/env python3
"""Allocate implementations and resolve tasks, capturing the current native turn.

CLI: records.py allocate NAME --records-root .agentic-workflow
     records.py resolve IMPLEMENTATION TASK
Native capture is best effort; missing telemetry never blocks task work.
"""
import argparse
from contextlib import contextmanager
import fcntl
import os
from pathlib import Path
import re
import tempfile
import sys


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', value):
        raise ValueError(f'unsafe identifier: {value!r}')
    return value


@contextmanager
def locked(path):
    """Serialize allocation/native capture/report refresh; locks release on process exit."""
    flags = os.O_RDONLY if Path(path).is_dir() else os.O_WRONLY | os.O_CREAT
    descriptor = os.open(path, flags, 0o666)
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX)
        yield
    finally:
        os.close(descriptor)


def write_atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.write-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb' if isinstance(data, bytes) else 'w') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def allocate(records_root, name):
    identifier(name)
    records_root = Path(records_root)
    records_root.mkdir(parents=True, exist_ok=True)
    with locked(records_root):
        numbers = [int(match[1]) for p in records_root.iterdir()
                   if p.is_dir() and (match := re.fullmatch(r'(\d{3,})_.+', p.name))]
        root = records_root / f'{max(numbers, default=0) + 1:03d}_{name}'
        root.mkdir()  # Reserve before writing; an interrupted allocation is not reused.
        for directory in ('tasks', 'runs', 'reports'):
            (root / directory).mkdir()
        from native_traces import capture_current
        with locked(root / '.records.lock'):
            capture_diagnostics = capture_current(root)
        for diagnostic in capture_diagnostics:
            print('records: ' + diagnostic['code'], file=sys.stderr)
    return root


def resolve_task(root, task):
    root = Path(root)
    target = root / 'tasks' / identifier(task)
    if not target.is_dir() or not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('task absent from identified implementation')
    from native_traces import capture_current
    with locked(root / '.records.lock'):
        for diagnostic in capture_current(root):
            print('records: ' + diagnostic['code'], file=sys.stderr)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    allocate_parser = commands.add_parser('allocate')
    allocate_parser.add_argument('name')
    allocate_parser.add_argument('--records-root', type=Path, default=Path('.agentic-workflow'))
    resolve_parser = commands.add_parser('resolve')
    resolve_parser.add_argument('implementation', type=Path)
    resolve_parser.add_argument('task')
    args = parser.parse_args()
    try:
        if args.command == 'allocate':
            print(allocate(args.records_root, args.name))
        else:
            print(resolve_task(args.implementation, args.task))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'records: {exc}\n')


if __name__ == '__main__':
    main()
