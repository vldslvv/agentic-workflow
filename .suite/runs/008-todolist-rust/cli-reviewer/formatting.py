"""Reviewer observations for disclosed C1/C3 output and C4 escaping clauses."""
import json
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[4]
app = root / 'apps/todolist_rust'
evidence = Path(__file__).parent / 'attempt-0/formatting.json'
data = app / 'tasks.json'
original = data.read_bytes() if data.exists() else None
records = []
result = {'requirements': ['C1', 'C3', 'C4'], 'commands': records}
try:
    data.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory(prefix='todo-rust-review-format-') as cwd:
        def cli(*args):
            command = [str(app / 'target/debug/todolist'), *args]
            p = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=10)
            records.append(dict(command=command, cwd=cwd, exit_code=p.returncode, stdout=p.stdout, stderr=p.stderr))
            assert p.returncode == 0 and not p.stderr, records[-1]
            return p.stdout
        added = cli('add', 'Alpha\tBeta\nGamma\rDelta\\End')
        assert '1' in added and added.strip(), added
        assert cli('list') == 'id\tstatus\tdescription\n1\tNew\tAlpha\\tBeta\\nGamma\\rDelta\\\\End\n'
        completed = cli('complete', '1')
        assert '1' in completed and 'complet' in completed.lower(), completed
        assert cli('list') == 'id\tstatus\tdescription\n1\tCompleted\tAlpha\\tBeta\\nGamma\\rDelta\\\\End\n'
        assert not (Path(cwd) / 'tasks.json').exists()
    result['status'] = 'PASS'
except Exception as error:
    result['status'] = 'FAIL'
    result['error'] = repr(error)
    raise
finally:
    if original is None:
        data.unlink(missing_ok=True)
    else:
        data.write_bytes(original)
    result['original_data_restored'] = (data.read_bytes() if data.exists() else None) == original
    evidence.write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
