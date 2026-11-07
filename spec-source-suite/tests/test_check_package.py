"""Package-check CLI contracts on disposable packages without Git history."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SUITE = Path(__file__).resolve().parents[1]


class PackageCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / 'spec-source-suite'
        shutil.copytree(SUITE, self.package,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))

    def cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(self.package / 'helpers/check_package.py'), *arguments],
            cwd=self.root, capture_output=True, text=True)

    def result(self, process, code):
        self.assertEqual(process.returncode, code, process.stdout + process.stderr)
        report = json.loads(process.stdout)
        self.assertEqual(report['status'], 'PASS' if code == 0 else 'FAIL')
        self.assertGreater(report['local_links_checked'], 0)
        return report

    def test_valid_package_without_git_and_legacy_base_compatibility(self):
        for arguments in ((), ('--base', 'unavailable-history')):
            with self.subTest(arguments=arguments):
                process = self.cli(*arguments)
                report = self.result(process, 0)
                self.assertEqual(report['errors'], [])
                self.assertNotIn('base_commit', report)
                if arguments:
                    self.assertIn('baseline comparison was removed', process.stderr)

    def test_additional_valid_markdown_is_allowed_and_checked(self):
        (self.package / 'extra.md').write_text(
            '# Extra\n[Routing](MODELS.md#model-routing)\n')
        self.assertEqual(self.result(self.cli(), 0)['errors'], [])

    def test_broken_local_link_and_anchor_fail(self):
        extra = self.package / 'extra.md'
        for target in ('missing.md', 'AGENTS.md#absent-heading'):
            with self.subTest(target=target):
                extra.write_text(f'# Extra\n[Reference]({target})\n')
                report = self.result(self.cli(), 1)
                self.assertTrue(any(target in error for error in report['errors']))

    def test_missing_required_role_and_template_fail(self):
        for relative in ('REVIEWER.md', 'templates/verification.md'):
            with self.subTest(path=relative):
                path = self.package / relative
                original = path.read_bytes()
                path.unlink()
                try:
                    report = self.result(self.cli(), 1)
                    self.assertIn(f'Missing package file: {relative}', report['errors'])
                finally:
                    path.write_bytes(original)

    def test_invalid_skill_entry_point_and_policy_fail(self):
        prefix = self.package / '.agents/skills/spec-planner'
        for relative, expected in (
                ('SKILL.md', 'Invalid skill entry point: spec-planner'),
                ('agents/openai.yaml', 'Invalid invocation policy: spec-planner')):
            with self.subTest(path=relative):
                path = prefix / relative
                original = path.read_bytes()
                path.write_text('invalid\n')
                try:
                    self.assertIn(expected, self.result(self.cli(), 1)['errors'])
                finally:
                    path.write_bytes(original)

    def test_unreadable_document_returns_inability_to_run(self):
        (self.package / 'extra.md').write_bytes(b'\xff')
        process = self.cli()
        self.assertEqual(process.returncode, 2)
        self.assertIn('Package check could not complete:', process.stderr)


if __name__ == '__main__':
    unittest.main()
