"""Package-check CLI contracts on disposable packages without Git history."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import TypedDict, cast


class PackageResult(TypedDict):
    status: str
    errors: list[str]
    local_links_checked: int


PACKAGE = Path(__file__).resolve().parents[1]


class PackageCheckTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / "agentic-workflow"
        shutil.copytree(
            PACKAGE, self.package, ignore=shutil.ignore_patterns("__pycache__", "*.pyc")
        )

    def cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.package / "helpers/check_package.py"), *arguments],
            cwd=self.root,
            capture_output=True,
            text=True,
        )

    def result(self, process: subprocess.CompletedProcess[str], code: int) -> PackageResult:
        self.assertEqual(process.returncode, code, process.stdout + process.stderr)
        report = cast(PackageResult, json.loads(process.stdout))
        self.assertEqual(report["status"], "PASS" if code == 0 else "FAIL")
        self.assertGreater(report["local_links_checked"], 0)
        return report

    def test_imports_stay_inside_standard_library_and_copy_boundary(self) -> None:
        (self.root / "repository_only.py").write_text("# Not in the copied package.\n")
        cases = (
            ("import json\nfrom pathlib import Path\n", None),
            ("def helper():\n    import records\n", None),
            ("from . import records\n", None),
            ("from .records import identifier\n", None),
            ("from ..helpers.records import identifier\n", None),
            ("from .. import helpers\n", None),
            ("import importlib as loader\nloader.import_module('json')\n", None),
            ("from importlib import import_module as load\nload('.records', 'helpers')\n", None),
            ("__import__('records')\n", None),
            ("if False:\n    import requests\n", "requests"),
            ("def helper():\n    from typing_extensions import TypedDict\n", "typing_extensions"),
            ("import repository_only\n", "repository_only"),
            ("from . import missing_local\n", "missing_local"),
            ("from ..repository_only import value\n", "repository_only"),
            ("import importlib\nimportlib.import_module('requests')\n", "requests"),
            (
                "from importlib import import_module as load\nload('repository_only')\n",
                "repository_only",
            ),
            ("from builtins import __import__ as load\nload('requests')\n", "requests"),
            ("__import__('requests')\n", "requests"),
            ("import importlib\nimportlib.import_module(module_name)\n", "computed import target"),
            ("__import__('json' + suffix)\n", "computed import target"),
            (
                "import importlib\nimportlib.import_module('.records', package_name)\n",
                "computed import package",
            ),
            ("__import__('records', level=level)\n", "computed import level"),
        )
        for source, violation in cases:
            with self.subTest(source=source):
                (self.package / "helpers/probe.py").write_text(source)
                report = self.result(self.cli(), 1 if violation else 0)
                if violation:
                    self.assertTrue(
                        any(
                            "helpers/probe.py:" in error and violation in error
                            for error in report["errors"]
                        ),
                        report["errors"],
                    )
                else:
                    self.assertEqual(report["errors"], [])

    def test_valid_package_ignores_host_instructions(self) -> None:
        (self.root / "AGENTS.md").write_text("[Host-only reference](absent.md)\n")
        self.assertEqual(self.result(self.cli(), 0)["errors"], [])

    def test_additional_valid_markdown_is_allowed_and_checked(self) -> None:
        (self.package / "extra.md").write_text(
            "# Extra\n[Routing](policies/MODELS.md#model-routing)\n"
        )
        self.assertEqual(self.result(self.cli(), 0)["errors"], [])

    def test_broken_local_link_and_anchor_fail(self) -> None:
        extra = self.package / "extra.md"
        for target in ("missing.md", "AGENTS.md#absent-heading"):
            with self.subTest(target=target):
                extra.write_text(f"# Extra\n[Reference]({target})\n")
                report = self.result(self.cli(), 1)
                self.assertTrue(any(target in error for error in report["errors"]))

    def test_missing_required_role_and_template_fail(self) -> None:
        for relative in ("roles/REVIEWER.md", "templates/verification.md", "helpers/records.py"):
            with self.subTest(path=relative):
                path = self.package / relative
                original = path.read_bytes()
                path.unlink()
                try:
                    report = self.result(self.cli(), 1)
                    self.assertIn(f"Missing package file: {relative}", report["errors"])
                finally:
                    path.write_bytes(original)

    def test_link_outside_package_fails_even_when_host_file_exists(self) -> None:
        (self.root / "host.md").write_text("# Host dependency\n")
        (self.package / "extra.md").write_text("[Host](../host.md)\n")
        report = self.result(self.cli(), 1)
        self.assertTrue(any("outside copy boundary" in error for error in report["errors"]))

    def test_unreadable_document_returns_inability_to_run(self) -> None:
        (self.package / "extra.md").write_bytes(b"\xff")
        process = self.cli()
        self.assertEqual(process.returncode, 2)
        self.assertIn("Package check could not complete:", process.stderr)


if __name__ == "__main__":
    unittest.main()
