"""CLI contracts for report-only specification reviews; no paid model calls."""

import json
from pathlib import Path
import shutil

from review_support import DocumentReviewFixture, SOURCE


class SpecificationReviewTests(DocumentReviewFixture):
    runner = "specs"

    def setUp(self):
        super().setUp()
        shutil.copytree(SOURCE / "specs", self.root / "specs")

    def test_all_bundles_and_each_judgment_report_once_without_edits(self):
        before_sources = self.project_files()
        for statuses, expected in ((("PASS",), "PASS"), (("FAIL",), "FAIL"),
                                   (("UNCLEAR",), "UNCLEAR"), (("UNCLEAR", "FAIL"), "FAIL")):
            with self.subTest(statuses=statuses):
                before = set(self.reports())
                count = len(self.calls.read_text().splitlines()) if self.calls.exists() else 0
                process = self.invoke(self.response(*statuses), make=expected == "PASS")
                self.assertEqual(process.returncode, 0 if expected == "PASS" else 1, process.stdout + process.stderr)
                directory, = set(self.reports()) - before
                final = json.loads((directory / "result.json").read_text())
                self.assertEqual(final["status"], expected)
                self.assertEqual(final["requested_settings"], {"model": "gpt-6-astra", "reasoning": "medium"})
                self.assertEqual(final["bundles"], ["specs/todolist", "specs/todolist_rust"])
                self.assertIn(f"Specification review: {expected}", (directory / "report.md").read_text())
                for filename in ("prompt.txt", "schema.json", "run.json", "judgment.json", "events.jsonl", "agent.stderr"):
                    self.assertTrue((directory / filename).is_file(), filename)
                calls = [json.loads(line) for line in self.calls.read_text().splitlines()[count:]]
                call, = calls
                self.assertEqual(call["args"][call["args"].index("--sandbox") + 1], "read-only")
                self.assertEqual(Path(call["cwd"]), directory / "inputs")
                self.assertEqual(self.project_files(), before_sources)

    def test_selected_bundle_current_files_and_linked_interfaces_are_snapshotted(self):
        project = self.root / "specs/todolist/project.md"
        project.write_text(project.read_text() + "\nUncommitted requirement. See [source][required].\n\n[required]: ../../sources/requirements.md\n")
        source = self.root / "sources/requirements.md"
        source.parent.mkdir()
        source.write_text("[Required interface](interface.py)\n")
        interface = source.with_name("interface.py")
        interface.write_text("def task_operation(text: str) -> int: ...\n")
        for name in ("apps/todolist/output.py", ".agentic-workflow/memory/index.md", ".agentic-workflow/records/001_old/result.md"):
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Excluded evidence")
        before = self.project_files()
        process = self.invoke(self.response("PASS"), arguments=["--bundle", "specs/todolist", "--model", "chosen-model", "--reasoning", "high", "--timeout", "9"])
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        directory, = self.reports()
        inputs = directory / "inputs"
        for relative in ("specs/todolist/project.md", "sources/requirements.md", "sources/interface.py",
                         "agentic-workflow/templates/tasks/task.md", "agentic-workflow/templates/contracts/contract.md",
                         "agentic-workflow/policies/BUNDLE.md", "agentic-workflow/policies/DOCUMENT_STYLE.md"):
            self.assertEqual((inputs / relative).read_bytes(), before[relative])
        for relative in ("specs/todolist_rust", "apps", ".agentic-workflow"):
            self.assertFalse((inputs / relative).exists(), relative)
        run = json.loads((directory / "run.json").read_text())
        self.assertEqual(run["requested_settings"], {"model": "chosen-model", "reasoning": "high"})
        self.assertEqual(run["timeout_seconds"], 9)
        self.assertEqual(self.project_files(), before)

    def test_make_selection_and_settings(self):
        process = self.invoke(self.response("PASS"), make=True, arguments=["SPEC_BUNDLE=specs/todolist_rust",
                              "SPECS_MODEL=chosen-model", "SPECS_REASONING=low", "SPECS_TIMEOUT=8"])
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        directory, = self.reports()
        final = json.loads((directory / "result.json").read_text())
        self.assertEqual(final["bundles"], ["specs/todolist_rust"])
        call, = [json.loads(line) for line in self.calls.read_text().splitlines()]
        self.assertEqual(call["args"][call["args"].index("--model") + 1], "chosen-model")
        self.assertIn('model_reasoning_effort="low"', call["args"])
        self.assertFalse((directory / "inputs/specs/todolist").exists())
        self.assertEqual(json.loads((directory / "run.json").read_text())["timeout_seconds"], 8)

    def test_invalid_or_empty_selection_never_invokes_model(self):
        (self.root / "specs/empty").mkdir()
        (self.root / "specs/alias").symlink_to(self.root / "specs/todolist", target_is_directory=True)
        for bundle in ("specs/missing", "specs/empty", "specs/alias", "specs/todolist/project.md", "specs", "agentic-workflow", ""):
            with self.subTest(bundle=bundle):
                process = self.invoke(self.response("PASS"), arguments=["--bundle", bundle])
                self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
                self.assertIn("RUNNER_ERROR", process.stderr)
        shutil.rmtree(self.root / "specs")
        for exists in (False, True):
            if exists:
                (self.root / "specs").mkdir()
            process = self.invoke(self.response("PASS"))
            self.assertEqual(process.returncode, 2, process.stdout + process.stderr)
        self.assertFalse(self.calls.exists())
        self.assertTrue(all(json.loads((directory / "result.json").read_text())["status"] == "RUNNER_ERROR"
                            for directory in self.reports()))

    def test_missing_or_excluded_review_references_prevent_false_pass(self):
        project = self.root / "specs/todolist/project.md"
        original = project.read_text()
        cases = (("missing source", "[Required source](../../sources/missing.md)"),
                 ("excluded history", "[Required source](../../.agentic-workflow/memory/index.md)"),
                 ("outside root", "[Required source](../../../outside.md)"),
                 ("missing template", ""))
        for name, link in cases:
            with self.subTest(name=name):
                project.write_text(original + "\n" + link)
                if name == "missing template":
                    (self.root / "agentic-workflow/templates/verification.md").unlink()
                before = set(self.reports())
                process = self.invoke(self.response("PASS"), arguments=["--bundle", "specs/todolist"])
                self.assertEqual(process.returncode, 1, process.stdout + process.stderr)
                directory, = set(self.reports()) - before
                result = json.loads((directory / "result.json").read_text())
                self.assertEqual(result["status"], "UNCLEAR")
                self.assertTrue(result["excluded_inputs"])
                self.assertIn("provide the required reference", (directory / "report.md").read_text())
