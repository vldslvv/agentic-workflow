"""Observe the CLI deadline when TCP succeeds but PostgreSQL never responds."""
import json
import os
from pathlib import Path
import socket
import subprocess
import time

output = Path(__file__).with_suffix('.json')
binary = str(Path('apps/todolist_rust/target/debug/todolist').resolve())
result = {'requirement': 'D2', 'scenario': 'TCP accepted; PostgreSQL session handshake stalled',
          'command': [binary, 'help'], 'deadline_seconds': 10}
with socket.socket() as listener:
    listener.bind(('127.0.0.1', 0))
    listener.listen(1)
    listener.settimeout(8)
    url = f'postgres://todolist:todolist@127.0.0.1:{listener.getsockname()[1]}/todolist'
    started = time.monotonic()
    process = subprocess.Popen(result['command'], env=dict(os.environ, DATABASE_URL=url),
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    connection = None
    try:
        connection, _ = listener.accept()
        result['tcp_accepted'] = True
        connection.settimeout(1)
        result['received_startup_bytes'] = len(connection.recv(4096))
        stdout, stderr = process.communicate(timeout=max(0.1, 11 - (time.monotonic() - started)))
        result.update(exit_code=process.returncode, stdout=stdout, stderr=stderr,
                      elapsed_seconds=time.monotonic() - started)
        assert result['received_startup_bytes'] > 0
        assert process.returncode != 0 and stderr.strip()
        assert result['elapsed_seconds'] < 10
        result['status'] = 'PASS'
    except Exception as error:
        process.kill()
        stdout, stderr = process.communicate()
        result.update(status='FAIL', error=str(error), exit_code=process.returncode,
                      stdout=stdout, stderr=stderr, elapsed_seconds=time.monotonic() - started)
    finally:
        if connection:
            connection.close()
output.write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
raise SystemExit(0 if result['status'] == 'PASS' else 1)
