"""Source-repository integration: copy boundary, optional wrappers and host entry points."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1]


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='workflow install ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'unrelated project'
        self.root.mkdir()
        self.package = self.root / 'agentic-workflow'
        shutil.copytree(SOURCE / 'agentic-workflow', self.package,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        readme = (self.package / 'README.md').read_text()
        self.block = re.search(r'```markdown\n(.*?)\n```', readme, re.S)[1]
        (self.root / 'AGENTS.md').write_text(
            '# Host instructions\n[Unrelated](missing-host-file.md)\n\n' + self.block + '\n')
        self.env = dict(os.environ, CODEX_HOME=str(self.root / 'no telemetry'), CODEX_THREAD_ID='')

    def cli(self, script, *args):
        return subprocess.run([sys.executable, str(self.package / 'helpers' / script), *map(str, args)],
                              cwd=self.root, env=self.env, capture_output=True, text=True, timeout=15)

    def check(self, code=0):
        process = self.cli('check_package.py', '--integration-root', self.root)
        self.assertEqual(process.returncode, code, process.stdout + process.stderr)
        return json.loads(process.stdout)

    def install(self, role):
        name = f'agentic-workflow-{role}'
        destination = self.root / '.agents/skills' / name
        shutil.copytree(SOURCE / '.agents/skills' / name, destination)
        return destination

    def test_optional_skills_can_be_installed_individually(self):
        self.assertEqual(self.check()['errors'], [])
        for role in ('planner', 'supervisor', 'acceptance'):
            with self.subTest(role=role):
                directory = self.install(role)
                self.assertEqual(self.check()['errors'], [])
                shutil.rmtree(directory)

    def test_invalid_installed_skill_and_policy_are_reported(self):
        for role in ('planner', 'supervisor', 'acceptance'):
            directory = self.install(role)
            for relative, message in (
                    ('SKILL.md', 'Invalid skill entry point'),
                    ('agents/openai.yaml', 'Invalid invocation policy')):
                with self.subTest(role=role, file=relative):
                    path = directory / relative
                    original = path.read_text()
                    path.write_text('invalid\n')
                    errors = self.check(1)['errors']
                    self.assertIn(f'{message}: agentic-workflow-{role}', errors)
                    path.write_text(original)

    def test_missing_or_broken_root_block_fails(self):
        for block in ('', self.block.replace('agentic-workflow/policies/MEMORY.md', 'missing.md')):
            with self.subTest(block=block):
                (self.root / 'AGENTS.md').write_text('# Host\n' + block)
                self.assertTrue(self.check(1)['errors'])

    def test_development_cleanup_retains_project_settings(self):
        shutil.copyfile(SOURCE / 'Makefile', self.root / 'Makefile')
        records = self.root / '.agentic-workflow'
        for name in ('001_example', '1000_example'):
            (records / name / 'runs').mkdir(parents=True)
        override = records / 'MODELS.md'
        override.write_text('Project-owned routing\n')
        process = subprocess.run(['make', 'cleanup'], cwd=self.root,
                                 capture_output=True, text=True, timeout=15)
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertEqual(override.read_text(), 'Project-owned routing\n')
        self.assertEqual(list(records.iterdir()), [override])

    def test_copy_operations_and_package_replacement_preserve_project_data(self):
        records = self.root / '.agentic-workflow'
        records.mkdir()
        override = records / 'MODELS.md'
        override.write_text('Project-owned routing\n')
        for relative in ('specs/example/project.md', '.agents/memory/index.md', 'app/main.py'):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('Project-owned content\n')
        for args, expected in (((), records / '001_example'),
                               (('--records-root', 'custom records'), self.root / 'custom records/001_example')):
            process = self.cli('records.py', 'allocate', 'example', *args)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual((self.root / process.stdout.strip()).resolve(), expected)
            (expected / 'tasks/one').mkdir()
            process = self.cli('records.py', 'resolve', expected, 'one')
            self.assertEqual(process.returncode, 0, process.stderr)
            process = self.cli('usage_report.py', expected)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertIn('summary', json.loads((expected / 'reports/usage.json').read_text()))
        shutil.rmtree(self.package)
        shutil.copytree(SOURCE / 'agentic-workflow', self.package,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        self.assertEqual(override.read_text(), 'Project-owned routing\n')
        self.assertTrue((records / '001_example/tasks/one').is_dir())
        for relative in ('specs/example/project.md', '.agents/memory/index.md', 'app/main.py'):
            self.assertEqual((self.root / relative).read_text(), 'Project-owned content\n')
        self.assertEqual(self.check()['errors'], [])


if __name__ == '__main__':
    unittest.main()
