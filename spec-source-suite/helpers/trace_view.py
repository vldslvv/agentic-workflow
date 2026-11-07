#!/usr/bin/env python3
"""Collect native evidence, analyze it and open one implementation's agent insights.

The foreground viewer serves normalized reports on loopback port 9001
(the port allowed by Perfetto's CSP). Repeated invocations reuse a compatible
viewer for the same implementation. The owning viewer refreshes immediately,
then waits the configured interval after each collection attempt until Ctrl+C.
"""
import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import errno
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import os
from pathlib import Path
import re
import secrets
import signal
import stat
import threading
import time
from urllib.parse import quote
from urllib.request import ProxyHandler, build_opener
import webbrowser

from trace_dashboard import render
from usage_report import refresh

HOST, PORT = '127.0.0.1', 9001
ORIGIN = 'https://ui.perfetto.dev'
SERVICE = 'suite-insights-v4'
# /status belongs to Perfetto's native RPC probe; it must remain a 404 here.
STATUS_PATH = '/__suite_trace_viewer__'


def viewer_url(token):
    return f'http://{HOST}:{PORT}/{token}/'


def perfetto_url(token):
    source = f'http://{HOST}:{PORT}/{token}/timeline.json'
    return f'{ORIGIN}/#!/?url={quote(source, safe="")}&referrer=spec-source-suite'


def read_report(root, filename):
    """Read only regular, unaliased reports, including after viewer startup.

    Directory descriptors and O_NOFOLLOW keep the opened boundary stable if a
    report directory is replaced between validation and reading.
    """
    with ExitStack() as resources:
        parent = None
        for path in (root, 'reports'):
            parent = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent)
            resources.callback(os.close, parent)
        descriptor = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        stream = resources.enter_context(os.fdopen(descriptor, 'rb'))
        metadata = os.fstat(stream.fileno())
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
            raise ValueError('report aliases another file or is not regular')
        return stream.read()


