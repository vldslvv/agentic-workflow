#!/usr/bin/env python3
"""Import explicit native evidence and rebuild implementation reports.

CLI: usage_report.py IMPLEMENTATION_ROOT
Run at task completion or explicit refresh. Reads implementation.json v2 (see
records.py); writes runs/<task>/<agent-run>/trace.jsonl and reports/{usage.json,
usage.md,timeline.json}. No discovery, recorder, database, services or costs.

Canonical tokens: input includes cache read/write; uncached=input-cache read;
output includes reasoning; total=input+output. Unknown measurements remain null.
Totals are complete only for the selected evidence and its reported coverage.
Chrome Trace uses M, X, i and s/f flow events; missing timing stays missing.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

from records import locked, validate_manifest, write_atomic
from trace_adapters import METRICS, read_source


def identity(*parts):
    return hashlib.sha256(json.dumps(parts, separators=(',', ':')).encode()).hexdigest()[:24]


def import_evidence(manifest, root):
    """I/O boundary; adapters supply evidence, bindings supply workflow context."""
    sources = validate_manifest(manifest)
    root = Path(root)
    bindings = {(b['source_id'], turn): b for b in manifest['bindings'] for turn in b['turn_ids']}
    events, diagnostics = {}, []
    for source in sources.values():
        native, gaps = read_source(source, root / source['path'])
        for item in [*native, *gaps]:
            binding = bindings.get((source['id'], item.get('turn_id')), {})
            item.update(implementation_id=manifest['implementation_id'], adapter=source['adapter'],
                        agent_id=f'{source["adapter"]}:{source["session_id"]}',
                        task_id=binding.get('task_id'), role=binding.get('role'),
                        agent_run_id=binding.get('agent_run_id'), binding_id=binding.get('id'))
        for e in native:
            binding = bindings.get((source['id'], e['turn_id']), {})
            e['requested'] = {k: binding.get('requested', {}).get(k) for k in ('model', 'reasoning_effort')}
            e['agent_name'] = binding.get('agent_name') or e.get('native_agent_name') or e.get('agent_run_id') or e['agent_id']
            e['purpose'] = binding.get('purpose')
            e['event_id'] = identity(e['implementation_id'], e['agent_id'], e['kind'], e['native_event_id'])
            old = events.get(e['event_id'])
            if old:
                ignored = {'provenance'}
                if {k: v for k, v in old.items() if k not in ignored} != {k: v for k, v in e.items() if k not in ignored}:
                    raise ValueError('conflicting duplicate native event')
                old['provenance'] += e['provenance']
            else:
                events[e['event_id']] = e
        diagnostics.extend(gaps)
    return sorted(events.values(), key=lambda e: e['event_id']), diagnostics


GAP_CODES = {'missing_usage', 'unidentified_usage', 'invalid_json_line'}
INCOMPLETE_CODES = GAP_CODES | {'source_unavailable', 'unfinished_turn', 'unverified_native_version',
                                'missing_native_identity', 'message_only_usage', 'unmeasured_message'}


def summarize(events, diagnostics):
    models = [e for e in events if e['kind'] == 'model']
    calls = [e for e in events if e['kind'] == 'tool']
    unknown = sum(d['code'] in GAP_CODES for d in diagnostics)
    incomplete = any(d['code'] in INCOMPLETE_CODES for d in diagnostics)
    metrics = {}
    for metric in METRICS:
        values = [(e.get('usage') or {}).get(metric) for e in models]
        measured = [v for v in values if v is not None]
        missing = len(values) - len(measured) + unknown
        metrics[metric] = dict(total=sum(measured) if measured and not missing and not incomplete else None,
                               known_subtotal=sum(measured) if measured else None,
                               measured_records=len(measured), missing_records=missing)
    durations = [e['end'] - e['start'] for e in events
                 if e.get('start') is not None and e.get('end') is not None and e['end'] >= e['start']]
    return dict(tokens=metrics, observed_model_measurements=len(models),
                observed_tool_calls=len(calls),
                wrapper_calls=sum(e.get('name') in ('functions.exec', 'exec') for e in calls),
                observed_nested_operations=sum(bool(e.get('parent_call_id')) for e in calls),
                missing_parent_call_relationships=sum(not e.get('parent_call_id') for e in calls),
                outcomes=dict(sorted(Counter(e['outcome'] or 'unknown' for e in calls).items())),
                observed_operation_seconds=sum(durations) if durations else None,
                timed_operations=len(durations), untimed_operations=len(events) - len(durations),
                coverage=dict(sorted(Counter(d['code'] for d in diagnostics).items())))


def spawn_tree(events):
    nodes = {}
    relations = set()
    for e in events:
        node = nodes.setdefault(e['agent_id'], dict(agent_id=e['agent_id'], session_id=e['session_id'],
                                                   agent_run_ids=set(), turns=set()))
        if e.get('agent_run_id'):
            node['agent_run_ids'].add(e['agent_run_id'])
        node['turns'].add(e['turn_id'])
        for field, kind in [('parent_session_id', 'spawn'), ('forked_from_id', 'fork'), ('continued_from_id', 'continuation')]:
            if e.get(field):
                relations.add((f'{e["adapter"]}:{e[field]}', e['agent_id'], kind))
    return dict(nodes=[dict(n, agent_run_ids=sorted(n['agent_run_ids']), turns=sorted(n['turns']))
                       for _, n in sorted(nodes.items())],
                edges=[dict(parent=p, child=c, relationship=k, parent_in_selection=p in nodes)
                       for p, c, k in sorted(relations)])


def build_report(events, diagnostics):
    """Pure accounting. No harness-specific parsing or grouping in adapters."""
    groups, omissions = {}, {}
    for name, fields in [('task', ('task_id',)), ('agent_run', ('agent_run_id',)),
                         ('role', ('role',)), ('model', ('model',)), ('effort', ('reasoning_effort',)),
                         ('model_effort', ('model', 'reasoning_effort')),
                         ('task_model_effort', ('task_id', 'model', 'reasoning_effort')),
                         ('tool', ('name',)), ('task_tool', ('task_id', 'name'))]:
        grouped, gaps = defaultdict(list), defaultdict(list)
        omitted = []
        for e in events:
            if name in ('model', 'effort', 'model_effort', 'task_model_effort') and e['kind'] != 'model':
                continue
            if name in ('tool', 'task_tool') and e['kind'] != 'tool':
                continue
            key = tuple(e.get(k) for k in fields)
            if any(v is None for v in key):
                omitted.append(e['event_id'])
            else:
                grouped[key].append(e)
        unassigned_gaps = 0
        for d in diagnostics:
            key = tuple(d.get(k) for k in fields)
            if all(v is not None for v in key):
                gaps[key].append(d)
                continue
            unassigned_gaps += 1
            # Preserve diagnostic scope across grouping. A source-wide gap can
            # affect several assignments; a turn gap can affect multiple models.
            affected = {tuple(e.get(k) for k in fields) for e in events
                        if any(p.get('source_id') == d.get('source_id') for p in e['provenance'])
                        and (d.get('turn_id') is None or e['turn_id'] == d['turn_id'])}
            affected = {key for key in affected if all(v is not None for v in key)}
            if not affected and d['code'] in INCOMPLETE_CODES:
                affected = set(grouped)  # Unknown attribution cannot prove completeness.
            for key in affected:
                gaps[key].append(d)
        groups[name] = [dict(key=dict(zip(fields, key)), summary=summarize(grouped[key], gaps[key]))
                        for key in sorted(grouped.keys() | gaps.keys())]
        omissions[name] = dict(event_ids=omitted, diagnostics_without_attribution=unassigned_gaps)
    return dict(version=2, summary=summarize(events, diagnostics), groups=groups,
                attribution_omissions=omissions, spawn_tree=spawn_tree(events), diagnostics=diagnostics,
                assignments=assignments(events),
                limitations=['Only explicit native sessions and selected turns are included.',
                             'Known subtotals exclude missing measurements; totals are scoped to observed evidence.',
                             'Operation durations can overlap and are not wall-clock, CPU or billed time.',
                             'Absent parent-call relationships do not establish absence of nested operations.',
                             'Observed settings come from native context, not necessarily provider confirmation.'])


def assignments(events):
    """Unique observed assignments, preserving session reuse and explicit context."""
    fields = ('agent_id', 'agent_run_id', 'agent_name', 'native_agent_name', 'native_agent_path',
              'task_id', 'role', 'purpose', 'binding_id')
    rows = {}
    for e in events:
        key = (e['agent_id'], e.get('binding_id'))
        row = rows.setdefault(key, dict({k: e.get(k) for k in fields}, turns=set(), outcomes=set(), observed_settings=set()))
        row['turns'].add(e.get('turn_id'))
        settings = (e.get('model'), e.get('reasoning_effort'))
        if any(value is not None for value in settings):
            row['observed_settings'].add(settings)
        if e['kind'] == 'agent':
            row['outcomes'].add(e.get('outcome') or 'unfinished')
    return [dict(row, turns=sorted(t for t in row['turns'] if t), outcomes=sorted(row['outcomes']),
                 observed_settings=[dict(model=model, reasoning_effort=effort) for model, effort in
                                    sorted(row['observed_settings'], key=lambda pair: tuple(v or '' for v in pair))])
            for _, row in sorted(rows.items(), key=lambda item: str(item[0]))]


def format_settings(settings):
    """Keep observed model/effort pairs together, without filling gaps from requests."""
    return '; '.join(f'{s.get("model") or "unavailable"} / {s.get("reasoning_effort") or "unavailable"}'
                     for s in settings) or 'unavailable'


def timeline(events):
    lanes = {agent: i + 1 for i, agent in enumerate(sorted({e['agent_id'] for e in events}))}
    labels = defaultdict(set)
    for assignment in assignments(events):
        context = ' / '.join(v for v in (assignment.get('role'), assignment.get('task_id')) if v)
        label = assignment.get('agent_name') or assignment['agent_id']
        label = f'{label} · {context}' if context else label
        labels[assignment['agent_id']].add(f'{label} · {format_settings(assignment["observed_settings"])}')
    output = [dict(ph='M', name='thread_name', pid=1, tid=tid, args={'name': '; '.join(sorted(labels[agent]))})
              for agent, tid in lanes.items()]
    omitted, flows = [], set()
    for e in events:
        start, end = e.get('start'), e.get('end')
        point = e.get('timestamp')
        label = e.get('name') or (e.get('agent_name') if e['kind'] == 'agent' else None) or e['kind']
        if e['kind'] == 'agent':
            label += ' · ' + (e.get('purpose') or ' / '.join(v for v in (e.get('role'), e.get('task_id')) if v) or 'assignment unavailable')
            label += ' · ' + format_settings([e])
        base = dict(name=label, cat=e['kind'], pid=1, tid=lanes[e['agent_id']],
                    args={k: e.get(k) for k in ('event_id', 'task_id', 'role', 'agent_run_id', 'agent_id',
                                               'agent_name', 'native_agent_name', 'native_agent_path', 'purpose',
                                               'outcome', 'model', 'reasoning_effort', 'call_id', 'parent_call_id')})
        base['args'].update({f'tokens.{k}': v for k, v in (e.get('usage') or {}).items() if v is not None})
        if start is not None and end is not None and end >= start:
            output.append(dict(base, ph='X', ts=start * 1_000_000, dur=(end - start) * 1_000_000))
        elif start is not None or end is not None or point is not None:
            observed = start if start is not None else end if end is not None else point
            output.append(dict(base, ph='i', s='t', ts=observed * 1_000_000))
            omitted.append(dict(event_id=e['event_id'], reason='duration_unavailable'))
        else:
            omitted.append(dict(event_id=e['event_id'], reason='timing_unavailable'))
        parent = f'{e["adapter"]}:{e.get("parent_session_id")}'
        spawn = e.get('spawn_timestamp')
        if parent in lanes and spawn is not None and e['agent_id'] not in flows:
            flows.add(e['agent_id'])
            fid = lanes[e['agent_id']]  # Chrome/Perfetto IDs are numeric (not arbitrary hash strings).
            for phase, agent in [('s', parent), ('f', e['agent_id'])]:
                # Bind each endpoint to an explicit observed creation instant.
                # Without anchors Perfetto can attach to unrelated enclosing
                # slices and reverse a flow when one lane has only instants.
                output.append(dict(name='native spawn', cat='agent', ph='i', s='t',
                                   pid=1, tid=lanes[agent], ts=spawn * 1_000_000))
                output.append(dict(name='spawn', cat='agent', ph=phase, id=fid, pid=1,
                                   tid=lanes[agent], ts=spawn * 1_000_000, **({'bp': 'e'} if phase == 'f' else {})))
    return dict(traceEvents=output, displayTimeUnit='ms', metadata=dict(timing_omissions=omitted))


def markdown(report):
    lines = ['# Selected implementation usage', '',
             'Null means unavailable. Known subtotals exclude missing measurements. Scope and omissions are in usage.json.', '',
             '| Metric | Total | Known subtotal | Measured records | Missing records |',
             '|---|---:|---:|---:|---:|']
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ') if value is not None else 'unavailable'
    for metric, values in report['summary']['tokens'].items():
        lines.append('| ' + ' | '.join(map(cell, [metric, *values.values()])) + ' |')
    for name, rows in report['groups'].items():
        tools = name in ('tool', 'task_tool')
        models = name in ('model', 'effort', 'model_effort', 'task_model_effort')
        headers = (['Group', 'Observed calls', 'Outcomes', 'Observed seconds', 'Untimed'] if tools else
                   ['Group', 'Total tokens', 'Known subtotal', 'Missing records'] + ([] if models else ['Tools']))
        lines += ['', f'## By {name}', '', '| ' + ' | '.join(headers) + ' |',
                  '| ' + ' | '.join('---' for _ in headers) + ' |']
        for row in rows:
            s = row['summary']
            tokens = s['tokens']['total_tokens']
            values = ([s['observed_tool_calls'], s['outcomes'], s['observed_operation_seconds'], s['untimed_operations']]
                      if tools else [tokens['total'], tokens['known_subtotal'], tokens['missing_records']]
                      + ([] if models else [s['observed_tool_calls']]))
            lines.append('| ' + ' | '.join(map(cell, [', '.join(row['key'].values()), *values])) + ' |')
        omission = report['attribution_omissions'][name]
        lines += ['', f'Attribution omissions: {len(omission["event_ids"])} events; {omission["diagnostics_without_attribution"]} diagnostics.']
    lines += ['', '## Native lineage', '']
    for edge in report['spawn_tree']['edges']:
        lines.append(f'- {edge["parent"]} → {edge["child"]} ({edge["relationship"]})')
    lines += ['', '## Coverage diagnostics', '']
    for code, n in report['summary']['coverage'].items():
        lines.append(f'- {code}: {n}')
    return '\n'.join(lines) + '\n'


def refresh(root):
    root = Path(root).resolve()
    with locked(root / '.records.lock'):
        manifest_path = root / 'implementation.json'
        manifest = json.loads(manifest_path.read_text())
        events, diagnostics = import_evidence(manifest, root)
        report = build_report(events, diagnostics)
        report['implementation_id'] = manifest['implementation_id']
        traces = defaultdict(list)
        for e in events:
            task = e['task_id'] or '_unassigned'
            run = e['agent_run_id'] or identity(e['agent_id'])
            traces[root / 'runs' / task / run / 'trace.jsonl'].append(e)
        outputs = {path: ''.join(json.dumps(e, sort_keys=True) + '\n' for e in values) for path, values in traces.items()}
        outputs.update({root / 'reports' / 'usage.json': json.dumps(report, indent=2) + '\n',
                        root / 'reports' / 'usage.md': markdown(report),
                        root / 'reports' / 'timeline.json': json.dumps(timeline(events), indent=2) + '\n'})
        # Clear previously generated traces for selected bindings even if sources
        # disappeared. Never traverse/delete historical or unrelated run evidence.
        for b in manifest['bindings']:
            outputs.setdefault(root / 'runs' / b['task_id'] / b['agent_run_id'] / 'trace.jsonl', '')
        for source in manifest['sources']:
            unassigned = root / 'runs' / '_unassigned' / identity(f'{source["adapter"]}:{source["session_id"]}') / 'trace.jsonl'
            if unassigned.exists():
                outputs.setdefault(unassigned, '')
        protected = [manifest_path] + [root / s['path'] for s in manifest['sources']]
        for path in outputs:
            if not path.resolve().is_relative_to(root):
                raise ValueError('output escapes implementation root')
            if any(path.resolve() == source.resolve() or
                   (path.exists() and source.exists() and path.samefile(source)) for source in protected):
                raise ValueError('output must not overwrite a native source or manifest')
        for path, data in outputs.items():
            write_atomic(path, data)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('implementation', type=Path)
    args = parser.parse_args()
    try:
        report = refresh(args.implementation)
        print(json.dumps({'implementation_id': report['implementation_id'], 'reports': str(args.implementation / 'reports'),
                          'coverage': report['summary']['coverage']}))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'usage-report: {exc}\n')


if __name__ == '__main__':
    main()
