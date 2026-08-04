from __future__ import annotations

import copy
import importlib.util
import tempfile
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
        self.assertEqual(self.rendered.count('class="capability-group"'), 4)
        self.assertEqual(self.rendered.count("<h4><a href="), 9)
        self.assertIn('data-capability-group-count="4"', self.rendered)
        self.assertIn('data-public-evidence-count="8"', self.rendered)
        self.assertIn("<dt>Capability areas</dt>\n      <dd>4</dd>", self.rendered)
        self.assertIn("<dt>Public demos, reports and docs</dt>\n      <dd>8</dd>", self.rendered)
        self.assertEqual(self.rendered.count(" CI workflow\">"), 9)
        self.assertEqual(self.rendered.count(" CI status\""), 9)

    def test_action_types_are_rendered_with_distinct_classes(self) -> None:
        # Only a genuinely interactive `demo` carries the play cue (the
        # `.btn.demo::before` glyph); static `report` and `documentation` links
        # use their own classes and must not be rendered as demos.
        self.assertIn(
            '<a class="btn documentation" '
            'href="https://neocognitus70.github.io/calculator-screenplay-bdd/">API reference</a>',
            self.rendered,
        )
        self.assertIn(
            '<a class="btn report" '
            'href="https://gbrooks1970.github.io/parabank-bank-automation/">Serenity report</a>',
            self.rendered,
        )
        self.assertIn(
            '<a class="btn demo" href="https://gbrooks1970.github.io/markdown-renderer/">Live demo</a>',
            self.rendered,
        )
        # No report or documentation link is styled as a demo (no false play cue).
        self.assertNotIn('class="btn demo" href="https://gbrooks1970.github.io/parabank', self.rendered)

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

    def test_respects_group_and_project_order(self) -> None:
        titles = [
            "Magento Checkout Automation",
            "OrangeHRM PIM Automation",
            "ParaBank Bank Automation",
            "Bitfinex WebSocket Screenplay",
            "Calculator Screenplay BDD",
            "Hand-Baked Screenplay Pattern",
            "Sudoku Multi-Stack Parity POC",
            "Markdown Renderer",
            "Mobile Forex Automation",
        ]
        positions = [self.rendered.index(title) for title in titles]
        self.assertEqual(positions, sorted(positions))

        group_labels = [
            "Web UI and end-to-end",
            "APIs, BDD and real-time protocols",
            "Multi-stack and framework design",
            "Mobile and shipped products",
        ]
        group_positions = [self.rendered.index(label) for label in group_labels]
        self.assertEqual(group_positions, sorted(group_positions))

    def test_rejects_invalid_capability_group_contracts(self) -> None:
        invalid = copy.deepcopy(self.manifest)
        invalid["projects"]["parabank-bank-automation"]["group"] = "unknown-group"
        with self.assertRaisesRegex(GENERATE.SourceError, "unknown capability group"):
            GENERATE.validate_sources(invalid, self.registry_lock)

        invalid = copy.deepcopy(self.manifest)
        invalid["projects"]["parabank-bank-automation"]["group"] = None
        with self.assertRaisesRegex(GENERATE.SourceError, "must have a capability group"):
            GENERATE.validate_sources(invalid, self.registry_lock)

        invalid = copy.deepcopy(self.manifest)
        invalid["capabilityGroups"]["unused-group"] = {
            "label": "Unused group",
            "description": "A group without projects.",
            "order": 50,
        }
        with self.assertRaisesRegex(GENERATE.SourceError, "empty capability groups"):
            GENERATE.validate_sources(invalid, self.registry_lock)

        invalid = copy.deepcopy(self.manifest)
        invalid["projects"]["portfolio-prompts"]["group"] = "web-ui-e2e"
        with self.assertRaisesRegex(GENERATE.SourceError, "must use group null"):
            GENERATE.validate_sources(invalid, self.registry_lock)

    def test_rejects_duplicate_capability_group_json_keys(self) -> None:
        duplicate = '''{
          "schemaVersion": 2,
          "capabilityGroups": {
            "duplicate": {"label": "First", "description": "First.", "order": 10},
            "duplicate": {"label": "Second", "description": "Second.", "order": 20}
          },
          "projects": {}
        }'''
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "presentation.json"
            path.write_text(duplicate, encoding="utf-8")
            with self.assertRaisesRegex(GENERATE.SourceError, "duplicate JSON key"):
                GENERATE.load_json(path)

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
