#!/usr/bin/env python3
"""Read explicit session/turn JSONL sources, never discover or modify logs.

CLI: usage_report.py MANIFEST --root ROOT [--output FILE]
Manifest v1: root {session_id, path, turn_ids, role?}, descendants with the same
fields plus parent_session_id. Single turn_id is also accepted. Paths may be
absolute for read-only Codex logs. Optional verification_subprocesses entries:
{session_id, turn_id, call_id, count, evidence_path}; evidence is mandatory.

Understands Codex token_usage_record, turn_context, response_item tool calls,
and normalized events {type: usage|tool_call, session_id, turn_id, response_id
or call_id, usage or name, timestamp}. Explicit parent_call_id distinguishes
nested operations. Never infer executed nested operations from source code.
Unknown totals are null; known subtotals and missing-record counts stay visible.
Reasoning is a subset of output and is never added again to total tokens.
"""
import argparse
from collections import Counter, defaultdict
from datetime import datetime
import json
from pathlib import Path
import sys

METRICS = ('input_tokens', 'cached_input_tokens', 'uncached_input_tokens',
           'output_tokens', 'reasoning_output_tokens', 'total_tokens')


def _stamp(value):
    if value is None:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()
    except (ValueError, AttributeError):
        return None


def _count(value):
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else None


def _category(name):
    short = name.split('.')[-1].split('__')[-1]
    if short == 'exec':
        return 'execution_batch'
    if short in ('exec_command', 'write_stdin'):
        return 'shell'
    if short in ('spawn_agent', 'send_message', 'followup_task', 'interrupt_agent', 'list_agents', 'wait_agent'):
        return 'agent'
    if short in ('wait', 'sleep'):
        return 'wait'
    if short in ('apply_patch',):
        return 'file_edit'
    if 'web' in name or 'browser' in name:
        return 'web'
    return 'other'


def _read_source(ref, root):
    sid = ref.get('session_id')
    turns = ref.get('turn_ids', [ref.get('turn_id')] if ref.get('turn_id') else [])
    if not isinstance(sid, str) or not sid or not turns or any(not isinstance(t, str) or not t for t in turns):
        raise ValueError('each source needs session_id and explicit nonempty turn_ids')
    path = root / ref['path']
    records = []
    active_turn, declared_sid = None, None
    with path.open() as stream:
        for number, line in enumerate(stream, 1):
            try:
                event = json.loads(line)
            except ValueError as exc:
                raise ValueError(f'invalid JSON: {path}:{number}') from exc
            payload = event.get('payload', {})
            if not isinstance(payload, dict):
                payload = {}
            kind = event.get('type')
            if kind == 'session_meta':
                declared_sid = payload.get('id', payload.get('session_id'))
                if declared_sid != sid:
                    raise ValueError(f'session identity mismatch: {path}')
            if kind == 'turn_context':
                active_turn = payload.get('turn_id')
            if kind == 'event_msg' and payload.get('type') == 'task_started':
                active_turn = payload.get('turn_id', active_turn)
            metadata = payload.get('internal_chat_message_metadata_passthrough', {})
            turn = payload.get('turn_id', event.get('turn_id', metadata.get('turn_id', active_turn)))
            record_sid = payload.get('thread_id', event.get('session_id', sid))
            if record_sid != sid or turn not in turns:
                continue
            records.append((event, payload, turn))
    return records


def _summary(usages, calls, stamps, unidentified_usage=0, unidentified_calls=0):
    counts = {}
    for metric in METRICS:
        values = [usage.get(metric) for usage in usages]
        missing = sum(v is None for v in values) + unidentified_usage
        known = sum(v for v in values if v is not None)
        counts[metric] = {'total': known if values and not missing else None,
                          'known_subtotal': known, 'missing_records': missing}
    categories = Counter(call['category'] for call in calls)
    nested = [call for call in calls if call.get('parent_call_id')]
    times = [s for s in stamps if s is not None]
    return {'tokens': counts,
            'model_responses': len(usages) if not unidentified_usage else None,
            'identified_model_responses': len(usages), 'unidentified_usage_records': unidentified_usage,
            'tool_calls': len(calls) if not unidentified_calls else None,
            'identified_tool_calls': len(calls), 'unidentified_tool_records': unidentified_calls,
            'tool_categories': dict(sorted(categories.items())),
            'execution_batches': categories['execution_batch'],
            'observed_nested_operations': len(nested) if nested else None,
            'nested_operation_measurement': 'explicit parent_call_id records only; unavailable otherwise',
            'elapsed_seconds': max(times) - min(times) if len(times) >= 2 else None,
            'elapsed_measurement': 'selected event timestamp span; not CPU or billed time'}


