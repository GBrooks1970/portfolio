from __future__ import annotations

import argparse
import re
import socket
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCUMENT = ROOT / "index.html"
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
        self.article_lines_outside_main: list[int] = []

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
        elif tag == "meta":
            if attributes.get("charset") is not None:
                self.charsets.append((attributes.get("charset") or "").strip())
            name = (attributes.get("name") or "").strip().lower()
            if name == "viewport":
                self.viewports.append((attributes.get("content") or "").strip())
            elif name == "description":
                self.descriptions.append((attributes.get("content") or "").strip())
        elif tag == "title":
            self._title_depth += 1
        elif tag == "style":
            self._style_depth += 1
        elif tag == "article" and not any(open_tag == "main" for open_tag, _ in self.stack):
            self.article_lines_outside_main.append(self.line)

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

    contrast_pairs = _validate_contrast("\n".join(parser.style_text), errors)
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
