"""Unit tests for portfolio-reviews central reference summary validation."""
from __future__ import annotations

import os
import re
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
NO_REVIEW_HEADING = "Registered projects without a review in the matrix"


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

    def test_every_registered_project_is_listed_or_stated_to_have_no_review(self) -> None:
        """A registered project is a row in the matrix, or the page says it has no review (CDS-38 follow-up).

        A project with code-review bundles must be in the matrix. A project without any may pass, but only if the central
        index (README.md and index.html) names it under 'Registered projects without a review in the matrix'.
        """
        if not REGISTRY_PATH.exists() or not REVIEWS_MD.exists():
            self.skipTest("registry.yml or portfolio-reviews not present (isolated CI environment)")

        registry_data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
        md_text = REVIEWS_MD.read_text(encoding="utf-8")
        html_text = REVIEWS_HTML.read_text(encoding="utf-8")

        md_section = re.search(rf"^## {re.escape(NO_REVIEW_HEADING)}\s*$(.*?)(?=^## |\Z)", md_text, re.S | re.M)
        html_section = re.search(rf"<h2>{re.escape(NO_REVIEW_HEADING)}</h2>(.*?)(?=<h2>|\Z)", html_text, re.S)
        self.assertIsNotNone(md_section, f"portfolio-reviews/README.md has no '{NO_REVIEW_HEADING}' section")
        self.assertIsNotNone(html_section, f"portfolio-reviews/index.html has no '{NO_REVIEW_HEADING}' section")
        stated_md = set(re.findall(r"^- `([^`]+)`", md_section.group(1), re.M))
        stated_html = set(re.findall(r"<li><code>([^<]+)</code>", html_section.group(1)))
        self.assertEqual(stated_md, stated_html, "README.md and index.html state different projects as having no review")

        registered = {p["project"] for p in registry_data.get("projects", [])}
        for name in sorted(stated_md - registered):
            self.fail(f"'{name}' is stated as having no review but is not a registered project")

        for p in registry_data.get("projects", []):
            name = p["project"]
            review_rel = p.get("deviations", {}).get("reviews", f"{name}/.review/")
            review_dir = PORTFOLIO_ROOT / review_rel if review_rel.startswith(name) else PORTFOLIO_ROOT / name / review_rel
            has_bundle = review_dir.exists() and any(child.name.startswith("CODE_REVIEW") for child in review_dir.iterdir())
            in_matrix = re.search(rf"^\| `{re.escape(name)}` \|", md_text, re.M) is not None
            in_matrix_html = re.search(rf"<tr>\s*<td><code>{re.escape(name)}</code></td>", html_text) is not None

            if has_bundle:
                self.assertTrue(in_matrix, f"Project {name} has review bundles but is missing from the matrix in portfolio-reviews/README.md")
                self.assertTrue(in_matrix_html, f"Project {name} has review bundles but is missing from portfolio-reviews/index.html")
                self.assertNotIn(name, stated_md, f"Project {name} has review bundles but is stated as having none")
            elif not in_matrix:
                self.assertIn(name, stated_md, f"Registered project {name} has no review and the page does not say so")

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
