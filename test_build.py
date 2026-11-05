#!/usr/bin/env python3
"""Tests for the privacy checkup directory build.

Run: python3 test_build.py   (unittest, no dependencies)
"""

import re
import sys
import html
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import build  # noqa: E402

MD_TEXT = build.MD_PATH.read_text(encoding="utf-8")


class TestDirectoryMarkdown(unittest.TestCase):
    def setUp(self):
        self.parsed = build.parse_directory(MD_TEXT)

    def test_parse_succeeds(self):
        _, intro_lines, categories = self.parsed
        self.assertGreater(len(categories), 0)
        self.assertGreater(len(intro_lines), 0)

    def test_expected_categories_present(self):
        _, _, categories = self.parsed
        titles = [t for t, _ in categories]
        for expected in (
            "Password-strength checkers",
            "Have-I-Been-Pwned-style breach checkers",
            "Email aliasing",
            "Browser privacy tests",
            "Router checks",
            "Phone-settings walkthroughs",
        ):
            self.assertIn(expected, titles)
        self.assertTrue(
            any("DNS" in t for t in titles),
            f"expected a DNS section in {titles}",
        )

    def test_every_entry_has_required_fields(self):
        _, _, categories = self.parsed
        for title, entries in categories:
            self.assertGreater(
                len(entries), 1, f"category '{title}' should list multiple tools"
            )
            for entry in entries:
                self.assertTrue(entry["title"].strip(), f"empty title in {title}")
                self.assertTrue(entry["url"].startswith("https://"), entry["url"])
                self.assertTrue(entry["one_liner"].strip())
                self.assertTrue(entry["inspects"].strip())

    def test_no_scraping_promises_stated(self):
        """The directory must promise no scraping and no-surprise-data collection."""
        lowered = MD_TEXT.lower()
        self.assertIn("no scraping", lowered)

    def test_links_are_https_only(self):
        urls = re.findall(r"\]\((http[^\s)]+)\)", MD_TEXT)
        self.assertTrue(urls)
        for url in urls:
            self.assertTrue(url.startswith("https://"), f"non-https link: {url}")

    def test_urls_unique_per_entry(self):
        _, _, categories = self.parsed
        seen = []
        for _, entries in categories:
            for entry in entries:
                seen.append(entry["url"])
        self.assertEqual(len(seen), len(set(seen)), "duplicate entry URLs")

    def test_one_liner_states_account_requirements(self):
        """Entries requiring an account must say so explicitly."""
        _, _, categories = self.parsed
        for _, entries in categories:
            for entry in entries:
                self.assertTrue(
                    entry["one_liner"].strip() and isinstance(entry["notes"], list)
                )


class TestHtmlBuild(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parsed = build.parse_directory(MD_TEXT)

    def test_build_runs(self):
        build.main()  # also refreshes index.html for test assertions
        self.assertTrue(build.OUT_PATH.exists())

    def test_html_contains_all_entries(self):
        _, _, categories = self.parsed
        raw = build.OUT_PATH.read_text(encoding="utf-8")
        html_text = re.sub(r"<[^>]+>", " ", html.unescape(raw))
        html_text = re.sub(r"\s+", " ", html_text)
        def flatten(text: str) -> str:
            return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html.unescape(text)))

        for _, entries in categories:
            for entry in entries:
                self.assertIn(entry["title"], html_text, entry["title"])
                self.assertIn(entry["url"], raw, entry["url"])
                self.assertIn(flatten(build.inline_md(entry["one_liner"])), html_text,
                              entry["one_liner"])
                self.assertIn(flatten(build.inline_md(entry["inspects"])), html_text,
                              entry["inspects"])

    def test_html_contains_all_categories(self):
        _, _, categories = self.parsed
        html_text = build.OUT_PATH.read_text(encoding="utf-8")
        for title, _ in categories:
            self.assertIn(title, html_text)

    def test_html_structure_and_clean_tags(self):
        html_text = build.OUT_PATH.read_text(encoding="utf-8")
        self.assertIn("<!doctype html>", html_text.lower())
        self.assertIn("</html>", html_text)
        self.assertNotIn("href=\">", html_text)
        self.assertNotIn("<script", html_text.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)
