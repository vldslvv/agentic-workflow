"""Public contracts for native evidence, accounting and reports.

Synthetic fixtures protect pinned parsing and expected totals. Collection tests
exercise real disposable native indexes; no live OpenCode capture is claimed.
"""
from concurrent.futures import ThreadPoolExecutor
import copy
import csv
import io
import os
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HELPERS = Path(__file__).resolve().parents[1] / 'helpers'
FIXTURES = Path(__file__).parent / 'fixtures'
sys.path.insert(0, str(HELPERS))
import records
import usage_report as usage
from trace_dashboard import render


class TraceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.addCleanup(patch.stopall)
        patch.dict(os.environ, CODEX_HOME=self.temp.name, CODEX_THREAD_ID='').start()
        import sqlite3
        c = sqlite3.connect(str(Path(self.temp.name) / 'state_5.sqlite'))
        c.execute('CREATE TABLE threads (id TEXT, rollout_path TEXT, source TEXT)')
        c.commit()
        c.close()
        self.suite = Path(self.temp.name) / '.suite'
        self.root = records.allocate(self.suite, 'test')

    def source(self, adapter='codex', sid='supervisor', turns=None, parent=None, fork=None, bind=True, role='supervisor', task='orchestration'):
        turns = turns or ['turn-1', 'turn-2']
        source_id = sid + '-' + adapter
        if adapter == 'codex':
            rows = [json.loads(line) for line in (FIXTURES / 'codex-0.167.0.jsonl').read_text().splitlines()]
            rows[0]['payload'].update(id=sid, parent_thread_id=parent, forked_from_id=fork)
            for row in rows:
                if 'thread_id' in row['payload']:
                    row['payload']['thread_id'] = sid
            data = ''.join(json.dumps(row) + '\n' for row in rows)
            version, suffix = 'codex-rollout-0.167.0', '.jsonl'
        else:
            data = json.loads((FIXTURES / 'opencode-1.2.27.json').read_text())
            data['info'].update(id=sid, parentID=parent)
            for msg in data['messages']:
                msg['info']['sessionID'] = sid
                for part in msg['parts']:
                    part['sessionID'] = sid
            data = json.dumps(data)
            version, suffix = 'opencode-export-1.2.27', '.json'
        path = self.root / 'native' / (source_id + suffix)
        path.parent.mkdir(exist_ok=True)
        if adapter == 'codex':
            selected, active = [rows[0]], None
            for row in rows[1:]:
                p = row['payload']
                active = p.get('turn_id') or active
                if active in turns:
                    selected.append(row)
                    if bind and row['type'] == 'turn_context':
                        selected.append(dict(timestamp=row['timestamp'], type='response_item', payload=dict(
                            type='message', role='user', content=[dict(type='input_text', text='SUITE ' + json.dumps(
                                dict(implementation=self.root.name, task=task, role=role)))])))
            data = ''.join(json.dumps(r) + '\n' for r in selected)
        elif bind:
            value = json.loads(data)
            value['messages'] = [m for m in value['messages'] if m['info']['id'] in turns or m['info'].get('parentID') in turns]
            for m in value['messages']:
                if m['info']['role'] == 'user':
                    m['parts'].append(dict(type='text', text='SUITE ' + json.dumps(
                        dict(implementation=self.root.name, task=task, role=role))))
            data = json.dumps(value)
        else:
            value = json.loads(data)
            value['messages'] = [m for m in value['messages'] if m['info']['id'] in turns or m['info'].get('parentID') in turns]
            data = json.dumps(value)
        path.write_text(data)
        return path, dict(id=source_id, session_id=sid, turn_ids=turns)

    def evidence(self):
        return usage.import_evidence(self.root)

    def tag(self, path, assignments):
        rows = [json.loads(line) for line in path.read_text().splitlines()]
        output = []
        for row in rows:
            output.append(row)
            if row['type'] == 'turn_context' and row['payload']['turn_id'] in assignments:
                value = dict(implementation=self.root.name, **assignments[row['payload']['turn_id']])
                output.append(dict(timestamp=row['timestamp'], type='response_item', payload=dict(
                    type='message', role='user', content=[dict(type='input_text', text='SUITE ' + json.dumps(value))])))
        path.write_text(''.join(json.dumps(r) + '\n' for r in output))

    def cli(self, script, *args):
        return subprocess.run([sys.executable, str(HELPERS / script), *map(str, args)], text=True, capture_output=True)

    def test_concurrent_allocations_resume_repair_and_scoped_resolution(self):
        # Real processes contend on the same lock, with different names.
        def allocate(i):
            result = self.cli('records.py', 'allocate', f'app-{i}', '--suite', self.suite)
            self.assertEqual(result.returncode, 0, result.stderr)
            return Path(result.stdout.strip())
        with ThreadPoolExecutor(max_workers=6) as pool:
            roots = list(pool.map(allocate, range(8)))
        self.assertEqual({int(p.name.split('_')[0]) for p in roots}, set(range(2, 10)))
        for task in ('work', 'repair-001'):
            (self.root / 'tasks' / task).mkdir()
            result = self.cli('records.py', 'resolve', self.root, task)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(Path(result.stdout.strip()), self.root / 'tasks' / task)
        self.assertEqual(len(list(self.suite.glob('[0-9]*_*'))), 9)
        self.assertNotEqual(self.cli('records.py', 'resolve', roots[0], 'work').returncode, 0)
        self.assertNotEqual(self.cli('records.py', 'resolve', self.root, '../work').returncode, 0)

    def test_both_adapters_normalize_tokens_without_aggregate_double_counting(self):
        expected = dict(input_tokens=150, cached_input_tokens=70, cache_write_input_tokens=10,
                        uncached_input_tokens=80, output_tokens=50, reasoning_output_tokens=15, total_tokens=200)
        for adapter in ('codex', 'opencode'):
            with self.subTest(adapter=adapter):
                self.root = records.allocate(self.suite, adapter)
                self.source(adapter)
                report = usage.refresh(self.root)
                self.assertEqual({k: v['total'] for k, v in report['summary']['tokens'].items()}, expected)
                self.assertEqual(report['summary']['observed_model_measurements'], 2)
                self.assertEqual(report['groups']['task'][0]['summary']['tokens']['total_tokens']['total'], 200)

    def test_requested_and_observed_settings_do_not_infer_effort_from_variant(self):
        _, source = self.source('opencode', bind=False)
        events, gaps = self.evidence()
        models = [e for e in events if e['kind'] == 'model']
        self.assertEqual({e['model'] for e in models}, {'model-a', 'model-b'})
        self.assertEqual({e['variant'] for e in models}, {'high', 'low'})
        self.assertTrue(all(e['reasoning_effort'] is None for e in models))
        self.assertTrue(all(not e['requested'] for e in models))
        report = usage.refresh(self.root)
        self.assertEqual(report['summary']['tokens']['total_tokens']['total'], 200)
        self.assertEqual(report['groups']['model_effort'], [])
        self.assertEqual(len(report['attribution_omissions']['model_effort']['event_ids']), 2)
        self.assertEqual([(r['key']['model'], r['summary']['tokens']['total_tokens']['total'])
                          for r in report['groups']['model']], [('model-a', 130), ('model-b', 70)])
        self.assertEqual(report['groups']['effort'], [])
        dashboard = render(report, 'https://ui.perfetto.dev')
        agent_table = dashboard.split('id="assignments"', 1)[1].split('</table>', 1)[0]
        self.assertIn('model-a / unavailable; model-b / unavailable', agent_table)
        self.assertNotIn('requested-model', agent_table)

    def test_codex_model_effort_changes_are_grouped_downstream(self):
        self.source()
        report = usage.refresh(self.root)
        rows = report['groups']['model_effort']
        self.assertEqual([(r['key'], r['summary']['tokens']['total_tokens']['total']) for r in rows],
                         [({'model':'model-a','reasoning_effort':'high'},130), ({'model':'model-b','reasoning_effort':'low'},70)])
        dashboard = render(report, 'https://ui.perfetto.dev')
        agent_table = dashboard.split('id="assignments"', 1)[1].split('</table>', 1)[0]
        self.assertIn('model-a / high; model-b / low', agent_table)

    def test_named_assignments_and_task_model_tool_breakdowns_survive_session_reuse(self):
        path, source = self.source(bind=False)
        rows = [json.loads(r) for r in path.read_text().splitlines()]
        rows[0]['payload'].update(agent_nickname='Ada', agent_path='/root/builder')
        path.write_text(''.join(json.dumps(r) + '\n' for r in rows))
        self.tag(path, {'turn-1': dict(task='build', role='implementer', purpose='Implement editor'),
                        'turn-2': dict(task='repair', role='reviewer', purpose='Check correction')})
        report = usage.refresh(self.root)
        assignments = report['assignments']
        self.assertEqual({a['agent_name'] for a in assignments}, {'Ada'})
        self.assertEqual({a['native_agent_path'] for a in assignments}, {'/root/builder'})
        self.assertEqual({(a['task_id'], a['purpose']) for a in assignments},
                         {('build', 'Implement editor'), ('repair', 'Check correction')})
        self.assertEqual(len(report['spawn_tree']['nodes']), 1)
        self.assertEqual([(r['key'], r['summary']['tokens']['total_tokens']['total'])
                          for r in report['groups']['task_model_effort']],
                         [({'task_id':'build', 'model':'model-a', 'reasoning_effort':'high'},130),
                          ({'task_id':'repair', 'model':'model-b', 'reasoning_effort':'low'},70)])
        tools = {r['key']['name']: r['summary'] for r in report['groups']['tool']}
        self.assertEqual(tools['functions.exec']['observed_tool_calls'], 1)
        self.assertEqual(tools['functions.exec']['wrapper_calls'], 1)
        self.assertEqual(tools['exec_command']['outcomes'], {'failed':1})
        self.assertEqual(tools['exec_command']['observed_nested_operations'], 1)
        self.assertAlmostEqual(tools['exec_command']['observed_operation_seconds'], 1)
        trace = json.loads((self.root / 'reports/timeline.json').read_text())['traceEvents']
        lane = next(e for e in trace if e['ph'] == 'M')['args']['name']
        self.assertIn('Ada · implementer / build · model-a / high', lane)
        self.assertIn('Ada · reviewer / repair · model-b / low', lane)
        agent_slices = [e for e in trace if e.get('cat') == 'agent' and e['ph'] == 'X']
        self.assertTrue(any('model-a / high' in e['name'] for e in agent_slices))
        self.assertTrue(any('model-b / low' in e['name'] for e in agent_slices))
        dashboard = render(report, 'https://ui.perfetto.dev')
        agent_table = dashboard.split('id="assignments"', 1)[1].split('</table>', 1)[0]
        self.assertIn('Observed model / effort', agent_table)
        for task, expected, other in [('build', 'model-a / high', 'model-b / low'),
                                     ('repair', 'model-b / low', 'model-a / high')]:
            row = next(row for row in agent_table.split('<tr>') if f'<td>{task}</td>' in row)
            self.assertIn(expected, row)
            self.assertNotIn(other, row)
        self.assertTrue(any(e['args'].get('purpose') == 'Implement editor' for e in trace if 'args' in e))
        self.assertTrue(any(e['args'].get('tokens.total_tokens') == 130 for e in trace if 'args' in e))

    def test_repeated_imports_preserve_native_bytes_and_content_free_stable_outputs(self):
        path, _ = self.source()
        before = path.read_bytes()
        first = self.cli('usage_report.py', self.root)
        self.assertEqual(first.returncode, 0, first.stderr)
        outputs = {p: p.read_bytes() for p in [*self.root.glob('reports/*'), *self.root.glob('runs/*/*/trace.jsonl')]}
        second = self.cli('usage_report.py', self.root)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual({p:p.read_bytes() for p in outputs}, outputs)
        self.assertEqual(path.read_bytes(), before)
        self.assertNotIn(b'PRIVATE_', b''.join(outputs.values()))
        events, _ = self.evidence()
        self.assertTrue(all(e['event_id'] and e['native_event_id'] and e['provenance'] for e in events))

    def test_response_dedup_and_conflicting_native_measurements(self):
        path, _ = self.source()
        rows = path.read_text().splitlines()
        duplicate = next(row for row in rows if 'token_usage_record' in row)
        path.write_text('\n'.join(rows + [duplicate]) + '\n')
        report = usage.refresh(self.root)
        self.assertEqual(report['summary']['tokens']['total_tokens']['total'], 200)
        changed = json.loads(duplicate)
        changed['payload']['usage']['input_tokens'] = 101
        with path.open('a') as stream:
            stream.write(json.dumps(changed) + '\n')
        with self.assertRaisesRegex(ValueError, 'conflicting duplicate'):
            usage.refresh(self.root)

    def test_missing_counters_and_partial_attribution_preserve_known_usage(self):
        path, _ = self.source(bind=False)
        rows = [json.loads(r) for r in path.read_text().splitlines()]
        for row in rows:
            if row['type'] == 'token_usage_record' and row['payload']['response_id'] == 'response-1':
                del row['payload']['usage']['cached_input_tokens']
        path.write_text(''.join(json.dumps(r) + '\n' for r in rows))
        report = usage.refresh(self.root)
        self.assertEqual(report['summary']['tokens']['input_tokens']['total'], 150)
        self.assertEqual(report['summary']['tokens']['cached_input_tokens'], dict(total=None, known_subtotal=10, measured_records=1, missing_records=1))
        self.assertEqual(report['groups']['task'], [])
        self.assertGreater(len(report['attribution_omissions']['task']['event_ids']), 0)
        self.assertFalse(list(self.root.glob('runs/*/*/trace.jsonl')))

    def test_aggregate_snapshots_and_truncated_capture_are_omissions(self):
        path, _ = self.source(turns=['turn-1'])
        rows = [json.loads(r) for r in path.read_text().splitlines()]
        rows = [r for r in rows if r['type'] != 'token_usage_record']
        path.write_text(''.join(json.dumps(r) + '\n' for r in rows) + '{"truncated":')
        report = usage.refresh(self.root)
        self.assertIsNone(report['summary']['tokens']['total_tokens']['known_subtotal'])
        self.assertIn('missing_usage', report['summary']['coverage'])
        self.assertIn('invalid_json_line', report['summary']['coverage'])
        self.assertIsNone(report['groups']['task'][0]['summary']['tokens']['total_tokens']['total'])

    def test_failed_tools_unfinished_runs_and_wrapper_nested_relationships(self):
        path, _ = self.source(turns=['turn-1'])
        rows = [json.loads(r) for r in path.read_text().splitlines()]
        rows = [r for r in rows if r['payload'].get('type') != 'task_complete']
        path.write_text(''.join(json.dumps(r) + '\n' for r in rows))
        events, gaps = self.evidence()
        report = usage.build_report(events, gaps)
        self.assertEqual(report['summary']['outcomes'], {'failed':1, 'returned':1})
        self.assertEqual(report['summary']['wrapper_calls'], 1)
        self.assertEqual(report['summary']['observed_nested_operations'], 1)
        self.assertIn('unfinished_turn', report['summary']['coverage'])
        self.assertIsNone(report['summary']['tokens']['input_tokens']['total'])
        self.assertEqual(report['summary']['tokens']['input_tokens']['known_subtotal'], 100)
        self.assertIsNone(report['groups']['model_effort'][0]['summary']['tokens']['total_tokens']['total'])

    def test_opencode_unfinished_zero_initialized_aggregate_is_not_measurement(self):
        path, _ = self.source('opencode', turns=['turn-2'])
        data = json.loads(path.read_text())
        data['messages'][1]['parts'] = []
        data['messages'][1]['info']['time'].pop('completed')
        data['messages'][1]['info'].pop('finish')
        data['messages'][1]['info']['tokens'] = {'input':0,'output':0,'reasoning':0,'cache':{'read':0,'write':0}}
        path.write_text(json.dumps(data))
        report = usage.refresh(self.root)
        self.assertIsNone(report['summary']['tokens']['total_tokens']['known_subtotal'])
        self.assertIn('unfinished_turn', report['summary']['coverage'])

    def test_native_lineage_parallel_children_forks_and_perfetto_subset(self):
        self.source()
        self.source(sid='implementer', parent='supervisor', role='implementer', task='work')
        self.source(sid='reviewer', parent='implementer', role='reviewer', task='work')
        self.source(sid='parallel', parent='supervisor', fork='implementer', role='validator', task='validation')
        events, gaps = self.evidence()
        tree = usage.build_report(events, gaps)['spawn_tree']
        self.assertEqual({(e['parent'],e['child'],e['relationship']) for e in tree['edges']},
                         {('codex:supervisor','codex:implementer','spawn'), ('codex:implementer','codex:reviewer','spawn'),
                          ('codex:supervisor','codex:parallel','spawn'), ('codex:implementer','codex:parallel','fork')})
        trace = usage.timeline(events)
        rows = trace['traceEvents']
        self.assertEqual(sum(r['ph'] == 'M' for r in rows), 4)
        self.assertEqual(sum(r['ph'] == 's' for r in rows), 3)
        self.assertEqual(sum(r['ph'] == 'f' for r in rows), 3)
        # Guard the Chrome Trace numeric/hex-ID contract caught by real Perfetto.
        for flow in (r for r in rows if r['ph'] in ('s', 'f')):
            fid = flow['id']
            if isinstance(fid, str):
                self.assertRegex(fid, r'^0x[0-9a-fA-F]{1,16}$')
            else:
                self.assertIsInstance(fid, int)
                self.assertTrue(0 <= fid < 2**53)
        self.assertTrue(all(r['ph'] in ('M','X','i','s','f') for r in rows))
        tool = next(r for r in rows if r['ph'] == 'X' and r['name'] == 'exec_command')
        self.assertEqual(tool['dur'], 1_000_000)
        self.assertTrue(all('dur' not in r for r in rows if r['ph'] != 'X'))
        self.assertTrue(trace['metadata']['timing_omissions'])

    def test_native_source_version_is_derived_and_unverified_versions_are_disclosed(self):
        path, _ = self.source()
        path.write_text(path.read_text().replace('0.167.0', 'unknown'))
        report = usage.refresh(self.root)
        self.assertIn('unverified_native_version', report['summary']['coverage'])
        self.assertEqual(report['summary']['tokens']['total_tokens']['known_subtotal'], 200)

    def test_output_aliases_and_directory_escapes_cannot_overwrite_native_logs(self):
        for alias in ('symlink', 'hardlink', 'directory', 'internal-directory', 'native-directory'):
            with self.subTest(alias=alias):
                self.root = records.allocate(self.suite, alias)
                path, _ = self.source('opencode' if alias in ('internal-directory', 'native-directory') else 'codex')
                output = self.root / 'reports/usage.json'
                if alias == 'symlink':
                    output.symlink_to(path)
                elif alias == 'hardlink':
                    output.hardlink_to(path)
                elif alias == 'internal-directory':
                    path = path.rename(self.root / 'native/usage.json')
                    (self.root / 'reports').rmdir()
                    (self.root / 'reports').symlink_to(self.root / 'native', target_is_directory=True)
                elif alias == 'native-directory':
                    path.rename(output)
                    (self.root / 'native').rmdir()
                    (self.root / 'native').symlink_to(self.root / 'reports', target_is_directory=True)
                    path = self.root / 'native/usage.json'
                else:
                    (self.root / 'reports').rmdir()
                    (self.root / 'reports').symlink_to(Path(self.temp.name))
                before = path.read_bytes()
                result = self.cli('usage_report.py', self.root)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual(path.read_bytes(), before)

    def test_opencode_multiple_steps_count_components_once_and_normalize_failure(self):
        path, _ = self.source('opencode', turns=['turn-1'])
        data = json.loads(path.read_text())
        message = data['messages'][1]
        message['parts'].insert(1, dict(message['parts'][0], id='step-2'))
        # Native message tokens repeat the latest step, not the sum.
        path.write_text(json.dumps(data))
        report = usage.refresh(self.root)
        self.assertEqual(report['summary']['tokens']['total_tokens']['total'], 260)
        self.assertEqual(report['summary']['observed_model_measurements'], 2)
        self.assertEqual(report['summary']['outcomes'], {'failed':1})

    def test_inconsistent_native_counters_are_rejected(self):
        for metric, invalid in [('cached_input_tokens',101), ('reasoning_output_tokens',31)]:
            with self.subTest(metric=metric):
                self.root = records.allocate(self.suite, 'invalid')
                path, _ = self.source()
                rows = [json.loads(r) for r in path.read_text().splitlines()]
                next(r for r in rows if r['type'] == 'token_usage_record')['payload']['usage'][metric] = invalid
                path.write_text(''.join(json.dumps(r) + '\n' for r in rows))
                with self.assertRaisesRegex(ValueError, 'exceed'):
                    usage.refresh(self.root)

    def test_completed_opencode_failure_has_no_measurement_but_retains_completed_steps(self):
        path, _ = self.source('opencode', turns=['turn-2'])
        data = json.loads(path.read_text())
        message = data['messages'][1]
        message['info'].pop('finish')
        message['info']['error'] = {'name':'APIError','data':{'message':'PRIVATE_ERROR'}}
        message['info']['tokens'] = {'input':0,'output':0,'reasoning':0,'cache':{'read':0,'write':0}}
        step = message['parts'].pop()
        path.write_text(json.dumps(data))
        report = usage.refresh(self.root)
        tokens = report['summary']['tokens']['total_tokens']
        self.assertIsNone(tokens['total'])
        self.assertIsNone(tokens['known_subtotal'])
        self.assertEqual(tokens['missing_records'], 1)
        self.assertIn('unmeasured_message', report['summary']['coverage'])
        message['parts'].append(step)
        path.write_text(json.dumps(data))
        report = usage.refresh(self.root)
        self.assertEqual(report['summary']['tokens']['total_tokens']['known_subtotal'], 70)

    def test_native_mcp_transport_tool_failure_success_and_unknown_status(self):
        for result, expected in [({'Err':'PRIVATE_ERROR'},'failed'), ({'Ok':{'isError':True}},'failed'),
                                 ({'Ok':{'isError':False}},'completed'), ({},'returned')]:
            with self.subTest(result=result):
                self.root = records.allocate(self.suite, 'mcp')
                path, _ = self.source(turns=['turn-1'])
                rows = [json.loads(r) for r in path.read_text().splitlines()]
                for row in rows:
                    p = row['payload']
                    if p.get('type') == 'exec_command_end':
                        p.pop('exit_code')
                        p.update(type='mcp_tool_call_end',result=result)
                path.write_text(''.join(json.dumps(r) + '\n' for r in rows))
                events, _ = self.evidence()
                tool = next(e for e in events if e.get('call_id') == 'nested')
                self.assertEqual(tool['outcome'], expected)
                self.assertNotIn('PRIVATE_ERROR', json.dumps(events))

    def test_source_wide_gaps_propagate_to_each_affected_assignment_and_model(self):
        path, source = self.source(bind=False)
        self.tag(path, {'turn-1': dict(task='first', role='implementer'),
                        'turn-2': dict(task='second', role='implementer')})
        with path.open('a') as stream:
            stream.write('{"truncated":')
        report = usage.refresh(self.root)
        for name in ('task','agent_run','role','model_effort'):
            with self.subTest(group=name):
                self.assertTrue(report['groups'][name])
                for row in report['groups'][name]:
                    self.assertIsNone(row['summary']['tokens']['total_tokens']['total'])
                    self.assertGreater(row['summary']['tokens']['total_tokens']['known_subtotal'], 0)
                    self.assertIn('invalid_json_line', row['summary']['coverage'])

    @unittest.skipUnless(os.environ.get('PERFETTO_TRACE_PROCESSOR'), 'optional real Perfetto parser unavailable')
    def test_real_perfetto_preserves_spawn_direction_without_enclosing_parent_slice(self):
        # Reduced metadata-only case from real capture: parent has an instant,
        # child has a running slice, and native creation is between operations.
        base = dict(kind='agent', adapter='codex', timestamp=None, parent_session_id=None,
                    event_id='parent', agent_id='codex:parent', start=100, end=None)
        events = [base, dict(base,event_id='child',agent_id='codex:child',parent_session_id='parent',
                            start=101,end=105,spawn_timestamp=101.5),
                  dict(base,kind='model',event_id='model',start=None,end=101.4,timestamp=101.4)]
        trace = self.root / 'timeline.json'
        trace.write_text(json.dumps(usage.timeline(events)))
        def query(sql):
            result = subprocess.run([os.environ['PERFETTO_TRACE_PROCESSOR'], 'query', '--format', 'csv', str(trace), sql],
                                    text=True, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr)
            return list(csv.DictReader(io.StringIO(result.stdout)))
        self.assertEqual(query("SELECT name,value FROM stats WHERE value != 0 AND severity IN ('error','data_loss')"), [])
        edges = query('SELECT outgoing.name AS parent, incoming.name AS child FROM flow '
                      'JOIN slice AS s1 ON flow.slice_out=s1.id JOIN thread_track AS t1 ON s1.track_id=t1.id '
                      'JOIN thread AS outgoing ON t1.utid=outgoing.utid JOIN slice AS s2 ON flow.slice_in=s2.id '
                      'JOIN thread_track AS t2 ON s2.track_id=t2.id JOIN thread AS incoming ON t2.utid=incoming.utid')
        self.assertEqual(edges, [{'parent':'codex:parent · unavailable','child':'codex:child · unavailable'}])

    def test_accounting_ignores_harness_identity_for_identical_normalized_evidence(self):
        self.source()
        events, diagnostics = self.evidence()
        other = copy.deepcopy(events)
        for event in other:
            event['adapter'] = 'another-adapter'
            event['provenance'] = [{'adapter':'another-adapter'}]
        self.assertEqual(usage.summarize(events, diagnostics), usage.summarize(other, diagnostics))


if __name__ == '__main__':
    unittest.main()
