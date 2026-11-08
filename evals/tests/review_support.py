"""Shared external model fixture and disposable document-review checkout."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[2]


class DocumentReviewFixture(unittest.TestCase):
    runner = "workflow"

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="workflow judge ")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / "repo"
        self.root.mkdir()
        (self.root / "evals").mkdir()
        for name in ("workflow.py", "specs.py", "spec_inputs.py", "document_review.py", "runtime.py"):
            shutil.copyfile(SOURCE / "evals" / name, self.root / "evals" / name)
        shutil.copyfile(SOURCE / "Makefile", self.root / "Makefile")
        shutil.copyfile(SOURCE / "evals/README.md", self.root / "evals/README.md")
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
        command = (["make", "-f", str(self.root / "Makefile"), f"eval-{self.runner}"] if make else
                   [sys.executable, "-B", f"evals/{self.runner}.py", "--timeout",
                    "0.2" if any(key.endswith("_SLEEP") for key in environment) else "10"])
        command.extend(arguments)
        return subprocess.run(command, cwd=self.base if make else self.root, env=env,
                              capture_output=True, text=True, timeout=15)

    def reports(self):
        return sorted((self.root / f".agentic-workflow/evals/{self.runner}").glob("review-*"))

    def project_files(self):
        return {str(path.relative_to(self.root)): path.read_bytes()
                for path in self.root.rglob("*")
                if path.is_file() and not path.is_relative_to(self.root / ".agentic-workflow/evals")}
