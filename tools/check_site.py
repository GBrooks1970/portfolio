from __future__ import annotations

import argparse
import json
import re
import socket
import sys
import time
import xml.etree.ElementTree as ElementTree
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

from generate_site import SourceError, load_json, validate_site


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCUMENT = ROOT / "index.html"
DEFAULT_SITE = ROOT / "data" / "site.json"
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
INTERACTIVE_ELEMENTS = {"a", "button", "input", "select", "summary", "textarea"}
TRANSIENT_HTTP_STATUSES = {408, 425, 429, 500, 502, 503, 504}
CONTRAST_THRESHOLD = 4.5
CONTRAST_PAIRS = (
    ("ink", "bg"),
    ("muted", "bg"),
    ("ink", "card"),
    ("muted", "card"),
    ("chip-ink", "chip"),
    ("accent", "bg"),
    ("accent", "card"),
    ("accent-ink", "accent"),
    ("focus", "bg"),
    ("focus", "card"),
)


class SiteError(ValueError):
    """Raised when the committed site violates its publication contract."""


@dataclass
class InteractiveElement:
    tag: str
    line: int
    aria_label: str = ""
    text: list[str] = field(default_factory=list)
    image_alts: list[str] = field(default_factory=list)

    @property
    def accessible_name(self) -> str:
        if self.aria_label.strip():
            return self.aria_label.strip()
        return " ".join(" ".join(self.text + self.image_alts).split())


@dataclass(frozen=True)
class Reference:
    value: str
    line: int
    attribute: str


