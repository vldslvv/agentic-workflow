"""Frozen acceptance support: evidence, candidate identity, and subprocesses."""
import hashlib
import json
import subprocess
import traceback
from pathlib import Path


def identity(app):
    excluded = {'.venv', '__pycache__', '.pytest_cache', '.git', 'dist', 'build'}
    return {str(p.relative_to(app)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(app.rglob('*')) if p.is_file()
            and not any(part in excluded or part.endswith('.egg-info') for part in p.relative_to(app).parts)
            and p.name != 'tasks.json' and p.suffix != '.pyc'}


class Evidence:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.results = {}
        self.events = []

    def command(self, argv, **kwargs):
        result = subprocess.run([str(x) for x in argv], capture_output=True, text=True,
                                timeout=120, **kwargs)
        self.events.append({'argv': [str(x) for x in argv], 'cwd': str(kwargs.get('cwd', Path.cwd())),
                            'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
        return result

    def check(self, name, function):
        start = len(self.events)
        try:
            function()
            self.results[name] = {'status': 'PASS'}
        except Exception:
            self.results[name] = {'status': 'FAIL', 'traceback': traceback.format_exc()}
        self.results[name]['events'] = self.events[start:]
        self.save()

    def observe(self, **values):
        self.events.append(values)

    def save(self):
        (self.directory / 'results.json').write_text(json.dumps(self.results, indent=2) + '\n')
        (self.directory / 'commands.json').write_text(json.dumps(self.events, indent=2) + '\n')

    def finish(self):
        self.save()
        print(json.dumps({key: value['status'] for key, value in self.results.items()}))
        return 0 if self.results and all(x['status'] == 'PASS' for x in self.results.values()) else 1
