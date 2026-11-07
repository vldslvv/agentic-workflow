"""CLI transport contract on real installed subprocesses and real storage."""
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[5] / 'apps/todolist'

class CliContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.temp.cleanup)
        cls.root = Path(cls.temp.name)
        cls.app = cls.root / 'app'
        shutil.copytree(SOURCE, cls.app, ignore=shutil.ignore_patterns('.venv', '__pycache__', '*.egg-info', 'tasks.json', '.agents'))
        result = subprocess.run(['uv', 'sync', '--project', str(cls.app)], capture_output=True, text=True, timeout=120)
        if result.returncode:
            raise RuntimeError(result.stderr)
        cls.command = [str(cls.app / '.venv/bin/todo')]

    def setUp(self):
        self.data = self.app / 'tasks.json'
        if self.data.is_dir():
            self.data.rmdir()
        else:
            self.data.unlink(missing_ok=True)

    def cli(self, *args, ok=True):
        result = subprocess.run(self.command + list(args), cwd=self.root, capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode == 0, ok, result)
        self.assertNotIn('Traceback', result.stderr)
        if not ok:
            self.assertTrue(result.stderr.strip(), result)
        return result.stdout

    def test_help_discovery(self):
        for args in ((), ('help',), ('--help',)):
            with self.subTest(args=args):
                output = self.cli(*args)
                for command in ('add', 'delete', 'complete', 'list', 'help'):
                    self.assertIn(command, output)
        self.assertFalse(self.data.exists())

    def test_command_routing_and_display(self):
        self.assertIn('No tasks', self.cli('list'))
        self.cli('add', 'Café supplies')
        item = json.loads(self.data.read_text())[0]
        output = self.cli('list')
        self.assertIn(str(item['id']), output)
        self.assertIn('Café supplies', output)
        self.assertIn('[ ]', output)
        self.cli('complete', str(item['id']))
        self.assertIn('[x]', self.cli('list'))
        self.cli('delete', str(item['id']))
        self.assertIn('No tasks', self.cli('list'))

    def test_cli_errors_preserve_data(self):
        self.cli('add', 'Keep')
        before = self.data.read_bytes()
        for args in (('add',), ('add', ' '), ('delete', '999'), ('complete', '999'), ('complete', 'abc'), ('nonesuch',)):
            with self.subTest(args=args):
                self.cli(*args, ok=False)
                self.assertEqual(self.data.read_bytes(), before)
        self.data.write_text('{damaged')
        self.cli('list', ok=False)
        self.assertEqual(self.data.read_text(), '{damaged')
        self.data.unlink()
        self.data.mkdir()
        self.cli('list', ok=False)

if __name__ == '__main__':
    unittest.main()
