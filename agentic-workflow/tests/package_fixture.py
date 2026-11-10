"""Shared disposable-package fixture for package checker CLI tests."""

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


class PackageCheckCase(unittest.TestCase):
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
