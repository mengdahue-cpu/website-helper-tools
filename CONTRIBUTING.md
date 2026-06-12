# Contributing

Thank you for helping improve Website Helper Tools. Contributions should remain focused
on practical enterprise website content, lightweight automation, or maintenance guidance.

## Good Contributions

- Add or improve reusable website copy while keeping claims verifiable.
- Fix content-ordering behavior with a small reproducible example.
- Add tests for English, Chinese, or mixed-language Markdown documents.
- Clarify setup, privacy, accessibility, or website maintenance guidance.

Please avoid vendor promotion, fabricated business claims, tracking code, generated filler,
or changes that collect more personal data than a website workflow requires.

## Report an Issue

Include:

1. A short description of the problem or proposed improvement.
2. Minimal sample input with private or customer information removed.
3. Expected and actual behavior.
4. Python version and operating system when reporting a script issue.

## Development

The project requires Python 3.9 or later and has no third-party runtime dependencies.

```bash
python -m unittest discover -s tests -v
```

For script changes, add or update a test in `tests/test_website_sort.py`. Keep file content
in UTF-8 and preserve unrecognized Markdown sections unless the proposed behavior is clearly
documented.

## Pull Requests

- Keep each pull request focused on one problem.
- Explain the user-facing change and how it was tested.
- Update documentation when command behavior changes.
- Confirm that examples contain no confidential or personally identifying information.

Maintainers may request a smaller example or revised wording before accepting a change.
