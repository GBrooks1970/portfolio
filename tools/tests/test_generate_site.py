from __future__ import annotations

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
        cls.template = (ROOT / "index.template.html").read_text(encoding="utf-8")
        cls.rendered = GENERATE.render_site(cls.template, cls.manifest, cls.registry_lock)

    def test_renders_current_public_inventory_and_counts(self) -> None:
        self.assertEqual(self.rendered.count('<article class="card" data-project='), 9)
        self.assertIn('data-project="portfolio-prompts"', self.rendered)
        self.assertIn("Nine showcase projects", self.rendered)
        self.assertIn("All nine showcase project repositories", self.rendered)
        self.assertIn("ParaBank Bank Automation", self.rendered)

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
        second = GENERATE.render_site(self.template, self.manifest, self.registry_lock)
        self.assertEqual(self.rendered.encode("utf-8"), second.encode("utf-8"))
        self.assertEqual(self.rendered.encode("utf-8"), (ROOT / "index.html").read_bytes())


if __name__ == "__main__":
    unittest.main()