@dataclass(frozen=True)
class SiteSummary:
    identifiers: int
    interactive_elements: int
    internal_references: int
    external_urls: int
    contrast_pairs: int


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.errors: list[str] = []
        self.stack: list[tuple[str, int]] = []
        self.counts: Counter[str] = Counter()
        self.doctypes = 0
        self.identifiers: dict[str, int] = {}
        self.references: list[Reference] = []
        self.label_references: list[tuple[str, int]] = []
        self.interactive_elements: list[InteractiveElement] = []
        self._interactive_stack: list[InteractiveElement] = []
        self._title_depth = 0
        self.title_text: list[str] = []
        self._style_depth = 0
        self.style_text: list[str] = []
        self.html_languages: list[str] = []
        self.charsets: list[str] = []
        self.viewports: list[str] = []
        self.descriptions: list[str] = []
        self.named_metadata: list[tuple[str, str, int]] = []
        self.property_metadata: list[tuple[str, str, int]] = []
        self.link_elements: list[tuple[set[str], dict[str, str], int]] = []
        self.json_ld_documents: list[tuple[str, int]] = []
        self._json_ld_depth = 0
        self._json_ld_line = 0
        self._json_ld_text: list[str] = []
        self._body_depth = 0
        self.visible_text: list[str] = []
        self.article_lines_outside_main: list[int] = []
        self.article_lines_outside_capability_group: list[int] = []
        self.skip_links: list[tuple[str, int]] = []
        self.main_landmarks: list[dict[str, str | None]] = []
        self.capability_sections: list[tuple[str, str, int]] = []
        self.capability_headings: list[tuple[str, str, int]] = []
        self._current_capability_group = ""
        self.project_headings: list[tuple[int, set[str], bool]] = []
        self.project_heading_text: list[str] = []
        self._project_heading_depth = 0
        self.headings: list[tuple[int, int, bool]] = []
        self.ci_badges: list[tuple[int, str, str]] = []

    @property
    def line(self) -> int:
        return self.getpos()[0]

    def handle_decl(self, decl: str) -> None:
        if decl.strip().lower() == "doctype html":
            self.doctypes += 1
        else:
            self.errors.append(f"line {self.line}: unsupported declaration <!{decl}>")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_start(tag.lower(), attrs, self_closing=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_start(tag.lower(), attrs, self_closing=True)

    def _handle_start(
        self, tag: str, attrs: list[tuple[str, str | None]], self_closing: bool
    ) -> None:
        names = [name.lower() for name, _ in attrs]
        duplicate_attributes = sorted(name for name in set(names) if names.count(name) > 1)
        if duplicate_attributes:
            self.errors.append(
                f"line {self.line}: <{tag}> duplicates attributes "
                + ", ".join(duplicate_attributes)
            )
        attributes = {name.lower(): value for name, value in attrs}
        classes = set((attributes.get("class") or "").split())
        self.counts[tag] += 1

        identifier = (attributes.get("id") or "").strip()
        if identifier:
            if identifier in self.identifiers:
                self.errors.append(
                    f"line {self.line}: duplicate id {identifier!r}; first seen on line "
                    f"{self.identifiers[identifier]}"
                )
            else:
                self.identifiers[identifier] = self.line

        tabindex = attributes.get("tabindex")
        if tabindex is not None:
            try:
                tab_value = int(tabindex)
            except (TypeError, ValueError):
                self.errors.append(f"line {self.line}: tabindex must be an integer")
            else:
                if tab_value > 0:
                    self.errors.append(
                        f"line {self.line}: positive tabindex {tab_value} disrupts focus order"
                    )
                if tag in INTERACTIVE_ELEMENTS and tab_value < 0:
                    self.errors.append(
                        f"line {self.line}: interactive <{tag}> is removed from keyboard focus"
                    )

        if tag == "html":
            self.html_languages.append((attributes.get("lang") or "").strip())
        elif tag == "body":
            self._body_depth += 1
        elif tag == "main":
            self.main_landmarks.append(attributes)
        elif tag == "meta":
            if attributes.get("charset") is not None:
                self.charsets.append((attributes.get("charset") or "").strip())
            name = (attributes.get("name") or "").strip().lower()
            if name == "viewport":
                self.viewports.append((attributes.get("content") or "").strip())
            elif name == "description":
                self.descriptions.append((attributes.get("content") or "").strip())
            if name:
                self.named_metadata.append(
                    (name, (attributes.get("content") or "").strip(), self.line)
                )
            property_name = (attributes.get("property") or "").strip().lower()
            if property_name:
                self.property_metadata.append(
                    (property_name, (attributes.get("content") or "").strip(), self.line)
                )
        elif tag == "link":
            relations = set((attributes.get("rel") or "").lower().split())
            self.link_elements.append(
                (relations, {key: value or "" for key, value in attributes.items()}, self.line)
            )
        elif tag == "script" and (attributes.get("type") or "").lower() == "application/ld+json":
            self._json_ld_depth += 1
            self._json_ld_line = self.line
            self._json_ld_text = []
        elif tag == "title":
            self._title_depth += 1
        elif tag == "style":
            self._style_depth += 1
        elif tag == "section" and "capability-group" in classes:
            key = (attributes.get("data-capability-group") or "").strip()
            labelled_by = (attributes.get("aria-labelledby") or "").strip()
            self.capability_sections.append((key, labelled_by, self.line))
            self._current_capability_group = key
        elif tag == "article":
            if not any(open_tag == "main" for open_tag, _ in self.stack):
                self.article_lines_outside_main.append(self.line)
            if not self._current_capability_group:
                self.article_lines_outside_capability_group.append(self.line)

        if tag == "a" and "skip-link" in classes:
            self.skip_links.append(((attributes.get("href") or "").strip(), self.line))

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(tag[1])
            in_article = any(open_tag == "article" for open_tag, _ in self.stack)
            self.headings.append((level, self.line, in_article))
            if identifier == "projects-heading":
                hidden = "hidden" in attributes or bool(
                    classes & {"hidden", "sr-only", "visually-hidden"}
                )
                self.project_headings.append((self.line, classes, hidden))
                self._project_heading_depth += 1
            if level == 3 and self._current_capability_group:
                self.capability_headings.append(
                    (self._current_capability_group, identifier, self.line)
                )

        labelled_by = (attributes.get("aria-labelledby") or "").strip()
        if labelled_by:
            for target in labelled_by.split():
                self.label_references.append((target, self.line))

        for attribute in ("href", "src"):
            value = attributes.get(attribute)
            if value is not None:
                self.references.append(Reference(value.strip(), self.line, attribute))

        if tag == "img":
            alt = attributes.get("alt")
            if alt is None or not alt.strip():
                self.errors.append(f"line {self.line}: image requires non-empty alt text")
            if self._interactive_stack and alt:
                self._interactive_stack[-1].image_alts.append(alt)
            if "badge" in classes:
                link_label = (
                    self._interactive_stack[-1].aria_label
                    if self._interactive_stack
                    else ""
                )
                self.ci_badges.append((self.line, alt or "", link_label))

        if tag in INTERACTIVE_ELEMENTS:
            if tag == "a" and not (attributes.get("href") or "").strip():
                self.errors.append(f"line {self.line}: anchor is not focusable without href")
            element = InteractiveElement(
                tag=tag,
                line=self.line,
                aria_label=(attributes.get("aria-label") or ""),
            )
            self._interactive_stack.append(element)

        if tag not in VOID_ELEMENTS and not self_closing:
            self.stack.append((tag, self.line))

    def handle_data(self, data: str) -> None:
        if self._title_depth:
            self.title_text.append(data)
        if self._style_depth:
            self.style_text.append(data)
        if self._json_ld_depth:
            self._json_ld_text.append(data)
        if self._body_depth and not self._style_depth and not self._json_ld_depth:
            self.visible_text.append(data)
        if self._project_heading_depth:
            self.project_heading_text.append(data)
        if self._interactive_stack:
            self._interactive_stack[-1].text.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in VOID_ELEMENTS:
            self.errors.append(f"line {self.line}: void element <{tag}> must not have an end tag")
            return
        if not self.stack:
            self.errors.append(f"line {self.line}: unexpected closing </{tag}>")
        else:
            expected, start_line = self.stack.pop()
            if expected != tag:
                self.errors.append(
                    f"line {self.line}: closing </{tag}> does not match <{expected}> "
                    f"from line {start_line}"
                )

        if tag == "title" and self._title_depth:
            self._title_depth -= 1
        elif tag == "style" and self._style_depth:
            self._style_depth -= 1
        elif tag == "script" and self._json_ld_depth:
            self.json_ld_documents.append(
                ("".join(self._json_ld_text).strip(), self._json_ld_line)
            )
            self._json_ld_depth -= 1
            self._json_ld_text = []
        elif tag == "body" and self._body_depth:
            self._body_depth -= 1
        elif tag == "h2" and self._project_heading_depth:
            self._project_heading_depth -= 1
        elif tag == "section" and self._current_capability_group:
            self._current_capability_group = ""

        if tag in INTERACTIVE_ELEMENTS:
            if not self._interactive_stack:
                self.errors.append(f"line {self.line}: closing </{tag}> has no open control")
            else:
                element = self._interactive_stack.pop()
                if element.tag != tag:
                    self.errors.append(
                        f"line {self.line}: closing </{tag}> does not match interactive "
                        f"<{element.tag}> from line {element.line}"
                    )
                self.interactive_elements.append(element)


def _normalise_title(parts: list[str]) -> str:
    return " ".join(" ".join(parts).split())


def _parse_theme_colours(styles: str) -> dict[str, dict[str, str]]:
    root_blocks = re.findall(r":root\s*\{([^{}]*)\}", styles, flags=re.DOTALL)
    dark_match = re.search(
        r"@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root\s*\{([^{}]*)\}",
        styles,
        flags=re.DOTALL,
    )
    if not root_blocks or dark_match is None:
        raise SiteError("CSS must define light and prefers-color-scheme: dark :root variables")

    def variables(block: str) -> dict[str, str]:
        return {
            name: value.lower()
            for name, value in re.findall(
                r"--([a-z0-9-]+)\s*:\s*(#[0-9a-fA-F]{6})\b", block
            )
        }

    light = variables(root_blocks[0])
    dark = dict(light)
    dark.update(variables(dark_match.group(1)))
    return {"light": light, "dark": dark}


def _relative_luminance(colour: str) -> float:
    channels = [int(colour[index : index + 2], 16) / 255 for index in (1, 3, 5)]

    def linear(value: float) -> float:
        return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4

    red, green, blue = (linear(channel) for channel in channels)
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def contrast_ratio(foreground: str, background: str) -> float:
    lighter, darker = sorted(
        (_relative_luminance(foreground), _relative_luminance(background)), reverse=True
    )
    return (lighter + 0.05) / (darker + 0.05)


def _validate_contrast(styles: str, errors: list[str]) -> int:
    try:
        themes = _parse_theme_colours(styles)
    except SiteError as exc:
        errors.append(str(exc))
        return 0
    checked = 0
    for theme, colours in themes.items():
        for foreground, background in CONTRAST_PAIRS:
            missing = [name for name in (foreground, background) if name not in colours]
            if missing:
                errors.append(f"{theme} theme is missing colour variables: {', '.join(missing)}")
                continue
            checked += 1
            ratio = contrast_ratio(colours[foreground], colours[background])
            if ratio + 1e-9 < CONTRAST_THRESHOLD:
                errors.append(
                    f"{theme} {foreground}/{background} contrast is {ratio:.2f}:1; "
                    f"requires {CONTRAST_THRESHOLD:.1f}:1"
                )
    return checked


def _validate_navigation_contract(
    parser: SiteParser, styles: str, errors: list[str]
) -> None:
    if len(parser.skip_links) != 1:
        errors.append(
            f"document must contain exactly one skip link; found {len(parser.skip_links)}"
        )
    elif parser.skip_links[0][0] != "#projects":
        errors.append(
            f"line {parser.skip_links[0][1]}: skip link must target '#projects'"
        )

    if len(parser.main_landmarks) == 1:
        main = parser.main_landmarks[0]
        if main.get("id") != "projects":
            errors.append("main landmark must use id='projects' as the skip target")
        if main.get("aria-labelledby") != "projects-heading":
            errors.append("main landmark must be labelled by 'projects-heading'")
        if main.get("tabindex") != "-1":
            errors.append("main landmark must use tabindex='-1' for skip-link focus")

    if len(parser.project_headings) != 1:
        errors.append(
            "document must contain exactly one visible projects-heading; "
            f"found {len(parser.project_headings)}"
        )
    else:
        line, _, hidden = parser.project_headings[0]
        if hidden:
            errors.append(f"line {line}: projects-heading must remain visible")
        if not _normalise_title(parser.project_heading_text):
            errors.append(f"line {line}: projects-heading must contain visible text")

    article_headings = [
        (level, line) for level, line, in_article in parser.headings if in_article
    ]
    if len(article_headings) != parser.counts["article"] or any(
        level != 4 for level, _ in article_headings
    ):
        errors.append("each project article must contain exactly one <h4> heading")

    group_keys = [key for key, _, _ in parser.capability_sections]
    if not group_keys or any(not key for key in group_keys) or len(group_keys) != len(set(group_keys)):
        errors.append("capability sections must use unique, non-empty data-capability-group keys")
    for key, labelled_by, line in parser.capability_sections:
        headings = [
            identifier
            for heading_group, identifier, _ in parser.capability_headings
            if heading_group == key
        ]
        if len(headings) != 1 or not labelled_by or headings[0] != labelled_by:
            errors.append(
                f"line {line}: capability section {key!r} must be labelled by exactly one <h3>"
            )

    previous_level = 0
    for level, line, _ in parser.headings:
        if previous_level and level > previous_level + 1:
            errors.append(
                f"line {line}: heading level jumps from h{previous_level} to h{level}"
            )
        previous_level = level

    for line, alt, link_label in parser.ci_badges:
        if re.fullmatch(r".+\sCI status", alt.strip()) is None:
            errors.append(f"line {line}: CI badge alt text must be project-specific")
        if re.fullmatch(r".+\sCI workflow", link_label.strip()) is None:
            errors.append(f"line {line}: CI link name must be project-specific")

    focus_rule = re.search(
        r"a\s*:\s*focus-visible\s*\{[^{}]*outline\s*:\s*3px\s+solid\s+"
        r"var\(--focus\)",
        styles,
        flags=re.DOTALL,
    )
    if focus_rule is None:
        errors.append("CSS must define a 3px --focus outline for a:focus-visible")
    if re.search(
        r"\.skip-link\s*:\s*focus-visible\s*\{[^{}]*transform\s*:\s*"
        r"translateY\(0\)",
        styles,
        flags=re.DOTALL,
    ) is None:
        errors.append("CSS must reveal the skip link on :focus-visible")
    touch_target = re.search(
        r"\.actions\s*>\s*a\s*\{[^{}]*min-height\s*:\s*"
        r"([0-9]+(?:\.[0-9]+)?)px",
        styles,
        flags=re.DOTALL,
    )
    if touch_target is None or float(touch_target.group(1)) < 44:
        errors.append("CSS project actions must provide at least a 44px touch target")


def _resolve_internal_reference(
    reference: Reference, root: Path, document: Path, identifiers: set[str]
) -> str | None:
    if not reference.value:
        return f"line {reference.line}: empty {reference.attribute}"
    parsed = urlsplit(reference.value)
    if parsed.scheme:
        if parsed.scheme not in {"http", "https", "mailto"}:
            return f"line {reference.line}: unsupported URL scheme {parsed.scheme!r}"
        if parsed.scheme == "http":
            return f"line {reference.line}: external URL must use HTTPS: {reference.value}"
        return None
    if parsed.netloc:
        return f"line {reference.line}: protocol-relative URL is not allowed: {reference.value}"

    relative_path = unquote(parsed.path)
    if relative_path.startswith("/"):
        target = root / relative_path.lstrip("/")
    elif relative_path:
        target = document.parent / relative_path
    else:
        target = document
    target = target.resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return (
            f"line {reference.line}: internal reference escapes repository root: "
            f"{reference.value}"
        )
    if target.is_dir():
        target = target / "index.html"
    if not target.exists():
        return f"line {reference.line}: internal target does not exist: {reference.value}"
    if (
        parsed.fragment
        and target == document.resolve()
        and unquote(parsed.fragment) not in identifiers
    ):
        return f"line {reference.line}: fragment target does not exist: {reference.value}"
    return None


def _single_metadata(
    entries: list[tuple[str, str, int]], key: str, label: str, errors: list[str]
) -> str:
    matches = [(value, line) for name, value, line in entries if name == key]
    if len(matches) != 1:
        errors.append(f"document must contain exactly one {label}; found {len(matches)}")
        return ""
    value, line = matches[0]
    if not value:
        errors.append(f"line {line}: {label} must have non-empty content")
    return value


def _png_dimensions(path: Path) -> tuple[int, int]:
    header = path.read_bytes()[:24]
    if len(header) != 24 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise SiteError(f"asset is not a valid PNG with an IHDR header: {path}")
    return int.from_bytes(header[16:20], "big"), int.from_bytes(header[20:24], "big")


def _local_path_for_canonical_asset(url: str, canonical: str, root: Path) -> Path | None:
    parsed = urlsplit(url)
    base = urlsplit(canonical)
    if parsed.scheme != base.scheme or parsed.netloc != base.netloc:
        return None
    if not parsed.path.startswith(base.path):
        return None
    relative = unquote(parsed.path[len(base.path) :])
    if not relative:
        return None
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def _validate_png(path: Path, expected: tuple[int, int], label: str, errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"{label} does not exist: {path.relative_to(path.parents[1])}")
        return
    try:
        actual = _png_dimensions(path)
    except (OSError, SiteError) as exc:
        errors.append(str(exc))
        return
    if actual != expected:
        errors.append(f"{label} dimensions are {actual[0]}x{actual[1]}; expected {expected[0]}x{expected[1]}")


def _validate_sitemap_and_robots(site: dict[str, Any], root: Path, errors: list[str]) -> None:
    sitemap = root / "sitemap.xml"
    try:
        tree = ElementTree.parse(sitemap)
    except (OSError, ElementTree.ParseError) as exc:
        errors.append(f"sitemap.xml is missing or invalid: {exc}")
    else:
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        root_element = tree.getroot()
        locations = root_element.findall(f"{namespace}url/{namespace}loc")
        last_modified = root_element.findall(f".//{namespace}lastmod")
        if root_element.tag != f"{namespace}urlset":
            errors.append("sitemap.xml must use the sitemap urlset namespace")
        if len(locations) != 1 or (locations[0].text or "").strip() != site["canonicalUrl"]:
            errors.append("sitemap.xml must contain exactly the canonical portfolio URL")
        if last_modified:
            errors.append("sitemap.xml must not contain an unverified lastmod value")

    sitemap_url = site["canonicalUrl"] + "sitemap.xml"
    expected_robots = f"User-agent: *\nAllow: /\n\nSitemap: {sitemap_url}\n"
    robots = root / "robots.txt"
    try:
        actual_robots = robots.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"robots.txt is missing or unreadable: {exc}")
    else:
        if actual_robots != expected_robots:
            errors.append("robots.txt must allow public crawling and identify the canonical sitemap")


