"""B1–B6: public business API, storage behavior, and project installation."""
import argparse
import json
import sys
import tempfile
from pathlib import Path
from common import Evidence, identity

parser = argparse.ArgumentParser()
parser.add_argument('--app', type=Path, required=True)
parser.add_argument('--evidence', type=Path, required=True)
args = parser.parse_args()
app = args.app.resolve()
evidence = Evidence(args.evidence)
before = identity(app)
sys.path.insert(0, str(app))
from todolist.core import TaskStore, TodoError


def rejected(action):
    try:
        action()
    except TodoError as error:
        assert str(error).strip(), 'Expected useful error text'
        evidence.observe(error=str(error))
    else:
        raise AssertionError('Expected TodoError')


def fixture(check):
    def run():
        with tempfile.TemporaryDirectory(prefix='todo-business-') as directory:
            path = Path(directory) / 'tasks.json'
            check(TaskStore(path), path)
            if path.is_file():
                evidence.observe(storage=path.read_text())
    return run


def create(store, path):
    first = store.create('  Buy café beans  ')
    second = store.create('Write notes')
    assert first.title == 'Buy café beans' and second.title == 'Write notes'
    assert type(first.id) is int and first.id > 0 and second.id > 0 and first.id != second.id
    assert first.completed is False and second.completed is False
    saved = path.read_bytes()
    rejected(lambda: store.create(' \t\n '))
    assert path.read_bytes() == saved


def listing(store, path):
    assert store.list() == [] and not path.exists()
    first, second = store.create('First'), store.create('Second')
    saved = path.read_bytes()
    tasks = store.list()
    assert [(x.id, x.title, x.completed) for x in tasks] == [(first.id, 'First', False), (second.id, 'Second', False)]
    assert path.read_bytes() == saved


def delete(store, path):
    first, second = store.create('First'), store.create('Second')
    store.delete(first.id)
    assert [x.id for x in TaskStore(path).list()] == [second.id]
    saved = path.read_bytes()
    rejected(lambda: store.delete(max(first.id, second.id) + 100))
    assert path.read_bytes() == saved
    store.delete(second.id)
    assert TaskStore(path).list() == []


def complete(store, path):
    first, second = store.create('First'), store.create('Second')
    store.complete(first.id)
    assert [(x.id, x.completed) for x in TaskStore(path).list()] == [(first.id, True), (second.id, False)]
    store.complete(first.id)
    assert TaskStore(path).list()[0].completed is True
    saved = path.read_bytes()
    rejected(lambda: store.complete(max(first.id, second.id) + 100))
    assert path.read_bytes() == saved


def persistence(store, path):
    task = store.create('Persist me')
    assert json.loads(path.read_text()) == [{'id': task.id, 'title': 'Persist me', 'completed': False}]
    assert TaskStore(path).list()[0].title == 'Persist me'
    invalid = ['{broken', '{}', '[{"id": 1, "title": "bad", "completed": "false"}]',
               '[{"id": 1, "title": "  ", "completed": false}]',
               '[{"id": 0, "title": "bad", "completed": false}]',
               '[{"id": true, "title": "bad", "completed": false}]',
               '[{"id": 1, "title": "A", "completed": false}, {"id": 1, "title": "B", "completed": false}]']
    for raw in invalid:
        path.write_text(raw)
        for action in (store.list, lambda: store.create('New'), lambda: store.delete(1), lambda: store.complete(1)):
            rejected(action)
            assert path.read_text() == raw
    path.unlink()
    path.mkdir()
    rejected(store.list)
    rejected(lambda: store.create('New'))
    assert path.is_dir()


for name, check in [('B1', create), ('B2', listing), ('B3', delete), ('B4', complete), ('B5', persistence)]:
    evidence.check(name, fixture(check))


def install():
    assert (app / 'pyproject.toml').is_file() and (app / 'uv.lock').is_file()
    result = evidence.command(['uv', 'sync', '--locked', '--project', app])
    assert result.returncode == 0, result.stderr


evidence.check('B6', install)
evidence.check('candidate-integrity', lambda: None if identity(app) == before else (_ for _ in ()).throw(AssertionError('Candidate changed')))
raise SystemExit(evidence.finish())
