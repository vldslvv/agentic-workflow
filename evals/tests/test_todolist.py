"""Public runner contract tests; fixtures isolate the costly model/uv boundary."""

import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest


EVALS = Path(__file__).resolve().parents[1]


class TodolistEvalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        self.bin = self.base / "bin"
        self.bin.mkdir()
        for name in ("codex", "uv"):
            path = self.bin / name
            path.write_text(f"#!{sys.executable}\n" + (EVALS / "tests/fixtures/tool.py").read_text())
            path.chmod(0o755)
        shutil.copyfile(EVALS / "tests/fixtures/todo.py", self.bin / "todo.py")
        self.env = dict(os.environ, PATH=f"{self.bin}:{os.environ['PATH']}")
        (self.root / "evals").mkdir()
        shutil.copyfile(EVALS / "todolist.py", self.root / "evals/todolist.py")
        shutil.copyfile(EVALS / "worktree.py", self.root / "evals/worktree.py")
        shutil.copyfile(EVALS / "runtime.py", self.root / "evals/runtime.py")
        shutil.copyfile(EVALS.parent / "Makefile", self.root / "Makefile")
        (self.root / "agentic-workflow/policies").mkdir(parents=True)
        (self.root / "agentic-workflow/policies/MODELS.md").write_text(
            "## Profiles\n| Profile | Model | Reasoning |\n|---|---|---|\n"
            "| coordinator | fixture-model | high |\n"
            "## Role routes\n| Role | Default | Demanding work |\n|---|---|---|\n"
            "| Supervisor | coordinator | coordinator |\n"
        )
        (self.root / ".gitignore").write_text(
            "/.agentic-workflow/evals/\n/.agentic-workflow/tmp/worktrees/\n/ignored\n__pycache__/\n")
        (self.root / "source.txt").write_text("original\n")
        self.git("init", "-q")
        self.git("add", ".")
        self.git("-c", "user.name=Eval Test", "-c", "user.email=eval@example.invalid", "commit", "-qm", "fixture")
        self.results = self.root / ".agentic-workflow/evals/todolist"

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                              capture_output=True, text=True).stdout

    def invoke(self, action="run", *args, mode="pass"):
        return subprocess.run([sys.executable, "evals/todolist.py", action, *args],
                              cwd=self.root, env=dict(self.env, EVAL_FIXTURE=mode),
                              capture_output=True, text=True, timeout=15)

    def report(self):
        return json.loads((self.results / "result.json").read_text())

    def test_success_preserves_evidence_and_empty_artifacts_pass(self):
        (self.root / "ignored").touch()
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = self.report()
        self.assertEqual([report[k]["status"] for k in ("agent", "cli", "artifacts")], ["PASS"] * 3)
        self.assertEqual(len(report["cli"]["commands"]), 11)
        self.assertEqual(json.loads((self.results / "cli.json").read_text())["status"], "PASS")
        self.assertEqual((self.results / "generation-tasks.json").read_text(), "generation data to preserve\n")
        self.assertEqual((self.results / "final-response.txt").read_text(), "fixture final response\n")
        self.assertIn("agent event", (self.results / "events.jsonl").read_text())
        self.assertIn("fixture stderr", (self.results / "agent.stderr").read_text())
        self.assertTrue((self.root / "apps/todolist/tasks.json").is_file())
        launch = json.loads((self.results / "run.json").read_text())
        received = json.loads((self.results / "received.json").read_text())
        self.assertEqual(launch["source_commit"], self.git("rev-parse", "HEAD").strip())
        self.assertEqual(received[-1], "Implement specs/todolist")
        for flag, value in (("--model", "fixture-model"), ("--sandbox", "workspace-write"),
                            ("--enable", "multi_agent")):
            self.assertEqual(received[received.index(flag) + 1], value)
        for setting in ('approval_policy="never"', 'model_reasoning_effort="high"',
                        "sandbox_workspace_write.network_access=true"):
            self.assertIn(setting, received)
        self.assertNotIn("--ephemeral", received)

    def test_dirty_checkout_rejected_before_creating_results(self):
        for kind in ("unstaged", "staged", "untracked"):
            with self.subTest(kind=kind):
                path = self.root / ("new.txt" if kind == "untracked" else "source.txt")
                path.write_text("changed\n")
                if kind == "staged":
                    self.git("add", "source.txt")
                result = self.invoke()
                self.assertEqual(result.returncode, 2)
                self.assertIn("Clean checkout required", result.stderr)
                self.assertFalse(self.results.exists())
                self.assertEqual(path.read_text(), "changed\n")
                # Reset only this disposable fixture to prepare the next case.
                if kind == "untracked":
                    path.unlink()
                else:
                    path.write_text("original\n")
                    self.git("add", "source.txt")

    def test_project_routing_replaces_defaults_and_survives_cleanup(self):
        override = self.root / ".agentic-workflow/config/MODELS.md"
        override.parent.mkdir(parents=True)
        source = (self.root / "agentic-workflow/policies/MODELS.md").read_text()
        content = source.replace("fixture-model", "project-model").replace("high", "default")
        override.write_text(content)
        result = self.invoke("run", "--allow-dirty")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        received = json.loads((self.results / "received.json").read_text())
        self.assertEqual(received[received.index("--model") + 1], "project-model")
        self.assertFalse(any("model_reasoning_effort" in arg for arg in received))
        self.assertEqual(self.invoke("clean").returncode, 0)
        self.assertEqual(override.read_text(), content)
        # A present override is authoritative even when invalid; no fallback.
        override.write_text("## Profiles\n")
        result = self.invoke("run", "--allow-dirty")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("Missing Supervisor default route", result.stderr)
        self.assertFalse(self.results.exists())

    def test_existing_ignored_output_paths_rejected(self):
        with (self.root / ".git/info/exclude").open("a") as f:
            f.write("\n/apps/todolist/\n")
        for name in ("apps/todolist", ".agentic-workflow/evals/todolist"):
            with self.subTest(path=name):
                path = self.root / name
                path.mkdir(parents=True)
                result = self.invoke()
                self.assertEqual(result.returncode, 2)
                self.assertIn("Required absent path", result.stderr)
                self.assertFalse((self.results / "run.json").exists())
                path.rmdir()

    def test_allow_dirty_preserves_inputs_and_still_rejects_existing_outputs(self):
        (self.root / "source.txt").write_text("uncommitted input\n")
        self.git("add", "source.txt")
        (self.root / "source.txt").write_text("further unstaged input\n")
        (self.root / "new.txt").write_text("untracked input\n")
        index_before = self.git("diff", "--cached")
        result = self.invoke("run", "--allow-dirty")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        launch = json.loads((self.results / "run.json").read_text())
        self.assertTrue(launch["allow_dirty"])
        self.assertIn("MM source.txt", launch["git_status_before"])
        self.assertIn("?? new.txt", launch["git_status_before"])
        result = self.invoke("run", "--allow-dirty")
        self.assertEqual(result.returncode, 2)
        self.assertIn("Required absent path", result.stderr)
        self.assertEqual(self.invoke("clean").returncode, 0)
        self.assertEqual((self.root / "source.txt").read_text(), "further unstaged input\n")
        self.assertEqual((self.root / "new.txt").read_text(), "untracked input\n")
        self.assertEqual(self.git("diff", "--cached"), index_before)

    def test_existing_execution_records_are_excluded_from_grading_and_cleanup(self):
        old = self.root / ".agentic-workflow/records/000_previous"
        old.mkdir(parents=True)
        (old / "keep.txt").write_text("existing evidence\n")
        self.git("add", ".agentic-workflow")
        self.git("-c", "user.name=Eval Test", "-c", "user.email=eval@example.invalid",
                 "commit", "-qm", "existing execution records")
        # Old records need no traces and may coexist with ignored local records.
        ignored = self.root / ".agentic-workflow/records/ignored"
        ignored.mkdir()
        (ignored / "keep.txt").write_text("ignored evidence\n")
        with (self.root / ".git/info/exclude").open("a") as f:
            f.write("\n/.agentic-workflow/records/ignored/\n")
        result = self.invoke()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.report()["artifacts"]["implementations"], ["001_todolist"])
        # A directory added after the trial also does not belong to its cleanup.
        later = self.root / ".agentic-workflow/records/002_later"
        later.mkdir()
        (later / "keep.txt").write_text("later evidence\n")
        result = self.invoke("clean")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        for directory, text in ((old, "existing evidence\n"), (ignored, "ignored evidence\n"),
                                (later, "later evidence\n")):
            self.assertEqual((directory / "keep.txt").read_text(), text)
        self.assertFalse((self.root / ".agentic-workflow/records/001_todolist").exists())
        self.assertFalse(self.results.exists())

    def test_unauthenticated_launch_rejected_before_creating_results(self):
        result = self.invoke(mode="unauthenticated")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not authenticated", result.stderr)
        self.assertFalse(self.results.exists())

    def test_existing_traces_cannot_satisfy_missing_new_implementation(self):
        old = self.root / ".agentic-workflow/records/000_previous"
        (old / "reports").mkdir(parents=True)
        (old / "native/session").mkdir(parents=True)
        for name in ("reports/usage.json", "reports/usage.md", "reports/timeline.json", "native/session/turn.jsonl"):
            (old / name).touch()
        with (self.root / ".git/info/exclude").open("a") as f:
            f.write("\n/.agentic-workflow/records/000_previous/\n")
        result = self.invoke(mode="no_implementation")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(self.report()["artifacts"]["status"], "FAIL")
        self.assertEqual(self.report()["artifacts"]["implementations"], [])
        self.assertEqual(self.invoke("clean").returncode, 0)
        self.assertTrue((old / "native/session/turn.jsonl").is_file())

    def test_launch_error_is_distinct_from_failed_assertion(self):
        # Exclude the host's real Codex so the disappeared fixture cannot fall back.
        self.env["PATH"] = str(self.bin)
        (self.bin / "git").symlink_to(shutil.which("git"))
        result = self.invoke(mode="launch_error")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(self.report()["overall"], "RUNNER_ERROR")
        self.assertEqual(self.report()["agent"]["status"], "RUNNER_ERROR")
        self.assertTrue((self.results / "run.json").is_file())

    def test_cli_negative_controls(self):
        for mode in ("wrong_output", "no_newline", "crlf", "cli_nonzero", "wrong_storage"):
            with self.subTest(mode=mode):
                result = self.invoke(mode=mode)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                report = self.report()
                self.assertEqual(report["cli"]["status"], "FAIL")
                self.assertEqual(report["agent"]["status"], "PASS")
                self.assertEqual(report["artifacts"]["status"], "PASS")
                self.assertTrue((self.results / "cli-01.stdout").is_file())
                self.assertEqual(self.invoke("clean").returncode, 0)

    def test_artifact_negative_controls(self):
        for mode in ("missing_artifacts", "artifact_directory", "multiple_implementations"):
            with self.subTest(mode=mode):
                result = self.invoke(mode=mode)
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                report = self.report()
                self.assertEqual(report["artifacts"]["status"], "FAIL")
                self.assertEqual(report["cli"]["status"], "PASS")
                if mode == "missing_artifacts":
                    self.assertEqual(len(report["artifacts"]["missing"]), 4)
                    self.assertFalse((self.root / ".agentic-workflow/records/001_todolist/reports/usage.json").exists())
                self.assertEqual(self.invoke("clean").returncode, 0)

    def test_nonzero_agent_exit_fails_independently(self):
        result = self.invoke(mode="agent_nonzero")
        self.assertEqual(result.returncode, 1)
        report = self.report()
        self.assertEqual(report["agent"]["returncode"], 9)
        self.assertEqual(report["cli"]["status"], "PASS")
        self.assertEqual(report["artifacts"]["status"], "PASS")

    def test_timeouts_kill_descendants_and_preserve_results(self):
        for mode, flag, grade in (("agent_timeout", "--agent-timeout", "agent"),
                                  ("cli_timeout", "--command-timeout", "cli")):
            with self.subTest(mode=mode):
                result = self.invoke("run", flag, "0.5", mode=mode)
                self.assertEqual(result.returncode, 124, result.stdout + result.stderr)
                self.assertEqual(self.report()[grade]["status"], "TIMEOUT")
                self.assertTrue((self.results / "ready").exists())
                time.sleep(1.6)
                self.assertFalse((self.results / "leaked-child").exists())
                self.assertEqual(self.invoke("clean").returncode, 0)

    def test_interrupts_kill_group_and_save_partial_evidence(self):
        for sig in (signal.SIGINT, signal.SIGTERM):
            with self.subTest(signal=sig):
                process = subprocess.Popen([sys.executable, "evals/todolist.py", "run"],
                                           cwd=self.root, env=dict(self.env, EVAL_FIXTURE="interrupt"),
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                try:
                    deadline = time.monotonic() + 5
                    while not (self.results / "ready").exists() and time.monotonic() < deadline:
                        time.sleep(0.01)
                    self.assertTrue((self.results / "ready").exists())
                    process.send_signal(sig)
                    out, err = process.communicate(timeout=5)
                    self.assertEqual(process.returncode, 128 + sig, out + err)
                    self.assertEqual(self.report()["agent"]["status"], "INTERRUPTED")
                    self.assertEqual(self.report()["cli"]["status"], "NOT_RUN")
                    time.sleep(1.6)
                    self.assertFalse((self.results / "leaked-child").exists())
                finally:
                    if process.poll() is None:
                        process.kill()
                        process.communicate()
                self.assertEqual(self.invoke("clean").returncode, 0)

    def test_cleanup_requires_run_and_leaves_unexpected_changes(self):
        self.assertEqual(self.invoke("clean").returncode, 2)
        run = self.invoke(mode="unexpected_changes")
        self.assertEqual(run.returncode, 0)
        self.assertIn("Unexpected changes retained", run.stdout)
        self.assertIn("source.txt", self.report()["unexpected_changes"])
        self.assertNotIn("apps/todolist", self.report()["unexpected_changes"])
        result = self.invoke("clean")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Unexpected changes retained", result.stdout)
        self.assertEqual((self.root / "source.txt").read_text(), "unexpected tracked modification\n")
        self.assertTrue((self.root / "unrelated").exists())
        for path in ("apps/todolist", ".agentic-workflow/records/001_todolist", ".agentic-workflow/evals/todolist"):
            self.assertFalse((self.root / path).exists())

    def test_cleanup_refuses_any_tracked_output_before_deleting(self):
        self.assertEqual(self.invoke().returncode, 0)
        for name in ("apps/todolist/todo.py", ".agentic-workflow/records/001_todolist/reports/usage.json", ".agentic-workflow/evals/todolist/run.json"):
            with self.subTest(path=name):
                self.git("add", "-f", name)
                result = self.invoke("clean")
                self.assertEqual(result.returncode, 2)
                self.assertIn("tracked files", result.stderr)
                self.assertTrue((self.results / "run.json").is_file())
                self.assertTrue((self.root / "apps/todolist").is_dir())
                self.git("rm", "--cached", "--", name)

    def test_cleanup_protects_head_files_even_when_staged_for_deletion(self):
        self.assertEqual(self.invoke().returncode, 0)
        name = "apps/todolist/todo.py"
        self.git("add", name)
        self.git("-c", "user.name=Eval Test", "-c", "user.email=eval@example.invalid",
                 "commit", "-qm", "track app")
        self.git("rm", "--cached", "--", name)
        result = self.invoke("clean")
        self.assertEqual(result.returncode, 2)
        self.assertIn("tracked files", result.stderr)
        self.assertTrue((self.root / name).is_file())
        self.assertTrue(self.results.exists())

    def test_cleanup_does_not_follow_symlinked_parent(self):
        self.assertEqual(self.invoke().returncode, 0)
        (self.root / "apps").rename(self.base / "external-apps")
        (self.root / "apps").symlink_to(self.base / "external-apps", target_is_directory=True)
        result = self.invoke("clean")
        self.assertEqual(result.returncode, 2)
        self.assertIn("symlink", result.stderr)
        self.assertTrue((self.base / "external-apps/todolist/todo.py").is_file())
        self.assertTrue(self.results.exists())

    def test_make_eval_uses_clean_head_and_preserves_dirty_source_checkout(self):
        (self.root / "source.txt").write_text("staged edit\n")
        self.git("add", "source.txt")
        (self.root / "source.txt").write_text("unstaged edit\n")
        (self.root / "untracked.txt").write_text("keep untracked\n")
        existing_app = self.root / "apps/todolist"
        existing_app.mkdir(parents=True)
        (existing_app / "keep.txt").write_text("existing app\n")
        self.results.mkdir(parents=True)
        (self.results / "keep.txt").write_text("previous eval\n")
        before = (self.git("status", "--porcelain"), self.git("diff", "--cached"), self.git("rev-parse", "HEAD"))
        result = subprocess.run(["make", "eval"], cwd=self.root, env=self.env,
                                capture_output=True, text=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Eval: PASS", result.stdout)
        archived, = (self.root / ".agentic-workflow/evals/todolist-worktrees").iterdir()
        summary = json.loads((archived / "worktree.json").read_text())
        launch = json.loads((archived / "run.json").read_text())
        self.assertTrue(summary["worktree_removed"])
        self.assertTrue(Path(summary["worktree"]).is_relative_to(self.root / ".agentic-workflow/tmp/worktrees"))
        self.assertFalse(Path(summary["worktree"]).exists())
        self.assertEqual(launch["git_status_before"], "")
        self.assertFalse(launch["allow_dirty"])
        self.assertEqual((archived / "fixture-source.txt").read_text(), "original\n")
        self.assertTrue((archived / "app/todo.py").is_file())
        self.assertTrue((archived / "records/001_todolist/native/session/turn.jsonl").is_file())
        self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 1)
        self.assertEqual((self.git("status", "--porcelain"), self.git("diff", "--cached"),
                          self.git("rev-parse", "HEAD")), before)
        self.assertEqual((existing_app / "keep.txt").read_text(), "existing app\n")
        self.assertEqual((self.results / "keep.txt").read_text(), "previous eval\n")

    def test_make_eval_reports_failures_and_archives_each_run_before_cleanup(self):
        for mode, status, code in (("wrong_output", "FAIL", 1), ("unauthenticated", "RUNNER_ERROR", 2),
                                   ("agent_timeout", "TIMEOUT", 124)):
            with self.subTest(mode=mode):
                archive_root = self.root / ".agentic-workflow/evals/todolist-worktrees"
                before = set(archive_root.iterdir()) if archive_root.exists() else set()
                result = subprocess.run(["make", "eval", "EVAL_AGENT_TIMEOUT=0.5"], cwd=self.root,
                                        env=dict(self.env, EVAL_FIXTURE=mode),
                                        capture_output=True, text=True, timeout=15)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn(f"Eval: {status}", result.stdout)
                archived, = set(archive_root.iterdir()) - before
                summary = json.loads((archived / "worktree.json").read_text())
                self.assertEqual(summary["exit_code"], code)
                self.assertTrue(summary["worktree_removed"])
                self.assertFalse(Path(summary["worktree"]).exists())
                if mode == "wrong_output":
                    self.assertEqual(json.loads((archived / "result.json").read_text())["cli"]["status"], "FAIL")
                    self.assertEqual((archived / "cli-01.stdout").read_text(), "Wrong output\n")
                self.assertEqual(self.git("worktree", "list", "--porcelain").count("worktree "), 1)
                self.assertEqual(self.git("status", "--porcelain"), "")


if __name__ == "__main__":
    unittest.main()
