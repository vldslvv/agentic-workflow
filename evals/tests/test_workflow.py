"""Workflow validation contract; only the paid model boundary is substituted."""
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

    def invoke(self, response, *, make=False, arguments=(), **environment):
        env = dict(self.env, **environment)
        if response is not None:
            env["JUDGE_RESPONSE"] = response
        command = (["make", "-f", str(self.root / "Makefile"), "eval-workflow"] if make else
                   [sys.executable, "-B", "evals/workflow.py", "--timeout",
                    "0.2" if any(key.endswith("_SLEEP") for key in environment) else "10"])
        command.extend(arguments)
        return subprocess.run(command, cwd=self.base if make else self.root, env=env,
                              capture_output=True, text=True, timeout=15)

    def reports(self):
        return sorted((self.root / ".evals/workflow").glob("review-*"))

    def project_files(self):
        return {str(path.relative_to(self.root)): path.read_bytes()
                for path in self.root.rglob("*")
                if path.is_file() and ".evals" not in path.relative_to(self.root).parts}

    def test_make_runs_one_read_only_pass_on_current_inputs_and_retains_report(self):
        contract = self.root / "agentic-workflow/WORKFLOW.md"
        contract.write_text(contract.read_text() + "\nUncommitted requirement.\n")
        before = contract.read_bytes()
        for relative in (".agents/memory/index.md", ".agentic-workflow/001_old/result.md", "apps/app.py"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Excluded input")
        project_before = self.project_files()
        result = self.invoke(self.response("PASS"), make=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.project_files(), project_before)
        calls = [json.loads(line) for line in self.calls.read_text().splitlines()]
        self.assertEqual(len(calls), 1)
        args = calls[0]["args"]
        self.assertEqual(args[0], "exec")
        self.assertEqual(args[args.index("--model") + 1], "gpt-6-astra")
        self.assertIn('model_reasoning_effort="medium"', args)
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

    def test_uncertainty_stops_repairs_even_when_review_also_fails(self):
        project_before = self.project_files()
        for statuses, review_status in ((["PASS", "UNCLEAR"], "UNCLEAR"),
                                        (["UNCLEAR", "FAIL", "PASS"], "FAIL")):
            with self.subTest(review_status=review_status):
                before = set(self.reports())
                result = self.invoke(self.response(*statuses))
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                directory, = set(self.reports()) - before
                self.assertEqual(json.loads((directory / "result.json").read_text())["status"], "UNCLEAR")
                self.assertIn(f"Workflow review: {review_status}", (directory / "report.md").read_text())
                self.assertIn("Workflow review: UNCLEAR", result.stdout)
                self.assertEqual(self.project_files(), project_before)
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
        for role, log, calls in (("JUDGE", "events.jsonl", 1), ("EDITOR", "repair/events.jsonl", 2)):
            with self.subTest(role=role):
                before = set(self.reports())
                call_count = len(self.calls.read_text().splitlines()) if self.calls.exists() else 0
                result = self.invoke(self.response("FAIL"), **{f"{role}_SLEEP": "20"})
                self.assertEqual(result.returncode, 124, result.stdout + result.stderr)
                directory, = set(self.reports()) - before
                self.assertEqual(json.loads((directory / "result.json").read_text())["status"], "TIMEOUT")
                self.assertIn("fixture.started", (directory / log).read_text())
                self.assertEqual(len(self.calls.read_text().splitlines()) - call_count, calls)
                if role == "EDITOR":
                    self.assertIn("partial edits may remain", result.stdout)

    def test_failed_review_repairs_working_files_once_and_checks_integration(self):
        override = self.root / ".agentic-workflow/MODELS.md"
        override.parent.mkdir()
        override.write_text("## Profiles\n| judge | judge-model | medium |\n"
                            "| editor | editor-model | high |\n"
                            "## Role routes\n| Reviewer | judge | judge |\n| Planner | editor | editor |\n")
        relative = "AGENTS.md"
        document = self.root / relative
        corrected = document.read_text() + "\nKeep this existing local instruction.\n"
        original = corrected.replace("agentic-workflow/policies/GUIDELINES.md", "missing.md")
        document.write_text(original)
        project_before = self.project_files()
        response = self.response("FAIL")
        result = self.invoke(response, make=True,
                             EDITOR_RESPONSE=json.dumps({"status": "FIXED", "summary": "Restored guideline link."}),
                             EDITOR_EDITS=json.dumps({relative: corrected}))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        project_before[relative] = corrected.encode()
        self.assertEqual(self.project_files(), project_before)
        calls = [json.loads(line) for line in self.calls.read_text().splitlines()]
        self.assertEqual(len(calls), 2)
        self.assertEqual(Path(calls[1]["cwd"]), self.root)
        args = calls[1]["args"]
        self.assertEqual(args[args.index("--sandbox") + 1], "workspace-write")
        for call in calls:
            self.assertEqual(call["args"][call["args"].index("--model") + 1], "gpt-6-astra")
            self.assertIn('model_reasoning_effort="medium"', call["args"])
        directory, = self.reports()
        self.assertIn(str(directory / "inputs"), args[-1])
        self.assertIn(str(directory / "judgment.json"), args[-1])
        self.assertEqual((directory / "inputs" / relative).read_text(), original)
        self.assertEqual((directory / "judgment.json").read_text(), response)
        self.assertIn("Workflow review: FAIL", (directory / "report.md").read_text())
        final = json.loads((directory / "result.json").read_text())
        self.assertEqual(final["status"], "FIXED")
        checks = json.loads((directory / "repair/checks.stdout").read_text())
        self.assertEqual(checks["status"], "PASS")
        self.assertIn("editor fixture stderr", (directory / "repair/agent.stderr").read_text())
        self.assertIn("Workflow review: FIXED", result.stdout)
        self.assertIn("No independent re-review occurred", result.stdout)

    def test_failed_or_unclear_repair_and_failed_checks_never_succeed_or_retry(self):
        fixed = json.dumps({"status": "FIXED", "summary": "Corrected findings."})
        unclear = json.dumps({"status": "UNCLEAR", "summary": "One finding is unresolved."})
        cases = [("missing output", None, {}, 2, "RUNNER_ERROR"),
                 ("malformed output", "not JSON", {}, 2, "RUNNER_ERROR"),
                 ("wrong shape", "[]", {}, 2, "RUNNER_ERROR"),
                 ("invalid status", json.dumps({"status": "PASS", "summary": "Done"}), {}, 2, "RUNNER_ERROR"),
                 ("empty summary", json.dumps({"status": "FIXED", "summary": ""}), {}, 2, "RUNNER_ERROR"),
                 ("unresolved finding", unclear, {}, 1, "UNCLEAR"),
                 ("editor failed", fixed, {"EDITOR_EXIT": "9"}, 2, "REPAIR_ERROR"),
                 ("broken integration", fixed, {"EDITOR_EDITS": json.dumps({"AGENTS.md": "Broken entry point\n"})}, 1, "FAIL"),
                 ("changed contract", fixed, {"EDITOR_EDITS": json.dumps({"agentic-workflow/WORKFLOW.md":
                     (SOURCE / "agentic-workflow/WORKFLOW.md").read_text() + "\nChanged contract\n"})}, 1, "FAIL")]
        for name, response, environment, code, status in cases:
            with self.subTest(case=name):
                # Each failed editor leaves a real partial edit; the launcher must retain it.
                edits = {"agentic-workflow/README.md": (SOURCE / "agentic-workflow/README.md").read_text()
                         + f"\nPartial edit: {name}\n"}
                edits.update(json.loads(environment.get("EDITOR_EDITS", "{}")))
                environment["EDITOR_EDITS"] = json.dumps(edits)
                if response is not None:
                    environment["EDITOR_RESPONSE"] = response
                before = set(self.reports())
                call_count = len(self.calls.read_text().splitlines()) if self.calls.exists() else 0
                result = self.invoke(self.response("FAIL"), **environment)
                self.assertEqual(len(self.calls.read_text().splitlines()) - call_count, 2)
                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                directory, = set(self.reports()) - before
                self.assertEqual(json.loads((directory / "result.json").read_text())["status"], status)
                self.assertIn("partial edits may remain", result.stdout)
                for relative, content in edits.items():
                    self.assertEqual((self.root / relative).read_text(), content)
                if name == "broken integration":
                    self.assertIn("Missing or invalid Agentic Workflow block",
                                  (directory / "repair/checks.stdout").read_text())
                if name == "changed contract":
                    self.assertIn("WORKFLOW.md changed", result.stdout)
                    self.assertEqual(json.loads((directory / "repair/checks.stdout").read_text())["status"], "PASS")
                for relative in edits:
                    shutil.copyfile(SOURCE / relative, self.root / relative)

    def test_command_model_settings_apply_to_both_calls_and_evidence(self):
        override = self.root / ".agentic-workflow/MODELS.md"
        override.parent.mkdir()
        override.write_text("Invalid routing remains a review input, not launch configuration.\n")
        cases = ((False, [], "gpt-6-astra", "medium"),
                 (True, ["WORKFLOW_MODEL=chosen-model", "WORKFLOW_REASONING=high"], "chosen-model", "high"),
                 (False, ["--model", "chosen-model", "--reasoning", "low"], "chosen-model", "low"))
        for make, arguments, model, reasoning in cases:
            with self.subTest(make=make, arguments=arguments):
                before = set(self.reports())
                call_count = len(self.calls.read_text().splitlines()) if self.calls.exists() else 0
                result = self.invoke(self.response("FAIL"), make=make, arguments=arguments,
                                     EDITOR_RESPONSE=json.dumps({"status": "FIXED", "summary": "Resolved findings."}))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                calls = [json.loads(line) for line in self.calls.read_text().splitlines()[call_count:]]
                self.assertEqual(len(calls), 2)
                for call in calls:
                    args = call["args"]
                    self.assertEqual(args[args.index("--model") + 1], model)
                    self.assertIn(f'model_reasoning_effort="{reasoning}"', args)
                directory, = set(self.reports()) - before
                for relative in ("run.json", "repair/run.json"):
                    recorded = json.loads((directory / relative).read_text())
                    self.assertEqual(recorded["requested_settings"], {"model": model, "reasoning": reasoning})


if __name__ == "__main__":
    unittest.main()
