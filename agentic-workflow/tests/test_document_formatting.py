"""Document formatting contracts for Markdown inside agentic-workflow."""

import unittest

from package_fixture import PackageCheckCase


class DocumentFormattingTests(PackageCheckCase):
    def test_additional_valid_markdown_is_allowed_and_checked(self) -> None:
        (self.package / "extra.md").write_text(
            "# Extra\nExplains additional behavior.\n\n# References:\n\n"
            "- [MODELS]: Model choices. agentic-workflow/policies/MODELS.md#codex\n"
            "- [GUIDELINES]: Engineering rules. agentic-workflow/policies/GUIDELINES.md\n"
            "- [EXTERNAL_GUIDE]: External guide. https://example.com/guide\n"
            "\n## Usage\nUse [MODELS].\n[Models](policies/MODELS.md#model-selection)\n"
            "Inline example: `- [EXAMPLE]: description path`.\n"
            "```markdown\n[EXAMPLE]: missing.md\n"
            "- [EXAMPLE]: Installation example. agentic-workflow/missing.md\n```\n"
        )
        self.assertEqual(self.result(self.cli(), 0)["errors"], [])

    def test_reference_structure_rejects_invalid_catalogs(self) -> None:
        entry = "- [MODELS]: Model choices. agentic-workflow/policies/MODELS.md\n"
        cases = (
            ("Use [MODELS].\n", "Missing References: section"),
            (entry, "outside References: section"),
            ("## References\n" + entry, "heading must be References:"),
            ("## Usage\n## References:\n" + entry, "first section"),
            ("## References:\n" + entry + "## References:\n" + entry, "Duplicate References:"),
            ("## References:\n" + entry + entry, "Duplicate reference [MODELS]"),
            ("## References:\n" + entry.removeprefix("- "), "Invalid reference entry"),
            ("## References:\n" + entry.replace("[MODELS]", "[models]"), "Invalid reference entry"),
            ("## References:\n" + entry.replace("Model choices. ", ""), "Invalid reference entry"),
            (
                "## References:\n" + entry + "## Usage\nUse [UNKNOWN].",
                "Undefined reference [UNKNOWN]",
            ),
            ("## References:\n" + entry + "## Usage\n" + entry, "outside References: section"),
            ("## References:\n", "Empty References: section"),
        )
        for body, expected in cases:
            with self.subTest(body=body):
                (self.package / "extra.md").write_text("# Extra\nPurpose.\n\n" + body)
                report = self.result(self.cli(), 1)
                self.assertTrue(
                    any("extra.md:" in error and expected in error for error in report["errors"]),
                    report["errors"],
                )

    def test_reference_paths_are_project_root_relative(self) -> None:
        target = self.package / "policies/MODELS.md"
        for path in (
            str(target),
            target.as_uri(),
            "C:/project/agentic-workflow/policies/MODELS.md",
            "policies/MODELS.md",
        ):
            with self.subTest(path=path):
                (self.package / "extra.md").write_text(
                    f"# Extra\nPurpose.\n\n## References:\n\n- [MODELS]: Model choices. {path}\n"
                )
                report = self.result(self.cli(), 1)
                self.assertTrue(any(path in error for error in report["errors"]), report["errors"])


if __name__ == "__main__":
    unittest.main()
