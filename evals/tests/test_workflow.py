"""Workflow judge command contract; only the paid model boundary is substituted."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[2]


class WorkflowReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="workflow judge ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        (self.root / "evals").mkdir()
        for name in ("workflow.py", "todolist.py"):
            shutil.copyfile(SOURCE / "evals" / name, self.root / "evals" / name)
        shutil.copyfile(SOURCE / "Makefile", self.root / "Makefile")
        shutil.copytree(SOURCE / "agentic-workflow", self.root / "agentic-workflow",
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        shutil.copyfile(SOURCE / "AGENTS.md", self.root / "AGENTS.md")
        shutil.copytree(SOURCE / ".agents/skills", self.root / ".agents/skills")
        binary = self.base / "bin/codex"
        binary.parent.mkdir()
        binary.write_text(f"#!{sys.executable}\n" + (SOURCE / "evals/tests/fixtures/judge.py").read_text())
        binary.chmod(0o755)
        self.calls = self.base / "calls.jsonl"
        self.env = dict(os.environ, PATH=f"{binary.parent}:{os.environ['PATH']}", JUDGE_CALLS=str(self.calls))

    def response(self, *statuses):
        return json.dumps({
            "scope": "Package and installed entry points against WORKFLOW.md",
            "excluded_inputs": ["Project memory and app artifacts"],
            "checks": [{"contract": f"Contract {index}", "status": status,
                        "evidence": f"roles/IMPLEMENTER.md:8 | finding {index}\nReading path"}
                       for index, status in enumerate(statuses)],
        })

    def invoke(self, response, *, make=False, **environment):
        env = dict(self.env, **environment)
        if response is not None:
            env["JUDGE_RESPONSE"] = response
        command = (["make", "-f", str(self.root / "Makefile"), "validate-workflow"] if make else
                   [sys.executable, "-B", "evals/workflow.py", "--timeout", "0.2" if "JUDGE_SLEEP" in env else "10"])
        return subprocess.run(command, cwd=self.base if make else self.root, env=env,
                              capture_output=True, text=True, timeout=15)

    def reports(self):
        return sorted((self.root / ".evals/workflow").glob("review-*"))

    def test_make_runs_one_read_only_pass_on_current_inputs_and_retains_report(self):
        contract = self.root / "agentic-workflow/WORKFLOW.md"
        contract.write_text(contract.read_text() + "\nUncommitted requirement.\n")
        before = contract.read_bytes()
        for relative in (".agents/memory/index.md", ".agentic-workflow/001_old/result.md", "apps/app.py"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Excluded input")
        result = self.invoke(self.response("PASS"), make=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        calls = [json.loads(line) for line in self.calls.read_text().splitlines()]
        self.assertEqual(len(calls), 1)
        args = calls[0]["args"]
        self.assertEqual(args[0], "exec")
        self.assertEqual(args[args.index("--sandbox") + 1], "read-only")
        self.assertIn("project_doc_max_bytes=0", args)
        self.assertIn("memories.use_memories=false", args)
        self.assertIn("agentic-workflow/WORKFLOW.md", args[-1])
        self.assertIn("agentic-workflow/guides/WORKFLOW_REVIEW.md", args[-1])
        directory, = self.reports()
        inputs = directory / "inputs"
        self.assertEqual(Path(calls[0]["cwd"]), inputs)
        self.assertEqual((inputs / "agentic-workflow/WORKFLOW.md").read_bytes(), before)
        self.assertEqual(contract.read_bytes(), before)
        self.assertTrue((inputs / ".agents/skills/agentic-workflow-planner/SKILL.md").is_file())
        self.assertFalse((inputs / ".agents/memory").exists())
        self.assertFalse((inputs / ".agentic-workflow/001_old").exists())
        self.assertFalse((inputs / "apps").exists())
        self.assertIn("Workflow review: PASS", result.stdout)
        report = (directory / "report.md").read_text()
        self.assertIn("| Step/contract | Status | Evidence or finding |", report)
        self.assertIn("\\| finding 0<br>Reading path", report)
        self.assertIn("judge fixture stderr", (directory / "agent.stderr").read_text())
        self.assertEqual(json.loads((directory / "result.json").read_text())["status"], "PASS")

    def test_verdict_precedence_and_exit_status(self):
        for statuses, expected in ((["PASS", "UNCLEAR"], "UNCLEAR"),
                                   (["UNCLEAR", "FAIL", "PASS"], "FAIL")):
            with self.subTest(expected=expected):
                before = set(self.reports())
                result = self.invoke(self.response(*statuses))
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                directory, = set(self.reports()) - before
                self.assertEqual(json.loads((directory / "result.json").read_text())["status"], expected)
                self.assertIn(f"Workflow review: {expected}", (directory / "report.md").read_text())
        self.assertEqual(len(self.reports()), 2)
        self.assertEqual(len(self.calls.read_text().splitlines()), 2)

    def test_unusable_response_or_failed_judge_never_passes_or_retries(self):
        for response, environment in ((None, {}), ("not JSON", {}), ("[]", {}),
                                      (self.response(), {}), (self.response("UNKNOWN"), {}),
                                      (self.response("PASS"), {"JUDGE_EXIT": "9"})):
            with self.subTest(response=response, environment=environment):
                before = set(self.reports())
                result = self.invoke(response, **environment)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                directory, = set(self.reports()) - before
                self.assertNotEqual(json.loads((directory / "result.json").read_text())["status"], "PASS")
                self.assertTrue((directory / "events.jsonl").is_file())
                self.assertFalse((directory / "report.md").exists())
        self.assertEqual(len(self.calls.read_text().splitlines()), 6)

    def test_timeout_retains_evidence_without_retry(self):
        result = self.invoke(None, JUDGE_SLEEP="20")
        self.assertEqual(result.returncode, 124, result.stdout + result.stderr)
        directory, = self.reports()
        self.assertEqual(json.loads((directory / "result.json").read_text())["status"], "TIMEOUT")
        self.assertIn("fixture.started", (directory / "events.jsonl").read_text())
        self.assertEqual(len(self.calls.read_text().splitlines()), 1)

    def test_project_reviewer_route_replaces_defaults_and_invalid_route_stops_launch(self):
        override = self.root / ".agentic-workflow/MODELS.md"
        override.parent.mkdir()
        override.write_text("## Profiles\n| judge | judge-model | medium |\n"
                            "## Role routes\n| Reviewer | judge | judge |\n")
        result = self.invoke(self.response("PASS"))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        args = json.loads(self.calls.read_text().splitlines()[0])["args"]
        self.assertEqual(args[args.index("--model") + 1], "judge-model")
        self.assertIn('model_reasoning_effort="medium"', args)
        override.write_text("## Profiles\n")
        result = self.invoke(self.response("PASS"))
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("Missing Reviewer default route", result.stderr)
        self.assertEqual(len(self.calls.read_text().splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