def _validate_structured_data(
    parser: SiteParser, site: dict[str, Any], image_url: str, errors: list[str]
) -> None:
    if len(parser.json_ld_documents) != 1:
        errors.append(
            "document must contain exactly one application/ld+json graph; "
            f"found {len(parser.json_ld_documents)}"
        )
        return
    text, line = parser.json_ld_documents[0]
    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        errors.append(f"line {line}: JSON-LD is malformed: {exc}")
        return
    graph = document.get("@graph") if isinstance(document, dict) else None
    context = document.get("@context") if isinstance(document, dict) else None
    if context != "https://schema.org" or not isinstance(graph, list):
        errors.append("JSON-LD must contain a Schema.org @graph")
        return
    typed = {
        node.get("@type"): node
        for node in graph
        if isinstance(node, dict) and isinstance(node.get("@type"), str)
    }
    if set(typed) != {"Person", "WebSite"} or len(graph) != 2:
        errors.append("JSON-LD graph must contain exactly one Person and one WebSite")
        return
    canonical = site["canonicalUrl"]
    person_id = canonical + "#person"
    expected_person = {
        "@type": "Person",
        "@id": person_id,
        "name": site["author"]["name"],
        "jobTitle": site["author"]["role"],
        "url": site["author"]["url"],
        "sameAs": site["author"]["sameAs"],
    }
    expected_website = {
        "@type": "WebSite",
        "@id": canonical + "#website",
        "url": canonical,
        "name": site["siteName"],
        "description": site["description"],
        "inLanguage": site["language"],
        "creator": {"@id": person_id},
        "image": {
            "@type": "ImageObject",
            "url": image_url,
            "width": site["socialImage"]["width"],
            "height": site["socialImage"]["height"],
        },
    }
    if typed["Person"] != expected_person:
        errors.append("JSON-LD Person must match the verified site author source exactly")
    if typed["WebSite"] != expected_website:
        errors.append("JSON-LD WebSite must match the canonical site source exactly")
    visible = " ".join(" ".join(parser.visible_text).split())
    for value in (site["author"]["name"], site["author"]["role"]):
        if value not in visible:
            errors.append(f"structured-data identity is not visible in page content: {value}")


