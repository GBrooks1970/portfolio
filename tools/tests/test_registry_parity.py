from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import check_registry_parity as PARITY  # noqa: E402
import generate_site as GENERATE  # noqa: E402


class RegistryParityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = GENERATE.load_json(ROOT / "data" / "presentation.json")
        cls.registry_lock = GENERATE.load_json(ROOT / "data" / "registry-lock.json")
        cls.site = GENERATE.load_json(ROOT / "data" / "site.json")
        cls.template = (ROOT / "index.template.html").read_text(encoding="utf-8")
        cls.rendered = GENERATE.render_site(
            cls.template, cls.manifest, cls.registry_lock, cls.site
        )

    def test_missing_public_project_is_rejected(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        del manifest["projects"]["parabank-bank-automation"]
        with self.assertRaisesRegex(GENERATE.SourceError, "missing public projects"):
            GENERATE.validate_sources(manifest, self.registry_lock)

    def test_extra_unknown_project_is_rejected(self) -> None:
        manifest = copy.deepcopy(self.manifest)
        manifest["projects"]["unknown-project"] = copy.deepcopy(
            manifest["projects"]["parabank-bank-automation"]
        )
        with self.assertRaisesRegex(GENERATE.SourceError, "unknown or hidden projects"):
            GENERATE.validate_sources(manifest, self.registry_lock)

    def test_duplicate_registry_project_is_rejected(self) -> None:
        registry_lock = copy.deepcopy(self.registry_lock)
        registry_lock["projects"].append(copy.deepcopy(registry_lock["projects"][0]))
        with self.assertRaisesRegex(GENERATE.SourceError, "duplicate registry project"):
            GENERATE.validate_sources(self.manifest, registry_lock)

    def test_hidden_project_is_excluded_and_cannot_enter_manifest(self) -> None:
        registry_lock = copy.deepcopy(self.registry_lock)
        registry_lock["projects"].append(
            {
                "project": "private-evidence",
                "github": "example/private-evidence",
                "presentation_role": "hidden",
            }
        )
        _, _, registry = GENERATE.validate_sources(self.manifest, registry_lock)
        rendered = GENERATE.render_site(
            self.template, self.manifest, registry_lock, self.site
        )
        PARITY.validate_rendered_inventory(rendered, registry, self.manifest)
        self.assertNotIn("private-evidence", rendered)

        manifest = copy.deepcopy(self.manifest)
        manifest["projects"]["private-evidence"] = copy.deepcopy(
            manifest["projects"]["parabank-bank-automation"]
        )
        with self.assertRaisesRegex(GENERATE.SourceError, "unknown or hidden projects"):
            GENERATE.validate_sources(manifest, registry_lock)

    def test_methodology_project_is_not_counted_as_showcase(self) -> None:
        _, _, registry = GENERATE.validate_sources(self.manifest, self.registry_lock)
        PARITY.validate_rendered_inventory(self.rendered, registry, self.manifest)
        self.assertNotIn(
            '<article class="card" data-project="portfolio-prompts">', self.rendered
        )
        self.assertIn('<div class="approach" data-project="portfolio-prompts">', self.rendered)

        incorrectly_counted = self.rendered.replace(
            '<div class="approach" data-project="portfolio-prompts">',
            '<article class="card" data-project="portfolio-prompts">',
            1,
        )
        with self.assertRaisesRegex(PARITY.ParityError, "showcase projects differ"):
            PARITY.validate_rendered_inventory(incorrectly_counted, registry, self.manifest)

    def test_displayed_showcase_count_must_match_manifest_roles(self) -> None:
        _, _, registry = GENERATE.validate_sources(self.manifest, self.registry_lock)
        wrong_count = self.rendered.replace(
            'data-showcase-count="10"', 'data-showcase-count="9"', 1
        )
        with self.assertRaisesRegex(PARITY.ParityError, "manifest requires 10"):
            PARITY.validate_rendered_inventory(wrong_count, registry, self.manifest)

    def test_rendered_capability_group_order_must_match_manifest(self) -> None:
        _, _, registry = GENERATE.validate_sources(self.manifest, self.registry_lock)
        wrong_order = self.rendered.replace(
            'data-capability-group="web-ui-e2e"',
            'data-capability-group="api-bdd-protocols"',
            1,
        )
        with self.assertRaisesRegex(PARITY.ParityError, "capability groups differ"):
            PARITY.validate_rendered_inventory(wrong_order, registry, self.manifest)

    def test_rendered_capability_assignment_must_match_manifest(self) -> None:
        _, _, registry = GENERATE.validate_sources(self.manifest, self.registry_lock)
        changed_manifest = copy.deepcopy(self.manifest)
        changed_manifest["projects"]["calculator-screenplay-bdd"]["group"] = (
            "multi-stack-frameworks"
        )
        with self.assertRaisesRegex(PARITY.ParityError, "assignments differ"):
            PARITY.validate_rendered_inventory(
                self.rendered, registry, changed_manifest
            )

    def test_rendered_generated_counts_must_match_manifest(self) -> None:
        _, _, registry = GENERATE.validate_sources(self.manifest, self.registry_lock)
        wrong_group_count = self.rendered.replace(
            'data-capability-group-count="5"', 'data-capability-group-count="4"', 1
        )
        with self.assertRaisesRegex(PARITY.ParityError, "capability group count is 4"):
            PARITY.validate_rendered_inventory(wrong_group_count, registry, self.manifest)

        wrong_evidence_count = self.rendered.replace(
            'data-public-evidence-count="9"', 'data-public-evidence-count="8"', 1
        )
        with self.assertRaisesRegex(PARITY.ParityError, "public evidence count is 8"):
            PARITY.validate_rendered_inventory(wrong_evidence_count, registry, self.manifest)

    def test_registry_lock_drift_is_rejected(self) -> None:
        committed_lock = copy.deepcopy(self.registry_lock)
        # The lock is sorted by project id, so which role sits at index 0 changes as
        # projects are onboarded. Derive a role that differs from the current one instead
        # of hard-coding one, or the mutation silently becomes a no-op and the test passes
        # without ever exercising drift detection.
        first = committed_lock["projects"][0]
        first["presentation_role"] = (
            "showcase" if first["presentation_role"] != "showcase" else "methodology"
        )
        with self.assertRaisesRegex(PARITY.ParityError, "changed fields"):
            PARITY.validate_registry_lock(committed_lock, self.registry_lock)


if __name__ == "__main__":
    unittest.main()
