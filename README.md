# Website Helper Tools

[![Tests](https://github.com/mengdahue-cpu/website-helper-tools/actions/workflows/tests.yml/badge.svg)](https://github.com/mengdahue-cpu/website-helper-tools/actions/workflows/tests.yml)

A small, practical toolkit for planning, writing, and maintaining enterprise websites.

The project focuses on reusable content templates, lightweight automation, and concise
operational guidance. It is intended for small teams, independent developers, and
site owners who want a consistent starting point without adopting a large framework.

## Use Cases

- Draft the core pages of a company website with consistent messaging.
- Organize page sections before handing content to a designer or developer.
- Keep recurring website maintenance tasks documented and repeatable.
- Use simple scripts to prepare Markdown content for review or publishing.

## Features

- **Enterprise copy templates:** practical Chinese prompts and placeholders for common pages.
- **Content organization:** a standard-library Python utility for ordering Markdown sections.
- **Maintenance guidance:** clear project conventions that are easy to adapt.

## Project Structure

```text
website-helper-tools/
|-- .github/workflows/tests.yml
|-- CONTRIBUTING.md
|-- README.md
|-- LICENSE
|-- website-template.md
|-- website_sort.py
`-- tests/
    `-- test_website_sort.py
```

## Getting Started

The template can be used directly in any Markdown editor. Replace every value in square
brackets with verified business information, then complete the publishing checklist at
the end of the document.

The sorting script requires Python 3.9 or later and has no third-party dependencies:

```bash
python website_sort.py company-content.md -o organized-content.md
```

Without `--output`, the organized Markdown is printed to standard output:

```bash
python website_sort.py company-content.md
```

## Sorting Behavior

`website_sort.py` recognizes common English and Chinese level-two headings and orders
them as home, about, services, solutions, cases, news, FAQ, and contact. Standard
Markdown variants such as `## About ##` are recognized as well. The document title
and introductory text stay at the top. Unrecognized sections are kept in their
original order after recognized sections, and section contents are not rewritten.
Headings shown inside backtick or tilde code fences are treated as examples and
ignored.

Run the test suite from the repository root:

```bash
python -m unittest discover -s tests -v
```

## Project Principles

- Keep examples useful and easy to customize.
- Prefer standard tools and transparent behavior.
- Avoid collecting personal data or embedding third-party tracking.
- Document changes that affect generated or reorganized content.

## Maintenance

The repository is maintained through small, reviewable updates. Template changes should
remain industry-neutral, and script changes should preserve existing content unless the
document structure is explicitly recognized.

Before merging a script change, run the unit tests and manually review a document that
contains both recognized and custom headings. Before merging a template change, verify
that it does not encourage unsupported claims or unnecessary collection of personal data.

Bug reports and focused pull requests are welcome. Please include a short example of the
input, expected output, and the environment used to reproduce the issue.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the project scope, development workflow, and
review checklist.

## License

Released under the [MIT License](LICENSE).