def _validate_discoverability(
    parser: SiteParser, site: dict[str, Any], root: Path, errors: list[str]
) -> None:
    canonical = site["canonicalUrl"]
    image = site["socialImage"]
    image_url = canonical + image["path"]

    canonical_links = [
        (attributes, line)
        for relations, attributes, line in parser.link_elements
        if "canonical" in relations
    ]
    if len(canonical_links) != 1:
        errors.append(
            f"document must contain exactly one canonical link; found {len(canonical_links)}"
        )
    elif canonical_links[0][0].get("href") != canonical:
        errors.append("canonical link must match data/site.json canonicalUrl")

    expected_named = {
        "description": site["description"],
        "author": site["author"]["name"],
        "twitter:card": "summary_large_image",
        "twitter:title": site["title"],
        "twitter:description": site["description"],
        "twitter:image": image_url,
        "twitter:image:alt": image["alt"],
    }
    for key, expected in expected_named.items():
        actual = _single_metadata(parser.named_metadata, key, f"meta name={key!r}", errors)
        if actual and actual != expected:
            errors.append(f"meta name={key!r} must match data/site.json")

    expected_properties = {
        "og:type": "website",
        "og:title": site["title"],
        "og:description": site["description"],
        "og:url": canonical,
        "og:site_name": site["siteName"],
        "og:locale": site["locale"],
        "og:image": image_url,
        "og:image:secure_url": image_url,
        "og:image:type": image["type"],
        "og:image:width": str(image["width"]),
        "og:image:height": str(image["height"]),
        "og:image:alt": image["alt"],
    }
    for key, expected in expected_properties.items():
        actual = _single_metadata(
            parser.property_metadata, key, f"meta property={key!r}", errors
        )
        if actual and actual != expected:
            errors.append(f"meta property={key!r} must match data/site.json")

    title = _normalise_title(parser.title_text)
    if title and title != site["title"]:
        errors.append("document title must match data/site.json")

    icon_contract = [
        ({"icon"}, "assets/favicon.svg", "image/svg+xml", ""),
        ({"icon"}, "assets/favicon-32x32.png", "image/png", "32x32"),
        ({"apple-touch-icon"}, "assets/apple-touch-icon.png", "", "180x180"),
    ]
    for relation, href, mime_type, sizes in icon_contract:
        matches = [
            attributes
            for relations, attributes, _ in parser.link_elements
            if relations == relation and attributes.get("href") == href
        ]
        if len(matches) != 1:
            errors.append(f"document must contain exactly one icon link for {href}")
            continue
        attributes = matches[0]
        if mime_type and attributes.get("type") != mime_type:
            errors.append(f"icon {href} must declare type={mime_type!r}")
        if sizes and attributes.get("sizes") != sizes:
            errors.append(f"icon {href} must declare sizes={sizes!r}")

    local_image = _local_path_for_canonical_asset(image_url, canonical, root)
    if local_image is None:
        errors.append("social-preview URL must map to a local asset under the canonical site")
    else:
        _validate_png(
            local_image,
            (image["width"], image["height"]),
            "webpage social-preview image",
            errors,
        )
    _validate_png(root / "assets" / "favicon-32x32.png", (32, 32), "PNG favicon", errors)
    _validate_png(root / "assets" / "apple-touch-icon.png", (180, 180), "Apple touch icon", errors)
    _validate_png(
        root / site["repository"]["socialImagePath"],
        (1280, 640),
        "GitHub social-preview image",
        errors,
    )
    _validate_structured_data(parser, site, image_url, errors)
    _validate_sitemap_and_robots(site, root, errors)


