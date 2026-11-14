"""Source-repository integration: copy boundary, optional wrappers and host entry points."""

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
import venv
from pathlib import Path
from typing import TypedDict, cast


class PackageResult(TypedDict):
    status: str
    errors: list[str]
    local_links_checked: int


SOURCE = Path(__file__).resolve().parents[1]


class InstallationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="workflow install ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "unrelated project"
        self.root.mkdir()
        self.package = self.root / "agentic-workflow"
        shutil.copytree(
            SOURCE / "agentic-workflow",
            self.package,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        readme = (self.package / "README.md").read_text()
        match = re.search(r"```markdown\n(.*?)\n```", readme, re.S)
        assert match is not None
        self.block = match[1]
        (self.root / "AGENTS.md").write_text(
            "# Host instructions\n[Unrelated](missing-host-file.md)\n\n" + self.block + "\n"
        )
        self.env = {key: value for key, value in os.environ.items() if not key.startswith("PYTHON")}
        self.env.update(
            CODEX_HOME=str(self.root / "no telemetry"), CODEX_THREAD_ID="", OPENCODE_SESSION_ID=""
        )
        environment = Path(self.temp.name) / "isolated-python"
        venv.EnvBuilder(with_pip=False, symlinks=True).create(environment)
        self.python = environment / "bin/python"

    def cli(self, script: str, *args: str | Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                str(self.python),
                "-E",
                "-s",
                "-B",
                str(self.package / "helpers" / script),
                *map(str, args),
            ],
            cwd=self.root,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=15,
        )

    def check(self, code: int = 0) -> PackageResult:
        process = self.cli("check_package.py", "--integration-root", self.root)
        self.assertEqual(process.returncode, code, process.stdout + process.stderr)
        return cast(PackageResult, json.loads(process.stdout))

    def install(self, role: str) -> Path:
        name = f"agentic-workflow-{role}"
        destination = self.root / ".agents/skills" / name
        shutil.copytree(SOURCE / ".agents/skills" / name, destination)
        return destination

    def test_helpers_load_without_development_environment(self) -> None:
        probe = subprocess.run(
            [
                str(self.python),
                "-E",
                "-s",
                "-c",
                "import importlib.util, site; assert importlib.util.find_spec('pip') is None; assert not site.ENABLE_USER_SITE",
            ],
            cwd=self.root,
            env=self.env,
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(probe.returncode, 0, probe.stderr)
        for script in ("check_package.py", "records.py", "usage_report.py", "trace_view.py"):
            with self.subTest(script=script):
                result = self.cli(script, "--help")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("usage:", result.stdout)

    def test_optional_skills_can_be_installed_individually(self) -> None:
        self.assertEqual(self.check()["errors"], [])
        for role in ("implementer", "supervisor", "acceptance"):
            with self.subTest(role=role):
                directory = self.install(role)
                self.assertEqual(self.check()["errors"], [])
                shutil.rmtree(directory)

    def test_invalid_installed_skill_and_policy_are_reported(self) -> None:
        for role in ("implementer", "supervisor", "acceptance"):
            directory = self.install(role)
            for relative, message in (
                ("SKILL.md", "Invalid skill entry point"),
                ("agents/openai.yaml", "Invalid invocation policy"),
            ):
                with self.subTest(role=role, file=relative):
                    path = directory / relative
                    original = path.read_text()
                    path.write_text("invalid\n")
                    errors = self.check(1)["errors"]
                    self.assertIn(f"{message}: agentic-workflow-{role}", errors)
                    path.write_text(original)

    def test_missing_or_broken_root_block_fails(self) -> None:
        for block in ("", self.block.replace("agentic-workflow/policies/MEMORY.md", "missing.md")):
            with self.subTest(block=block):
                (self.root / "AGENTS.md").write_text("# Host\n" + block)
                self.assertTrue(self.check(1)["errors"])

    def test_development_cleanup_retains_project_settings(self) -> None:
        shutil.copyfile(SOURCE / "Makefile", self.root / "Makefile")
        records = self.root / ".agentic-workflow/records"
        for name in ("001_example", "1000_example"):
            (records / name / "runs").mkdir(parents=True)
        override = self.root / ".agentic-workflow/config/MODELS.md"
        override.parent.mkdir(parents=True)
        override.write_text("Project-owned routing\n")
        process = subprocess.run(
            ["make", "cleanup"], cwd=self.root, capture_output=True, text=True, timeout=15
        )
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertEqual(override.read_text(), "Project-owned routing\n")
        self.assertEqual(list(records.iterdir()), [])

    def test_copy_operations_and_package_replacement_preserve_project_data(self) -> None:
        records = self.root / ".agentic-workflow/records"
        records.mkdir(parents=True)
        override = self.root / ".agentic-workflow/config/MODELS.md"
        override.parent.mkdir(parents=True)
        override.write_text("Project-owned routing\n")
        for relative in (
            "specs/example/project.md",
            ".agentic-workflow/memory/index.md",
            "app/main.py",
        ):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Project-owned content\n")
        for args, expected in (
            ((), records / "001_example"),
            (("--records-root", "custom records"), self.root / "custom records/001_example"),
        ):
            process = self.cli("records.py", "allocate", "example", *args)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual((self.root / process.stdout.strip()).resolve(), expected)
            (expected / "tasks/one").mkdir()
            process = self.cli("records.py", "resolve", expected, "one")
            self.assertEqual(process.returncode, 0, process.stderr)
            for provider in ("codex", "opencode"):
                filename = "codex-0.167.0.jsonl" if provider == "codex" else "opencode-2.2.6.json"
                native = expected / "native" / filename
                native.parent.mkdir(exist_ok=True)
                native.write_bytes((self.package / "tests/fixtures" / filename).read_bytes())
                process = self.cli("usage_report.py", expected)
                self.assertEqual(process.returncode, 0, process.stderr)
                report = json.loads((expected / "reports/usage.json").read_text())
                self.assertIn("summary", report)
                self.assertEqual(report["tracing_provider"], provider)
                native.unlink()
        shutil.rmtree(self.package)
        shutil.copytree(
            SOURCE / "agentic-workflow",
            self.package,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        self.assertEqual(override.read_text(), "Project-owned routing\n")
        self.assertTrue((records / "001_example/tasks/one").is_dir())
        for relative in (
            "specs/example/project.md",
            ".agentic-workflow/memory/index.md",
            "app/main.py",
        ):
            self.assertEqual((self.root / relative).read_text(), "Project-owned content\n")
        self.assertEqual(self.check()["errors"], [])


if __name__ == "__main__":
    unittest.main()
