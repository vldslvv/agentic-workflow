"""Independent observations of disclosed storage behavior; temporary data only."""
import json
import os
import subprocess
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[4]
app = root / "apps/todolist"
python = app / ".venv/bin/python"
env = dict(os.environ, PYTHONPATH=str(app))
with tempfile.TemporaryDirectory() as temporary:
    path = Path(temporary) / "tasks.json"
    code = "from todolist import TaskStore; from pathlib import Path; import json; s=TaskStore(); assert s.path == Path(" + repr(str(app / "tasks.json")) + "); s=TaskStore(" + repr(str(path)) + "); print(json.dumps(s.create_task('Persist across processes')))"
    created = subprocess.run([str(python), "-c", code], cwd=temporary, env=env, capture_output=True, text=True, check=True)
    task = json.loads(created.stdout)
    code = "from todolist import TaskStore; import json; print(json.dumps(TaskStore(" + repr(str(path)) + ").list_tasks()))"
    loaded = subprocess.run([str(python), "-c", code], cwd=temporary, env=env, capture_output=True, text=True, check=True)
    assert json.loads(loaded.stdout) == [task]
    assert json.loads(path.read_text()) == [task]
    print("PASS: default path is app root from a different cwd; JSON array reloads in a separate process")
