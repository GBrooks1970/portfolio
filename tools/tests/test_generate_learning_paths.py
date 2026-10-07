import re
import unittest

from generate_learning_paths import PAGE, check_learning_paths, load, public_link, render


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