def audit_document(
    document: Path = DEFAULT_DOCUMENT, root: Path = ROOT
) -> tuple[SiteSummary, list[str]]:
    html = document.read_text(encoding="utf-8")
    parser = SiteParser()
    parser.feed(html)
    parser.close()
    errors = list(parser.errors)
    if parser.stack:
        errors.extend(
            f"line {line}: unclosed <{tag}>" for tag, line in reversed(parser.stack)
        )
    if parser.doctypes != 1:
        errors.append(f"document must contain exactly one HTML5 doctype; found {parser.doctypes}")
    for tag in ("html", "head", "body", "header", "main", "footer", "h1"):
        if parser.counts[tag] != 1:
            errors.append(f"document must contain exactly one <{tag}>; found {parser.counts[tag]}")
    if parser.article_lines_outside_main:
        errors.append(
            "project articles must be inside <main>; offending lines: "
            + ", ".join(map(str, parser.article_lines_outside_main))
        )
    if parser.article_lines_outside_capability_group:
        errors.append(
            "project articles must be inside a named capability section; offending lines: "
            + ", ".join(map(str, parser.article_lines_outside_capability_group))
        )
    if parser.html_languages != ["en-GB"]:
        errors.append(f"<html> must declare lang=\"en-GB\"; found {parser.html_languages}")
    if [value.lower() for value in parser.charsets] != ["utf-8"]:
        errors.append(f"document must declare one UTF-8 charset; found {parser.charsets}")
    if len(parser.viewports) != 1 or not {
        "width=device-width",
        "initial-scale=1",
    }.issubset(
        {
            part.strip()
            for part in (parser.viewports[0] if parser.viewports else "").split(",")
        }
    ):
        errors.append("document must declare one responsive width/device initial-scale viewport")
    if len(parser.descriptions) != 1 or not parser.descriptions[0]:
        errors.append("document must declare one non-empty meta description")
    if parser.counts["title"] != 1 or not _normalise_title(parser.title_text):
        errors.append("document must contain one non-empty <title>")
    if not parser.counts["article"]:
        errors.append("main landmark must contain at least one project article")

    try:
        site = validate_site(load_json(root / "data" / "site.json"))
    except (OSError, SourceError) as exc:
        errors.append(f"site metadata source is invalid: {exc}")
    else:
        _validate_discoverability(parser, site, root.resolve(), errors)

    for target, line in parser.label_references:
        if target not in parser.identifiers:
            errors.append(f"line {line}: aria-labelledby target {target!r} does not exist")
    for element in parser.interactive_elements:
        if not element.accessible_name:
            errors.append(
                f"line {element.line}: interactive <{element.tag}> has no accessible name"
            )

    external_urls: set[str] = set()
    internal_count = 0
    for reference in parser.references:
        parsed = urlsplit(reference.value)
        if parsed.scheme in {"http", "https"}:
            external_urls.add(reference.value)
            if parsed.scheme == "http":
                errors.append(
                    f"line {reference.line}: external URL must use HTTPS: {reference.value}"
                )
            continue
        if parsed.scheme == "mailto":
            continue
        internal_count += 1
        error = _resolve_internal_reference(
            reference, root.resolve(), document.resolve(), set(parser.identifiers)
        )
        if error:
            errors.append(error)

    styles = "\n".join(parser.style_text)
    _validate_navigation_contract(parser, styles, errors)
    contrast_pairs = _validate_contrast(styles, errors)
    summary = SiteSummary(
        identifiers=len(parser.identifiers),
        interactive_elements=len(parser.interactive_elements),
        internal_references=internal_count,
        external_urls=len(external_urls),
        contrast_pairs=contrast_pairs,
    )
    return summary, errors


