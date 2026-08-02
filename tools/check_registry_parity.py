from __future__ import annotations

import argparse
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

from generate_site import (
    DEFAULT_MANIFEST,
    DEFAULT_OUTPUT,
    DEFAULT_REGISTRY_LOCK,
    DEFAULT_ROBOTS_OUTPUT,
    DEFAULT_SITE,
    DEFAULT_SITEMAP_OUTPUT,
    DEFAULT_TEMPLATE,
    SourceError,
    load_json,
    render_robots,
    render_site,
    render_sitemap,
    validate_sources,
)
from lock_registry import SOURCE_PATH, SOURCE_REPOSITORY, build_lock


class ParityError(ValueError):
    """Raised when upstream, landing-owned data and generated output disagree."""


class _InventoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.showcase_counts: list[str | None] = []
        self.capability_group_counts: list[str | None] = []
        self.public_evidence_counts: list[str | None] = []
        self.showcase_projects: list[str] = []
        self.showcase_assignments: list[tuple[str, str]] = []
        self.capability_groups: list[str] = []
        self.methodology_projects: list[str] = []
        self._in_methodology = False
        self._current_capability_group = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        if tag == "main" and attributes.get("id") == "projects":
            self.showcase_counts.append(attributes.get("data-showcase-count"))
            self.capability_group_counts.append(attributes.get("data-capability-group-count"))
            self.public_evidence_counts.append(attributes.get("data-public-evidence-count"))
        if tag == "section" and "capability-group" in classes:
            key = attributes.get("data-capability-group") or ""
            self.capability_groups.append(key)
            self._current_capability_group = key
        if tag == "article" and "card" in classes and attributes.get("data-project"):
            project = attributes["data-project"] or ""
            self.showcase_projects.append(project)
            self.showcase_assignments.append((project, self._current_capability_group))
        if tag == "section" and "methodology" in classes:
            self._in_methodology = True
        if tag == "p" and self._in_methodology and attributes.get("data-project"):
            self.methodology_projects.append(attributes["data-project"] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self._in_methodology:
            self._in_methodology = False
        elif tag == "section" and self._current_capability_group:
            self._current_capability_group = ""


def _duplicates(values: list[str]) -> list[str]:
    return sorted(value for value in set(values) if values.count(value) > 1)


def _validate_single_count(
    values: list[str | None], expected: int, label: str
) -> None:
    if len(values) != 1:
        raise ParityError(f"rendered page must contain exactly one {label} count marker")
    try:
        displayed = int(values[0] or "")
    except ValueError as exc:
        raise ParityError(f"rendered {label} count marker must be an integer") from exc
    if displayed != expected:
        raise ParityError(f"rendered {label} count is {displayed}; manifest requires {expected}")


def validate_rendered_inventory(
    rendered: str,
    registry: dict[str, dict[str, str]],
    manifest: dict[str, Any],
) -> None:
    parser = _InventoryParser()
    parser.feed(rendered)

    expected_showcase = {
        project for project, row in registry.items() if row["presentation_role"] == "showcase"
    }
    expected_methodology = {
        project for project, row in registry.items() if row["presentation_role"] == "methodology"
    }

    duplicate_showcase = _duplicates(parser.showcase_projects)
    duplicate_methodology = _duplicates(parser.methodology_projects)
    if duplicate_showcase or duplicate_methodology:
        parts = []
        if duplicate_showcase:
            parts.append("duplicate showcase projects: " + ", ".join(duplicate_showcase))
        if duplicate_methodology:
            parts.append("duplicate methodology projects: " + ", ".join(duplicate_methodology))
        raise ParityError("; ".join(parts))

    actual_showcase = set(parser.showcase_projects)
    actual_methodology = set(parser.methodology_projects)
    if actual_showcase != expected_showcase:
        raise ParityError(
            "rendered showcase projects differ from manifest roles: "
            f"expected {sorted(expected_showcase)}, found {sorted(actual_showcase)}"
        )
    if actual_methodology != expected_methodology:
        raise ParityError(
            "rendered methodology projects differ from manifest roles: "
            f"expected {sorted(expected_methodology)}, found {sorted(actual_methodology)}"
        )

    groups = manifest["capabilityGroups"]
    projects = manifest["projects"]
    expected_groups = [
        key for key, _ in sorted(groups.items(), key=lambda item: (item[1]["order"], item[0]))
    ]
    if parser.capability_groups != expected_groups:
        raise ParityError(
            "rendered capability groups differ from manifest order: "
            f"expected {expected_groups}, found {parser.capability_groups}"
        )
    expected_assignments = {
        project: projects[project]["group"] for project in expected_showcase
    }
    actual_assignments = dict(parser.showcase_assignments)
    if actual_assignments != expected_assignments:
        raise ParityError(
            "rendered capability assignments differ from manifest: "
            f"expected {sorted(expected_assignments.items())}, "
            f"found {sorted(actual_assignments.items())}"
        )

    public_evidence_count = sum(
        projects[project]["actions"][field] is not None
        for project in expected_showcase
        for field in ("demo", "report")
    )
    _validate_single_count(parser.showcase_counts, len(expected_showcase), "showcase")
    _validate_single_count(parser.capability_group_counts, len(groups), "capability group")
    _validate_single_count(
        parser.public_evidence_counts, public_evidence_count, "public evidence"
    )


def validate_registry_lock(
    committed_lock: dict[str, Any], canonical_lock: dict[str, Any]
) -> None:
    if committed_lock == canonical_lock:
        return

    committed_rows = {
        row["project"]: row
        for row in committed_lock.get("projects", [])
        if isinstance(row, dict) and isinstance(row.get("project"), str)
    }
    canonical_rows = {row["project"]: row for row in canonical_lock["projects"]}
    missing = sorted(set(canonical_rows) - set(committed_rows))
    extra = sorted(set(committed_rows) - set(canonical_rows))
    changed = sorted(
        project
        for project in set(committed_rows) & set(canonical_rows)
        if committed_rows[project] != canonical_rows[project]
    )
    details = []
    if missing:
        details.append("missing from lock: " + ", ".join(missing))
    if extra:
        details.append("unknown in lock: " + ", ".join(extra))
    if changed:
        details.append("changed fields: " + ", ".join(changed))
    if committed_lock.get("source") != canonical_lock.get("source"):
        details.append("source metadata differs")
    suffix = "; ".join(details) or "serialised lock differs"
    raise ParityError(
        "registry lock does not match its recorded canonical source ("
        + suffix
        + "); refresh the lock and regenerate the site"
    )


def check_registry_parity(
    registry_repository: Path,
    manifest_path: Path = DEFAULT_MANIFEST,
    registry_lock_path: Path = DEFAULT_REGISTRY_LOCK,
    site_path: Path = DEFAULT_SITE,
    template_path: Path = DEFAULT_TEMPLATE,
    output_path: Path = DEFAULT_OUTPUT,
    sitemap_path: Path = DEFAULT_SITEMAP_OUTPUT,
    robots_path: Path = DEFAULT_ROBOTS_OUTPUT,
) -> tuple[int, int]:
    manifest = load_json(manifest_path)
    committed_lock = load_json(registry_lock_path)
    site = load_json(site_path)

    # Validate the committed pair first so local authoring errors remain specific and actionable.
    validate_sources(manifest, committed_lock)
    source = committed_lock.get("source")
    if not isinstance(source, dict):
        raise ParityError("registry lock must record source metadata")
    if source.get("repository") != SOURCE_REPOSITORY or source.get("path") != SOURCE_PATH:
        raise ParityError(
            f"registry source must be {SOURCE_REPOSITORY} at {SOURCE_PATH}"
        )

    canonical_lock = build_lock(registry_repository.resolve(), str(source.get("commit", "")))
    validate_registry_lock(committed_lock, canonical_lock)
    _, _, registry = validate_sources(manifest, canonical_lock)

    rendered = render_site(
        template_path.read_text(encoding="utf-8"), manifest, canonical_lock, site
    )
    validate_rendered_inventory(rendered, registry, manifest)
    if output_path.read_bytes() != rendered.encode("utf-8"):
        raise ParityError("index.html is stale; run python tools/generate_site.py")
    if sitemap_path.read_bytes() != render_sitemap(site).encode("utf-8"):
        raise ParityError("sitemap.xml is stale; run python tools/generate_site.py")
    if robots_path.read_bytes() != render_robots(site).encode("utf-8"):
        raise ParityError("robots.txt is stale; run python tools/generate_site.py")

    showcase_count = sum(
        row["presentation_role"] == "showcase" for row in registry.values()
    )
    methodology_count = sum(
        row["presentation_role"] == "methodology" for row in registry.values()
    )
    return showcase_count, methodology_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify canonical registry, landing manifest and generated HTML parity."
    )
    parser.add_argument(
        "--registry-repository",
        type=Path,
        required=True,
        help="Clean/full-history checkout of NeoCognitus70/portfolio-prompts.",
    )
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--registry-lock", type=Path, default=DEFAULT_REGISTRY_LOCK)
    parser.add_argument("--site", type=Path, default=DEFAULT_SITE)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sitemap", type=Path, default=DEFAULT_SITEMAP_OUTPUT)
    parser.add_argument("--robots", type=Path, default=DEFAULT_ROBOTS_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        showcase_count, methodology_count = check_registry_parity(
            args.registry_repository,
            args.manifest,
            args.registry_lock,
            args.site,
            args.template,
            args.output,
            args.sitemap,
            args.robots,
        )
    except (
        OSError,
        ParityError,
        RuntimeError,
        SourceError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"registry-parity: ERROR — {exc}", file=sys.stderr)
        return 2
    print(
        "registry-parity: PASS — "
        f"{showcase_count} showcase and {methodology_count} methodology projects match "
        "the canonical registry, manifest and generated page"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
