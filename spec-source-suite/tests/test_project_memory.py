"""AC-1: public validator CLI, valid library and malformed input diagnostics."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HELPER = Path(__file__).resolve().parents[1] / 'helpers/project_memory.py'
ENTRY = '''# Fixture prerequisite

- Kind: command
- Use when: Running the synthetic check.
- Source: fixture/check.md
- Last checked: 2026-11-06

Create the fixture's output directory before running its check.
'''
INDEX = '# Project memory\n\n- [Fixture prerequisite](entries/fixture-prerequisite.md) — Read when running the synthetic check.\n'


class ProjectMemoryCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.memory = self.root / '.agents/memory'
        self.entry = self.memory / 'entries/fixture-prerequisite.md'
        self.entry.parent.mkdir(parents=True)
        self.entry.write_text(ENTRY)
        self.index = self.memory / 'index.md'
        self.index.write_text(INDEX)

    def run_cli(self, root=None):
        return subprocess.run([sys.executable, str(HELPER), str(root or self.memory)],
                              capture_output=True, text=True)

    def test_valid_kinds_and_absent_memory(self):
        for kind in ('navigation', 'command', 'pitfall', 'decision'):
            self.entry.write_text(ENTRY.replace('Kind: command', 'Kind: ' + kind))
            result = self.run_cli()
            with self.subTest(kind=kind):
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout), {'status': 'PASS', 'entries': [{
                    'path': 'entries/fixture-prerequisite.md', 'title': 'Fixture prerequisite',
                    'use_when': 'running the synthetic check.'}]})
        result = self.run_cli(self.root / 'missing')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {'status': 'NO_MEMORY', 'entries': []})
        self.assertFalse((self.root / 'missing').exists())

    def test_entry_errors_have_actionable_diagnostics(self):
        cases = []
        for field in ('Kind', 'Use when', 'Source', 'Last checked'):
            lines = ENTRY.splitlines(keepends=True)
            cases.append((''.join(line for line in lines if not line.startswith('- ' + field + ':')),
                          'missing field ' + field))
        cases += [
            (ENTRY.replace('Kind: command', 'Kind: guess'), 'invalid Kind'),
            (ENTRY.replace('Source: fixture/check.md', 'Source: '), 'missing field Source'),
            (ENTRY + '\n- Kind: command\n', 'duplicate field Kind'),
            (ENTRY.replace('# Fixture prerequisite', ''), 'missing title'),
            (ENTRY.replace("Create the fixture's output directory before running its check.", ''), 'missing lesson body'),
        ]
        for stamp in ('2026-02-30', '2026-1-06', '20261106', 'not-a-date'):
            cases.append((ENTRY.replace('2026-11-06', stamp), 'invalid Last checked date'))
        for body, diagnostic in cases:
            self.entry.write_text(body)
            with self.subTest(diagnostic=diagnostic, body=body):
                result = self.run_cli()
                self.assertEqual(result.returncode, 2)
                self.assertIn(diagnostic, result.stderr)
                self.assertIn('fixture-prerequisite.md', result.stderr)

    def test_index_links_and_symlink_containment(self):
        outside = self.root / 'outside.md'
        outside.write_text(ENTRY)
        (self.memory / 'entries/alias.md').symlink_to(outside)
        for target, diagnostic in (
            ('entries/missing.md', 'broken link'),
            ('../../outside.md', 'escapes directory'),
            (str(outside), 'escapes directory'),
            ('entries/alias.md', 'escapes directory'),
        ):
            self.index.write_text(INDEX.replace('entries/fixture-prerequisite.md', target))
            result = self.run_cli()
            with self.subTest(target=target):
                self.assertEqual(result.returncode, 2)
                self.assertIn(diagnostic, result.stderr)
        (self.memory / 'entries/alias.md').unlink()
        for content, diagnostic in (
            (INDEX + INDEX.splitlines()[-1] + '\n', 'duplicate entry link'),
            (INDEX.replace(' — Read when running the synthetic check.', ''), 'Read when hint'),
            (INDEX.rstrip() + ' [extra](../../outside.md)\n', 'one entry link'),
            ('# Project memory\n', 'entry missing from index'),
        ):
            self.index.write_text(content)
            result = self.run_cli()
            with self.subTest(diagnostic=diagnostic):
                self.assertEqual(result.returncode, 2)
                self.assertIn(diagnostic, result.stderr)
        self.index.unlink()
        result = self.run_cli()
        self.assertEqual(result.returncode, 2)
        self.assertIn('index.md', result.stderr)


if __name__ == '__main__':
    unittest.main()