def check_external_url(
    url: str,
    attempts: int = 3,
    timeout: float = 15.0,
    opener: Callable[..., Any] = urlopen,
    sleeper: Callable[[float], None] = time.sleep,
) -> None:
    last_problem = "unknown failure"
    for attempt in range(1, attempts + 1):
        request = Request(
            url,
            headers={
                "User-Agent": "portfolio-quality-gate/1.0",
                "Accept": "text/html,application/xhtml+xml,image/*,*/*;q=0.8",
                "Range": "bytes=0-2047",
            },
        )
        try:
            with opener(request, timeout=timeout) as response:
                status = int(getattr(response, "status", response.getcode()))
            if 200 <= status < 400:
                return
            last_problem = f"HTTP {status}"
            transient = status in TRANSIENT_HTTP_STATUSES
        except HTTPError as exc:
            last_problem = f"HTTP {exc.code}"
            transient = exc.code in TRANSIENT_HTTP_STATUSES
        except (TimeoutError, socket.timeout, URLError, ConnectionError, OSError) as exc:
            last_problem = f"{type(exc).__name__}: {exc}"
            transient = True

        if not transient:
            raise SiteError(f"external URL failed permanently: {url} ({last_problem})")
        if attempt < attempts:
            sleeper(1.0 if attempt == 1 else 3.0)
    raise SiteError(
        f"external URL remained transiently unavailable after {attempts} attempts: "
        f"{url} ({last_problem})"
    )


