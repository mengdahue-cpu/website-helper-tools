"""Sort common enterprise website sections in a Markdown document."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Optional


SECTION_ORDER = (
    ("home", "homepage", "首页"),
    ("about", "about us", "关于", "关于我们"),
    ("services", "products", "产品", "服务", "产品与服务"),
    ("solutions", "解决方案"),
    (
        "cases",
        "case studies",
        "customer stories",
        "success stories",
        "projects",
        "案例",
        "客户案例",
    ),
    ("news", "insights", "新闻", "资讯"),
    ("faq", "faqs", "frequently asked questions", "常见问题"),
    ("contact", "contact us", "联系", "联系我们"),
)

HEADING_PATTERN = re.compile(r"^[ \t]{0,3}##[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*(?:\r?\n)?$")
FENCE_PATTERN = re.compile(r"^[ \t]{0,3}(`{3,}|~{3,})")


def section_priority(heading: str) -> int:
    """Return the preferred position for a recognized section heading."""
    normalized = " ".join(heading.split()).casefold()
    if normalized in {
        "products and services",
        "services and products",
        "products & services",
        "services & products",
    }:
        normalized = "services"
    for index, aliases in enumerate(SECTION_ORDER):
        if normalized in aliases:
            return index
    return len(SECTION_ORDER)


def find_section_headings(content: str) -> list[tuple[int, str]]:
    """Return level-two headings that are outside fenced code blocks."""
    headings: list[tuple[int, str]] = []
    offset = 0
    fence_character: Optional[str] = None
    fence_length = 0

    for line in content.splitlines(keepends=True):
        if fence_character:
            closing_pattern = rf"^[ \t]{{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*(?:\r?\n)?$"
            if re.match(closing_pattern, line):
                fence_character = None
                fence_length = 0
        else:
            fence_match = FENCE_PATTERN.match(line)
            if fence_match:
                fence = fence_match.group(1)
                fence_character = fence[0]
                fence_length = len(fence)
            else:
                heading_match = HEADING_PATTERN.match(line)
                if heading_match:
                    headings.append((offset, heading_match.group(1)))

        offset += len(line)

    return headings


def sort_markdown(content: str) -> str:
    """Sort level-two Markdown sections while preserving their contents."""
    headings = find_section_headings(content)
    if not headings:
        return content

    prefix = content[: headings[0][0]]
    sections: list[tuple[int, int, str]] = []

    for original_index, (start, heading) in enumerate(headings):
        end = headings[original_index + 1][0] if original_index + 1 < len(headings) else len(content)
        sections.append(
            (section_priority(heading), original_index, content[start:end])
        )

    sections.sort(key=lambda item: (item[0], item[1]))
    return prefix + "".join(section for _, _, section in sections)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sort common enterprise website sections in a Markdown file."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Return a non-zero exit code if the file would be reordered",
    )
    parser.add_argument("input", type=Path, help="UTF-8 Markdown file to organize")
    parser.add_argument("-o", "--output", type=Path, help="Write to this file instead of stdout")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.check and args.output:
        parser.error("--check cannot be used with --output")

    content = args.input.read_text(encoding="utf-8-sig")
    organized = sort_markdown(content)

    if args.check:
        if organized == content:
            return 0
        print(
            f"{args.input}: sections are not in the preferred order",
            file=sys.stderr,
        )
        return 1

    if args.output:
        args.output.write_text(organized, encoding="utf-8")
    else:
        sys.stdout.buffer.write(organized.encode("utf-8"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
