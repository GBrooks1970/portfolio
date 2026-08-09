"""Unit tests for portfolio-reviews central reference summary validation."""
from __future__ import annotations

import os
import unittest
from pathlib import Path
import yaml

TOOLS_DIR = Path(__file__).resolve().parent.parent        # portfolio-landing/tools/
LANDING_ROOT = TOOLS_DIR.parent                             # portfolio-landing/
PORTFOLIO_ROOT = LANDING_ROOT.parent                       # test-automation-portfolio/
REVIEWS_DIR = PORTFOLIO_ROOT / "portfolio-reviews"
REVIEWS_MD = REVIEWS_DIR / "README.md"
REVIEWS_HTML = REVIEWS_DIR / "index.html"
REGISTRY_PATH = PORTFOLIO_ROOT / "portfolio-prompts" / "registry.yml"


class TestReviewsSummary(unittest.TestCase):
    """Verifies that portfolio-reviews central reference summary files exist and are valid."""

    def test_landing_reviews_html_exists_and_valid(self) -> None:
        landing_reviews_html = LANDING_ROOT / "reviews.html"
        self.assertTrue(
            landing_reviews_html.exists(),
            f"portfolio-landing/reviews.html not found at {landing_reviews_html}",
        )
        self.assertGreater(
            landing_reviews_html.stat().st_size,
            500,
            "portfolio-landing/reviews.html is empty or too small",
        )
        html_text = landing_reviews_html.read_text(encoding="utf-8")
        self.assertIn("Portfolio Code Reviews — Central Index", html_text)
        self.assertIn("Latest Reviews Matrix", html_text)

    def test_summary_files_exist_and_non_empty(self) -> None:
        if not REVIEWS_DIR.exists():
            self.skipTest(f"portfolio-reviews directory not present at {REVIEWS_DIR} (isolated CI environment)")

        self.assertTrue(
            REVIEWS_MD.exists(),
            f"portfolio-reviews/README.md not found at {REVIEWS_MD}",
        )
        self.assertTrue(
            REVIEWS_HTML.exists(),
            f"portfolio-reviews/index.html not found at {REVIEWS_HTML}",
        )
        self.assertGreater(
            REVIEWS_MD.stat().st_size,
            100,
            "portfolio-reviews/README.md is empty or too small",
        )
        self.assertGreater(
            REVIEWS_HTML.stat().st_size,
            100,
            "portfolio-reviews/index.html is empty or too small",
        )

    def test_all_registered_showcase_projects_present(self) -> None:
        if not REGISTRY_PATH.exists() or not REVIEWS_MD.exists():
            self.skipTest(f"registry.yml or portfolio-reviews not present (isolated CI environment)")

        registry_data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
        md_text = REVIEWS_MD.read_text(encoding="utf-8")
        html_text = REVIEWS_HTML.read_text(encoding="utf-8")

        for p in registry_data.get("projects", []):
            proj_name = p["project"]
            deviations = p.get("deviations", {})
            review_rel = deviations.get("reviews", f"{proj_name}/.review/")
            review_dir = PORTFOLIO_ROOT / review_rel if review_rel.startswith(proj_name) else PORTFOLIO_ROOT / proj_name / review_rel

            # Only check projects that maintain a review directory
            if not review_dir.exists():
                continue

            self.assertIn(
                proj_name,
                md_text,
                f"Project {proj_name} missing from portfolio-reviews/README.md",
            )
            self.assertIn(
                proj_name,
                html_text,
                f"Project {proj_name} missing from portfolio-reviews/index.html",
            )

    def test_summary_relative_links_valid(self) -> None:
        if not REVIEWS_MD.exists():
            self.skipTest("portfolio-reviews/README.md not present (isolated CI environment)")

        md_text = REVIEWS_MD.read_text(encoding="utf-8")
        import re
        links = re.findall(r"\]\(([^)]+)\)", md_text)
        checked = 0
        for link in links:
            if link.startswith("http://") or link.startswith("https://") or link.startswith("#"):
                continue
            target_path = (REVIEWS_DIR / link.split("#")[0]).resolve()
            self.assertTrue(
                target_path.exists(),
                f"Broken relative link in portfolio-reviews/README.md: '{link}' -> {target_path}",
            )
            checked += 1
        self.assertGreater(checked, 0, "No relative drill-down links checked in portfolio-reviews/README.md")


if __name__ == "__main__":
    unittest.main()
