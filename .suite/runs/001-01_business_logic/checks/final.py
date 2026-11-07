"""Assembled CLI subprocess scenario, using a copied app and actual default store."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

source = Path(__file__).resolve().parents[4] / 'apps/todolist'
with tempfile.TemporaryDirectory() as raw:
    root = Path(raw)
    app = root / 'app'
    shutil.copytree(source, app, ignore=shutil.ignore_patterns('.venv', '__pycache__', '*.egg-info', 'tasks.json', '.agents'))
    def cli(*args, ok=True):
        result = subprocess.run(['uv', 'run', '--project', str(app), 'todo', *args], cwd=root,
                                capture_output=True, text=True, timeout=120)
        print(json.dumps({'args': args, 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}))
        assert (result.returncode == 0) == ok, result
        return result.stdout
    assert 'No tasks' in cli('list')
    cli('add', 'Pack suitcase')
    cli('add', 'Book train')
    tasks = json.loads((app / 'tasks.json').read_text())
    first, second = tasks
    assert first['title'] == 'Pack suitcase' and not first['completed']
    assert second['title'] == 'Book train' and first['id'] != second['id']
    cli('complete', str(first['id']))
    output = cli('list')
    assert '[x]' in output and 'Pack suitcase' in output and 'Book train' in output
    cli('delete', str(second['id']))
    assert json.loads((app / 'tasks.json').read_text()) == [dict(first, completed=True)]
    assert not (root / 'tasks.json').exists(), 'store must resolve against app root, not cwd'
    cli('delete', str(first['id']))
    assert 'No tasks' in cli('list')
    assert json.loads((app / 'tasks.json').read_text()) == []
print('PASS: assembled CLI lifecycle, persistence across processes, default app-root storage')
