"""AC-5: exercise the helper through its real CLI and durable evidence files."""

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest


HELPER = Path(__file__).resolve().parents[1] / "helpers" / "check_execution.py"


class CheckExecutionCLI(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.manifest = self.root / "checks.json"
        self.output = self.root / "evidence"

    def step(self, identifier, code="pass", **updates):
        step = {"id": identifier, "argv": [sys.executable, "-c", code], "cwd": ".",
                "timeout_seconds": 5, "timeout_kind": "infrastructure", "expected_exit_codes": [0]}
        step.update(updates)
        return step

    def check(self, identifier="verify", code="pass", **updates):
        return self.step(identifier, code, requirements=["AC-5"], mandatory=True, **updates)

    def write_manifest(self, checks=None, setup=None, cleanup=None):
        manifest = {"version": 1, "requirements": ["AC-5"], "setup": setup or [],
                    "checks": [self.check()] if checks is None else checks, "cleanup": cleanup or []}
        self.manifest.write_text(json.dumps(manifest), encoding="utf-8")
        return manifest

    def invoke(self, env=None):
        process = subprocess.run([sys.executable, str(HELPER), str(self.manifest), "--output", str(self.output)],
                                 capture_output=True, text=True, timeout=15, env=env)
        receipt = json.loads(process.stdout)
        summary = json.loads((self.output / "summary.json").read_text())
        self.assertEqual(receipt["status"], summary["status"])
        self.assertEqual(receipt["evidence"], str(self.output))
        return process, summary

    def test_success_expected_nonzero_and_start_evidence_precede_execution(self):
        invocation = self.output / "steps" / "checks-000-verify" / "invocation.json"
        code = ("import json,pathlib,sys; "
                f"record=json.loads(pathlib.Path({str(invocation)!r}).read_text()); "
                "assert record['started_at']; assert record['argv']; "
                "print('observed stdout'); print('observed stderr', file=sys.stderr)")
        self.write_manifest(checks=[self.check(code=code), self.check("nonzero", "raise SystemExit(7)",
                                                                  expected_exit_codes=[7])],
                            setup=[self.step("prepare", "from pathlib import Path; Path('ready').touch()")],
                            cleanup=[self.step("remove", "from pathlib import Path; Path('ready').unlink()")])
        env = dict(os.environ, CHECK_EXECUTION_CREDENTIAL="private-environment-sentinel")
        process, summary = self.invoke(env)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(summary["status"], "PASS")
        self.assertEqual(summary["requirements"], {"AC-5": "PASS"})
        self.assertEqual(summary["mandatory_executed"], 2)
        self.assertEqual(summary["cleanup_status"], "PASS")
        self.assertFalse((self.root / "ready").exists())
        checked = summary["steps"][1]
        directory = Path(checked["evidence"])
        self.assertEqual((directory / "stdout.txt").read_text(), "observed stdout\n")
        self.assertEqual((directory / "stderr.txt").read_text(), "observed stderr\n")
        self.assertEqual(checked["exit_code"], 0)
        self.assertIsNone(checked["signal"])
        self.assertGreaterEqual(checked["duration_seconds"], 0)
        self.assertEqual(summary["steps"][2]["exit_code"], 7)
        for path in self.output.rglob("*"):
            if path.is_file():
                self.assertNotIn(b"private-environment-sentinel", path.read_bytes())

    def test_failure_classification_and_cleanup(self):
        cases = [
            ("unexpected", {"code": "raise SystemExit(9)"}, "FAIL", 9, False),
            ("missing", {"argv": [str(self.root / "no-such-executable")]}, "BLOCKED", None, False),
            ("infrastructure", {"code": "import time; time.sleep(10)", "timeout_seconds": 0.1},
             "BLOCKED", None, True),
            ("behavioral", {"code": "import time; time.sleep(10)", "timeout_seconds": 0.1,
                            "timeout_kind": "behavioral"}, "FAIL", None, True),
        ]
        for name, arguments, expected_status, exit_code, timed_out in cases:
            with self.subTest(name=name):
                self.output = self.root / name
                marker = self.root / f"{name}-cleaned"
                self.write_manifest(checks=[self.check(**arguments)], cleanup=[self.step(
                    "cleanup", f"from pathlib import Path; Path({str(marker)!r}).touch()")])
                process, summary = self.invoke()
                self.assertEqual(process.returncode, 1 if expected_status == "FAIL" else 2)
                self.assertEqual(summary["primary_status"], expected_status)
                self.assertEqual(summary["status"], expected_status)
                self.assertEqual(summary["cleanup_status"], "PASS")
                self.assertEqual(summary["steps"][0]["exit_code"], exit_code)
                self.assertEqual(summary["steps"][0]["timed_out"], timed_out)
                self.assertTrue(marker.exists())

    def test_cleanup_failure_preserves_primary_failure_and_later_cleanup(self):
        self.write_manifest(checks=[self.check(code="raise SystemExit(9)")], cleanup=[
            self.step("broken-cleanup", "raise SystemExit(13)"),
            self.step("final-cleanup", "from pathlib import Path; Path('cleaned').touch()")])
        _, summary = self.invoke()
        self.assertEqual(summary["primary_status"], "FAIL")
        self.assertEqual(summary["cleanup_status"], "FAIL")
        self.assertEqual([step["exit_code"] for step in summary["steps"]], [9, 13, 0])
        self.assertTrue((self.root / "cleaned").exists())

    def test_failed_setup_does_not_run_checks_but_always_cleans_up(self):
        self.write_manifest(setup=[self.step("setup", "raise SystemExit(6)")],
                            checks=[self.check(code="from pathlib import Path; Path('check-ran').touch()")],
                            cleanup=[self.step("cleanup", "from pathlib import Path; Path('cleaned').touch()")])
        _, summary = self.invoke()
        self.assertEqual(summary["status"], "FAIL")
        self.assertEqual(summary["mandatory_executed"], 0)
        self.assertEqual(summary["steps"][1]["status"], "NOT_RUN")
        self.assertFalse((self.root / "check-ran").exists())
        self.assertTrue((self.root / "cleaned").exists())

    def test_incomplete_or_ambiguous_manifests_cannot_run_or_pass(self):
        for name in ("empty", "unmapped", "unknown", "duplicate", "shell", "version", "zero-timeout"):
            with self.subTest(name=name):
                self.output = self.root / name
                manifest = self.write_manifest()
                if name == "empty":
                    manifest["checks"] = []
                elif name == "unmapped":
                    manifest["checks"][0]["mandatory"] = False
                elif name == "unknown":
                    manifest["checks"][0]["requirements"] = ["OTHER"]
                elif name == "duplicate":
                    manifest["checks"] *= 2
                elif name == "shell":
                    manifest["checks"][0]["argv"] = "echo shell"
                elif name == "version":
                    manifest["version"] = 2
                else:
                    manifest["checks"][0]["timeout_seconds"] = 0
                self.manifest.write_text(json.dumps(manifest))
                process, summary = self.invoke()
                self.assertEqual(process.returncode, 2)
                self.assertEqual(summary["status"], "BLOCKED")
                self.assertEqual(summary["mandatory_executed"], 0)
                self.assertTrue(summary["reason"])
                self.assertFalse((self.output / "steps").exists())

    def test_existing_evidence_is_never_overwritten(self):
        self.write_manifest()
        self.invoke()
        original = {str(path.relative_to(self.output)): path.read_bytes()
                    for path in self.output.rglob("*") if path.is_file()}
        process = subprocess.run([sys.executable, str(HELPER), str(self.manifest), "--output", str(self.output)],
                                 capture_output=True, text=True, timeout=10)
        self.assertEqual(process.returncode, 2)
        self.assertEqual(json.loads(process.stdout)["status"], "BLOCKED")
        current = {str(path.relative_to(self.output)): path.read_bytes()
                   for path in self.output.rglob("*") if path.is_file()}
        self.assertEqual(current, original)

    @unittest.skipUnless(os.name == "posix", "POSIX signal lifecycle")
    def test_cleanup_interruption_preserves_primary_and_continues_remaining_cleanup(self):
        self.write_manifest(checks=[self.check(code="raise SystemExit(9)")], cleanup=[
            self.step("slow-cleanup", "import time; from pathlib import Path; Path('started').touch(); time.sleep(60)"),
            self.step("final-cleanup", "from pathlib import Path; Path('cleaned').touch()")])
        process = subprocess.Popen([sys.executable, str(HELPER), str(self.manifest), "--output", str(self.output)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        deadline = time.monotonic() + 5
        while not (self.root / "started").exists() and time.monotonic() < deadline:
            if process.poll() is not None:
                self.fail("runner exited before cleanup started")
            time.sleep(0.01)
        self.assertTrue((self.root / "started").exists())
        process.send_signal(signal.SIGINT)
        _, stderr = process.communicate(timeout=5)
        self.assertEqual(process.returncode, 1, stderr)
        summary = json.loads((self.output / "summary.json").read_text())
        self.assertEqual(summary["primary_status"], "FAIL")
        self.assertEqual(summary["cleanup_status"], "BLOCKED")
        self.assertEqual(summary["steps"][0]["exit_code"], 9)
        self.assertEqual(summary["steps"][1]["interrupted_by"], signal.SIGINT)
        self.assertTrue((self.root / "cleaned").exists())

    @unittest.skipUnless(os.name == "posix", "POSIX signal lifecycle")
    def test_child_signal_is_recorded_as_behavioral_failure(self):
        self.write_manifest(checks=[self.check(code="import os,signal; os.kill(os.getpid(), signal.SIGTERM)")])
        _, summary = self.invoke()
        self.assertEqual(summary["status"], "FAIL")
        self.assertEqual(summary["steps"][0]["signal"], signal.SIGTERM)
        self.assertIsNone(summary["steps"][0]["exit_code"])

    @unittest.skipUnless(os.name == "posix", "POSIX signal lifecycle")
    def test_external_interruption_reaps_child_and_retains_cleanup_and_partial_output(self):
        self.write_manifest(checks=[self.check(code=(
            "import os,time; from pathlib import Path; print('partial', flush=True); "
            "Path('started').write_text(str(os.getpid())); time.sleep(60)"))], cleanup=[
                self.step("cleanup", "from pathlib import Path; Path('cleaned').touch()")])
        process = subprocess.Popen([sys.executable, str(HELPER), str(self.manifest), "--output", str(self.output)],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.addCleanup(lambda: process.kill() if process.poll() is None else None)
        deadline = time.monotonic() + 5
        while not (self.root / "started").exists() and time.monotonic() < deadline:
            if process.poll() is not None:
                self.fail("runner exited before child started")
            time.sleep(0.01)
        self.assertTrue((self.root / "started").exists(), "child did not start")
        child_pid = int((self.root / "started").read_text())
        process.send_signal(signal.SIGTERM)
        stdout, stderr = process.communicate(timeout=5)
        self.assertEqual(process.returncode, 2, stderr)
        self.assertEqual(json.loads(stdout)["status"], "BLOCKED")
        summary = json.loads((self.output / "summary.json").read_text())
        checked = summary["steps"][0]
        self.assertEqual(checked["interrupted_by"], signal.SIGTERM)
        self.assertEqual(checked["status"], "BLOCKED")
        self.assertEqual(checked["signal"], signal.SIGTERM)
        self.assertEqual((Path(checked["evidence"]) / "stdout.txt").read_text(), "partial\n")
        self.assertTrue((self.root / "cleaned").exists())
        self.assertEqual(summary["cleanup_status"], "PASS")
        with self.assertRaises(ProcessLookupError):
            os.kill(child_pid, 0)


if __name__ == "__main__":
    unittest.main()