class Viewer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, root, interval):
        self.root = root
        self.interval = interval
        self.refresh_status = (None, None)
        self.initial_collection = threading.Event()
        self.token = secrets.token_hex(16)
        super().__init__((HOST, PORT), Handler)

    def collect(self):
        report = refresh(self.root)
        self.refresh_status = (datetime.now(timezone.utc).isoformat(timespec='seconds'), None)
        return report


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def reply(self, code, data=b'', content_type='application/json'):
        self.send_response(code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Access-Control-Allow-Origin', ORIGIN)
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Private-Network', 'true')
        self.end_headers()
        self.wfile.write(data)

    def allowed(self):
        return (self.headers.get('Host') == f'{HOST}:{PORT}' and
                self.headers.get('Origin') in (None, ORIGIN))

    def do_OPTIONS(self):
        self.reply(204 if self.allowed() else 403)

    def do_GET(self):
        if not self.allowed():
            self.reply(403)
        elif self.path == STATUS_PATH:
            self.reply(200, json.dumps(dict(service=SERVICE, implementation=str(self.server.root),
                                           token=self.server.token, pid=os.getpid(),
                                           interval=self.server.interval)).encode())
        elif self.path in (f'/{self.server.token}/', f'/{self.server.token}/usage.json',
                           f'/{self.server.token}/timeline.json'):
            # Identity is available while initial collection waits on the
            # implementation lock, but pages must wait for its first result.
            self.server.initial_collection.wait()
            if self.server.refresh_status[0] is None:
                self.reply(503)
                return
            dashboard = self.path.endswith('/')
            filename = 'usage.json' if dashboard else self.path.rsplit('/', 1)[1]
            try:
                data = read_report(self.server.root, filename)
                if dashboard:
                    try:
                        timeline = read_report(self.server.root, 'timeline.json')
                    except FileNotFoundError:
                        timeline = b'{"traceEvents":[]}'
                    available = any(e.get('ph') != 'M' for e in json.loads(timeline).get('traceEvents', []))
                    refreshed, error = self.server.refresh_status
                    self.reply(200, render(json.loads(data), perfetto_url(self.server.token) if available else None,
                                           interval=self.server.interval, refreshed=refreshed,
                                           error=error).encode(), 'text/html; charset=utf-8')
                else:
                    self.reply(200, data)
            except FileNotFoundError:
                self.reply(404)
            except (OSError, ValueError):
                self.reply(403)
        else:
            self.reply(404)


def existing_viewer(root):
    """Check identity before reusing a listener; never kill a port occupant."""
    opener = build_opener(ProxyHandler({}))
    for _ in range(10):
        try:
            with opener.open(f'http://{HOST}:{PORT}{STATUS_PATH}', timeout=.2) as response:
                status = json.loads(response.read(8192))
            if (status.get('service') == SERVICE and status.get('implementation') == str(root)
                    and re.fullmatch(r'[0-9a-f]{32}', status.get('token', ''))):
                return status
            break
        except (OSError, ValueError, AttributeError, TypeError):
            time.sleep(.1)  # A concurrently starting viewer may not yet be serving.
    raise ValueError(f'Port {PORT} is occupied by another process, implementation or older viewer; stop that viewer before retrying.')


def open_browser(url):
    print(f'Agent insights: {url}', flush=True)
    print('Use “Open timeline in Perfetto” for timing; allow local-device access if prompted.', flush=True)
    try:
        opened = webbrowser.open(url, new=0)
    except (OSError, webbrowser.Error):
        opened = False
    if not opened:
        print('Browser launch unavailable. Open the dashboard URL above on this machine.', flush=True)


def positive_interval(value):
    try:
        interval = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError('interval must be positive and finite') from None
    if not math.isfinite(interval) or interval <= 0:
        raise argparse.ArgumentTypeError('interval must be positive and finite')
    return interval


def wait_interval(interval):
    # Bound individual sleeps so even very large finite intervals are supported.
    started = time.monotonic()
    while (remaining := interval - (time.monotonic() - started)) > 0:
        time.sleep(min(remaining, 3600))


def run(root, interval=5):
    root = Path(root).resolve()
    try:
        server = Viewer(root, interval)
    except OSError as exc:
        if exc.errno != errno.EADDRINUSE:
            raise
        status = existing_viewer(root)
        print(f'Reusing the running viewer (interval {status["interval"]:g}s). '
              'Restart the owning viewer to change its interval.', flush=True)
        open_browser(viewer_url(status['token']))
        return
    with server:
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            # Initial failures remain command errors; only the owner collects.
            report = server.collect()
            server.initial_collection.set()
            print(f'Refreshed {report["implementation_id"]}: {root / "reports"}', flush=True)
            if not report['summary']['observed_model_measurements'] and not report['summary']['observed_tool_calls']:
                print('No imported execution observations in this report; the viewer cannot reconstruct missing native evidence.', flush=True)
            if report['summary']['coverage']:
                print('Coverage: ' + json.dumps(report['summary']['coverage'], sort_keys=True), flush=True)
            print(f'Serving agent insights locally; refreshing every {interval:g}s after collection. '
                  'Ctrl+C stops collection and serving.', flush=True)
            open_browser(viewer_url(server.token))
            while True:
                wait_interval(interval)
                try:
                    server.collect()
                except (OSError, ValueError, KeyError, TypeError) as exc:
                    server.refresh_status = (server.refresh_status[0], 'Refresh failed; retrying on the next cycle.')
                    print(f'trace-view: refresh failed: {exc}', flush=True)
        finally:
            server.initial_collection.set()
            server.shutdown()
            worker.join()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('implementation', type=Path)
    parser.add_argument('--interval', type=positive_interval, default=5,
                        metavar='SECONDS', help='collection and browser poll interval (default: 5; restart viewer to change)')
    args = parser.parse_args()
    def stop(_signum, _frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)
    try:
        run(args.implementation, args.interval)
    except KeyboardInterrupt:
        print('\nViewer stopped.', flush=True)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'trace-view: {exc}\n')


if __name__ == '__main__':
    main()
