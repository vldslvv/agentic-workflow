#!/usr/bin/env python3
"""Frozen acceptance at public library, CLI and PostgreSQL boundaries."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import socket
import subprocess
import tempfile
import time
import traceback

ROOT = Path(__file__).resolve().parents[4]
APP = ROOT / 'apps/todolist_rust'
RUN = ROOT / '.suite/runs/008-todolist-rust'
parser = argparse.ArgumentParser()
parser.add_argument('stage', choices=['business', 'cli', 'database', 'integrity', 'identity'])
parser.add_argument('--evidence', type=Path, required=True)
args = parser.parse_args()
args.evidence.mkdir(parents=True, exist_ok=True)
logs = []
passed = []

def command(argv, *, cwd=APP, env=None, ok=True, timeout=180):
    p = subprocess.run([str(x) for x in argv], cwd=cwd, env=env, text=True,
                       capture_output=True, timeout=timeout)
    logs.append(dict(command=[str(x) for x in argv], cwd=str(cwd), exit_code=p.returncode,
                     stdout=p.stdout, stderr=p.stderr))
    (args.evidence / 'commands.json').write_text(json.dumps(logs, indent=2))
    if ok:
        assert p.returncode == 0, f'{argv}: {p.stderr}\n{p.stdout}'
    else:
        assert p.returncode != 0 and p.stderr.strip(), f'expected explanatory failure: {argv}'
    return p.stdout

def inventory():
    frozen = json.loads((RUN / 'frozen-inventory.json').read_text())
    mismatches = [p for p, digest in frozen.items()
                  if not (ROOT / p).is_file() or hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != digest]
    assert not mismatches, f'Protected inputs changed: {mismatches}'
    return {'result': 'PASS', 'files_checked': len(frozen)}

def identity():
    files = {str(p.relative_to(APP)): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(APP.rglob('*')) if p.is_file()
             and 'target' not in p.relative_to(APP).parts
             and p.name != 'tasks.json' and '.git' not in p.relative_to(APP).parts}
    return {'files': files, 'sha256': hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()}

def build():
    command(['cargo', 'build', '--locked'])
    return APP / 'target/debug/todolist'

def business():
    with tempfile.TemporaryDirectory(prefix='todo-rust-business-') as tmp:
        tmp = Path(tmp)
        (tmp / 'src').mkdir()
        (tmp / 'Cargo.toml').write_text('[package]\nname="business-acceptance"\nversion="0.1.0"\nedition="2021"\n[dependencies]\ntodolist={path=' + json.dumps(str(APP)) + '}\n')
        (tmp / 'src/main.rs').write_text(r'''
use todolist::Store;
fn main() {
    let path = std::path::PathBuf::from(std::env::args().nth(1).unwrap());
    let mut store = Store::open(&path).unwrap();
    assert!(store.list().unwrap().is_empty());
    assert!(store.add(" \t\n").is_err());
    let a = store.add("  Buy milk 🥛  ").unwrap();
    let b = store.add("Book appointment").unwrap();
    assert!(a.id > 0 && b.id == a.id + 1);
    assert_eq!(a.description, "Buy milk 🥛");
    assert_eq!(format!("{:?}", a.status), "New");
    drop(store);
    let mut store = Store::open(&path).unwrap();
    assert_eq!(store.list().unwrap().len(), 2);
    store.complete(a.id).unwrap();
    store.complete(a.id).unwrap();
    assert_eq!(format!("{:?}", store.list().unwrap()[0].status), "Completed");
    assert!(store.complete(999999).is_err());
    assert!(store.delete(999999).is_err());
    store.delete(b.id).unwrap();
    assert!(store.complete(b.id).is_err());
    let c = store.add("Third").unwrap();
    assert!(c.id > b.id);
    drop(store);
    let mut store = Store::open(&path).unwrap();
    let tasks = store.list().unwrap();
    assert_eq!(tasks.len(), 2);
    assert_eq!(tasks[0].id, a.id);
    assert_eq!(tasks[1].id, c.id);
    drop(store);
    std::fs::write(&path, b"{broken JSON").unwrap();
    assert!(Store::open(&path).is_err());
    assert_eq!(std::fs::read(&path).unwrap(), b"{broken JSON");
    println!("B1 B2 B3 B4 B5 PASS");
}
''')
        env = dict(os.environ, CARGO_TARGET_DIR=str(APP / 'target/acceptance'))
        command(['cargo', 'run', '--quiet', '--manifest-path', tmp / 'Cargo.toml', '--', tmp / 'tasks.json'], cwd=tmp, env=env)
    passed.extend(['B1', 'B2', 'B3', 'B4', 'B5'])

def operations(binary, env, cwd):
    def cli(*parts, ok=True):
        return command([binary, *parts], cwd=cwd, env=env, ok=ok, timeout=10)
    def rows():
        lines = cli('list').strip().splitlines()
        assert lines and [x.lower() for x in lines[0].split('\t')] == ['id', 'status', 'description'], lines
        return [line.split('\t', 2) for line in lines[1:]]
    for help_args in [(), ('help',), ('--help',)]:
        help_text = cli(*help_args).lower()
        assert all(word in help_text for word in ['add', 'list', 'complete', 'delete', 'help']), help_text
    assert rows() == []
    cli('add', '  Buy milk 🥛  ')
    cli('add', "Quote ' and ; SQL --")
    initial = rows()
    assert len(initial) == 2 and initial[0][1:] == ['New', 'Buy milk 🥛'], initial
    assert initial[1][1:] == ['New', "Quote ' and ; SQL --"]
    a, b = initial[0][0], initial[1][0]
    assert int(a) > 0 and int(b) == int(a) + 1
    cli('complete', a)
    cli('complete', a)
    assert rows()[0] == [a, 'Completed', 'Buy milk 🥛']
    for invalid in [('add', '  '), ('add',), ('complete', 'wat'), ('delete', '-1'), ('complete', '999999'), ('delete', '999999'), ('unknown',), ('list', 'extra')]:
        cli(*invalid, ok=False)
    assert len(rows()) == 2
    cli('delete', b)
    cli('delete', b, ok=False)
    cli('complete', b, ok=False)
    assert rows() == [[a, 'Completed', 'Buy milk 🥛']]
    cli('add', 'Third')
    assert int(rows()[1][0]) > int(b)
    return a, b, rows()

def cli_checks():
    business()
    binary = build()
    data = APP / 'tasks.json'
    original = data.read_bytes() if data.exists() else None
    try:
        data.unlink(missing_ok=True)
        with tempfile.TemporaryDirectory(prefix='todo-rust-cli-') as tmp:
            operations(binary, os.environ.copy(), tmp)
            assert data.exists() and not (Path(tmp) / 'tasks.json').exists()
            data.write_text('{broken JSON')
            command([binary, 'list'], cwd=tmp, ok=False)
            assert data.read_text() == '{broken JSON'
        passed.extend(['C1', 'C2', 'C3', 'C4', 'C5'])
    finally:
        if original is None:
            data.unlink(missing_ok=True)
        else:
            data.write_bytes(original)

def database():
    binary = build()
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    env = dict(os.environ, POSTGRES_PORT=str(port), DATABASE_URL=f'postgres://todolist:todolist@127.0.0.1:{port}/todolist')
    project = 'todolist-rust-accept-' + str(os.getpid())
    compose = ['docker', 'compose', '-f', APP / 'compose.yaml', '-p', project]
    data = APP / 'tasks.json'
    original = data.read_bytes() if data.exists() else None
    def sql(query):
        return command([*compose, 'exec', '-T', 'db', 'psql', '-U', 'todolist', '-d', 'todolist', '-At', '-v', 'ON_ERROR_STOP=1', '-c', query], env=env).strip()
    try:
        command([*compose, 'up', '-d', '--wait', '--wait-timeout', '90'], env=env, timeout=240)
        with tempfile.TemporaryDirectory(prefix='todo-rust-db-') as tmp:
            a, b, expected = operations(binary, env, tmp)
            schema = dict(line.split('|') for line in sql("SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='public' AND table_name='tasks' ORDER BY ordinal_position").splitlines())
            assert schema['id'] == 'integer' and schema['description'] in ('text', 'character varying')
            assert schema['added'].startswith('timestamp') and schema['update'].startswith('timestamp')
            assert schema['status'] == 'USER-DEFINED'
            labels = sql("SELECT e.enumlabel FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid JOIN information_schema.columns c ON c.udt_name=t.typname WHERE c.table_schema='public' AND c.table_name='tasks' AND c.column_name='status'").splitlines()
            assert set(labels) == {'New', 'Completed', 'Deleted'}
            assert sql(f'SELECT status::text FROM tasks WHERE id={a}') == 'Completed'
            assert sql(f'SELECT status::text FROM tasks WHERE id={b}') == 'Deleted'
            assert sql('SELECT count(*)=count(DISTINCT id) AND bool_and(id>0) FROM tasks') == 't'
            assert sql('SELECT bool_and(added IS NOT NULL AND "update" IS NOT NULL AND "update">=added) FROM tasks') == 't'
            third = expected[-1][0]
            added = sql(f'SELECT added::text FROM tasks WHERE id={third}')
            previous_update = sql(f'SELECT "update"::text FROM tasks WHERE id={third}')
            command([binary, 'complete', third], cwd=tmp, env=env)
            assert sql(f'SELECT added::text FROM tasks WHERE id={third}') == added
            assert sql(f'SELECT "update">\'{previous_update}\'::timestamptz FROM tasks WHERE id={third}') == 't'
            before_restart = command([binary, 'list'], cwd=tmp, env=env)
            command([*compose, 'restart', 'db'], env=env)
            command([*compose, 'up', '-d', '--wait', '--wait-timeout', '60'], env=env)
            assert command([binary, 'list'], cwd=tmp, env=env) == before_restart
            assert (data.read_bytes() if data.exists() else None) == original
            assert not (Path(tmp) / 'tasks.json').exists()
            command([*compose, 'stop', 'db'], env=env)
            for parts in [('list',), ('add', 'offline'), ('complete', a), ('delete', a), ('help',), ('--help',), ()]:
                started = time.monotonic()
                command([binary, *parts], cwd=tmp, env=env, ok=False, timeout=10)
                assert time.monotonic() - started < 10
        passed.extend(['D1', 'D2', 'D3', 'D4', 'D5', 'ASSEMBLED'])
    finally:
        command([*compose, 'down', '-v', '--remove-orphans'], env=env)

result = {'stage': args.stage, 'passed_requirements': passed}
try:
    result['integrity_before'] = inventory()
    if args.stage == 'identity':
        result['candidate'] = identity()
    elif args.stage != 'integrity':
        {'business': business, 'cli': cli_checks, 'database': database}[args.stage]()
        result['candidate'] = identity()
    result['integrity_after'] = inventory()
    result['status'] = 'PASS'
except Exception as error:
    result['status'] = 'FAIL'
    result['error'] = str(error)
    result['traceback'] = traceback.format_exc()
finally:
    (args.evidence / 'results.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
if result['status'] != 'PASS':
    raise SystemExit(1)
