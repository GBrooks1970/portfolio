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
    DEFAULT_TEMPLATE,
    SourceError,
    load_json,
    render_site,
    validate_sources,
)
from lock_registry import SOURCE_PATH, SOURCE_REPOSITORY, build_lock


class ParityError(ValueError):
    """Raised when upstream, landing-owned data and generated output disagree."""


class _InventoryParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.showcase_counts: list[str | None] = []
        self.showcase_projects: list[str] = []
        self.methodology_projects: list[str] = []
        self._in_methodology = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = set((attributes.get("class") or "").split())
        if tag == "main" and "grid" in classes:
            self.showcase_counts.append(attributes.get("data-showcase-count"))
        if tag == "article" and "card" in classes and attributes.get("data-project"):
            self.showcase_projects.append(attributes["data-project"] or "")
        if tag == "section" and "methodology" in classes:
            self._in_methodology = True
        if tag == "p" and self._in_methodology and attributes.get("data-project"):
            self.methodology_projects.append(attributes["data-project"] or "")

    def handle_endtag(self, tag: str) -> None:
        if tag == "section" and self._in_methodology:
            self._in_methodology = False


def _duplicates(values: list[str]) -> list[str]:
    return sorted(value for value in set(values) if values.count(value) > 1)


def validate_rendered_inventory(rendered: str, registry: dict[str, dict[str, str]]) -> None:
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

    if len(parser.showcase_counts) != 1:
        raise ParityError("rendered page must contain exactly one showcase count marker")
    try:
        displayed_count = int(parser.showcase_counts[0] or "")
    except ValueError as exc:
        raise ParityError("rendered showcase count marker must be an integer") from exc
    if displayed_count != len(expected_showcase):
        raise ParityError(
            f"rendered showcase count is {displayed_count}; manifest requires "
            f"{len(expected_showcase)}"
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
    template_path: Path = DEFAULT_TEMPLATE,
    output_path: Path = DEFAULT_OUTPUT,
) -> tuple[int, int]:
    manifest = load_json(manifest_path)
    committed_lock = load_json(registry_lock_path)

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
    _, registry = validate_sources(manifest, canonical_lock)

    rendered = render_site(
        template_path.read_text(encoding="utf-8"), manifest, canonical_lock
    )
    validate_rendered_inventory(rendered, registry)
    if output_path.read_bytes() != rendered.encode("utf-8"):
        raise ParityError("index.html is stale; run python tools/generate_site.py")

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
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        showcase_count, methodology_count = check_registry_parity(
            args.registry_repository,
            args.manifest,
            args.registry_lock,
            args.template,
            args.output,
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
