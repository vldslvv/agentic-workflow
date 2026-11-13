"""Package-check CLI contracts on disposable packages without Git history."""

import unittest

from package_fixture import PackageCheckCase


class PackageCheckTests(PackageCheckCase):
    def test_policies_reject_other_policy_references(self) -> None:
        (self.package / "policies/new.md").write_text("# Policy\n\nUse CHECKS.\n")
        report = self.result(self.cli(), 1)
        self.assertIn(
            "policies/new.md:3: prohibited policy reference: CHECKS",
            report["errors"],
        )

    def test_policies_reject_role_mentions_and_dependencies(self) -> None:
        (self.package / "roles/AUDITOR.md").write_text("# Auditor\n")
        cases = (
            ("policies/CHECKS.md", "Use the Supervisor.", 3, "Supervisor"),
            ("policies/new/nested.md", "Ask PLANNERS.", 3, "PLANNERS"),
            ("policies/new/nested.md", "Ask Implementers.", 3, "Implementers"),
            ("policies/new/nested.md", "Ask reviewers.", 3, "reviewers"),
            ("policies/new/nested.md", "Ask VALIDATORS.", 3, "VALIDATORS"),
            ("policies/new/nested.md", "Each RoLe has inputs.", 3, "RoLe"),
            ("policies/new/nested.md", "Apply to all ROLES.", 3, "ROLES"),
            ("policies/new/nested.md", "Use `role` in the marker.", 3, "role"),
            ("policies/new/nested.md", '```json\n{"role":"implementer"}\n```', 4, "role"),
            ("policies/new/nested.md", "~~~text\nSend to a Validator.\n~~~", 4, "Validator"),
            ("policies/new/nested.md", "Ask auditors.", 3, "auditors"),
            ("policies/new/extra.MD", "Ask an Auditor.", 3, "Auditor"),
            (
                "policies/new/nested.md",
                "## References:\n\n- [GUIDE]: Applicable instructions. "
                "agentic-workflow/roles/AUDITOR.md",
                5,
                "AUDITOR",
            ),
            (
                "policies/new/nested.md",
                "## References:\n\n- [GUIDE]: Applicable instructions. "
                "agentic-workflow/r%6fles/P%4cANNER.md",
                5,
                "r%6fles/P%4cANNER.md",
            ),
            (
                "policies/new/nested.md",
                "[Guide](../../r%6fles/P%4cANNER.md)",
                3,
                "../../r%6fles/P%4cANNER.md",
            ),
            (
                "policies/new/nested.md",
                '```md\n[guide]: <../../r%6fles/P%4cANNER.md> "Guide"\n```',
                4,
                "../../r%6fles/P%4cANNER.md",
            ),
            (
                "policies/new/nested.md",
                "```md\n[Guide](<../../r%6fles/P%4cANNER.md>)\n```",
                4,
                "../../r%6fles/P%4cANNER.md",
            ),
        )
        for relative, content, line, reference in cases:
            with self.subTest(path=relative, content=content):
                path = self.package / relative
                original = path.read_bytes() if path.exists() else None
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"# Policy\n\n{content}\n")
                try:
                    report = self.result(self.cli(), 1)
                    self.assertTrue(
                        any(
                            error.startswith(f"{relative}:{line}: prohibited policy reference:")
                            and reference in error
                            for error in report["errors"]
                        ),
                        report["errors"],
                    )
                finally:
                    if original is None:
                        path.unlink()
                    else:
                        path.write_bytes(original)

    def test_policy_boundary_allows_activities_and_references_elsewhere(self) -> None:
        (self.package / "roles/AUDITOR.md").write_text("# Auditor\n")
        cases = (
            ("policies/new.md", "Review and validation prepare checks for orchestration."),
            ("policies/new.md", "Use controllers and roleplay for implementation previews."),
            (
                "guides/new.md",
                "Roles: Supervisor, Planner, Implementer, Reviewer, Validator, Auditor.",
            ),
            ("guides/new.md", "[Instructions](../roles/AUDITOR.md)"),
            ("roles/AUDITOR.md", '```json\n{"role":"implementer"}\n```'),
        )
        for relative, content in cases:
            with self.subTest(path=relative, content=content):
                path = self.package / relative
                path.write_text(f"# Guidance\n\n{content}\n")
                try:
                    self.assertEqual(self.result(self.cli(), 0)["errors"], [])
                finally:
                    path.unlink()

    def test_imports_stay_inside_standard_library_and_copy_boundary(self) -> None:
        (self.root / "repository_only.py").write_text("# Not in the copied package.\n")
        cases = (
            ("import json\nfrom pathlib import Path\n", None),
            ("def helper():\n    import records\n", None),
            ("from . import records\n", None),
            ("from .records import identifier\n", None),
            ("from ..helpers.records import identifier\n", None),
            ("from .. import helpers\n", None),
            ("import importlib as loader\nloader.import_module('json')\n", None),
            ("from importlib import import_module as load\nload('.records', 'helpers')\n", None),
            ("__import__('records')\n", None),
            ("if False:\n    import requests\n", "requests"),
            ("def helper():\n    from typing_extensions import TypedDict\n", "typing_extensions"),
            ("import repository_only\n", "repository_only"),
            ("from . import missing_local\n", "missing_local"),
            ("from ..repository_only import value\n", "repository_only"),
            ("import importlib\nimportlib.import_module('requests')\n", "requests"),
            (
                "from importlib import import_module as load\nload('repository_only')\n",
                "repository_only",
            ),
            ("from builtins import __import__ as load\nload('requests')\n", "requests"),
            ("__import__('requests')\n", "requests"),
            ("import importlib\nimportlib.import_module(module_name)\n", "computed import target"),
            ("__import__('json' + suffix)\n", "computed import target"),
            (
                "import importlib\nimportlib.import_module('.records', package_name)\n",
                "computed import package",
            ),
            ("__import__('records', level=level)\n", "computed import level"),
        )
        for source, violation in cases:
            with self.subTest(source=source):
                (self.package / "helpers/probe.py").write_text(source)
                report = self.result(self.cli(), 1 if violation else 0)
                if violation:
                    self.assertTrue(
                        any(
                            "helpers/probe.py:" in error and violation in error
                            for error in report["errors"]
                        ),
                        report["errors"],
                    )
                else:
                    self.assertEqual(report["errors"], [])

    def test_tracing_dependencies_follow_provider_and_shared_boundaries(self) -> None:
        cases = (
            ("", "from . import codex\n", False),
            ("", "import records\n", True),
            ("shared", "from .types import Event\n", False),
            ("shared", "from tracing.codex import collect\n", True),
            ("shared", "from tracing import opencode\n", True),
            ("shared", "from ..registry import select\n", True),
            ("shared", "from ... import usage_report\n", True),
            ("codex", "from tracing.shared.files import locked\n", False),
            ("codex", "from .parser import parse\n", False),
            ("codex", "from tracing.opencode import collect\n", True),
            ("codex", "from .. import opencode\n", True),
            ("codex", "from records import allocate\n", True),
            ("codex", "import importlib\nimportlib.import_module('trace_view')\n", True),
            ("opencode", "from ..shared.types import Event\n", False),
            ("opencode", "from tracing import codex\n", True),
            ("opencode", "import usage_report\n", True),
            ("opencode", "__import__('tracing.codex')\n", True),
        )
        for owner, source, violation in cases:
            with self.subTest(owner=owner, source=source):
                path = self.package / f"helpers/tracing/{owner}/probe.py"
                path.write_text(source)
                try:
                    report = self.result(self.cli(), 1 if violation else 0)
                    if violation:
                        self.assertTrue(
                            any(
                                "prohibited tracing dependency" in error
                                for error in report["errors"]
                            ),
                            report,
                        )
                    else:
                        self.assertEqual(report["errors"], [])
                finally:
                    path.unlink()

    def test_valid_package_ignores_host_instructions(self) -> None:
        (self.root / "AGENTS.md").write_text("[Host-only reference](absent.md)\n")
        self.assertEqual(self.result(self.cli(), 0)["errors"], [])

    def test_broken_local_link_and_anchor_fail(self) -> None:
        extra = self.package / "extra.md"
        for target in ("missing.md", "AGENTS.md#absent-heading"):
            for reference in (
                f"[Reference]({target})",
                f"[REFERENCE]\n\n[REFERENCE]: {target}",
                f'[REFERENCE]\n\n[REFERENCE]: <{target}> "Reference"',
                f"- [REFERENCE]: Referenced document. agentic-workflow/{target}",
            ):
                with self.subTest(target=target, reference=reference):
                    extra.write_text(f"# Extra\n{reference}\n")
                    report = self.result(self.cli(), 1)
                    self.assertTrue(any(target in error for error in report["errors"]))

    def test_missing_required_role_and_template_fail(self) -> None:
        for relative in ("roles/REVIEWER.md", "templates/verification.md", "helpers/records.py"):
            with self.subTest(path=relative):
                path = self.package / relative
                original = path.read_bytes()
                path.unlink()
                try:
                    report = self.result(self.cli(), 1)
                    self.assertIn(f"Missing package file: {relative}", report["errors"])
                finally:
                    path.write_bytes(original)

    def test_link_outside_package_fails_even_when_host_file_exists(self) -> None:
        (self.root / "host.md").write_text("# Host dependency\n")
        for reference in (
            "[Host](../host.md)",
            "[HOST]\n\n[HOST]: ../host.md",
            "- [HOST]: Host dependency. host.md",
        ):
            with self.subTest(reference=reference):
                (self.package / "extra.md").write_text(reference + "\n")
                report = self.result(self.cli(), 1)
                self.assertTrue(any("outside copy boundary" in error for error in report["errors"]))

    def test_unreadable_document_returns_inability_to_run(self) -> None:
        (self.package / "extra.md").write_bytes(b"\xff")
        process = self.cli()
        self.assertEqual(process.returncode, 2)
        self.assertIn("Package check could not complete:", process.stderr)


if __name__ == "__main__":
    unittest.main()
