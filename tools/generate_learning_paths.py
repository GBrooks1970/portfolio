"""Publish the pinned Learning Paths snapshot as a standalone public page.

The snapshot (data/learning-paths.json) is rebuilt from the source repository's generated page by
tools/refresh_learning_paths_snapshot.py; the procedure is in docs/learning-paths-refresh.md.
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "learning-paths.html"
SOURCE = ROOT / "data" / "learning-paths.json"
PRIVATE_SOURCE_HOST = "github.com/GBrooks1970/test-automation-portfolio"
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
# The landing page puts 'Back to portfolio' on the left of the top bar and keeps the source's switch on the right.
EXTRA_CSS = (
    "  .topbar { justify-content: space-between; gap: 12px; }\n"
    "  nav.back { font-size: 0.9rem; }"
)


def public_link(url: str) -> str | None:
    """Return a public href, or None when the link targets a private file and must become text."""
    url = html.unescape(url)
    if url.startswith("#"):
        return url
    if url.startswith("https://"):
        if PRIVATE_SOURCE_HOST in url:
            return None
        return url
    if re.fullmatch(r"[A-Za-z0-9_.-]+\.(?:md|html)", url):
        return None
    raise ValueError(f"Unsupported Learning Paths link: {url}")


def format_timestamp(iso: str) -> str:
    """'2026-10-07T17:53Z' -> '7 October 2026, 17:53 UTC'."""
    match = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})T(\d{2}:\d{2})Z", iso)
    if not match:
        raise ValueError(f"Unsupported timestamp: {iso}")
    year, month, day, clock = match.groups()
    return f"{int(day)} {MONTHS[int(month) - 1]} {year}, {clock} UTC"


def snapshot_row(snapshot: dict) -> str:
    source = snapshot["source"]
    stamp = snapshot["snapshot"]
    return (
        "<div><dt>Public snapshot</dt><dd>Pinned from document commit "
        f'<code title="{html.escape(source["commit"], quote=True)}">{html.escape(source["commit"][:7])}</code>; '
        f"refreshed {html.escape(format_timestamp(stamp['refreshed']))} ({html.escape(stamp['item'])}).</dd></div>\n"
    )


def render(snapshot: dict) -> str:
    def rewrite(match: re.Match[str]) -> str:
        target = public_link(match[1])
        label = match[2]
        if target is None:
            return label
        return f'<a href="{html.escape(target, quote=True)}">{label}</a>'

    body = re.sub(r'<a href="([^"]+)">(.*?)</a>', rewrite, snapshot["html"], flags=re.S)
    if "</dl>" not in body:
        raise ValueError("The snapshot has no metadata block to carry the public snapshot row")
    body = body.replace("</dl>", snapshot_row(snapshot) + "</dl>", 1)
    source = snapshot["source"]
    provenance = (
        '<footer class="doc">\n'
        f"Pinned snapshot of <code>{html.escape(source['path'])}</code> in the private repository "
        f"<code>{html.escape(source['repository'])}</code> at commit <code>{html.escape(source['commit'][:7])}</code>. "
        "Documents it refers to (the Tool Atlas, the outline and the maintenance guide) are in that repository and are not linked here. "
        "Edit the source and refresh <code>data/learning-paths.json</code>; never edit this page by hand.\n"
        "</footer>"
    )
    document = (
        "<!doctype html>\n"
        '<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(snapshot['title'])}</title>\n"
        f"<style>\n{snapshot['style']}\n{EXTRA_CSS}\n</style>\n"
        f"<script>{snapshot['scripts']['prePaint']}</script>\n"
        "</head>\n<body>\n"
        '<div class="wrap">\n'
        '<header class="topbar"><nav class="back" aria-label="Portfolio"><a href="index.html">Back to portfolio</a></nav>'
        f"{snapshot['topbarButton']}</header>\n"
        f"{body}\n{provenance}\n</div>\n"
        f"<script>\n{snapshot['scripts']['toggle']}\n</script>\n"
        "</body>\n</html>\n"
    )
    return "\n".join(line.rstrip() for line in document.splitlines()) + "\n"


def load() -> dict:
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def check_learning_paths() -> None:
    if PAGE.read_text(encoding="utf-8") != render(load()):
        raise ValueError("learning-paths.html is stale; run python tools/generate_learning_paths.py")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        check_learning_paths()
    else:
        PAGE.write_text(render(load()), encoding="utf-8", newline="\n")
    print("learning-paths generation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
