from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "tools" / "generate_site.py"
SPEC = importlib.util.spec_from_file_location("generate_site", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
GENERATE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GENERATE)


class GenerateSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = GENERATE.load_json(ROOT / "data" / "presentation.json")
        cls.registry_lock = GENERATE.load_json(ROOT / "data" / "registry-lock.json")
        cls.site = GENERATE.load_json(ROOT / "data" / "site.json")
        cls.template = (ROOT / "index.template.html").read_text(encoding="utf-8")
        cls.rendered = GENERATE.render_site(
            cls.template, cls.manifest, cls.registry_lock, cls.site
        )

    def test_renders_current_public_inventory_and_counts(self) -> None:
        self.assertEqual(self.rendered.count('<article class="card" data-project='), 9)
        self.assertIn('data-project="portfolio-prompts"', self.rendered)
        self.assertIn("Nine showcase projects", self.rendered)
        self.assertIn("All nine showcase project repositories", self.rendered)
        self.assertIn("ParaBank Bank Automation", self.rendered)
        self.assertIn('<a class="skip-link" href="#projects">', self.rendered)
        self.assertIn('aria-labelledby="projects-heading"', self.rendered)
        self.assertEqual(self.rendered.count("<h3><a href="), 9)
        self.assertEqual(self.rendered.count(" CI workflow\">"), 9)
        self.assertEqual(self.rendered.count(" CI status\""), 9)

    def test_renders_consistent_search_and_social_metadata(self) -> None:
        canonical = self.site["canonicalUrl"]
        image_url = canonical + self.site["socialImage"]["path"]
        self.assertEqual(self.rendered.count('rel="canonical"'), 1)
        self.assertIn(f'<link rel="canonical" href="{canonical}">', self.rendered)
        self.assertIn(f'<meta property="og:url" content="{canonical}">', self.rendered)
        self.assertIn(f'<meta property="og:image" content="{image_url}">', self.rendered)
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', self.rendered)
        self.assertIn('"@type": "Person"', self.rendered)
        self.assertIn('"@type": "WebSite"', self.rendered)
        self.assertNotIn('"@type": "ProfilePage"', self.rendered)
        self.assertIn('href="assets/favicon.svg"', self.rendered)

    def test_respects_explicit_showcase_order(self) -> None:
        titles = [
            "Magento Checkout Automation",
            "OrangeHRM PIM Automation",
            "ParaBank Bank Automation",
            "Bitfinex WebSocket Screenplay",
            "Hand-Baked Screenplay Pattern",
            "Markdown Renderer",
            "Mobile Forex Automation",
            "Calculator Screenplay BDD",
            "Sudoku Multi-Stack Parity POC",
        ]
        positions = [self.rendered.index(title) for title in titles]
        self.assertEqual(positions, sorted(positions))

    def test_render_is_byte_stable_and_matches_committed_output(self) -> None:
        second = GENERATE.render_site(
            self.template, self.manifest, self.registry_lock, self.site
        )
        self.assertEqual(self.rendered.encode("utf-8"), second.encode("utf-8"))
        self.assertEqual(self.rendered.encode("utf-8"), (ROOT / "index.html").read_bytes())

    def test_sitemap_and_robots_are_canonical_and_byte_stable(self) -> None:
        sitemap = GENERATE.render_sitemap(self.site)
        robots = GENERATE.render_robots(self.site)
        self.assertIn(f'<loc>{self.site["canonicalUrl"]}</loc>', sitemap)
        self.assertNotIn("lastmod", sitemap)
        self.assertEqual(
            robots,
            "User-agent: *\nAllow: /\n\n"
            f'Sitemap: {self.site["canonicalUrl"]}sitemap.xml\n',
        )
        self.assertEqual(sitemap.encode("utf-8"), (ROOT / "sitemap.xml").read_bytes())
        self.assertEqual(robots.encode("utf-8"), (ROOT / "robots.txt").read_bytes())

    def test_site_manifest_rejects_identity_and_url_drift(self) -> None:
        invalid = copy.deepcopy(self.site)
        invalid["author"]["url"] = "https://example.test/"
        with self.assertRaisesRegex(GENERATE.SourceError, "url must equal canonicalUrl"):
            GENERATE.validate_site(invalid)

        invalid = copy.deepcopy(self.site)
        invalid["socialImage"]["path"] = "../preview.png"
        with self.assertRaisesRegex(GENERATE.SourceError, "safe repository-relative"):
            GENERATE.validate_site(invalid)


if __name__ == "__main__":
    unittest.main()
