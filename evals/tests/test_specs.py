"""Specification review behavior through the public CLI and saved evidence."""

import json
from pathlib import Path
import shutil

from review_support import DocumentReviewFixture


class SpecificationReviewTests(DocumentReviewFixture):
    runner = "specs"

    def setUp(self):
        super().setUp()
        for name in ("alpha", "beta"):
            bundle = self.root / "specs" / name
            bundle.mkdir(parents=True)
            (bundle / "project.md").write_text(f"# {name}\n\nA test-owned specification.\n")

    def test_judgments_preserve_sources_and_report_the_delivered_prompt_and_result(self):
        before_sources = self.project_files()
        for statuses, expected in ((("PASS",), "PASS"), (("FAIL",), "FAIL"),
                                   (("UNCLEAR",), "UNCLEAR"), (("UNCLEAR", "FAIL"), "FAIL")):
            with self.subTest(statuses=statuses):
                before = set(self.reports())
                response = self.response(*statuses)
                process = self.invoke(response, make=expected == "PASS")
                self.assertEqual(process.returncode, 0 if expected == "PASS" else 1, process.stdout + process.stderr)
                directory, = set(self.reports()) - before
                result = json.loads((directory / "result.json").read_text())
                self.assertEqual((result["status"], result["review"]["status"], result["execution"]["status"]),
                                 (expected, expected, "PASS"))
                self.assertEqual(result["bundles"], ["specs/alpha", "specs/beta"])
                self.assertEqual((directory / "judgment.json").read_text(), response)
                report = (directory / "report.md").read_text()
                self.assertIn(f"Specification eval: {expected}", report)
                self.assertIn("\\| finding 0<br>Reading path", report)
                call = json.loads(self.calls.read_text().splitlines()[-1])
                self.assertEqual(call["prompt"], (directory / "prompt.txt").read_text())
                self.assertIn("specs/alpha, specs/beta", call["prompt"])
                self.assertEqual(call["schema"], json.loads((directory / "schema.json").read_text()))
                self.assertEqual(Path(call["cwd"]), directory / "inputs")
                self.assertEqual(call["args"][call["args"].index("--sandbox") + 1], "read-only")
                for setting in ("project_doc_max_bytes=0", "memories.use_memories=false"):
                    self.assertIn(setting, call["args"])
                for filename in ("run.json", "events.jsonl", "agent.stderr"):
                    self.assertTrue((directory / filename).is_file())
                self.assertEqual(self.project_files(), before_sources)
        self.assertEqual(len(self.calls.read_text().splitlines()), 4)

    def test_selected_current_bundle_and_linked_interfaces_with_make_settings(self):
        project = self.root / "specs/alpha/project.md"
        project.write_text("Current requirement. See [source][required].\n\n[required]: ../../sources/requirements.md\n")
        source = self.root / "sources/requirements.md"
        source.parent.mkdir()
        source.write_text("[Required interface](interface.py)\n")
        source.with_name("interface.py").write_text("def task_operation(text: str) -> int: ...\n")
        for name in ("apps/output.py", ".agentic-workflow/memory/index.md", ".agentic-workflow/records/001_old/result.md"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Excluded evidence")
        before = self.project_files()
        process = self.invoke(self.response("PASS"), make=True, arguments=["SPEC_BUNDLE=specs/alpha",
                              "SPECS_MODEL=chosen-model", "SPECS_REASONING=low", "SPECS_TIMEOUT=8"])
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        directory, = self.reports()
        for relative in ("specs/alpha/project.md", "sources/requirements.md", "sources/interface.py",
                         "agentic-workflow/templates/tasks/task.md", "agentic-workflow/policies/BUNDLE.md"):
            self.assertEqual((directory / "inputs" / relative).read_bytes(), before[relative])
        for relative in ("specs/beta", "apps", ".agentic-workflow"):
            self.assertFalse((directory / "inputs" / relative).exists())
        call, = [json.loads(line) for line in self.calls.read_text().splitlines()]
        self.assertEqual(call["args"][call["args"].index("--model") + 1], "chosen-model")
        self.assertIn('model_reasoning_effort="low"', call["args"])
        run = json.loads((directory / "run.json").read_text())
        self.assertEqual(run["requested_settings"], {"model": "chosen-model", "reasoning": "low"})
        self.assertEqual(run["timeout_seconds"], 8)
        self.assertEqual(self.project_files(), before)

    def test_invalid_or_empty_selection_never_invokes_model(self):
        (self.root / "specs/empty").mkdir()
        (self.root / "specs/alias").symlink_to(self.root / "specs/alpha", target_is_directory=True)
        for bundle in ("specs/missing", "specs/empty", "specs/alias", "specs/alpha/project.md", "specs", "agentic-workflow", ""):
            with self.subTest(bundle=bundle):
                process = self.invoke(self.response("PASS"), arguments=["--bundle", bundle])
                self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
                self.assertIn("RUNNER_ERROR", process.stderr)
        shutil.rmtree(self.root / "specs")
        for exists in (False, True):
            if exists:
                (self.root / "specs").mkdir()
            self.assertEqual(self.invoke(self.response("PASS")).returncode, 2)
        self.assertFalse(self.calls.exists())
        self.assertTrue(all(json.loads((directory / "result.json").read_text())["status"] == "RUNNER_ERROR"
                            for directory in self.reports()))

    def test_unavailable_references_prevent_false_pass(self):
        project = self.root / "specs/alpha/project.md"
        cases = (("missing source", "[Source](../../sources/missing.md)"),
                 ("excluded history", "[Source](../../.agentic-workflow/memory/index.md)"),
                 ("outside root", "[Source](../../../outside.md)"), ("missing template", ""))
        for name, link in cases:
            with self.subTest(name=name):
                project.write_text(link)
                if name == "missing template":
                    (self.root / "agentic-workflow/templates/verification.md").unlink()
                before = set(self.reports())
                process = self.invoke(self.response("PASS"), arguments=["--bundle", "specs/alpha"])
                self.assertEqual(process.returncode, 1, process.stdout + process.stderr)
                directory, = set(self.reports()) - before
                result = json.loads((directory / "result.json").read_text())
                self.assertEqual(result["status"], "UNCLEAR")
                self.assertTrue(result["review"]["excluded_inputs"])
                self.assertIn("provide the required reference", (directory / "report.md").read_text())
