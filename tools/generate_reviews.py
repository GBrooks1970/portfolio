"""Publish the pinned central review snapshot with public repository links."""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REVIEWS_DATA = ROOT / "data" / "reviews.json"
DEFAULT_REVIEWS_OUTPUT = ROOT / "reviews.html"


def public_link(url: str, repositories: dict[str, str]) -> str:
    url = html.unescape(url)
    if url.startswith(("https://", "#")):
        return url
    if not url.startswith("../"):
        raise ValueError(f"Unsupported review link: {url}")
    project, separator, path = url[3:].partition("/")
    if not separator or project not in repositories or ".." in path.split("/"):
        raise ValueError(f"Unknown or unsafe review link: {url}")
    kind = "tree" if path.endswith("/") else "blob"
    return f"https://github.com/{repositories[project]}/{kind}/main/{path}"


def validate_snapshot(snapshot: dict) -> None:
    source = snapshot.get("source")
    if not isinstance(source, dict) or not source.get("repository") or not source.get("commit"):
        raise ValueError("reviews snapshot requires source repository and commit")
    commit = source["commit"]
    if not isinstance(commit, str) or re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise ValueError(f"source.commit must be a 40-character lowercase git SHA: {commit}")
    repositories = snapshot.get("repositories")
    if not isinstance(repositories, dict) or not repositories:
        raise ValueError("reviews snapshot requires repositories map")
    review_projects = snapshot.get("reviewProjects")
    if not isinstance(review_projects, list) or not review_projects:
        raise ValueError("reviews snapshot requires reviewProjects list")
    for project in review_projects:
        if project not in repositories:
            raise ValueError(f"reviewProject {project} not present in repositories map")
    html_text = snapshot.get("html", "")
    if not isinstance(html_text, str) or not html_text.strip():
        raise ValueError("reviews snapshot requires non-empty html")
    if "azure-dotnet-platform" in html_text or "azure-dotnet-platform" in review_projects:
        raise ValueError("hidden project azure-dotnet-platform must not be published in reviews")
    for project in review_projects:
        expected_anchor = f'id="review-{project}"'
        if expected_anchor not in html_text:
            raise ValueError(f"reviews html missing card anchor: {expected_anchor}")


def render(snapshot: dict) -> str:
    validate_snapshot(snapshot)
    document = re.sub(
        r'href="([^"]+)"',
        lambda match: 'href="' + html.escape(public_link(match[1], snapshot['repositories']), quote=True) + '"',
        snapshot['html'],
    )
    if '<nav aria-label="Portfolio">' not in document:
        nav_html = '<nav aria-label="Portfolio"><a href="index.html">Back to portfolio</a></nav>\n'
        if '<main class="container">' in document:
            document = document.replace('<main class="container">', f'<main class="container">\n{nav_html}', 1)
        elif '<div class="container">' in document:
            document = document.replace('<div class="container">', f'<div class="container">\n{nav_html}', 1)
    return "\n".join(line.rstrip() for line in document.splitlines()) + "\n"


def check_reviews(
    data_path: Path = DEFAULT_REVIEWS_DATA,
    output_path: Path = DEFAULT_REVIEWS_OUTPUT,
) -> None:
    snapshot = json.loads(data_path.read_text(encoding="utf-8"))
    expected = render(snapshot)
    if not output_path.exists() or output_path.read_text(encoding="utf-8") != expected:
        raise ValueError("reviews.html is stale; run python tools/generate_reviews.py")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if output is stale.")
    parser.add_argument("--data", type=Path, default=DEFAULT_REVIEWS_DATA)
    parser.add_argument("--output", type=Path, default=DEFAULT_REVIEWS_OUTPUT)
    args = parser.parse_args()
    if args.check:
        check_reviews(args.data, args.output)
    else:
        snapshot = json.loads(args.data.read_text(encoding="utf-8"))
        rendered = render(snapshot)
        args.output.write_text(rendered, encoding="utf-8", newline="\n")
    print("reviews generation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
