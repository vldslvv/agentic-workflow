"""Reviewer observations for disclosed criteria missing from frozen assertions."""
import json
import os
from pathlib import Path
import socket
import subprocess
import time

ROOT = Path.cwd()
APP = ROOT / 'apps/todolist_rust'
OUT = ROOT / '.suite/runs/008-todolist-rust/database-reviewer/attempt-1/supplemental.json'
logs = []
with socket.socket() as listener:
    listener.bind(('127.0.0.1', 0))
    port = listener.getsockname()[1]
env = dict(os.environ, POSTGRES_PORT=str(port), DATABASE_URL=f'postgres://todolist:todolist@127.0.0.1:{port}/todolist')
compose = ['docker', 'compose', '-f', str(APP / 'compose.yaml'), '-p', f'todolist-review-{os.getpid()}']

def run(argv):
    p = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=120)
    logs.append(dict(command=argv, exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr))
    OUT.write_text(json.dumps({'commands': logs}, indent=2))
    assert p.returncode == 0, p.stderr
    return p.stdout.strip()

def cli(*args):
    return run([str(APP / 'target/debug/todolist'), *args])

def sql(query):
    return run([*compose, 'exec', '-T', 'db', 'psql', '-U', 'todolist', '-d', 'todolist', '-At', '-v', 'ON_ERROR_STOP=1', '-c', query])

result = {'requirements': ['B1', 'B2', 'B3', 'B4', 'C1', 'C3', 'C4', 'D3', 'D4']}
try:
    run([*compose, 'up', '-d', '--wait'])
    assert cli('add', '  Escaped\ttext\nline\\slash\rreturn  ') == 'Added task 1'
    assert cli('list') == 'id\tstatus\tdescription\n1\tNew\tEscaped\\ttext\\nline\\\\slash\\rreturn'
    assert sql("SELECT is_identity||'|'||identity_generation FROM information_schema.columns WHERE table_schema='public' AND table_name='tasks' AND column_name='id'") == 'YES|ALWAYS'
    assert sql("SELECT count(*) FROM pg_constraint WHERE conrelid='public.tasks'::regclass AND contype='p'") == '1'
    assert cli('complete', '1') == 'Completed task 1'
    before = sql('SELECT added::text||\'|\'||"update"::text FROM tasks WHERE id=1')
    assert cli('complete', '1') == 'Completed task 1'
    assert sql('SELECT added::text||\'|\'||"update"::text FROM tasks WHERE id=1') == before
    time.sleep(0.02)
    assert cli('delete', '1') == 'Deleted task 1'
    after = sql('SELECT added::text||\'|\'||"update"::text FROM tasks WHERE id=1')
    assert after.split('|')[0] == before.split('|')[0]
    assert after.split('|')[1] > before.split('|')[1]
    assert cli('list') == 'id\tstatus\tdescription'
    result['status'] = 'PASS'
except Exception as error:
    result.update(status='FAIL', error=str(error))
finally:
    run([*compose, 'down', '-v', '--remove-orphans'])
    result['commands'] = logs
    OUT.write_text(json.dumps(result, indent=2))
    print(json.dumps({k:v for k,v in result.items() if k != 'commands'}, indent=2))
