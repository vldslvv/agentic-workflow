"""AC-6: known totals, deduplication, scope, and unavailable counters."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'helpers' / 'usage_report.py'
spec = importlib.util.spec_from_file_location('usage_report', MODULE)
usage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(usage)


class UsageReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = {'version': 1,
                         'root': {'session_id': 'root', 'path': 'root.jsonl', 'turn_ids': ['selected'], 'role': 'supervisor'},
                         'descendants': [{'session_id': 'child', 'path': 'child.jsonl', 'turn_ids': ['work'], 'parent_session_id': 'root', 'role': 'reviewer'}]}

    def write(self, name, events):
        (self.root / name).write_text(''.join(json.dumps(e) + '\n' for e in events))

    def event(self, sid, turn, rid, tokens, timestamp='2026-01-01T00:00:00Z'):
        return {'type': 'usage', 'session_id': sid, 'turn_id': turn, 'response_id': rid,
                'timestamp': timestamp, 'usage': tokens}

    def test_known_totals_dedup_scope_descendants_and_batch_nested_counts(self):
        root = self.event('root', 'selected', 'response-1', {'input_tokens': 100, 'cached_input_tokens': 60, 'output_tokens': 30, 'reasoning_output_tokens': 10})
        child = self.event('child', 'work', 'response-1', {'input_tokens': 50, 'cached_input_tokens': 10, 'output_tokens': 20, 'reasoning_output_tokens': 5}, '2026-01-01T00:00:10Z')
        batch = {'type': 'tool_call', 'session_id': 'root', 'turn_id': 'selected', 'call_id': 'batch', 'name': 'functions.exec'}
        nested = {'type': 'tool_call', 'session_id': 'root', 'turn_id': 'selected', 'call_id': 'nested', 'name': 'exec_command', 'parent_call_id': 'batch'}
        self.write('root.jsonl', [root, root, batch, batch, nested,
                                 self.event('root', 'other', 'excluded', {'input_tokens': 999}),
                                 self.event('unrelated', 'selected', 'excluded2', {'input_tokens': 999})])
        self.write('child.jsonl', [child, child])
        (self.root / 'verification.json').write_text('{}')
        self.manifest['verification_subprocesses'] = [{'session_id': 'root', 'turn_id': 'selected', 'call_id': 'nested', 'count': 2, 'evidence_path': 'verification.json'}]
        result = usage.build_report(self.manifest, self.root)
        self.assertEqual({k: v['total'] for k, v in result['tokens'].items()},
                         {'input_tokens': 150, 'cached_input_tokens': 70, 'uncached_input_tokens': 80,
                          'output_tokens': 50, 'reasoning_output_tokens': 15, 'total_tokens': 200})
        self.assertEqual(result['model_responses'], 2)
        self.assertEqual(result['tool_calls'], 2)
        self.assertEqual(result['execution_batches'], 1)
        self.assertEqual(result['observed_nested_operations'], 1)
        self.assertEqual(result['verification_subprocesses'], 2)
        self.assertEqual(result['elapsed_seconds'], 10)
        self.assertEqual(result['roles']['reviewer']['tokens']['input_tokens']['total'], 50)

    def test_missing_counters_remain_unavailable_with_known_subtotals(self):
        self.write('root.jsonl', [self.event('root', 'selected', 'a', {'input_tokens': 10, 'output_tokens': 2})])
        self.write('child.jsonl', [self.event('child', 'work', 'b', {'input_tokens': 20, 'cached_input_tokens': 5, 'output_tokens': 3, 'reasoning_output_tokens': 1})])
        result = usage.build_report(self.manifest, self.root)
        self.assertEqual(result['tokens']['input_tokens']['total'], 30)
        self.assertEqual(result['tokens']['cached_input_tokens'], {'total': None, 'known_subtotal': 5, 'missing_records': 1})
        self.assertEqual(result['tokens']['uncached_input_tokens']['total'], None)
        self.assertIsNone(result['observed_nested_operations'])
        self.assertIsNone(result['verification_subprocesses'])

    def test_codex_records_use_thread_identity_and_response_ids_without_snapshot_double_count(self):
        events = [
            {'type': 'session_meta', 'payload': {'id': 'root', 'session_id': 'different-global-id'}},
            {'type': 'turn_context', 'timestamp': '2026-01-01T00:00:00Z', 'payload': {'turn_id': 'selected'}},
            {'type': 'token_usage_record', 'payload': {'thread_id': 'root', 'turn_id': 'selected', 'session_id': 'different-global-id', 'response_id': 'a', 'usage': {'input_tokens': 10, 'cached_input_tokens': 4, 'output_tokens': 2, 'reasoning_output_tokens': 1}}},
            {'type': 'event_msg', 'payload': {'type': 'token_count', 'info': {'last_token_usage': {'input_tokens': 10}}}},
            {'type': 'response_item', 'payload': {'type': 'custom_tool_call', 'call_id': 'c', 'name': 'exec'}},
            {'type': 'turn_context', 'payload': {'turn_id': 'unrelated'}},
            {'type': 'response_item', 'payload': {'type': 'function_call', 'call_id': 'ignored', 'name': 'exec_command'}},
        ]
        self.write('root.jsonl', events)
        self.manifest['descendants'] = []
        before = (self.root / 'root.jsonl').read_bytes()
        result = usage.build_report(self.manifest, self.root)
        self.assertEqual(result['model_responses'], 1)
        self.assertEqual(result['tokens']['total_tokens']['total'], 12)
        self.assertEqual(result['tool_calls'], 1)
        self.assertEqual((self.root / 'root.jsonl').read_bytes(), before)

    def test_unidentified_usage_and_legacy_snapshots_cannot_claim_zero(self):
        self.write('root.jsonl', [{'type': 'turn_context', 'payload': {'turn_id': 'selected'}}, {'type': 'event_msg', 'payload': {'type': 'token_count', 'info': {'last_token_usage': {'input_tokens': 123}}}}])
        self.manifest['descendants'] = []
        result = usage.build_report(self.manifest, self.root)
        self.assertIsNone(result['tokens']['input_tokens']['total'])
        self.assertIsNone(result['model_responses'])
        self.assertEqual(result['unidentified_usage_records'], 1)

    def test_selected_turn_without_usage_cannot_disappear_from_totals(self):
        self.write('root.jsonl', [self.event('root', 'selected', 'a', {'input_tokens': 10})])
        self.write('child.jsonl', [])
        result = usage.build_report(self.manifest, self.root)
        self.assertIsNone(result['tokens']['input_tokens']['total'])
        self.assertEqual(result['tokens']['input_tokens']['known_subtotal'], 10)
        self.assertIsNone(result['model_responses'])

    def test_disconnected_descendant_and_conflicting_duplicate_are_errors(self):
        self.manifest['descendants'][0]['parent_session_id'] = 'outside'
        with self.assertRaisesRegex(ValueError, 'connected'):
            usage.build_report(self.manifest, self.root)
        self.manifest['descendants'] = []
        self.write('root.jsonl', [self.event('root', 'selected', 'a', {'input_tokens': 10}), self.event('root', 'selected', 'a', {'input_tokens': 11})])
        with self.assertRaisesRegex(ValueError, 'conflicting duplicate'):
            usage.build_report(self.manifest, self.root)

    def test_cli_output_aliases_cannot_modify_input_logs(self):
        self.manifest['descendants'] = []
        manifest = self.root / 'sessions.json'
        manifest.write_text(json.dumps(self.manifest))
        source = self.root / 'root.jsonl'
        for alias_kind in ('same', 'symlink', 'hardlink'):
            with self.subTest(alias=alias_kind):
                self.write('root.jsonl', [self.event('root', 'selected', 'a', {'input_tokens': 10})])
                before = source.read_bytes()
                output = self.root / (alias_kind + '.json')
                if alias_kind == 'same':
                    output = source
                elif alias_kind == 'symlink':
                    output.symlink_to(source)
                else:
                    output.hardlink_to(source)
                result = subprocess.run([sys.executable, str(MODULE), str(manifest),
                                         '--root', str(self.root), '--output', str(output)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual(source.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
