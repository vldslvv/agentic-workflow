#!/usr/bin/env python3
"""Validate explicit role context, without traversing document links.

CLI: role_context.py MANIFEST --root ROOT [--output FILE]
Manifest v1: role, reads [{path, sha256, section? (exact heading text), category?}],
owned_paths (existing paths or future outputs), forbidden_paths (reviewer only).
Digests identify whole files, including when only a Markdown section is selected.
Canonical instructions and AGENTS routers must appear as complete files in reads.
Sections are allowed only for noncanonical references.
Byte counts measure selected UTF-8 context, not tokens or measured model reads.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

COMMON = ('AGENTS.md', 'spec-source-suite/AGENTS.md',
          'spec-source-suite/docs/SUITE_CONTRACT.md')
ROLES = {
    'supervisor': ('docs/GENERATE.md', 'docs/MARKDOWN_BUNDLES.md'),
    'planner': ('docs/DEFINE.md', 'docs/PLANNING.md', 'docs/MARKDOWN_BUNDLES.md'),
    'implementer': ('docs/IMPLEMENT.md',),
    'reviewer': ('prompts/REVIEWER.md', 'prompts/VERIFIER.md'),
}
EXCLUDED = re.compile(r'(^|[/\\_. -])(plans?|conversations?|transcripts?|implementation[-_ ]summar(?:y|ies))(?=$|[/\\_. -])', re.I)


def section_bytes(data, heading):
    """Select one uniquely named ATX section including its subheadings."""
    lines = data.decode('utf-8').splitlines(keepends=True)
    matches = []
    fenced = False
    for i, line in enumerate(lines):
        if re.match(r'^\s*(```|~~~)', line):
            fenced = not fenced
        match = None if fenced else re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$', line.rstrip('\n\r'))
        if match:
            matches.append((i, len(match[1]), match[2]))
    starts = [(i, depth) for i, depth, title in matches if title == heading]
    if len(starts) != 1:
        raise ValueError(f'section missing or ambiguous: {heading}')
    start, depth = starts[0]
    end = next((i for i, d, _ in matches if i > start and d <= depth), len(lines))
    return ''.join(lines[start:end]).encode('utf-8')


def _resolve(root, value, must_exist=True):
    if not isinstance(value, str) or not value:
        raise ValueError('path must be a nonempty string')
    path = (root / value).resolve()
    if not path.is_relative_to(root):
        raise ValueError(f'path escapes root: {value}')
    if must_exist and not path.is_file():
        raise ValueError(f'missing referenced file: {value}')
    return path


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield str(key)
            yield from _strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)


def build_context(manifest, root):
    root = Path(root).resolve()
    role = manifest.get('role')
    if manifest.get('version') != 1 or role not in ROLES:
        raise ValueError('version 1 and a known role are required')
    reads = manifest.get('reads')
    if not isinstance(reads, list) or not reads:
        raise ValueError('nonempty explicit reads are required')
    if not isinstance(manifest.get('owned_paths'), list):
        raise ValueError('owned_paths must be explicit (possibly empty)')
    forbidden = []
    for value in manifest.get('forbidden_paths', []):
        forbidden.append(_resolve(root, value, must_exist=False))
    if role == 'reviewer':
        # Metadata cannot smuggle references excluded from the top-level read list.
        for value in _strings({k: v for k, v in manifest.items() if k != 'forbidden_paths'}):
            target = (root / value).resolve() if '\n' not in value else root
            resolved_exclusion = target.is_file() and (EXCLUDED.search(str(target)) or target.suffix.lower() == '.jsonl' or any(target == p or target.is_relative_to(p) for p in forbidden))
            if EXCLUDED.search(value) or value.lower().endswith('.jsonl') or resolved_exclusion:
                raise ValueError(f'reviewer excludes plan/conversation references: {value}')
    required = set(COMMON) | {'spec-source-suite/' + p for p in ROLES[role]}
    result, seen, actual = [], set(), set()
    for item in reads:
        if not isinstance(item, dict):
            raise ValueError('each read must identify path and sha256')
        path = _resolve(root, item.get('path'))
        rel = path.relative_to(root).as_posix()
        if role == 'reviewer' and (EXCLUDED.search(rel) or path.suffix.lower() == '.jsonl' or any(path == p or path.is_relative_to(p) for p in forbidden)):
            raise ValueError(f'forbidden reviewer input: {item["path"]}')
        raw = path.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        if not isinstance(item.get('sha256'), str) or item['sha256'].removeprefix('sha256:') != digest:
            raise ValueError(f'digest mismatch: {item["path"]}')
        section = item.get('section')
        if rel in required and section:
            raise ValueError(f'canonical instructions require full file: {rel}')
        selected = section_bytes(raw, section) if section else raw
        key = (rel, section)
        if key in seen:
            raise ValueError(f'duplicate read: {key}')
        seen.add(key)
        actual.add(rel)
        result.append({'path': rel, 'sha256': digest, 'section': section,
                       'category': item.get('category'), 'file_bytes': len(raw),
                       'selected_bytes': len(selected),
                       'suite_controlled': rel in COMMON or rel.startswith('spec-source-suite/')})
    missing = sorted(required - actual)
    if missing:
        raise ValueError('missing canonical role instructions: ' + ', '.join(missing))
    for value in manifest['owned_paths']:
        _resolve(root, value, must_exist=False)
    return {'version': 1, 'role': role, 'reads': result,
            'owned_paths': manifest['owned_paths'],
            'suite_controlled_selected_bytes': sum(r['selected_bytes'] for r in result if r['suite_controlled']),
            'suite_controlled_validated_file_bytes': sum(v for _, v in {r['path']: r['file_bytes'] for r in result if r['suite_controlled']}.items()),
            'selected_bytes': sum(r['selected_bytes'] for r in result),
            'measurement': 'selected context bytes; actual model reads are not observable'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        result = build_context(json.loads(args.manifest.read_text()), args.root)
        rendered = json.dumps(result, indent=2) + '\n'
        if args.output:
            args.output.write_text(rendered)
        else:
            print(rendered, end='')
    except (OSError, ValueError, TypeError) as exc:
        print(f'role-context: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
