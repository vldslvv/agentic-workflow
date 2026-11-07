"""CLI transport and process lifecycle contracts, using isolated real storage."""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class CliTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        self.app = root / "app"
        shutil.copytree(
            Path(__file__).resolve().parents[1] / "todolist",
            self.app / "todolist",
            ignore=shutil.ignore_patterns("__pycache__"),
        )
        self.cwd = root / "elsewhere"
        self.cwd.mkdir()
        self.storage = self.app / "tasks.json"

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "todolist", *args],
            cwd=self.cwd,
            env={**os.environ, "PYTHONPATH": str(self.app)},
            capture_output=True, text=True, timeout=10,
        )

    def success(self, *args):
        result = self.run_cli(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        return result.stdout

    def test_help_and_no_command(self):
        for args in ((), ("help",), ("--help",)):
            with self.subTest(args=args):
                output = self.success(*args)
                self.assertIn("usage:", output)
                for command in ("add", "list", "complete", "delete", "help"):
                    self.assertIn(command, output)
        self.assertFalse(self.storage.exists())

    def test_lifecycle_across_processes(self):
        self.assertIn("No tasks", self.success("list"))
        self.assertIn("Added task 1: Buy milk", self.success("add", "Buy milk"))
        self.assertIn("Added task 2: Walk the dog", self.success("add", "Walk the dog"))
        self.assertEqual(self.success("list").splitlines(), [
            "1 [pending] Buy milk", "2 [pending] Walk the dog",
        ])
        self.assertIn("Completed task 1", self.success("complete", "1"))
        self.assertIn("Deleted task 2", self.success("delete", "2"))
        self.assertEqual(self.success("list").strip(), "1 [completed] Buy milk")
        self.assertEqual(json.loads(self.storage.read_text()), [
            {"id": 1, "title": "Buy milk", "completed": True},
        ])
        self.success("delete", "1")
        self.assertIn("No tasks", self.success("list"))
        self.assertFalse((self.cwd / "tasks.json").exists())

    def test_argument_and_business_errors_reach_stderr_without_mutation(self):
        self.success("add", "Keep me")
        before = self.storage.read_bytes()
        for args, message in (
            (("add",), "required"),
            (("complete",), "required"),
            (("delete",), "required"),
            (("complete", "abc"), "invalid int"),
            (("delete", "0"), "positive integer"),
            (("unknown",), "invalid choice"),
            (("add", " "), "must not be blank"),
            (("complete", "999"), "not found"),
            (("delete", "999"), "not found"),
        ):
            with self.subTest(args=args):
                result = self.run_cli(*args)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, "")
                self.assertIn(message, result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(self.storage.read_bytes(), before)

    def test_storage_errors_are_concise_failures(self):
        self.storage.write_text("{")
        result = self.run_cli("add", "New task")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Invalid task storage", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertEqual(self.storage.read_text(), "{")

        self.storage.unlink()
        self.storage.mkdir()
        result = self.run_cli("list")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Error:", result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        self.assertTrue(self.storage.is_dir())


if __name__ == "__main__":
    unittest.main()