def check_external_urls(urls: set[str], attempts: int = 3, timeout: float = 15.0) -> None:
    failures: list[str] = []
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(urls)))) as executor:
        futures = {
            executor.submit(check_external_url, url, attempts, timeout): url for url in sorted(urls)
        }
        for future in as_completed(futures):
            try:
                future.result()
            except SiteError as exc:
                failures.append(str(exc))
    if failures:
        raise SiteError("\n".join(sorted(failures)))


def external_urls(document: Path = DEFAULT_DOCUMENT) -> set[str]:
    parser = SiteParser()
    parser.feed(document.read_text(encoding="utf-8"))
    parser.close()
    return {
        reference.value
        for reference in parser.references
        if urlsplit(reference.value).scheme in {"http", "https"}
    }


def check_site(
    document: Path = DEFAULT_DOCUMENT,
    root: Path = ROOT,
    check_external: bool = True,
    attempts: int = 3,
    timeout: float = 15.0,
) -> SiteSummary:
    summary, errors = audit_document(document.resolve(), root.resolve())
    if errors:
        raise SiteError("site quality failures:\n- " + "\n- ".join(errors))
    if check_external:
        check_external_urls(external_urls(document), attempts=attempts, timeout=timeout)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate portfolio HTML, links, metadata and static accessibility contracts."
    )
    parser.add_argument("--document", type=Path, default=DEFAULT_DOCUMENT)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--skip-external",
        action="store_true",
        help="Run deterministic checks only; this is not equivalent to the complete CI gate.",
    )
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--timeout", type=float, default=15.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.attempts < 1 or args.timeout <= 0:
        print("site-quality: ERROR — attempts and timeout must be positive", file=sys.stderr)
        return 2
    try:
        summary = check_site(
            args.document,
            args.root,
            check_external=not args.skip_external,
            attempts=args.attempts,
            timeout=args.timeout,
        )
    except (OSError, SiteError) as exc:
        print(f"site-quality: ERROR — {exc}", file=sys.stderr)
        return 2
    external = "skipped" if args.skip_external else str(summary.external_urls)
    print(
        "site-quality: PASS — "
        f"{summary.identifiers} ids, {summary.interactive_elements} named controls, "
        f"{summary.internal_references} internal references, {external} external URLs, "
        f"{summary.contrast_pairs} contrast pairs"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
