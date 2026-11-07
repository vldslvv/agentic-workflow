"""Public Make/HTTP lifecycle checks using real processes and disposable native sources.

BROWSER points to a recording executable: browser-window behavior is checked by
separate real-UI smoke evidence, while these tests verify the actual launch URL.
Port 9001 must be free; no unrelated process is terminated to run these checks.
"""
from concurrent.futures import ThreadPoolExecutor
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
from html import unescape
import json
import os
import re
from pathlib import Path
import shlex
import signal
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
        (root / 'native.jsonl').write_bytes((ROOT / 'spec-source-suite/tests/fixtures/codex-0.167.0.jsonl').read_bytes())
        records.add_source(root, dict(id='native', adapter='codex', source_version='codex-rollout-0.167.0',
                                     path='native.jsonl', session_id='supervisor', turn_ids=['turn-1','turn-2']))
        records.bind(root, dict(id='work', source_id='native', turn_ids=['turn-1','turn-2'],
                               task_id='work', role='implementer', agent_run_id='worker',
                               agent_name='Builder <one>', purpose='Implement <script>alert(1)</script>'))
        return root

    def command(self, root=None):
        # Run from another cwd and pass a path with spaces through the real Makefile.
        return ['make', '-f', str(ROOT / 'Makefile'), 'trace', f'IMPL={root or self.root}']

    def launch(self):
        output = tempfile.TemporaryFile(mode='w+')
        process = subprocess.Popen(self.command(), cwd=self.base, env=self.env, stdout=output,
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

    def test_make_refreshes_opens_reuses_and_serves_only_normalized_insights(self):
        native = self.root / 'native.jsonl'
        original = native.read_bytes()
        self.launch()
        status, urls = self.ready()
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
        for path in ('/', '/status', '/implementation.json', '/native.jsonl', '/../native.jsonl'):
            with self.subTest(path=path), self.assertRaises(HTTPError) as failure:
                self.http.open('http://127.0.0.1:9001'+path)
            self.assertEqual(failure.exception.code, 404)
            failure.exception.close()
        with self.assertRaises(HTTPError) as failure:
            self.http.open(Request(trace_url, headers={'Origin':'https://unrelated.invalid'}))
        self.assertEqual(failure.exception.code, 403)
        failure.exception.close()
        # Refresh must be visible through the already-running server.
        native.write_text(original.decode().replace('model-a', 'updated-model'))
        repeat = subprocess.run(self.command(), cwd=self.base, env=self.env, capture_output=True, text=True, timeout=8)
        self.assertEqual(repeat.returncode, 0, repeat.stderr)
        with self.http.open(trace_url) as response:
            latest = response.read()
        self.assertIn(b'updated-model', latest)
        self.assertNotEqual(initial, latest)
        report = json.loads((self.root/'reports/usage.json').read_text())
        self.assertEqual(report['summary']['tokens']['total_tokens']['total'], 200)
        self.assertEqual(report['summary']['observed_model_measurements'], 2)
        other = self.implementation('other')
        rejected = subprocess.run(self.command(other), cwd=self.base, env=self.env, capture_output=True, text=True, timeout=8)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn('occupied', rejected.stderr)
        self.assertEqual(self.status()['pid'], status['pid'])

    def test_concurrent_make_invocations_and_shutdown_restart(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            processes = list(pool.map(lambda _:self.launch(), range(2)))
        status, urls = self.ready(2)
        self.assertEqual(urls[0], urls[1])
        deadline = time.monotonic()+5
        while all(p.poll() is None for p in processes) and time.monotonic()<deadline:
            time.sleep(.05)
        self.assertEqual(sum(p.poll() is None for p in processes), 1)
        self.assertEqual([p.returncode for p in processes if p.poll() is not None], [0])
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
