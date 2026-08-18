from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path


import sys

ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import check_site as SITE  # noqa: E402


class FakeResponse:
    def __init__(self, status: int) -> None:
        self.status = status

    def getcode(self) -> int:
        return self.status

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, *_: object) -> None:
        return None


class SiteQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.document = ROOT / "index.html"
        cls.html = cls.document.read_text(encoding="utf-8")

    def audit_variant(
        self,
        html: str,
        *,
        omit: tuple[str, ...] = (),
        text_overrides: dict[str, str] | None = None,
        file_replacements: dict[str, str] | None = None,
    ) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text(html, encoding="utf-8", newline="\n")
            shutil.copy(ROOT / "LICENSE", root / "LICENSE")
            shutil.copytree(ROOT / "assets", root / "assets")
            shutil.copytree(ROOT / "data", root / "data")
            shutil.copy(ROOT / "sitemap.xml", root / "sitemap.xml")
            shutil.copy(ROOT / "robots.txt", root / "robots.txt")
            for relative in omit:
                (root / relative).unlink()
            for relative, content in (text_overrides or {}).items():
                (root / relative).write_text(content, encoding="utf-8", newline="\n")
            for target, source in (file_replacements or {}).items():
                shutil.copy(ROOT / source, root / target)
            _, errors = SITE.audit_document(root / "index.html", root)
            return errors

    def test_current_document_passes_static_quality_contract(self) -> None:
        summary, errors = SITE.audit_document(self.document, ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(summary.external_urls, 44)
        self.assertEqual(summary.interactive_elements, 46)
        self.assertEqual(summary.internal_references, 6)
        self.assertEqual(summary.contrast_pairs, 20)

    def test_duplicate_canonical_is_rejected(self) -> None:
        canonical = '<link rel="canonical" href="https://gbrooks1970.github.io/portfolio/">'
        html = self.html.replace(canonical, f"{canonical}\n{canonical}", 1)
        self.assertTrue(
            any("exactly one canonical link" in error for error in self.audit_variant(html))
        )

    def test_open_graph_url_drift_is_rejected(self) -> None:
        html = self.html.replace(
            '<meta property="og:url" content="https://gbrooks1970.github.io/portfolio/">',
            '<meta property="og:url" content="https://example.test/portfolio/">',
            1,
        )
        self.assertTrue(
            any("meta property='og:url' must match" in error for error in self.audit_variant(html))
        )

    def test_missing_social_preview_asset_is_rejected(self) -> None:
        errors = self.audit_variant(
            self.html, omit=("assets/portfolio-social-preview-1200x630.png",)
        )
        self.assertTrue(any("social-preview image does not exist" in error for error in errors))

    def test_social_preview_dimensions_are_verified_from_png(self) -> None:
        errors = self.audit_variant(
            self.html,
            file_replacements={
                "assets/portfolio-social-preview-1200x630.png": "assets/favicon-32x32.png"
            },
        )
        self.assertTrue(any("dimensions are 32x32" in error for error in errors))

    def test_malformed_structured_data_is_rejected(self) -> None:
        html = self.html.replace('"@context": "https://schema.org",', '"@context" "broken",', 1)
        self.assertTrue(any("JSON-LD is malformed" in error for error in self.audit_variant(html)))

    def test_profile_page_structured_data_is_rejected(self) -> None:
        html = self.html.replace('"@type": "WebSite"', '"@type": "ProfilePage"', 1)
        self.assertTrue(
            any("exactly one Person and one WebSite" in error for error in self.audit_variant(html))
        )

    def test_required_favicon_contract_is_enforced(self) -> None:
        errors = self.audit_variant(self.html.replace(
            'href="assets/favicon.svg"', 'href="assets/favicon-v2.svg"', 1
        ))
        self.assertTrue(any("exactly one icon link" in error for error in errors))

    def test_sitemap_and_robots_must_agree_with_canonical(self) -> None:
        errors = self.audit_variant(
            self.html,
            text_overrides={
                "sitemap.xml": "<?xml version=\"1.0\"?><urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"><url><loc>https://example.test/</loc><lastmod>2026-08-02</lastmod></url></urlset>\n",
                "robots.txt": "User-agent: *\nDisallow: /\n",
            },
        )
        self.assertTrue(any("canonical portfolio URL" in error for error in errors))
        self.assertTrue(any("unverified lastmod" in error for error in errors))
        self.assertTrue(any("robots.txt must allow" in error for error in errors))

    def test_duplicate_identifier_is_rejected(self) -> None:
        html = self.html.replace(
            '<footer>', '<footer id="methodology-heading">', 1
        )
        self.assertTrue(any("duplicate id" in error for error in self.audit_variant(html)))

    def test_missing_required_metadata_is_rejected(self) -> None:
        html = self.html.replace('<meta name="description"', '<meta name="summary"', 1)
        self.assertTrue(
            any("meta description" in error for error in self.audit_variant(html))
        )

    def test_broken_internal_link_is_rejected(self) -> None:
        html = self.html.replace('href="LICENSE"', 'href="missing.txt"', 1)
        self.assertTrue(
            any("internal target does not exist" in error for error in self.audit_variant(html))
        )

    def test_unnamed_interactive_control_is_rejected(self) -> None:
        html = self.html.replace(
            '<a href="https://github.com/GBrooks1970">GitHub: @GBrooks1970</a>',
            '<a href="https://github.com/GBrooks1970"></a>',
            1,
        )
        self.assertTrue(
            any("no accessible name" in error for error in self.audit_variant(html))
        )

    def test_positive_tabindex_is_rejected(self) -> None:
        html = self.html.replace('<header class="hero">', '<header class="hero" tabindex="2">', 1)
        self.assertTrue(
            any("positive tabindex" in error for error in self.audit_variant(html))
        )

    def test_missing_main_landmark_is_rejected(self) -> None:
        html = self.html.replace('<main class="portfolio"', '<div class="portfolio"', 1).replace(
            '</main>', '</div>', 1
        )
        self.assertTrue(
            any("exactly one <main>" in error for error in self.audit_variant(html))
        )

    def test_dark_primary_button_contrast_is_enforced(self) -> None:
        html = self.html.replace(
            '--accent-ink:#0f151b;', '--accent-ink:#ffffff;', 1
        )
        self.assertTrue(
            any("dark accent-ink/accent contrast" in error for error in self.audit_variant(html))
        )

    def test_skip_link_must_target_the_project_collection(self) -> None:
        html = self.html.replace('href="#projects"', 'href="#methodology-heading"', 1)
        self.assertTrue(
            any("skip link must target" in error for error in self.audit_variant(html))
        )

    def test_project_articles_require_level_four_headings(self) -> None:
        html = self.html.replace("<h4>", "<h3>", 1).replace("</h4>", "</h3>", 1)
        self.assertTrue(
            any("exactly one <h4>" in error for error in self.audit_variant(html))
        )

    def test_capability_section_requires_matching_level_three_heading(self) -> None:
        html = self.html.replace(
            'aria-labelledby="capability-web-ui-e2e"',
            'aria-labelledby="capability-web-ui-e2e-missing"',
            1,
        )
        self.assertTrue(
            any(
                "must be labelled by exactly one <h3>" in error
                for error in self.audit_variant(html)
            )
        )

    def test_project_articles_must_remain_inside_capability_sections(self) -> None:
        html = self.html.replace('class="capability-group"', 'class="group-copy"', 1)
        self.assertTrue(
            any(
                "inside a named capability section" in error
                for error in self.audit_variant(html)
            )
        )

    def test_ci_link_name_must_identify_its_project(self) -> None:
        html = self.html.replace(
            'aria-label="Magento Checkout Automation CI workflow"',
            'aria-label="CI workflow"',
            1,
        )
        self.assertTrue(
            any(
                "CI link name must be project-specific" in error
                for error in self.audit_variant(html)
            )
        )

    def test_focus_visible_outline_is_enforced(self) -> None:
        html = self.html.replace("a:focus-visible", "a:focus", 1)
        self.assertTrue(
            any("a:focus-visible" in error for error in self.audit_variant(html))
        )

    def test_project_action_touch_target_is_enforced(self) -> None:
        html = self.html.replace(
            ".actions > a { min-height: 45px;",
            ".actions > a { min-height: 40px;",
            1,
        )
        self.assertTrue(
            any("at least a 44px touch target" in error for error in self.audit_variant(html))
        )

    def test_transient_external_failure_is_retried(self) -> None:
        statuses = iter([503, 200])
        delays: list[float] = []

        def opener(*_: object, **__: object) -> FakeResponse:
            return FakeResponse(next(statuses))

        SITE.check_external_url(
            "https://example.test/",
            opener=opener,
            sleeper=delays.append,
        )
        self.assertEqual(delays, [1.0])

    def test_permanent_external_failure_is_not_retried(self) -> None:
        calls = 0

        def opener(*_: object, **__: object) -> FakeResponse:
            nonlocal calls
            calls += 1
            return FakeResponse(404)

        with self.assertRaisesRegex(SITE.SiteError, "failed permanently"):
            SITE.check_external_url(
                "https://example.test/missing",
                opener=opener,
                sleeper=lambda _: None,
            )
        self.assertEqual(calls, 1)


if __name__ == "__main__":
    unittest.main()
