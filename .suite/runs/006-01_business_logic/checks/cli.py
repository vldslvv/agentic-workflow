"""C1–C6 and A1: installed console script in independent processes."""
import argparse
import json
import os
import re
import shutil
import tempfile
from pathlib import Path
from common import Evidence, identity

parser = argparse.ArgumentParser()
parser.add_argument('--app', type=Path, required=True)
parser.add_argument('--evidence', type=Path, required=True)
parser.add_argument('--only', choices=['A1'])
args = parser.parse_args()
app = args.app.resolve()
evidence = Evidence(args.evidence)
before = identity(app)

with tempfile.TemporaryDirectory(prefix='todo-cli-') as directory:
    sandbox = Path(directory)
    copy = sandbox / 'app'
    shutil.copytree(app, copy, ignore=shutil.ignore_patterns('.venv', '__pycache__', '*.egg-info', 'tasks.json', 'dist', 'build'))
    data = copy / 'tasks.json'
    elsewhere = sandbox / 'elsewhere'
    elsewhere.mkdir()
    env = os.environ.copy()
    env.pop('VIRTUAL_ENV', None)
    setup = evidence.command(['uv', 'sync', '--locked', '--offline', '--project', copy], env=env)
    if setup.returncode:
        evidence.results['setup'] = {'status': 'FAIL', 'stderr': setup.stderr}
        raise SystemExit(evidence.finish())

    def command(*argv, ok=True, cwd=None):
        result = evidence.command(['uv', 'run', '--offline', '--no-sync', '--project', copy, 'todo', *argv], cwd=cwd or copy, env=env)
        assert (result.returncode == 0) == ok, (argv, result.returncode, result.stdout, result.stderr)
        if not ok:
            assert result.stderr.strip() and 'Traceback' not in result.stderr
        return result.stdout

    def tasks():
        value = json.loads(data.read_text())
        evidence.observe(storage=value)
        return value

    def reset():
        if data.is_dir():
            data.rmdir()
        elif data.exists():
            data.unlink()

    def row(output, task, marker):
        lines = [line for line in output.splitlines() if task['title'] in line]
        assert len(lines) == 1 and marker in lines[0] and re.search(r'\b' + str(task['id']) + r'\b', lines[0]), output

    def add():
        reset()
        command('add', 'Buy café beans')
        command('add', 'Write notes')
        saved = tasks()
        assert [x['title'] for x in saved] == ['Buy café beans', 'Write notes']
        assert len({x['id'] for x in saved}) == 2
        output = command('list')
        for task in saved:
            assert task['completed'] is False
            row(output, task, '[ ]')

    def delete():
        reset()
        command('add', 'Delete me')
        command('add', 'Keep me')
        first, second = tasks()
        command('delete', str(first['id']))
        assert tasks() == [second]
        output = command('list')
        assert first['title'] not in output
        row(output, second, '[ ]')
        saved = data.read_bytes()
        command('delete', '999999', ok=False)
        assert data.read_bytes() == saved

    def complete():
        reset()
        command('add', 'Complete me')
        task = tasks()[0]
        command('complete', str(task['id']))
        command('complete', str(task['id']))
        assert tasks()[0]['completed'] is True
        row(command('list'), task, '[x]')
        saved = data.read_bytes()
        command('complete', '999999', ok=False)
        assert data.read_bytes() == saved

    def listing():
        reset()
        assert command('list').strip() == 'No tasks.' and not data.exists()
        command('add', 'Read only')
        saved = data.read_bytes()
        row(command('list'), tasks()[0], '[ ]')
        assert data.read_bytes() == saved

    def help_check():
        reset()
        for existing in (False, True):
            if existing:
                data.write_text('{broken')
            for option in ('help', '--help'):
                output = command(option)
                assert all(word in output for word in ('add', 'delete', 'complete', 'list', 'help'))
                assert data.read_text() == '{broken' if existing else not data.exists()

    def errors():
        reset()
        command('add', 'Keep bytes')
        saved = data.read_bytes()
        for argv in [(), ('unknown',), ('add',), ('add', '  '), ('delete', 'abc'), ('delete', '0'), ('complete', '-1')]:
            command(*argv, ok=False)
            assert data.read_bytes() == saved
        data.write_text('{broken')
        for argv in [('list',), ('add', 'New'), ('delete', '1'), ('complete', '1')]:
            command(*argv, ok=False)
            assert data.read_text() == '{broken'
        reset()
        data.mkdir()
        command('list', ok=False)
        command('add', 'New', ok=False)
        assert data.is_dir()

    def assembled():
        reset()
        command('add', 'Finish report')
        command('add', 'Discard draft')
        first, second = tasks()
        command('complete', str(first['id']), cwd=elsewhere)
        command('delete', str(second['id']), cwd=elsewhere)
        output = command('list', cwd=elsewhere)
        assert tasks() == [{'id': first['id'], 'title': 'Finish report', 'completed': True}]
        row(output, first, '[x]')
        assert 'Discard draft' not in output and not (elsewhere / 'tasks.json').exists()

    selected = [('A1', assembled)] if args.only else [('C1', add), ('C2', delete), ('C3', complete), ('C4', listing), ('C5', help_check), ('C6', errors), ('A1', assembled)]
    for name, check in selected:
        evidence.check(name, check)

evidence.check('candidate-integrity', lambda: None if identity(app) == before else (_ for _ in ()).throw(AssertionError('Candidate changed')))
raise SystemExit(evidence.finish())
