from __future__ import annotations

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

    def audit_variant(self, html: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text(html, encoding="utf-8", newline="\n")
            (root / "LICENSE").write_text("test", encoding="utf-8")
            _, errors = SITE.audit_document(root / "index.html", root)
            return errors

    def test_current_document_passes_static_quality_contract(self) -> None:
        summary, errors = SITE.audit_document(self.document, ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(summary.external_urls, 33)
        self.assertEqual(summary.interactive_elements, 35)
        self.assertEqual(summary.internal_references, 2)
        self.assertEqual(summary.contrast_pairs, 20)

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
        html = self.html.replace('<main class="grid"', '<div class="grid"', 1).replace(
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

    def test_project_articles_require_level_three_headings(self) -> None:
        html = self.html.replace("<h3>", "<h2>", 1).replace("</h3>", "</h2>", 1)
        self.assertTrue(
            any("exactly one <h3>" in error for error in self.audit_variant(html))
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
