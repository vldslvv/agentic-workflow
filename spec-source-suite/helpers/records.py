#!/usr/bin/env python3
"""Implementation records (stdlib, local filesystem).

CLI: records.py allocate NAME --suite .suite
     records.py source IMPLEMENTATION SOURCE.json
     records.py bind IMPLEMENTATION BINDING.json
     records.py resolve IMPLEMENTATION TASK

implementation.json v2: implementation_id, sources[], bindings[]. Sources:
{id, adapter, source_version, path, session_id, turn_ids}. Paths are relative to
implementation root or absolute. Bindings: {id, source_id, turn_ids, task_id,
role, agent_run_id, agent_name?, purpose?, requested?: {model, reasoning_effort}}. Append a binding for
new turns/assignments; never reassign an already bound turn. One native session
keeps one agent_run_id across follow-ups; replacements use new native identities.
Add sources explicitly to the manifest, then bind; no history discovery.
"""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import json
import os
from pathlib import Path
import re
import tempfile


def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', value):
        raise ValueError(f'unsafe identifier: {value!r}')
    return value


@contextmanager
def locked(path):
    """Serialize allocation/manifest refresh; locks release on process exit."""
    with Path(path).open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def write_atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix='.write-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def save_manifest(root, manifest):
    write_atomic(Path(root) / 'implementation.json', json.dumps(manifest, indent=2) + '\n')


def allocate(suite, name):
    identifier(name)
    suite = Path(suite)
    suite.mkdir(parents=True, exist_ok=True)
    with locked(suite / '.allocation.lock'):
        numbers = [int(match[1]) for p in suite.iterdir()
                   if p.is_dir() and (match := re.fullmatch(r'(\d{3,})_.+', p.name))]
        root = suite / f'{max(numbers, default=0) + 1:03d}_{name}'
        root.mkdir()  # Reserve before writing; an interrupted allocation is not reused.
        for directory in ('tasks', 'runs', 'reports'):
            (root / directory).mkdir()
        save_manifest(root, {'version': 2, 'implementation_id': root.name,
                             'created_at': datetime.now(timezone.utc).isoformat(),
                             'sources': [], 'bindings': []})
    return root


def validate_manifest(manifest):
    if manifest.get('version') != 2:
        raise ValueError('implementation manifest version 2 required')
    identifier(manifest.get('implementation_id'))
    sources, selected = {}, set()
    for source in manifest['sources']:
        sid = identifier(source.get('id'))
        if sid in sources:
            raise ValueError('duplicate source id')
        for field in ('adapter', 'source_version', 'path', 'session_id'):
            if not isinstance(source.get(field), str) or not source[field]:
                raise ValueError(f'source needs {field}')
        turns = source.get('turn_ids')
        if not isinstance(turns, list) or not turns or any(not isinstance(t, str) or not t for t in turns):
            raise ValueError('source needs explicit nonempty turn_ids')
        for turn in turns:
            key = (source['adapter'], source['session_id'], turn)
            if key in selected:
                raise ValueError('duplicate selected native turn')
            selected.add(key)
        sources[sid] = source
    bound, ids, runs, agents = set(), set(), {}, {}
    for binding in manifest['bindings']:
        for field in ('id', 'task_id', 'agent_run_id', 'role'):
            identifier(binding.get(field))
        for field in ('agent_name', 'purpose'):
            if field in binding and (not isinstance(binding[field], str) or not binding[field].strip()
                                     or len(binding[field]) > 500):
                raise ValueError(f'{field} must be nonempty text, at most 500 characters')
        if binding['id'] in ids:
            raise ValueError('duplicate binding id')
        ids.add(binding['id'])
        source = sources.get(binding.get('source_id'))
        if not source or not binding.get('turn_ids') or not set(binding['turn_ids']) <= set(source['turn_ids']):
            raise ValueError('binding must select explicit source turns')
        native = (source['adapter'], source['session_id'])
        run = binding['agent_run_id']
        if native in agents and agents[native] != run:
            raise ValueError('follow-ups must retain agent_run_id')
        if run in runs and runs[run] != native:
            raise ValueError('replacement native agents need distinct agent_run_id')
        agents[native], runs[run] = run, native
        for turn in binding['turn_ids']:
            key = (binding['source_id'], turn)
            if key in bound:
                raise ValueError('turn already bound; assignment history is immutable')
            bound.add(key)
    return sources


def bind(root, binding):
    root = Path(root)
    with locked(root / '.records.lock'):
        manifest = json.loads((root / 'implementation.json').read_text())
        old = next((b for b in manifest['bindings'] if b['id'] == binding['id']), None)
        if old:
            if {k: v for k, v in old.items() if k != 'recorded_at'} != binding:
                raise ValueError('binding id already recorded with different assignment')
            return old
        entry = dict(binding, recorded_at=datetime.now(timezone.utc).isoformat())
        manifest['bindings'].append(entry)
        validate_manifest(manifest)
        save_manifest(root, manifest)
        return entry


def add_source(root, source):
    root = Path(root)
    with locked(root / '.records.lock'):
        manifest = json.loads((root / 'implementation.json').read_text())
        old = next((s for s in manifest['sources'] if s['id'] == source['id']), None)
        if old:
            if old != source:
                raise ValueError('source id already recorded; use a new source for new turns')
            return old
        manifest['sources'].append(source)
        validate_manifest(manifest)
        save_manifest(root, manifest)
        return source


def resolve_task(root, task):
    root = Path(root)
    manifest = json.loads((root / 'implementation.json').read_text())
    validate_manifest(manifest)
    target = root / 'tasks' / identifier(task)
    if not target.is_dir() or not target.resolve().is_relative_to(root.resolve()):
        raise ValueError('task absent from identified implementation')
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    allocate_parser = commands.add_parser('allocate')
    allocate_parser.add_argument('name')
    allocate_parser.add_argument('--suite', type=Path, default=Path('.suite'))
    bind_parser = commands.add_parser('bind')
    bind_parser.add_argument('implementation', type=Path)
    bind_parser.add_argument('binding', type=Path)
    source_parser = commands.add_parser('source')
    source_parser.add_argument('implementation', type=Path)
    source_parser.add_argument('source', type=Path)
    resolve_parser = commands.add_parser('resolve')
    resolve_parser.add_argument('implementation', type=Path)
    resolve_parser.add_argument('task')
    args = parser.parse_args()
    try:
        if args.command == 'allocate':
            print(allocate(args.suite, args.name))
        elif args.command == 'source':
            print(json.dumps(add_source(args.implementation, json.loads(args.source.read_text()))))
        elif args.command == 'bind':
            print(json.dumps(bind(args.implementation, json.loads(args.binding.read_text()))))
        else:
            print(resolve_task(args.implementation, args.task))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'records: {exc}\n')


if __name__ == '__main__':
    main()
