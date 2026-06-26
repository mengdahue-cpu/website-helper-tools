import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from website_sort import sort_markdown


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "website_sort.py"


class SortMarkdownTests(unittest.TestCase):
    def test_sorts_recognized_sections_and_keeps_preamble(self) -> None:
        source = "# Example\n\nIntro.\n\n## 联系我们\nCall us.\n\n## 关于我们\nOur story.\n"

        result = sort_markdown(source)

        self.assertTrue(result.startswith("# Example\n\nIntro."))
        self.assertLess(result.index("## 关于我们"), result.index("## 联系我们"))

    def test_places_unknown_sections_after_recognized_sections_stably(self) -> None:
        source = "## Team\nPeople.\n\n## Services\nWork.\n\n## Careers\nJobs.\n"

        result = sort_markdown(source)

        self.assertLess(result.index("## Services"), result.index("## Team"))
        self.assertLess(result.index("## Team"), result.index("## Careers"))

    def test_returns_documents_without_level_two_sections_unchanged(self) -> None:
        source = "# Title\n\nPlain content.\n"

        self.assertEqual(sort_markdown(source), source)

    def test_preserves_unicode_content(self) -> None:
        source = "# 企业官网\n\n## 服务\n内容整理。\n"

        self.assertEqual(sort_markdown(source), source)

    def test_ignores_headings_inside_fenced_code_blocks(self) -> None:
        source = (
            "# Guide\n\n"
            "## Contact\nReal contact content.\n\n"
            "```markdown\n## Services\nExample only.\n```\n\n"
            "## About\nReal about content.\n"
        )

        result = sort_markdown(source)

        self.assertLess(result.index("## About"), result.index("## Contact"))
        self.assertIn("```markdown\n## Services\nExample only.\n```", result)
        self.assertEqual(result.count("## Services"), 1)

    def test_ignores_headings_inside_tilde_fences(self) -> None:
        source = "~~~markdown\n## Contact\n~~~\n\n## Services\nWork.\n"

        self.assertEqual(sort_markdown(source), source)

    def test_recognizes_headings_with_closing_hashes(self) -> None:
        source = "## Contact ##\nCall us.\n\n## About ##\nOur story.\n"

        result = sort_markdown(source)

        self.assertLess(result.index("## About ##"), result.index("## Contact ##"))

    def test_recognizes_headings_with_leading_spaces(self) -> None:
        source = "   ## Contact\nCall us.\n\n  ## About\nOur story.\n"

        result = sort_markdown(source)

        self.assertLess(result.index("  ## About"), result.index("   ## Contact"))

    def test_places_faq_before_contact(self) -> None:
        source = "## Contact\nCall us.\n\n## FAQ\nCommon answers.\n\n## Services\nWork.\n"

        result = sort_markdown(source)

        self.assertLess(result.index("## Services"), result.index("## FAQ"))
        self.assertLess(result.index("## FAQ"), result.index("## Contact"))

    def test_recognizes_products_and_services_heading(self) -> None:
        source = "## Contact\nCall us.\n\n## Products and Services\nWork.\n\n## About\nOur story.\n"

        result = sort_markdown(source)

        self.assertLess(result.index("## About"), result.index("## Products and Services"))
        self.assertLess(result.index("## Products and Services"), result.index("## Contact"))

    def test_recognizes_services_ampersand_products_heading(self) -> None:
        source = "## Contact\nCall us.\n\n## Services & Products\nWork.\n\n## About\nOur story.\n"

        result = sort_markdown(source)

        self.assertLess(result.index("## About"), result.index("## Services & Products"))
        self.assertLess(result.index("## Services & Products"), result.index("## Contact"))

    def test_recognizes_chinese_faq_heading(self) -> None:
        source = "## 联系我们\nCall us.\n\n## 常见问题\nAnswers.\n\n## 服务\nWork.\n"

        result = sort_markdown(source)

        self.assertLess(result.index("## 服务"), result.index("## 常见问题"))
        self.assertLess(result.index("## 常见问题"), result.index("## 联系我们"))

    def test_check_mode_succeeds_for_ordered_document(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "ordered.md"
            source_path.write_text(
                "## About\nOur story.\n\n## Contact\nCall us.\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--check", str(source_path)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "")

    def test_check_mode_fails_for_unordered_document(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            source_path = Path(temp_dir) / "unordered.md"
            source_path.write_text(
                "## Contact\nCall us.\n\n## About\nOur story.\n",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--check", str(source_path)],
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(completed.returncode, 1)
        self.assertIn("not in the preferred order", completed.stderr)


if __name__ == "__main__":
    unittest.main()
