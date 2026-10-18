"""Publish the pinned central review snapshot with public repository links."""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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


def render(snapshot: dict) -> str:
    document = re.sub(
        r'href="([^"]+)"',
        lambda match: 'href="' + html.escape(public_link(match[1], snapshot['repositories']), quote=True) + '"',
        snapshot['html'],
    )
    # Prefer the explicit overall grade over the central parser's table-header match.
    for card in re.findall(r'<div class="card">(.*?)(?=<div class="card">|\Z)', document, re.S):
        project = re.search(r'<h3>([^<]+)', card)
        grade = re.search(r'Overall Grade:\s*([A-F][+-]?)\b', card)
        if project and grade:
            name, value = project[1].strip(), grade[1]
            row = re.compile(r'<tr>\s*<td><code>' + re.escape(name) + r'</code></td>.*?</tr>', re.S)
            def correct_row(match):
                cells = list(re.finditer(r'<td>.*?</td>', match[0], re.S))
                if len(cells) != 7:
                    raise ValueError('Expected seven review matrix columns')
                cell = cells[5]
                return match[0][:cell.start()] + '<td><code>' + value + '</code></td>' + match[0][cell.end():]
            document = row.sub(correct_row, document)
            corrected = re.sub(r'(<strong>Grade:</strong>\s*<code>)[^<]+', lambda m: m[1] + value, card, count=1)
            document = document.replace(card, corrected)
    document = re.sub(r'\s*<p>Generation audit:.*?</p>', '', document, flags=re.S)
    document = document.replace('Coverage and Generation Audit', 'Review snapshot coverage')
    document = document.replace('<div class="container">', '<div class="container">\n<nav aria-label="Portfolio"><a href="index.html">Back to portfolio</a></nav>', 1)
    document = document.replace('<table>', '<div class="table-scroll" tabindex="0" role="region" aria-label="Latest reviews matrix"><table>')
    document = document.replace('</table>', '</table></div>')
    style = """
    * { box-sizing: border-box; }
    .container { min-width: 0; }
    .table-scroll { max-width: 100%; overflow-x: auto; }
    .card, p, h3, code, a { overflow-wrap: anywhere; }
    a:focus-visible, summary:focus-visible, .table-scroll:focus-visible { outline: 3px solid #fbbf24; outline-offset: 3px; }
    nav { margin-bottom: 1.5rem; }
    @media (max-width: 600px) { body { padding: 1rem; } .card { padding: 1rem; } }
"""
    document = document.replace('</style>', style + '</style>', 1)
    return '\n'.join(line.rstrip() for line in document.splitlines()) + '\n'


def check_reviews() -> None:
    snapshot = json.loads((ROOT / 'data/reviews.json').read_text(encoding='utf-8'))
    expected = render(snapshot)
    if (ROOT / 'reviews.html').read_text(encoding='utf-8') != expected:
        raise ValueError('reviews.html is stale; run python tools/generate_reviews.py')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.check:
        check_reviews()
    else:
        snapshot = json.loads((ROOT / 'data/reviews.json').read_text(encoding='utf-8'))
        (ROOT / 'reviews.html').write_text(render(snapshot), encoding='utf-8', newline='\n')
    print('reviews generation: PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
