#!/usr/bin/env python3
"""Validate a project's curated memory without following its Source references.

CLI: project_memory.py MEMORY_DIRECTORY
Missing directory means no notes yet. Existing memory requires index.md and
one indexed entries/<short-name>.md per note. Reports structure, not truth.
"""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import sys

FIELDS = ('Kind', 'Use when', 'Source', 'Last checked')
KINDS = {'navigation', 'command', 'pitfall', 'decision'}
INDEX_ROW = re.compile(r'- \[([^\]]+)\]\(([^)]+)\) — Read when (\S.*)')
ENTRY_PATH = re.compile(r'entries/[a-z0-9]+(?:-[a-z0-9]+)*\.md')


def _contained_file(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f'memory link escapes directory: {relative}')
    if not path.is_file():
        raise ValueError(f'missing memory file (broken link): {relative}')
    return path


def _validate_entry(path, label):
    lines = path.read_text(encoding='utf-8').splitlines()
    if not lines or not re.fullmatch(r'# \S.*', lines[0]):
        raise ValueError(f'{label}: missing title')
    fields, body = {}, []
    for line in lines[1:]:
        match = re.fullmatch(r'- (Kind|Use when|Source|Last checked):\s*(.*)', line)
        if match:
            key, value = match.groups()
            if key in fields:
                raise ValueError(f'{label}: duplicate field {key}')
            fields[key] = value.strip()
        elif line.strip():
            body.append(line)
    for key in FIELDS:
        if not fields.get(key):
            raise ValueError(f'{label}: missing field {key}')
    if fields['Kind'] not in KINDS:
        raise ValueError(f'{label}: invalid Kind {fields["Kind"]!r}')
    stamp = fields['Last checked']
    try:
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', stamp):
            raise ValueError()
        date.fromisoformat(stamp)
    except ValueError:
        raise ValueError(f'{label}: invalid Last checked date {stamp!r}; expected YYYY-MM-DD') from None
    if not body:
        raise ValueError(f'{label}: missing lesson body')


def validate_memory(directory):
    root = Path(directory)
    if not root.exists() and not root.is_symlink():
        return {'status': 'NO_MEMORY', 'entries': []}
    root = root.resolve()
    index = _contained_file(root, 'index.md')
    lines = index.read_text(encoding='utf-8').splitlines()
    if not lines or lines[0] != '# Project memory':
        raise ValueError('index.md: expected # Project memory heading')
    entries, seen = [], set()
    for number, line in enumerate(lines[1:], 2):
        if not line.strip():
            continue
        match = INDEX_ROW.fullmatch(line)
        if not match:
            raise ValueError(f'index.md:{number}: expected one entry link and Read when hint')
        title, relative, hint = match.groups()
        if not title.strip() or re.search(r'\[[^\]]*\]\(', hint):
            raise ValueError(f'index.md:{number}: expected one entry link and Read when hint')
        path = _contained_file(root, relative)
        if not ENTRY_PATH.fullmatch(relative):
            raise ValueError(f'index.md:{number}: link must use entries/<short-name>.md: {relative}')
        if path in seen:
            raise ValueError(f'index.md:{number}: duplicate entry link: {relative}')
        seen.add(path)
        _validate_entry(path, relative)
        entries.append({'path': relative, 'title': title, 'use_when': hint})
    indexed = {entry['path'] for entry in entries}
    if not (root / 'entries').resolve().is_relative_to(root):
        raise ValueError('memory entries directory escapes directory')
    for path in sorted((root / 'entries').glob('*.md')):
        relative = path.relative_to(root).as_posix()
        _contained_file(root, relative)
        if relative not in indexed:
            raise ValueError(f'entry missing from index: {relative}')
    return {'status': 'PASS', 'entries': entries}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(validate_memory(args.directory), indent=2))
    except (OSError, ValueError) as exc:
        print(f'project-memory: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