def build_report(manifest, root):
    root = Path(root).resolve()
    if manifest.get('version') != 1 or not isinstance(manifest.get('root'), dict):
        raise ValueError('version 1 and explicit root source are required')
    sources = [manifest['root']] + manifest.get('descendants', [])
    by_sid = {}
    for ref in sources:
        sid = ref.get('session_id')
        if sid in by_sid:
            raise ValueError(f'duplicate session reference: {sid}')
        by_sid[sid] = ref
    root_sid = sources[0].get('session_id')
    for ref in sources[1:]:
        seen, cursor = set(), ref
        while cursor.get('session_id') != root_sid:
            sid = cursor.get('session_id')
            if sid in seen or cursor.get('parent_session_id') not in by_sid:
                raise ValueError(f'descendant is not connected to root: {sid}')
            seen.add(sid)
            cursor = by_sid[cursor['parent_session_id']]
    usage_by_key, calls_by_key = {}, {}
    stamps, session_stamps = [], defaultdict(list)
    unknown_usage, unknown_calls = Counter(), Counter()
    observed_usage_turns = defaultdict(set)
    selected_turns = {}
    for ref in sources:
        sid = ref['session_id']
        selected_turns[sid] = set(ref.get('turn_ids', [ref.get('turn_id')]))
        for event, payload, turn in _read_source(ref, root):
            kind = event.get('type')
            stamp = _stamp(event.get('timestamp'))
            stamps.append(stamp)
            session_stamps[sid].append(stamp)
            if kind in ('token_usage_record', 'usage'):
                record = payload if kind == 'token_usage_record' else event
                observed_usage_turns[sid].add(turn)
                rid = record.get('response_id')
                if not rid:
                    unknown_usage[sid] += 1
                    continue
                usage = record.get('usage') or {}
                values = {metric: _count(usage.get(metric)) for metric in METRICS}
                if values['input_tokens'] is not None and values['cached_input_tokens'] is not None:
                    if values['cached_input_tokens'] > values['input_tokens']:
                        raise ValueError(f'cached tokens exceed input: {sid}/{rid}')
                    values['uncached_input_tokens'] = values['input_tokens'] - values['cached_input_tokens']
                if values['input_tokens'] is not None and values['output_tokens'] is not None:
                    values['total_tokens'] = values['input_tokens'] + values['output_tokens']
                if values['reasoning_output_tokens'] is not None and values['output_tokens'] is not None and values['reasoning_output_tokens'] > values['output_tokens']:
                    raise ValueError(f'reasoning tokens exceed output: {sid}/{rid}')
                key = (sid, rid)
                if key in usage_by_key and usage_by_key[key] != values:
                    raise ValueError(f'conflicting duplicate usage: {sid}/{rid}')
                usage_by_key[key] = values
            elif kind == 'tool_call' or (kind == 'response_item' and payload.get('type') in ('function_call', 'custom_tool_call')):
                record = event if kind == 'tool_call' else payload
                cid = record.get('call_id')
                if not cid:
                    unknown_calls[sid] += 1
                    continue
                name = record.get('name', 'unknown')
                call = {'name': name, 'category': _category(name),
                        'parent_call_id': record.get('parent_call_id'), 'turn_id': turn}
                key = (sid, cid)
                if key in calls_by_key and calls_by_key[key] != call:
                    raise ValueError(f'conflicting duplicate tool call: {sid}/{cid}')
                calls_by_key[key] = call
    # Legacy snapshots mirror token_usage_record in current Codex. Without a
    # response ID they cannot safely supply deduplicated response accounting.
    for sid, turns in selected_turns.items():
        # A selected turn without response-identified usage is unmeasured,
        # whether a legacy snapshot or no usage event was emitted.
        unknown_usage[sid] += len(turns - observed_usage_turns[sid])
    result = _summary(list(usage_by_key.values()), list(calls_by_key.values()), stamps,
                      sum(unknown_usage.values()), sum(unknown_calls.values()))
    result.update({'version': 1, 'root_session_id': root_sid, 'sessions': {}, 'roles': {}})
    grouped_roles = defaultdict(list)
    for ref in sources:
        sid = ref['session_id']
        summary = _summary([v for k, v in usage_by_key.items() if k[0] == sid],
                           [v for k, v in calls_by_key.items() if k[0] == sid], session_stamps[sid],
                           unknown_usage[sid], unknown_calls[sid])
        summary['role'] = ref.get('role', 'unspecified')
        summary['turn_ids'] = ref.get('turn_ids', [ref.get('turn_id')])
        result['sessions'][sid] = summary
        grouped_roles[summary['role']].append(sid)
    for role, sids in grouped_roles.items():
        result['roles'][role] = _summary([v for k, v in usage_by_key.items() if k[0] in sids],
                                       [v for k, v in calls_by_key.items() if k[0] in sids],
                                       [s for sid in sids for s in session_stamps[sid]],
                                       sum(unknown_usage[sid] for sid in sids), sum(unknown_calls[sid] for sid in sids))
    verification, evidence_keys = 0, set()
    for evidence in manifest.get('verification_subprocesses', []):
        sid, cid = evidence.get('session_id'), evidence.get('call_id')
        key = (sid, cid)
        if key not in calls_by_key or calls_by_key[key]['turn_id'] != evidence.get('turn_id'):
            raise ValueError('verification evidence must reference an included tool call and turn')
        count = _count(evidence.get('count'))
        if count is None or not (root / evidence.get('evidence_path', '')).is_file():
            raise ValueError('verification subprocess count needs an explicit count and existing evidence')
        if key in evidence_keys:
            raise ValueError('duplicate verification subprocess evidence')
        evidence_keys.add(key)
        verification += count
    result['verification_subprocesses'] = verification if evidence_keys else None
    result['limitations'] = ['Only explicitly selected sessions and turns are included.',
                            'Nested execution is unavailable unless explicit parent call IDs were logged.',
                            'Legacy token_count snapshots lack response IDs and cannot establish deduplicated totals.']
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text())
        if args.output:
            sources = [manifest.get('root', {})] + manifest.get('descendants', [])
            if any(args.output.resolve() == (args.root / ref['path']).resolve()
                   or (args.output.exists() and args.output.samefile(args.root / ref['path']))
                   for ref in sources if 'path' in ref):
                raise ValueError('output must not overwrite a source log')
        report = build_report(manifest, args.root)
        rendered = json.dumps(report, indent=2) + '\n'
        if args.output:
            args.output.write_text(rendered)
        else:
            print(rendered, end='')
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(f'usage-report: {exc}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
