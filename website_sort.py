"""Sort common enterprise website sections in a Markdown document."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SECTION_ORDER = (
    ("home", "homepage", "首页"),
    ("about", "about us", "关于", "关于我们"),
    ("services", "products", "产品", "服务", "产品与服务"),
    ("solutions", "解决方案"),
    ("cases", "case studies", "projects", "案例", "客户案例"),
    ("news", "insights", "新闻", "资讯"),
    ("contact", "contact us", "联系", "联系我们"),
)

HEADING_PATTERN = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


def section_priority(heading: str) -> int:
    """Return the preferred position for a recognized section heading."""
    normalized = heading.strip().casefold()
    for index, aliases in enumerate(SECTION_ORDER):
        if normalized in aliases:
            return index
    return len(SECTION_ORDER)


def sort_markdown(content: str) -> str:
    """Sort level-two Markdown sections while preserving their contents."""
    matches = list(HEADING_PATTERN.finditer(content))
    if not matches:
        return content

    prefix = content[: matches[0].start()]
    sections: list[tuple[int, int, str]] = []

    for original_index, match in enumerate(matches):
        end = matches[original_index + 1].start() if original_index + 1 < len(matches) else len(content)
        sections.append(
            (section_priority(match.group(1)), original_index, content[match.start() : end])
        )

    sections.sort(key=lambda item: (item[0], item[1]))
    return prefix + "".join(section for _, _, section in sections)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Sort common enterprise website sections in a Markdown file."
    )
    parser.add_argument("input", type=Path, help="UTF-8 Markdown file to organize")
    parser.add_argument("-o", "--output", type=Path, help="Write to this file instead of stdout")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    content = args.input.read_text(encoding="utf-8-sig")
    organized = sort_markdown(content)

    if args.output:
        args.output.write_text(organized, encoding="utf-8")
    else:
        sys.stdout.buffer.write(organized.encode("utf-8"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
