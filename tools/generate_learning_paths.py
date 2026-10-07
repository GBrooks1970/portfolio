"""Publish the pinned Learning Paths snapshot as a standalone public page."""
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


def public_link(url: str) -> str | None:
    """Return a public href, or None when the link targets a private file and must become text."""
    url = html.unescape(url)
    if url.startswith("#"):
        return url
    if url.startswith("https://"):
        if PRIVATE_SOURCE_HOST in url:
            return None
        return url
    if re.fullmatch(r"[A-Za-z0-9_.-]+\.md", url):
        return None
    raise ValueError(f"Unsupported Learning Paths link: {url}")


def render(snapshot: dict) -> str:
    def rewrite(match: re.Match[str]) -> str:
        target = public_link(match[1])
        label = match[2]
        if target is None:
            return label
        return f'<a href="{html.escape(target, quote=True)}">{label}</a>'

    body = re.sub(r'<a href="([^"]+)">(.*?)</a>', rewrite, snapshot["html"], flags=re.S)
    body = body.replace("<table>", '<div class="table-scroll" tabindex="0" role="region" aria-label="Learning Paths stages"><table>')
    body = body.replace("</table>", "</table></div>")
    source = snapshot["source"]
    provenance = (
        '<footer class="doc">\n'
        f"Pinned snapshot of <code>{html.escape(source['path'])}</code> in the private repository "
        f"<code>{html.escape(source['repository'])}</code> at commit <code>{html.escape(source['commit'][:7])}</code>. "
        "Documents it refers to (the Tool Atlas and the outline) are in that repository and are not linked here. "
        "Edit the source and refresh <code>data/learning-paths.json</code>; never edit this page by hand.\n"
        "</footer>"
    )
    extra = (
        "\n  .table-scroll { max-width: 100%; overflow-x: auto; }"
        "\n  .table-scroll:focus-visible, a:focus-visible { outline: 3px solid #fbbf24; outline-offset: 3px; }"
        "\n  nav.back { margin-bottom: 1.5rem; font-size: 0.9rem; }"
        "\n  @media (max-width: 600px) { .wrap { padding: 24px 16px 64px; } }"
    )
    document = (
        "<!doctype html>\n"
        '<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{html.escape(snapshot['title'])}</title>\n"
        f"<style>\n{snapshot['style']}{extra}\n</style>\n</head>\n<body>\n"
        '<div class="wrap">\n<nav class="back" aria-label="Portfolio"><a href="index.html">Back to portfolio</a></nav>\n'
        f"{body}\n{provenance}\n</div>\n</body>\n</html>\n"
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
