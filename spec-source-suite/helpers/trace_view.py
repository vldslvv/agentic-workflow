#!/usr/bin/env python3
"""Refresh one implementation and open its agent insights dashboard.

The foreground viewer serves normalized reports on loopback port 9001
(the port allowed by Perfetto's CSP). Repeated invocations reuse a compatible
viewer for the same implementation. No source discovery or background daemon.
"""
import argparse
import errno
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import secrets
import signal
import threading
import time
from urllib.parse import quote
from urllib.request import ProxyHandler, build_opener
import webbrowser

from usage_report import refresh
from trace_dashboard import render

HOST, PORT = '127.0.0.1', 9001
ORIGIN = 'https://ui.perfetto.dev'
SERVICE = 'suite-insights-v2'
# /status belongs to Perfetto's native RPC probe; it must remain a 404 here.
STATUS_PATH = '/__suite_trace_viewer__'


def viewer_url(token):
    return f'http://{HOST}:{PORT}/{token}/'


def perfetto_url(token):
    source = f'http://{HOST}:{PORT}/{token}/timeline.json'
    return f'{ORIGIN}/#!/?url={quote(source, safe="")}&referrer=spec-source-suite'


class Viewer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, root):
        self.root = root
        self.token = secrets.token_hex(16)
        super().__init__((HOST, PORT), Handler)


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
                                           token=self.server.token, pid=os.getpid())).encode())
        elif self.path in (f'/{self.server.token}/', f'/{self.server.token}/usage.json',
                           f'/{self.server.token}/timeline.json'):
            dashboard = self.path.endswith('/')
            filename = 'usage.json' if dashboard else self.path.rsplit('/', 1)[1]
            path = self.server.root / 'reports' / filename
            if path.is_symlink() or not path.resolve().is_relative_to(self.server.root):
                self.reply(403)
                return
            try:
                data = path.read_bytes()
                if dashboard:
                    self.reply(200, render(json.loads(data), perfetto_url(self.server.token)).encode(), 'text/html; charset=utf-8')
                else:
                    self.reply(200, data)
            except FileNotFoundError:
                self.reply(404)
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
                return viewer_url(status['token'])
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


def run(root):
    root = Path(root).resolve()
    report = refresh(root)
    print(f'Refreshed {report["implementation_id"]}: {root / "reports"}', flush=True)
    if report['summary']['coverage']:
        print('Coverage: ' + json.dumps(report['summary']['coverage'], sort_keys=True), flush=True)
    try:
        server = Viewer(root)
    except OSError as exc:
        if exc.errno != errno.EADDRINUSE:
            raise
        url = existing_viewer(root)
        print('Reusing the running viewer; refreshed reports are available.', flush=True)
        open_browser(url)
        return
    with server:
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            print('Serving agent insights locally. Ctrl+C stops this viewer.', flush=True)
            open_browser(viewer_url(server.token))
            worker.join()
        finally:
            server.shutdown()
            worker.join()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('implementation', type=Path)
    args = parser.parse_args()
    def stop(_signum, _frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)
    try:
        run(args.implementation)
    except KeyboardInterrupt:
        print('\nViewer stopped.', flush=True)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(2, f'trace-view: {exc}\n')


if __name__ == '__main__':
    main()
