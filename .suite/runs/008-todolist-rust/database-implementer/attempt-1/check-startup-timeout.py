"""Observe the D2 failure deadline through an actual nonresponsive TCP endpoint."""
import json
import os
from pathlib import Path
import socket
import subprocess
import threading
import time

root = Path.cwd()
binary = root / 'apps/todolist_rust/target/debug/todolist'
listener = socket.socket()
listener.bind(('127.0.0.1', 0))
listener.listen()
stop = threading.Event()
accepted = []

def accept():
    connection, _ = listener.accept()
    accepted.append(connection)
    stop.wait(12)
    connection.close()

thread = threading.Thread(target=accept, daemon=True)
thread.start()
env = dict(os.environ, DATABASE_URL=f'postgres://todolist:todolist@127.0.0.1:{listener.getsockname()[1]}/todolist')
started = time.monotonic()
try:
    result = subprocess.run([str(binary), 'help'], env=env, capture_output=True, text=True, timeout=10)
    elapsed = time.monotonic() - started
    record = dict(requirement='D2', scenario='TCP accepted; PostgreSQL handshake stalled', command=[str(binary), 'help'], exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr, elapsed_seconds=elapsed)
    record['status'] = 'PASS' if result.returncode != 0 and 'database' in result.stderr.lower() and 'timed out' in result.stderr.lower() and elapsed < 10 and accepted else 'FAIL'
    Path(__file__).with_suffix('.json').write_text(json.dumps(record, indent=2))
    print(json.dumps(record, indent=2))
    assert record['status'] == 'PASS'
finally:
    stop.set()
    listener.close()
    thread.join(timeout=1)
