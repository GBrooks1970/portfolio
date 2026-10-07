"""Rewrite data/learning-paths.json from the source repository's generated Learning Paths page.

    python tools/refresh_learning_paths_snapshot.py --source <PORTFOLIO_LEARNING_PATHS.html> \\
        --commit <full SHA that last changed the document> --item LAND-<n>
    python tools/refresh_learning_paths_snapshot.py --source <...html> --check

The source page marks its document with <!-- doc:begin --> and <!-- doc:end -->, and carries the theme style, the two
scripts and the switch. Nothing is guessed: a missing marker, script, style or switch is an error. The full procedure is
in docs/learning-paths-refresh.md.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / "data" / "learning-paths.json"
SCHEMA_VERSION = 2


def extract(source_html: str) -> dict:
    """Pull the snapshot fields out of the source page; raise ValueError naming whatever is missing."""
    text = source_html.replace("\r\n", "\n")
    for marker in ("<!-- doc:begin -->", "<!-- doc:end -->"):
        if text.count(marker) != 1:
            raise ValueError(f"Expected exactly one {marker} in the source page, found {text.count(marker)}")
    begin = text.index("<!-- doc:begin -->") + len("<!-- doc:begin -->")
    end = text.index("<!-- doc:end -->")
    if end < begin:
        raise ValueError("<!-- doc:end --> comes before <!-- doc:begin -->")

    title = re.search(r"<title>(.*?)</title>", text, re.S)
    style = re.search(r"<style>(.*?)</style>", text, re.S)
    head = re.search(r"<head>(.*?)</head>", text, re.S)
    topbar = re.search(r'<header class="topbar">(.*?)</header>', text, re.S)
    if not (title and style and head and topbar):
        raise ValueError("The source page is missing its title, style, head or top bar")
    pre_paint = re.findall(r"<script>(.*?)</script>", head.group(1), re.S)
    after_head = text[head.end():]
    toggle = re.findall(r"<script>(.*?)</script>", after_head, re.S)
    if len(pre_paint) != 1 or len(toggle) != 1:
        raise ValueError(f"Expected one script in <head> and one after it, found {len(pre_paint)} and {len(toggle)}")
    button = topbar.group(1).strip()
    if 'id="theme-toggle"' not in button:
        raise ValueError("The source page's top bar has no theme switch (id=theme-toggle)")
    return {
        "title": html.unescape(title.group(1)).strip(),
        "style": style.group(1).strip(),
        "scripts": {"prePaint": pre_paint[0].strip(), "toggle": toggle[0].strip()},
        "topbarButton": button,
        "html": text[begin:end].strip() + "\n",
    }


def validate_arguments(commit: str, item: str, refreshed: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("--commit must be a full 40-character lower-case SHA")
    if not re.fullmatch(r"LAND-\d+", item):
        raise ValueError("--item must look like LAND-14")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z", refreshed):
        raise ValueError("--refreshed must look like 2026-10-07T18:00Z")


def build_snapshot(old: dict, extracted: dict, commit: str, item: str, refreshed: str) -> dict:
    validate_arguments(commit, item, refreshed)
    source = old["source"]
    return {
        "schemaVersion": SCHEMA_VERSION,
        "source": {
            "repository": source["repository"],
            "path": source["path"],
            "commit": commit,
            "note": source["note"],
        },
        "snapshot": {"refreshed": refreshed, "item": item},
        "title": extracted["title"],
        "style": extracted["style"],
        "scripts": extracted["scripts"],
        "topbarButton": extracted["topbarButton"],
        "html": extracted["html"],
    }


def dumps(snapshot: dict) -> str:
    """The file's layout: one-space indent, non-ASCII kept, a trailing newline."""
    return json.dumps(snapshot, indent=1, ensure_ascii=False) + "\n"


def matches_source(committed: dict, extracted: dict) -> list[str]:
    """Names of the extractable fields whose committed value differs from the source page."""
    return [key for key in ("title", "style", "scripts", "topbarButton", "html") if committed.get(key) != extracted[key]]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source", required=True, type=Path, help="the source repository's generated Learning Paths .html")
    parser.add_argument("--commit", help="full SHA of the commit that last changed the source document")
    parser.add_argument("--item", help="the backlog item doing the refresh, e.g. LAND-14")
    parser.add_argument("--refreshed", default=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"), help="UTC timestamp (default: now)")
    parser.add_argument("--check", action="store_true", help="compare the committed snapshot with the source page; change nothing")
    args = parser.parse_args(argv)

    extracted = extract(args.source.read_text(encoding="utf-8"))
    old = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    if args.check:
        differing = matches_source(old, extracted)
        if differing:
            print(f"refresh-learning-paths: the snapshot differs from the source in: {', '.join(differing)}", file=sys.stderr)
            return 1
        print("refresh-learning-paths: the snapshot matches the source page")
        return 0
    if not (args.commit and args.item):
        parser.error("--commit and --item are required unless --check is given")
    snapshot = build_snapshot(old, extracted, args.commit, args.item, args.refreshed)
    SNAPSHOT.write_text(dumps(snapshot), encoding="utf-8", newline="\n")
    print(f"refresh-learning-paths: wrote {SNAPSHOT.name} (commit {args.commit[:7]}, {args.item}, {args.refreshed})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
