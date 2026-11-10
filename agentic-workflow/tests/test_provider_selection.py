"""Provider isolation through public commands and real disposable host storage.

An audit hook rejects forbidden filesystem/CLI access in the command process;
fixture executables provide deterministic OpenCode exports without a live host.
"""

import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_native_collection import row, turn
from test_opencode_capture import idle, prompt, step

HELPERS = Path(__file__).resolve().parents[1] / "helpers"

# Audit the actual command, including imports, rather than replacing its providers.
GUARDED_COMMAND = """
import json, os, runpy, sys
blocked = json.loads(os.environ['TRACE_TEST_FORBIDDEN'])
def guard(event, args):
    if event in ('open', 'os.scandir', 'os.listdir', 'sqlite3.connect', 'subprocess.Popen'):
        value = args[0] if args else None
        if isinstance(value, (str, bytes, os.PathLike)):
            path = os.path.abspath(os.fsdecode(value))
            if any(path == target or path.startswith(target + os.sep) for target in blocked):
                raise RuntimeError('foreign provider access: ' + path)
sys.addaudithook(guard)
sys.argv = sys.argv[1:]
sys.path.insert(0, os.path.dirname(sys.argv[0]))
"""


class ProviderSelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "001_demo"
        self.root.mkdir()
        self.codex = self.base / "codex"
        self.codex.mkdir()
        self.rollout = self.codex / "session.jsonl"
        self.rollout.write_text(
            "".join(
                json.dumps(r) + "\n"
                for r in [
                    row("session_meta", dict(id="shared", cli_version="0.167.0")),
                    *turn("shared", "turn-1", 100),
                ]
            )
        )
        with sqlite3.connect(self.codex / "state_5.sqlite") as connection:
            connection.execute("CREATE TABLE threads (id TEXT, rollout_path TEXT, source TEXT)")
            connection.execute(
                "INSERT INTO threads VALUES (?, ?, ?)", ("shared", str(self.rollout), '"cli"')
            )
        connection.close()
        self.export = self.base / "export.json"
        self.export.write_text(
            json.dumps(
                dict(
                    info=dict(id="shared"),
                    messages=[
                        prompt("turn-1", 1000, "Work"),
                        step("step", 1010),
                        idle("end", 1100),
                    ],
                )
            )
        )
        self.binary = self.base / "opencode"
        self.calls = self.base / "exports-called"
        self.binary.write_text(
            f"#!{sys.executable}\nimport pathlib, sys\n"
            "assert sys.argv[1:] == ['session', 'export', 'shared']\n"
            f"pathlib.Path({str(self.calls)!r}).touch()\n"
            f"print(pathlib.Path({str(self.export)!r}).read_text())\n"
        )
        self.binary.chmod(0o755)
        self.env = dict(
            os.environ,
            CODEX_HOME=str(self.codex),
            CODEX_THREAD_ID="shared",
            OPENCODE_SESSION_ID="shared",
            PATH=str(self.base) + os.pathsep + os.environ["PATH"],
        )

    def command(
        self,
        script: str,
        *args: str | Path,
        forbidden: tuple[Path, ...] = (),
        internal_refresh: bool = False,
    ) -> subprocess.CompletedProcess[str]:
        entry = (
            "from pathlib import Path; from usage_report import refresh; "
            "refresh(Path(sys.argv[1]), sys.argv[2])"
            if internal_refresh
            else "runpy.run_path(sys.argv[0], run_name='__main__')"
        )
        return subprocess.run(
            [
                sys.executable,
                "-B",
                "-c",
                GUARDED_COMMAND + entry,
                str(HELPERS / script),
                *map(str, args),
            ],
            env=dict(self.env, TRACE_TEST_FORBIDDEN=json.dumps([str(p) for p in forbidden])),
            capture_output=True,
            text=True,
            timeout=10,
        )

    def seed(self) -> tuple[Path, Path]:
        directory = self.root / "native/shared"
        directory.mkdir(parents=True)
        codex, opencode = directory / "turn-1.jsonl", directory / "turn-1.json"
        codex.write_bytes(self.rollout.read_bytes())
        opencode.write_bytes(self.export.read_bytes())
        return codex, opencode

    def test_unique_or_missing_detection_and_capture_failure_never_fall_back(self) -> None:
        for provider in ("codex", "opencode", "none"):
            for failing in (False, True):
                if provider == "none" and failing:
                    continue
                with self.subTest(provider=provider, failing=failing):
                    self.env.update(
                        CODEX_HOME=str(self.codex),
                        CODEX_THREAD_ID="shared" if provider == "codex" else "",
                        OPENCODE_SESSION_ID="shared" if provider == "opencode" else "",
                    )
                    if failing:
                        if provider == "codex":
                            self.env["CODEX_HOME"] = str(self.base / "missing")
                        else:
                            self.export.write_text("invalid export")
                    records = self.base / f"records-{provider}-{failing}"
                    result = self.command(
                        "records.py",
                        "allocate",
                        "demo",
                        "--records-root",
                        records,
                        forbidden=(self.binary,)
                        if provider == "codex"
                        else (self.codex,)
                        if provider == "opencode"
                        else (self.codex, self.binary),
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    root = Path(result.stdout.strip())
                    self.assertTrue((root / "tasks").is_dir())
                    if provider == "none":
                        self.assertIn("current_session_unavailable", result.stderr)
                        self.assertIn("capture unavailable", result.stderr)
                    elif failing:
                        self.assertIn(
                            "native_storage_unavailable"
                            if provider == "codex"
                            else "opencode_export_unavailable",
                            result.stderr,
                        )
                    else:
                        suffix = "jsonl" if provider == "codex" else "json"
                        self.assertTrue((root / f"native/shared/turn-1.{suffix}").is_file())
                    if failing or provider == "none":
                        self.assertFalse((root / "native").exists())
                    # Resolution repeats the same detection rules without creating a task.
                    (root / "tasks/work").mkdir()
                    resolved = self.command("records.py", "resolve", root, "work")
                    self.assertEqual(resolved.returncode, 0, resolved.stderr)
                    self.assertEqual(Path(resolved.stdout.strip()), root / "tasks/work")

    def test_ambiguous_detection_fails_before_allocation_or_resolution_writes(self) -> None:
        records = self.base / "new-records"
        result = self.command("records.py", "allocate", "demo", "--records-root", records)
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("conflicting tracing providers: codex, opencode", result.stderr)
        self.assertFalse(records.exists())
        (self.root / "tasks/work").mkdir(parents=True)
        result = self.command("records.py", "resolve", self.root, "work")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn("conflicting tracing providers: codex, opencode", result.stderr)
        self.assertEqual(
            sorted(str(p.relative_to(self.root)) for p in self.root.rglob("*")),
            ["tasks", "tasks/work"],
        )
        self.assertFalse(self.calls.exists())

    def test_undetectable_evidence_fails_before_reporting_or_viewer_writes(self) -> None:
        for state in ("missing-directory", "empty", "unknown", "ambiguous", "invalid"):
            with self.subTest(state=state):
                root = self.base / state
                if state != "missing-directory":
                    native = root / "native/shared"
                    native.mkdir(parents=True)
                    (root / "reports").mkdir()
                    (root / "reports/usage.json").write_text("Previous report")
                    if state == "unknown":
                        (native / "trace.txt").write_text("Unknown format")
                    elif state == "ambiguous":
                        (native / "turn.jsonl").write_bytes(self.rollout.read_bytes())
                        (native / "turn.json").write_bytes(self.export.read_bytes())
                    elif state == "invalid":
                        (native / "turn.json").write_text("{}")
                before = {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}
                for script in ("usage_report.py", "trace_view.py"):
                    result = self.command(script, root, forbidden=(self.codex, self.binary))
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("tracing provider", result.stderr)
                    if state == "ambiguous":
                        self.assertIn("codex, opencode", result.stderr)
                    self.assertEqual(
                        {p: p.read_bytes() for p in root.rglob("*") if p.is_file()}, before
                    )
                    self.assertEqual(root.exists(), state != "missing-directory")

    def test_commands_do_not_expose_provider_selection(self) -> None:
        self.seed()
        for script in ("usage_report.py", "trace_view.py"):
            help_result = self.command(script, "--help")
            self.assertEqual(help_result.returncode, 0, help_result.stderr)
            self.assertNotIn("--provider", help_result.stdout)
            for provider in ("codex", "opencode"):
                result = self.command(script, self.root, "--provider", provider)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("unrecognized arguments: --provider", result.stderr)

    def test_reporting_detects_saved_provider_independently_of_active_hosts(self) -> None:
        for provider, source, suffix, blocked, expected in (
            ("codex", self.rollout, "jsonl", self.binary, 13),
            ("opencode", self.export, "json", self.codex, 12),
        ):
            with self.subTest(provider=provider):
                native = self.root / f"native/shared/turn-1.{suffix}"
                native.parent.mkdir(parents=True, exist_ok=True)
                native.write_bytes(source.read_bytes())
                result = self.command("usage_report.py", self.root, forbidden=(blocked,))
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["tracing_provider"], provider)
                report = json.loads((self.root / "reports/usage.json").read_text())
                self.assertEqual(report["tracing_provider"], provider)
                self.assertEqual(report["summary"]["tokens"]["total_tokens"]["total"], expected)
                native.unlink()

    def test_selection_isolates_native_files_host_access_and_assignment_joins(self) -> None:
        codex, opencode = self.seed()
        (self.root / "proof.txt").write_text("Verified task attribution")
        (self.root / "assignment-annotations.json").write_text(
            json.dumps(
                dict(
                    version=1,
                    assignments=[
                        dict(
                            adapter=provider,
                            session_id="shared",
                            turn_id="turn-1",
                            task=provider + "-task",
                            role="implementer",
                            evidence=["proof.txt"],
                        )
                        for provider in ("codex", "opencode")
                    ],
                )
            )
        )
        for provider, foreign, blocked, expected in (
            ("codex", opencode, self.binary, 13),
            ("opencode", codex, self.codex, 12),
        ):
            with self.subTest(provider=provider):
                before = foreign.read_bytes()
                result = self.command(
                    "usage_report.py",
                    self.root,
                    provider,
                    forbidden=(foreign, blocked),
                    internal_refresh=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(foreign.read_bytes(), before)
                report = json.loads((self.root / "reports/usage.json").read_text())
                self.assertEqual(report["summary"]["tokens"]["total_tokens"]["total"], expected)
                self.assertEqual(report["tracing_provider"], provider)
                self.assertEqual(report["assignments"][0]["task_id"], provider + "-task")
                self.assertEqual({s["adapter"] for s in report["native_sources"]}, {provider})
                content = json.loads((self.root / "reports/events.json").read_text())
                self.assertEqual(content["tracing_provider"], provider)
                self.assertEqual({e["tracing_provider"] for e in content["events"]}, {provider})
                self.assertEqual(
                    json.loads((self.root / "reports/timeline.json").read_text())["metadata"][
                        "tracing_provider"
                    ],
                    provider,
                )
                self.assertIn(
                    f"Tracing provider: {provider}", (self.root / "reports/usage.md").read_text()
                )
                if provider == "opencode":
                    model = next(e for e in content["events"] if e["kind"] == "model")
                    self.assertEqual(model["provider"], "openai")

    def test_empty_selection_does_not_parse_or_refresh_foreign_evidence(self) -> None:
        codex, opencode = self.seed()
        for provider, selected, foreign, blocked in (
            ("codex", codex, opencode, self.binary),
            ("opencode", opencode, codex, self.codex),
        ):
            with self.subTest(provider=provider):
                data = selected.read_bytes()
                selected.unlink()
                before = foreign.read_bytes()
                result = self.command(
                    "usage_report.py",
                    self.root,
                    provider,
                    forbidden=(foreign, blocked),
                    internal_refresh=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                report = json.loads((self.root / "reports/usage.json").read_text())
                self.assertIn("no_native_evidence", report["summary"]["coverage"])
                self.assertEqual(report["native_sources"], [])
                self.assertIsNone(report["summary"]["tokens"]["total_tokens"]["known_subtotal"])
                self.assertEqual(foreign.read_bytes(), before)
                selected.write_bytes(data)
        self.assertFalse(self.calls.exists())


if __name__ == "__main__":
    unittest.main()
