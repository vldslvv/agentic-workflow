"""Workflow review and optional repair through the public command boundary."""

import json
import shutil
from pathlib import Path

from evals.tests.review_support import SOURCE, DocumentReviewFixture


class WorkflowReviewTests(DocumentReviewFixture):
    def test_default_review_and_passing_opt_in_never_edit(self) -> None:
        contract = self.root / "agentic-workflow/WORKFLOW.md"
        contract.write_text(contract.read_text() + "\nUncommitted requirement.\n")
        for relative in (
            ".agentic-workflow/memory/index.md",
            ".agentic-workflow/records/001_old/result.md",
            "apps/app.py",
        ):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Excluded input")
        before_sources = self.project_files()
        cases = (
            (False, ("PASS",), "PASS"),
            (False, ("FAIL",), "FAIL"),
            (True, ("PASS",), "PASS"),
            (False, ("PASS", "FAIL"), "FAIL"),
        )
        for repair, statuses, expected in cases:
            with self.subTest(repair=repair, statuses=statuses):
                before = set(self.reports())
                process = self.invoke(
                    self.response(*statuses),
                    make=not repair and expected == "PASS",
                    arguments=["--repair"] if repair else [],
                )
                self.assertEqual(process.returncode, 0 if expected == "PASS" else 1)
                (directory,) = set(self.reports()) - before
                result = json.loads((directory / "result.json").read_text())
                self.assertEqual(result["status"], expected)
                self.assertEqual(result["review"]["status"], expected)
                self.assertIn(f"Workflow eval: {expected}", process.stdout)
                for index, status in enumerate(statuses):
                    self.assertIn(
                        f"- [{status}] Contract {index}\n"
                        f"  roles/IMPLEMENTER.md:8 | finding {index}\n  Reading path",
                        process.stdout,
                    )
                if repair:
                    self.assertEqual(result["repair"]["status"], "NOT_RUN")
                else:
                    self.assertNotIn("repair", result)
                inputs = directory / "inputs"
                self.assertEqual(
                    (inputs / "agentic-workflow/WORKFLOW.md").read_bytes(), contract.read_bytes()
                )
                self.assertTrue(
                    (inputs / ".agents/skills/agentic-workflow-planner/SKILL.md").is_file()
                )
                for relative in (".agentic-workflow/memory", ".agentic-workflow/records", "apps"):
                    self.assertFalse((inputs / relative).exists())
                call = json.loads(self.calls.read_text().splitlines()[-1])
                args = call["args"]
                self.assertEqual(args[args.index("--model") + 1], "gpt-6-astra")
                self.assertIn('model_reasoning_effort="medium"', args)
                self.assertEqual(
                    json.loads((directory / "run.json").read_text())["requested_settings"],
                    {"model": "gpt-6-astra", "reasoning": "medium"},
                )
                self.assertEqual(call["prompt"], (directory / "prompt.txt").read_text())
                self.assertIn("agentic-workflow/WORKFLOW.md", call["prompt"])
                self.assertIn("agentic-workflow/guides/WORKFLOW_REVIEW.md", call["prompt"])
                self.assertEqual(self.project_files(), before_sources)
        self.assertEqual(len(self.calls.read_text().splitlines()), len(cases))

    def test_review_errors_and_timeouts_preserve_evidence_without_retry(self) -> None:
        cases = [
            (None, {}, "RUNNER_ERROR", 2),
            ("not JSON", {}, "RUNNER_ERROR", 2),
            ("[]", {}, "RUNNER_ERROR", 2),
            (self.response(), {}, "RUNNER_ERROR", 2),
            (self.response("UNCLEAR"), {}, "RUNNER_ERROR", 2),
            (self.response("PASS"), {"JUDGE_EXIT": "9"}, "JUDGE_ERROR", 2),
            (self.response("PASS"), {"JUDGE_SLEEP": "20"}, "TIMEOUT", 124),
        ]
        for response, environment, status, code in cases:
            with self.subTest(status=status, response=response):
                before = set(self.reports())
                process = self.invoke(response, arguments=["--repair"], make=False, **environment)
                self.assertEqual(process.returncode, code, process.stdout + process.stderr)
                (directory,) = set(self.reports()) - before
                result = json.loads((directory / "result.json").read_text())
                self.assertEqual(result["status"], status)
                self.assertEqual(result["review"]["status"], "NOT_RUN")
                self.assertIn(status, (directory / "report.md").read_text())
                self.assertIn("fixture.started", (directory / "events.jsonl").read_text())
        self.assertEqual(len(self.calls.read_text().splitlines()), len(cases))

    def test_opt_in_repair_preserves_review_and_applies_cli_or_make_settings(self) -> None:
        override = self.root / ".agentic-workflow/config/MODELS.md"
        override.parent.mkdir(parents=True)
        override.write_text("Invalid routing is review input, not launch configuration.\n")
        document = self.root / "AGENTS.md"
        corrected = document.read_text() + "\nKeep this existing local instruction.\n"
        original = corrected.replace("agentic-workflow/policies/GUIDELINES.md", "missing.md")
        for make in (False, True):
            with self.subTest(make=make):
                document.write_text(original)
                before_sources = self.project_files()
                before = set(self.reports())
                arguments = (
                    ["WORKFLOW_REPAIR=1", "WORKFLOW_MODEL=chosen-model", "WORKFLOW_REASONING=high"]
                    if make
                    else ["--repair", "--model", "chosen-model", "--reasoning", "high"]
                )
                response = self.response("FAIL")
                process = self.invoke(
                    response,
                    make=make,
                    arguments=arguments,
                    EDITOR_RESPONSE=json.dumps(
                        {"status": "PASS", "summary": "Restored guideline link."}
                    ),
                    EDITOR_EDITS=json.dumps({"AGENTS.md": corrected}),
                )
                self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
                before_sources["AGENTS.md"] = corrected.encode()
                self.assertEqual(self.project_files(), before_sources)
                (directory,) = set(self.reports()) - before
                result = json.loads((directory / "result.json").read_text())
                self.assertEqual(
                    (result["status"], result["review"]["status"], result["repair"]["status"]),
                    ("PASS", "FAIL", "PASS"),
                )
                self.assertEqual(result["repair"]["checks"]["status"], "PASS")
                self.assertEqual((directory / "judgment.json").read_text(), response)
                self.assertEqual((directory / "inputs/AGENTS.md").read_text(), original)
                report = (directory / "report.md").read_text()
                for text in (
                    "Workflow eval: PASS",
                    "Original review: FAIL",
                    "Repair: PASS",
                    "No independent re-review occurred",
                ):
                    self.assertIn(text, report)
                    self.assertIn(text, process.stdout)
                self.assertIn("Restored guideline link.", process.stdout)
                self.assertIn("Package checks: PASS", process.stdout)
                calls = [json.loads(line) for line in self.calls.read_text().splitlines()[-2:]]
                for call, evidence, cwd, sandbox in (
                    (calls[0], directory, directory / "inputs", "read-only"),
                    (calls[1], directory / "repair", self.root, "workspace-write"),
                ):
                    self.assertEqual(call["prompt"], (evidence / "prompt.txt").read_text())
                    self.assertEqual(
                        call["schema"], json.loads((evidence / "schema.json").read_text())
                    )
                    self.assertEqual(Path(call["cwd"]), cwd)
                    args = call["args"]
                    self.assertEqual(args[args.index("--sandbox") + 1], sandbox)
                    self.assertEqual(args[args.index("--model") + 1], "chosen-model")
                    self.assertIn('model_reasoning_effort="high"', args)
                    self.assertEqual(
                        json.loads((evidence / "run.json").read_text())["requested_settings"],
                        {"model": "chosen-model", "reasoning": "high"},
                    )
                self.assertEqual(
                    calls[1]["schema"]["properties"]["status"]["enum"], ["PASS", "FAIL"]
                )
                self.assertIn(str(directory / "inputs"), calls[1]["prompt"])
                self.assertIn(str(directory / "judgment.json"), calls[1]["prompt"])
        self.assertEqual(len(self.calls.read_text().splitlines()), 4)

    def test_unsuccessful_repairs_keep_partial_edits_and_original_failure(self) -> None:
        fixed = json.dumps({"status": "PASS", "summary": "Corrected findings."})
        cases = [
            ("missing output", None, {}, 2, "RUNNER_ERROR"),
            ("malformed output", "not JSON", {}, 2, "RUNNER_ERROR"),
            ("wrong shape", "[]", {}, 2, "RUNNER_ERROR"),
            (
                "invalid status",
                json.dumps({"status": "UNCLEAR", "summary": "Done"}),
                {},
                2,
                "RUNNER_ERROR",
            ),
            (
                "empty summary",
                json.dumps({"status": "PASS", "summary": ""}),
                {},
                2,
                "RUNNER_ERROR",
            ),
            (
                "unresolved",
                json.dumps(
                    {"status": "FAIL", "summary": "Finding remains; provide the missing reference."}
                ),
                {},
                1,
                "FAIL",
            ),
            ("editor failed", fixed, {"EDITOR_EXIT": "9"}, 2, "REPAIR_ERROR"),
            ("timeout", fixed, {"EDITOR_SLEEP": "20"}, 124, "TIMEOUT"),
            ("broken integration", fixed, {"AGENTS.md": "Broken entry point\n"}, 1, "FAIL"),
            (
                "changed contract",
                fixed,
                {
                    "agentic-workflow/WORKFLOW.md": (
                        SOURCE / "agentic-workflow/WORKFLOW.md"
                    ).read_text()
                    + "\nChanged contract\n"
                },
                1,
                "FAIL",
            ),
        ]
        for name, response, options, code, status in cases:
            with self.subTest(case=name):
                edits = {
                    "agentic-workflow/README.md": (
                        SOURCE / "agentic-workflow/README.md"
                    ).read_text()
                    + f"\nPartial edit: {name}\n"
                }
                environment = {
                    key: value for key, value in options.items() if key.startswith("EDITOR_")
                }
                edits.update(
                    {key: value for key, value in options.items() if not key.startswith("EDITOR_")}
                )
                environment["EDITOR_EDITS"] = json.dumps(edits)
                if response is not None:
                    environment["EDITOR_RESPONSE"] = response
                before = set(self.reports())
                process = self.invoke(
                    self.response("FAIL"), arguments=["--repair"], make=False, **environment
                )
                self.assertEqual(process.returncode, code, process.stdout + process.stderr)
                (directory,) = set(self.reports()) - before
                result = json.loads((directory / "result.json").read_text())
                self.assertEqual(result["status"], status)
                self.assertEqual(result["review"]["status"], "FAIL")
                self.assertEqual(result["repair"]["status"], status)
                self.assertTrue(result["partial_edits_may_remain"])
                self.assertIn("partial edits may remain", (directory / "report.md").read_text())
                if name == "broken integration":
                    self.assertEqual(result["repair"]["checks"]["status"], "FAIL")
                if name == "changed contract":
                    self.assertFalse(result["repair"]["source_contract_unchanged"])
                    self.assertEqual(result["repair"]["checks"]["status"], "PASS")
                for relative, content in edits.items():
                    self.assertEqual((self.root / relative).read_text(), content)
                    shutil.copyfile(SOURCE / relative, self.root / relative)
        self.assertEqual(len(self.calls.read_text().splitlines()), 2 * len(cases))
