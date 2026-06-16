import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from website_sort import sort_markdown


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

    def test_places_faq_before_contact(self) -> None:
        source = "## Contact\nCall us.\n\n## FAQ\nCommon answers.\n\n## Services\nWork.\n"

        result = sort_markdown(source)

        self.assertLess(result.index("## Services"), result.index("## FAQ"))
        self.assertLess(result.index("## FAQ"), result.index("## Contact"))

if __name__ == "__main__":
    unittest.main()
