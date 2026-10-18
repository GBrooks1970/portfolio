import re
import unittest

from generate_learning_paths import PAGE, check_learning_paths, format_timestamp, load, public_link, render


class LearningPathsPublicationTests(unittest.TestCase):
    def test_private_documents_become_text_and_public_links_survive(self):
        self.assertIsNone(public_link("PORTFOLIO_TOOL_ATLAS.md"))
        self.assertIsNone(public_link("https://github.com/GBrooks1970/test-automation-portfolio/blob/main/x.md"))
        self.assertEqual(public_link("#top"), "#top")
        self.assertEqual(public_link("https://example.org/a"), "https://example.org/a")

    def test_unsupported_links_fail_closed(self):
        for url in ["../secret.md", "file:///private", "http://unsafe", "dir/file.md"]:
            with self.assertRaises(ValueError):
                public_link(url)

    def test_committed_page_matches_snapshot(self):
        check_learning_paths()

    def test_page_links_nothing_private_and_has_a_way_back(self):
        output = PAGE.read_text(encoding="utf-8")
        self.assertNotIn('href="PORTFOLIO_', output)
        for href in re.findall(r'href="([^"]+)"', output):
            self.assertNotIn("test-automation-portfolio", href)
        self.assertIn('<a href="index.html">Back to portfolio</a>', output)
        self.assertEqual(output, render(load()))


class LearningPathsVersionedPageTests(unittest.TestCase):
    """LAND-14: the version and snapshot block, the house switch at the top right, and the scripts."""

    def setUp(self):
        self.output = PAGE.read_text(encoding="utf-8")
        self.snapshot = load()

    def test_html_names_become_text_but_other_relative_forms_still_fail(self):
        self.assertIsNone(public_link("PORTFOLIO_LEARNING_PATHS_MAINTENANCE.html"))
        for url in ["dir/guide.html", "../guide.html", "guide.html?x=1"]:
            with self.assertRaises(ValueError):
                public_link(url)

    def test_the_private_maintenance_guide_is_text_not_a_link(self):
        self.assertIn("Maintaining this document: maintenance guide.", self.output)
        self.assertNotIn("MAINTENANCE.html", self.output)

    def test_switch_is_at_the_top_right_beside_the_back_link(self):
        header = re.search(r'<header class="topbar">(.*?)</header>', self.output, re.S).group(1)
        self.assertLess(header.index("Back to portfolio"), header.index('id="theme-toggle"'))
        self.assertIn('aria-label="Toggle light/dark theme"', header)
        self.assertIn(" hidden ", header, "the switch stays hidden until the script runs, so there is no dead control without JavaScript")

    def test_page_has_both_palettes_and_exactly_two_scripts(self):
        self.assertIn('[data-theme="dark"]', self.output)
        self.assertIn("prefers-color-scheme: dark", self.output)
        self.assertEqual(self.output.count("<script>"), 2)
        self.assertIn("localStorage.getItem('portfolio-docs-theme')", self.output)

    def test_metadata_block_shows_version_and_the_public_snapshot_row(self):
        self.assertIn("<dt>Version</dt>", self.output)
        self.assertIn("<dt>Public snapshot</dt>", self.output)
        commit = self.snapshot["source"]["commit"]
        self.assertIn(f'<code title="{commit}">{commit[:7]}</code>', self.output)
        self.assertIn(self.snapshot["snapshot"]["item"], self.output)
        self.assertEqual(self.output.count("<dt>Public snapshot</dt>"), 1)

    def test_each_table_is_wrapped_once(self):
        self.assertEqual(self.output.count("<table>"), self.output.count('class="table-scroll"'))

    def test_format_timestamp(self):
        self.assertEqual(format_timestamp("2026-10-07T17:54Z"), "7 October 2026, 17:54 UTC")
        with self.assertRaises(ValueError):
            format_timestamp("2026-10-07 17:54")

    def test_a_snapshot_without_a_metadata_block_fails_closed(self):
        broken = dict(self.snapshot, html="<h1>No metadata</h1>")
        with self.assertRaises(ValueError):
            render(broken)
