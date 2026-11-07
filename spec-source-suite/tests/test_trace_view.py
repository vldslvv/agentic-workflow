"""Public Make/HTTP lifecycle checks using real processes and disposable native sources.

BROWSER points to a recording executable: browser-window behavior is checked by
separate real-UI smoke evidence, while these tests verify the actual launch URL.
Port 9001 must be free; no unrelated process is terminated to run these checks.
"""
from concurrent.futures import ThreadPoolExecutor
import fcntl
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from html import unescape
import json
import os
import re
from pathlib import Path
import shlex
import signal
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request, ProxyHandler, build_opener

ROOT = Path(__file__).resolve().parents[2]
HELPERS = ROOT / 'spec-source-suite/helpers'
sys.path.insert(0, str(HELPERS))
import records
from usage_report import refresh
from unittest.mock import patch
from test_native_collection import row, turn, dispatch


class ViewerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='suite viewer ')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.http = build_opener(ProxyHandler({}))
        try:
            self.http.open('http://127.0.0.1:9001/__suite_trace_viewer__', timeout=.2).close()
        except HTTPError as exc:
            exc.close()
            self.fail('Port 9001 is occupied; stop the local viewer before running tests.')
        except URLError:
            pass
        else:
            self.fail('Port 9001 is occupied; stop the local viewer before running tests.')
        self.environment = patch.dict(os.environ, CODEX_HOME=str(self.base), CODEX_THREAD_ID='')
        self.environment.start()
        self.addCleanup(self.environment.stop)
        c = sqlite3.connect(str(self.base / 'state_5.sqlite'))
        c.execute('CREATE TABLE threads (id TEXT, rollout_path TEXT, source TEXT)')
        c.commit()
        c.close()
        self.root = self.implementation('demo')
        self.browser_log = self.base / 'browser.jsonl'
        browser = self.base / 'browser.py'
        browser.write_text('import os,sys,json\nwith open(os.environ["TRACE_BROWSER_LOG"],"a") as f: f.write(json.dumps(sys.argv[1:])+"\\n")\n')
        self.env = dict(os.environ, BROWSER=shlex.join([sys.executable, str(browser), '%s']),
                        TRACE_BROWSER_LOG=str(self.browser_log))
        self.processes = []
        self.addCleanup(self.stop_all)

    def implementation(self, name):
        root = records.allocate(self.base / '.suite', name)
        path = root / 'native' / 'capture.jsonl'
        path.parent.mkdir()
        rows = [json.loads(line) for line in (ROOT / 'spec-source-suite/tests/fixtures/codex-0.167.0.jsonl').read_text().splitlines()]
        rows[0]['payload']['agent_nickname'] = 'Builder <one>'
        selected = []
        active = None
        for row in rows:
            active = row['payload'].get('turn_id') or active
            if active == 'unselected':
                continue
            selected.append(row)
            if row['type'] == 'turn_context':
                tag = dict(implementation=root.name, task='work', role='implementer', purpose='Implement <script>alert(1)</script>')
                selected.append(dict(timestamp=row['timestamp'], type='response_item', payload=dict(
                    type='message', role='user', content=[dict(type='input_text', text='SUITE ' + json.dumps(tag))])))
        path.write_text(''.join(json.dumps(r) + '\n' for r in selected))
        refresh(root)
        return root

    @unittest.skipUnless(os.environ.get('PLAYWRIGHT_MODULE'), 'optional real browser unavailable')
    def test_browser_content_search_selection_refresh_and_inert_payloads(self):
        native = self.root / 'native/capture.jsonl'
        marker = 'Unicode 雪\nprint("snow")\n</script><script>globalThis.injected=true</script>\n' + 'long content\n' * 200
        with native.open('a') as stream:
            for i in range(60):
                stream.write(json.dumps(dict(timestamp=1793959261, type='response_item', payload=dict(
                    type='message', id=f'browser-{i}', turn_id='turn-2', role='assistant', content=marker))) + '\n')
        self.launch(interval=.2)
        _, urls = self.ready()
        result = subprocess.run(['node', str(Path(__file__).with_name('trace_dashboard_browser.cjs')), urls[0], str(native)],
                                env=self.env, capture_output=True, text=True, timeout=40)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_empty_recording_is_explained_after_refresh(self):
        self.root = records.allocate(self.base / '.suite', 'empty')
        refresh(self.root)
        before = {str(p): p.read_bytes()
                  for p in self.root.rglob('*') if p.is_file()}
        self.launch()
        _, urls = self.ready()
        with self.http.open(urls[0]) as response:
            dashboard = response.read().decode()
        self.assertIn('No imported execution observations', dashboard)
        self.assertIn('No timeline events to display', dashboard)
        self.assertNotIn('id="perfetto" href=', dashboard)
        self.assertEqual(before, {str(p): p.read_bytes()
                                 for p in self.root.rglob('*') if p.is_file()})

    def command(self, root=None, interval=None):
        # Run from another cwd and pass a path with spaces through the real Makefile.
        return ['make', '-f', str(ROOT / 'Makefile'), 'trace', f'IMPL={root or self.root}',
                *([] if interval is None else [f'TRACE_INTERVAL={interval}'])]

    def launch(self, interval=None):
        output = tempfile.TemporaryFile(mode='w+')
        process = subprocess.Popen(self.command(interval=interval), cwd=self.base, env=self.env, stdout=output,
                                   stderr=subprocess.STDOUT, start_new_session=True)
        self.processes.append((process, output))
        return process

    def stop_all(self):
        for process, output in self.processes:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGINT)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait(timeout=5)
            output.close()

    def status(self):
        with self.http.open('http://127.0.0.1:9001/__suite_trace_viewer__', timeout=.5) as response:
            return json.load(response)

    def ready(self, browser_calls=1):
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            try:
                status = self.status()
                lines = self.browser_log.read_text().splitlines()
                if len(lines) >= browser_calls:
                    return status, [json.loads(line)[0] for line in lines]
            except (OSError, ValueError):
                pass
            time.sleep(.05)
        self.fail('Viewer/browser did not become ready')

    def wait_for(self, read, predicate):
        deadline = time.monotonic() + 8
        value = None
        while time.monotonic() < deadline:
            value = read()
            if predicate(value):
                return value
            time.sleep(.05)
        self.fail(f'Viewer did not update: {str(value)[:1000]}')

    def dashboard(self, url):
        with self.http.open(url, timeout=1) as response:
            return response.read().decode()

    def report(self):
        return json.loads((self.root / 'reports/usage.json').read_text())

    def native(self, sid, rows, parent=None):
        source = dict(subagent=dict(thread_spawn=dict(parent_thread_id=parent, agent_path='/root/child'))) if parent else 'cli'
        path = self.base / f'{sid}.jsonl'
        meta = row('session_meta', dict(id=sid, cli_version='0.167.0', timestamp=100, source=source))
        path.write_text(''.join(json.dumps(r) + '\n' for r in [meta, *rows]))
        with sqlite3.connect(self.base / 'state_5.sqlite') as index:
            index.execute('INSERT INTO threads VALUES (?,?,?)', (sid, str(path), json.dumps(source)))
        return path

    def append_native(self, path, rows):
        with path.open('a') as stream:
            stream.write(''.join(json.dumps(r) + '\n' for r in rows))

    def test_live_collection_discovers_delayed_children_and_excludes_unselected_turns(self):
        tag = 'SUITE ' + json.dumps(dict(implementation=self.root.name, task='work', role='implementer'))
        selected = turn('root', 'selected', 100, tag)
        native = self.native('root', selected[:3])
        (self.root / 'native/capture.jsonl').unlink()
        (self.root / 'tasks/work').mkdir(parents=True)
        captured = subprocess.run([sys.executable, str(HELPERS / 'records.py'), 'resolve', str(self.root), 'work'],
                                  env=dict(self.env, CODEX_THREAD_ID='root'), capture_output=True, text=True)
        self.assertEqual(captured.returncode, 0, captured.stderr)
        self.launch(interval=.1)
        status, urls = self.ready()
        self.assertEqual(self.report()['summary']['observed_model_measurements'], 0)
        initial_timeline = (self.root / 'reports/timeline.json').read_bytes()
        self.append_native(native, [selected[3], *dispatch('spawn_agent', 'spawn',
                           dict(task_name='child', message=tag), dict(agent_id='child')), selected[4]])
        self.wait_for(self.report, lambda report: report['summary']['observed_model_measurements'] == 1)
        self.assertEqual(status['interval'], .1)
        # The dispatch is already captured when the child's native file arrives.
        child = self.native('child', turn('child', 'child-work', 200, tag), parent='root')
        unrelated = self.native('unrelated', turn('unrelated', 'unrelated-work', 100))
        self.append_native(native, turn('root', 'later-root-work', 300))
        originals = {path: path.read_bytes() for path in (native, child, unrelated, self.base / 'state_5.sqlite')}
        report = self.wait_for(self.report, lambda report: report['summary']['tokens']['total_tokens']['total'] == 26)
        self.assertEqual({t for node in report['spawn_tree']['nodes'] for t in node['turns']}, {'selected', 'child-work'})
        self.assertNotIn('unfinished_turn', report['summary']['coverage'])
        self.assertNotEqual((self.root / 'reports/timeline.json').read_bytes(), initial_timeline)
        self.assertIn('Last successful refresh:', self.dashboard(urls[0]))
        self.assertEqual({path: path.read_bytes() for path in originals}, originals)
        self.assertEqual(len(self.browser_log.read_text().splitlines()), 1)
        self.stop_all()
        self.processes.clear()
        with self.assertRaises(URLError):
            self.status()
        before = {path: path.read_bytes() for path in self.root.glob('reports/*')}
        after_stop = turn('child', 'child-work', 400)[3]
        after_stop['payload']['response_id'] = 'after-stop-response'
        self.append_native(child, [after_stop])
        time.sleep(.3)
        self.assertEqual({path: path.read_bytes() for path in before}, before)

    def test_refresh_failure_keeps_reports_reuses_owner_and_retries(self):
        self.launch(interval=.1)
        status, urls = self.ready()
        before = {path: path.read_bytes() for path in self.root.glob('reports/*')}
        annotations = self.root / 'assignment-annotations.json'
        annotations.write_text('{')
        failed = self.wait_for(lambda: self.dashboard(urls[0]), lambda page: 'data-error="Refresh failed;' in page)
        last_success = re.search(r'<time>(.*?)</time>', failed)[1]
        repeat = subprocess.run(self.command(interval=.02), cwd=self.base, env=self.env,
                                capture_output=True, text=True, timeout=8)
        self.assertEqual(repeat.returncode, 0, repeat.stderr)
        self.assertIn('Restart the owning viewer', repeat.stdout)
        self.assertEqual(self.status(), status)
        self.assertEqual({path: path.read_bytes() for path in before}, before)
        self.assertIn(f'<time>{last_success}</time>', self.dashboard(urls[0]))
        native = self.root / 'native/capture.jsonl'
        native.write_text(native.read_text().replace('model-a', 'recovered-model'))
        annotations.unlink()
        page = self.wait_for(lambda: self.dashboard(urls[0]),
                             lambda page: 'recovered-model' in page and 'data-error=""' in page)
        self.assertNotIn('data-error="Refresh failed;', page)
        self.assertEqual(self.report()['summary']['tokens']['total_tokens']['total'], 200)

    def test_invalid_intervals_and_initial_collection_failure_are_command_errors(self):
        for interval in ('0', '-1', 'nan', 'inf', '-inf', 'abc'):
            with self.subTest(interval=interval):
                result = subprocess.run(self.command(interval=interval), cwd=self.base, env=self.env,
                                        capture_output=True, text=True, timeout=8)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn('interval must be positive and finite', result.stderr)
        (self.root / 'assignment-annotations.json').write_text('{')
        result = subprocess.run(self.command(), cwd=self.base, env=self.env,
                                capture_output=True, text=True, timeout=8)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('trace-view:', result.stderr)
        self.assertFalse(self.browser_log.exists())
        with self.assertRaises(URLError):
            self.status()

    def test_make_refreshes_reuses_and_serves_only_reports(self):
        native = self.root / 'native/capture.jsonl'
        original = native.read_bytes()
        self.launch()
        status, urls = self.ready()
        self.assertEqual(status['interval'], 5)
        self.assertEqual(status['implementation'], str(self.root))
        self.assertEqual(urlsplit(urls[0]).netloc, '127.0.0.1:9001')
        with self.http.open(urls[0]) as response:
            self.assertIn('text/html', response.headers['Content-Type'])
            dashboard = response.read().decode()
        self.assertIn('Builder &lt;one&gt;', dashboard)
        self.assertIn('Implement &lt;script&gt;', dashboard)
        self.assertNotIn('<script>alert(1)</script>', dashboard)
        self.assertIn('Task + model + effort', dashboard)
        self.assertIn('Observed duration (s)', dashboard)
        perfetto = unescape(re.search(r'id="perfetto" href="([^"]+)"', dashboard)[1])
        self.assertEqual(urlsplit(perfetto).netloc, 'ui.perfetto.dev')
        trace_url = parse_qs(urlsplit(perfetto).fragment.split('?',1)[1])['url'][0]
        with self.http.open(urls[0] + 'usage.json') as response:
            self.assertEqual(json.load(response)['summary']['tokens']['total_tokens']['total'], 200)
        with self.http.open(urls[0] + 'events.json') as response:
            exported = json.load(response)
        self.assertTrue(any(e.get('content', {}).get('values', {}).get('arguments') == 'PRIVATE_ARGUMENTS'
                            for e in exported['events']))
        with self.http.open(Request(trace_url, headers={'Origin':'https://ui.perfetto.dev'})) as response:
            self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'https://ui.perfetto.dev')
            initial = response.read()
        self.assertEqual(initial, (self.root / 'reports/timeline.json').read_bytes())
        reports = {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (self.root/'reports').iterdir()}
        repeat = subprocess.run(self.command(), cwd=self.base, env=self.env, capture_output=True, text=True, timeout=8)
        self.assertEqual(repeat.returncode, 0, repeat.stdout+repeat.stderr)
        self.assertIn('Reusing', repeat.stdout)
        self.assertEqual(self.status()['pid'], status['pid'])
        self.assertEqual(reports, {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (self.root/'reports').iterdir()})
        self.assertEqual(native.read_bytes(), original)
        self.assertEqual(self.ready(2)[1], [urls[0], urls[0]])
        for path in ('/', '/status', '/implementation.json', '/native.jsonl', '/../native.jsonl', f'/{status["token"]}/../native/capture.jsonl',
                     f'/{status["token"]}/native/capture.jsonl'):
            with self.subTest(path=path), self.assertRaises(HTTPError) as failure:
                self.http.open('http://127.0.0.1:9001'+path)
            self.assertEqual(failure.exception.code, 404)
            failure.exception.close()
        with self.assertRaises(HTTPError) as failure:
            self.http.open(Request(trace_url, headers={'Origin':'https://unrelated.invalid'}))
        self.assertEqual(failure.exception.code, 403)
        failure.exception.close()
        other = self.implementation('other')
        rejected = subprocess.run(self.command(other), cwd=self.base, env=self.env, capture_output=True, text=True, timeout=8)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn('occupied', rejected.stderr)
        self.assertEqual(self.status()['pid'], status['pid'])

    def test_running_viewer_rejects_aliased_report_storage(self):
        self.launch()
        _, urls = self.ready()
        reports = self.root / 'reports'
        parked = self.root / 'parked-reports'
        private = b'{"private_prompt":"SYNTHETIC_PRIVATE_NATIVE"}'
        for filename in ('usage.json', 'timeline.json', 'events.json'):
            (self.root / 'native' / filename).write_bytes(private)
        # A running server must recheck storage on every request, including
        # report changes after the valid startup and refresh.
        reports.rename(parked)
        reports.symlink_to(self.root / 'native', target_is_directory=True)
        try:
            for endpoint in ('usage.json', 'timeline.json', 'events.json', ''):
                with self.subTest(alias='directory', endpoint=endpoint):
                    with self.assertRaises(HTTPError) as failure:
                        self.http.open(urls[0] + endpoint)
                    self.assertEqual(failure.exception.code, 403)
                    failure.exception.close()
        finally:
            reports.unlink()
            parked.rename(reports)
        for filename in ('usage.json', 'timeline.json', 'events.json'):
            output = reports / filename
            original = output.read_bytes()
            output.unlink()
            output.hardlink_to(self.root / 'native' / filename)
            try:
                for endpoint in (filename, ''):
                    with self.subTest(alias='hardlink', endpoint=endpoint):
                        with self.assertRaises(HTTPError) as failure:
                            self.http.open(urls[0] + endpoint)
                        self.assertEqual(failure.exception.code, 403)
                        failure.exception.close()
            finally:
                output.unlink()
                output.write_bytes(original)
        self.assertEqual((self.root / 'native/usage.json').read_bytes(), private)
        with self.http.open(urls[0] + 'usage.json') as response:
            self.assertEqual(json.load(response)['summary']['tokens']['total_tokens']['total'], 200)

    def test_concurrent_make_invocations_and_shutdown_restart(self):
        # Hold the real collection lock: reuse must work even before the owner
        # finishes its first pass, without launching a second collector.
        with (self.root / '.records.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            with ThreadPoolExecutor(max_workers=2) as pool:
                processes = list(pool.map(lambda _:self.launch(), range(2)))
            self.ready(1)
            deadline = time.monotonic()+5
            while all(p.poll() is None for p in processes) and time.monotonic()<deadline:
                time.sleep(.05)
            self.assertEqual(sum(p.poll() is None for p in processes), 1)
            self.assertEqual([p.returncode for p in processes if p.poll() is not None], [0])
        status, urls = self.ready(2)
        self.assertEqual(urls[0], urls[1])
        self.stop_all()
        self.processes.clear()
        with self.assertRaises(URLError):
            self.status()
        self.launch()
        restarted, _ = self.ready(3)
        self.assertNotEqual(restarted['pid'], status['pid'])
        self.assertEqual(json.loads((self.root/'reports/usage.json').read_text())['summary']['observed_model_measurements'], 2)

    def test_headless_cli_prints_usable_link_when_browser_is_unavailable(self):
        env = dict(os.environ, PATH=str(self.base), BROWSER='/missing-browser %s')
        env.pop('DISPLAY', None)
        env.pop('WAYLAND_DISPLAY', None)
        path = self.base / 'headless.log'
        output = path.open('w')
        process = subprocess.Popen([sys.executable, str(HELPERS/'trace_view.py'), str(self.root)],
                                   cwd=self.base, env=env, stdout=output, stderr=subprocess.STDOUT,
                                   start_new_session=True)
        self.processes.append((process,output))
        deadline = time.monotonic()+8
        while time.monotonic()<deadline:
            content = path.read_text()
            if 'Browser launch unavailable' in content:
                break
            if process.poll() is not None:
                self.fail(content)
            time.sleep(.05)
        self.assertIn('Browser launch unavailable', content)
        self.assertIn('Agent insights: http://127.0.0.1:9001/', content)
        self.assertEqual(self.status()['implementation'], str(self.root))

    def test_unrelated_port_occupant_is_preserved_and_no_browser_is_launched(self):
        class Unrelated(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b'{"service":"unrelated"}')
            def log_message(self,*args):
                pass
        with HTTPServer(('127.0.0.1',9001),Unrelated) as server:
            thread=threading.Thread(target=server.serve_forever,daemon=True)
            thread.start()
            try:
                result=subprocess.run(self.command(),cwd=self.base,env=self.env,capture_output=True,text=True,timeout=8)
                self.assertNotEqual(result.returncode,0)
                self.assertIn('occupied',result.stderr)
                self.assertFalse(self.browser_log.exists())
                self.assertEqual(self.status()['service'],'unrelated')
            finally:
                server.shutdown()
                thread.join()


if __name__ == '__main__':
    unittest.main()
