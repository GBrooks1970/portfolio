from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from textwrap import indent
from typing import Any
from urllib.parse import urljoin, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "presentation.json"
DEFAULT_REGISTRY_LOCK = ROOT / "data" / "registry-lock.json"
DEFAULT_SITE = ROOT / "data" / "site.json"
DEFAULT_TEMPLATE = ROOT / "index.template.html"
DEFAULT_OUTPUT = ROOT / "index.html"
DEFAULT_SITEMAP_OUTPUT = ROOT / "sitemap.xml"
DEFAULT_ROBOTS_OUTPUT = ROOT / "robots.txt"
PUBLIC_ROLES = {"showcase", "methodology"}
ALLOWED_ROLES = PUBLIC_ROLES | {"hidden"}
MANIFEST_FIELDS = {"schemaVersion", "capabilityGroups", "projects"}
GROUP_FIELDS = {"label", "description", "order"}
ENTRY_FIELDS = {"title", "discipline", "summary", "order", "group", "tags", "actions"}
ACTION_FIELDS = {"workflow", "demo", "report", "documentation"}
LINK_FIELDS = {"label", "url"}
SITE_FIELDS = {
    "schemaVersion", "canonicalUrl", "title", "description", "language", "locale",
    "siteName", "author", "socialImage", "repository",
}
AUTHOR_FIELDS = {"name", "role", "url", "sameAs"}
SOCIAL_IMAGE_FIELDS = {"path", "width", "height", "type", "alt"}
REPOSITORY_FIELDS = {
    "slug", "description", "homepage", "topics", "socialImagePath",
}


class SourceError(ValueError):
    """Raised when a generated-site source violates its documented contract."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SourceError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (OSError, json.JSONDecodeError, SourceError) as exc:
        raise SourceError(f"cannot load {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SourceError(f"{path} must contain a JSON object")
    return data


def _require_text(value: Any, field: str, project: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceError(f"{project}: {field} must be a non-empty string")
    return value


def _validate_link(value: Any, field: str, project: str) -> None:
    if value is None:
        return
    if not isinstance(value, dict) or set(value) != LINK_FIELDS:
        raise SourceError(f"{project}: actions.{field} must be null or contain label and url")
    _require_text(value["label"], f"actions.{field}.label", project)
    url = _require_text(value["url"], f"actions.{field}.url", project)
    if not url.startswith("https://"):
        raise SourceError(f"{project}: actions.{field}.url must use https")


def _require_https_url(value: Any, field: str, context: str) -> str:
    url = _require_text(value, field, context)
    parsed = urlsplit(url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.query or parsed.fragment:
        raise SourceError(f"{context}: {field} must be an absolute HTTPS URL without query or fragment")
    return url


def _validate_asset_path(value: Any, field: str) -> str:
    path = _require_text(value, field, "site")
    candidate = Path(path)
    if candidate.is_absolute() or "\\" in path or not path.startswith("assets/") or ".." in candidate.parts:
        raise SourceError(f"site: {field} must be a safe repository-relative assets/ path")
    return path


def validate_site(site: dict[str, Any]) -> dict[str, Any]:
    if set(site) != SITE_FIELDS or site.get("schemaVersion") != 1:
        raise SourceError(
            f"site manifest must use schemaVersion 1 and contain exactly {sorted(SITE_FIELDS)}"
        )
    canonical = _require_https_url(site["canonicalUrl"], "canonicalUrl", "site")
    if not canonical.endswith("/"):
        raise SourceError("site: canonicalUrl must end with /")
    for field in ("title", "description", "siteName"):
        _require_text(site[field], field, "site")
    if site["language"] != "en-GB" or site["locale"] != "en_GB":
        raise SourceError("site: language and locale must be en-GB and en_GB")

    author = site["author"]
    if not isinstance(author, dict) or set(author) != AUTHOR_FIELDS:
        raise SourceError(f"site: author must contain exactly {sorted(AUTHOR_FIELDS)}")
    for field in ("name", "role"):
        _require_text(author[field], field, "site.author")
    if _require_https_url(author["url"], "url", "site.author") != canonical:
        raise SourceError("site.author: url must equal canonicalUrl")
    same_as = author["sameAs"]
    if not isinstance(same_as, list) or not same_as:
        raise SourceError("site.author: sameAs must be a non-empty list")
    checked_same_as = [
        _require_https_url(value, "sameAs", "site.author") for value in same_as
    ]
    if len(checked_same_as) != len(set(checked_same_as)):
        raise SourceError("site.author: sameAs URLs must be unique")

    image = site["socialImage"]
    if not isinstance(image, dict) or set(image) != SOCIAL_IMAGE_FIELDS:
        raise SourceError(
            f"site: socialImage must contain exactly {sorted(SOCIAL_IMAGE_FIELDS)}"
        )
    _validate_asset_path(image["path"], "socialImage.path")
    for field in ("width", "height"):
        value = image[field]
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise SourceError(f"site.socialImage: {field} must be a positive integer")
    if image["type"] != "image/png":
        raise SourceError("site.socialImage: type must be image/png")
    _require_text(image["alt"], "alt", "site.socialImage")

    repository = site["repository"]
    if not isinstance(repository, dict) or set(repository) != REPOSITORY_FIELDS:
        raise SourceError(
            f"site: repository must contain exactly {sorted(REPOSITORY_FIELDS)}"
        )
    slug = _require_text(repository["slug"], "slug", "site.repository")
    if re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", slug) is None:
        raise SourceError("site.repository: slug must be an owner/repository pair")
    _require_text(repository["description"], "description", "site.repository")
    if _require_https_url(repository["homepage"], "homepage", "site.repository") != canonical:
        raise SourceError("site.repository: homepage must equal canonicalUrl")
    topics = repository["topics"]
    if (
        not isinstance(topics, list)
        or not topics
        or any(not isinstance(topic, str) or re.fullmatch(r"[a-z0-9-]{1,50}", topic) is None for topic in topics)
        or len(topics) != len(set(topics))
    ):
        raise SourceError("site.repository: topics must be unique lowercase topic names")
    _validate_asset_path(repository["socialImagePath"], "repository.socialImagePath")
    return site


def _social_image_url(site: dict[str, Any]) -> str:
    return urljoin(site["canonicalUrl"], site["socialImage"]["path"])


def render_metadata(site: dict[str, Any]) -> str:
    validate_site(site)
    canonical = site["canonicalUrl"]
    image = site["socialImage"]
    image_url = _social_image_url(site)
    person_id = f"{canonical}#person"
    website_id = f"{canonical}#website"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Person",
                "@id": person_id,
                "name": site["author"]["name"],
                "jobTitle": site["author"]["role"],
                "url": site["author"]["url"],
                "sameAs": site["author"]["sameAs"],
            },
            {
                "@type": "WebSite",
                "@id": website_id,
                "url": canonical,
                "name": site["siteName"],
                "description": site["description"],
                "inLanguage": site["language"],
                "creator": {"@id": person_id},
                "image": {
                    "@type": "ImageObject",
                    "url": image_url,
                    "width": image["width"],
                    "height": image["height"],
                },
            },
        ],
    }
    json_ld = json.dumps(graph, ensure_ascii=False, indent=2).replace("</", "<\\/")
    values = {
        "title": _escape(site["title"]),
        "description": _escape(site["description"]),
        "canonical": _escape(canonical),
        "site_name": _escape(site["siteName"]),
        "locale": _escape(site["locale"]),
        "author": _escape(site["author"]["name"]),
        "image_url": _escape(image_url),
        "image_type": _escape(image["type"]),
        "image_width": str(image["width"]),
        "image_height": str(image["height"]),
        "image_alt": _escape(image["alt"]),
    }
    return f'''<title>{values["title"]}</title>
<meta name="description" content="{values["description"]}">
<meta name="author" content="{values["author"]}">
<link rel="canonical" href="{values["canonical"]}">
<meta property="og:type" content="website">
<meta property="og:title" content="{values["title"]}">
<meta property="og:description" content="{values["description"]}">
<meta property="og:url" content="{values["canonical"]}">
<meta property="og:site_name" content="{values["site_name"]}">
<meta property="og:locale" content="{values["locale"]}">
<meta property="og:image" content="{values["image_url"]}">
<meta property="og:image:secure_url" content="{values["image_url"]}">
<meta property="og:image:type" content="{values["image_type"]}">
<meta property="og:image:width" content="{values["image_width"]}">
<meta property="og:image:height" content="{values["image_height"]}">
<meta property="og:image:alt" content="{values["image_alt"]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{values["title"]}">
<meta name="twitter:description" content="{values["description"]}">
<meta name="twitter:image" content="{values["image_url"]}">
<meta name="twitter:image:alt" content="{values["image_alt"]}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/favicon-32x32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png" sizes="180x180">
<script type="application/ld+json">
{json_ld}
</script>'''


def validate_sources(
    manifest: dict[str, Any], registry_lock: dict[str, Any]
) -> tuple[
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, str]],
]:
    if (
        set(manifest) != MANIFEST_FIELDS
        or manifest.get("schemaVersion") != 2
        or not isinstance(manifest.get("capabilityGroups"), dict)
        or not isinstance(manifest.get("projects"), dict)
    ):
        raise SourceError(
            "presentation manifest must use schemaVersion 2 and contain exactly "
            "capabilityGroups and projects"
        )
    if registry_lock.get("schemaVersion") != 1:
        raise SourceError("registry lock must use schemaVersion 1")

    groups = manifest["capabilityGroups"]
    if not groups:
        raise SourceError("presentation manifest must define at least one capability group")
    group_orders: set[int] = set()
    group_labels: set[str] = set()
    for key, group in groups.items():
        if not isinstance(key, str) or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", key) is None:
            raise SourceError(f"invalid capability group key: {key!r}")
        if not isinstance(group, dict) or set(group) != GROUP_FIELDS:
            raise SourceError(
                f"{key}: capability group must contain exactly {sorted(GROUP_FIELDS)}"
            )
        label = _require_text(group["label"], "label", f"capability group {key}")
        _require_text(group["description"], "description", f"capability group {key}")
        order = group["order"]
        if isinstance(order, bool) or not isinstance(order, int) or order < 0:
            raise SourceError(f"{key}: capability group order must be a non-negative integer")
        if order in group_orders:
            raise SourceError(f"{key}: capability group order {order} is duplicated")
        if label in group_labels:
            raise SourceError(f"{key}: capability group label {label!r} is duplicated")
        group_orders.add(order)
        group_labels.add(label)

    source = registry_lock.get("source")
    if not isinstance(source, dict):
        raise SourceError("registry lock must record source metadata")
    commit = source.get("commit")
    if not isinstance(commit, str) or re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise SourceError("registry lock source.commit must be a full lowercase Git commit")

    locked_rows = registry_lock.get("projects")
    if not isinstance(locked_rows, list):
        raise SourceError("registry lock projects must be a list")

    registry: dict[str, dict[str, str]] = {}
    for row in locked_rows:
        if not isinstance(row, dict) or set(row) != {"project", "github", "presentation_role"}:
            raise SourceError("each registry lock row must contain project, github and presentation_role")
        project = _require_text(row["project"], "project", "registry row")
        if project in registry:
            raise SourceError(f"duplicate registry project: {project}")
        github = _require_text(row["github"], "github", project)
        role = _require_text(row["presentation_role"], "presentation_role", project)
        if role not in ALLOWED_ROLES:
            raise SourceError(f"{project}: unsupported presentation_role {role!r}")
        registry[project] = {"github": github, "presentation_role": role}

    projects = manifest["projects"]
    public_ids = {project for project, row in registry.items() if row["presentation_role"] in PUBLIC_ROLES}
    manifest_ids = set(projects)
    missing = sorted(public_ids - manifest_ids)
    extra = sorted(manifest_ids - public_ids)
    if missing or extra:
        parts = []
        if missing:
            parts.append("missing public projects: " + ", ".join(missing))
        if extra:
            parts.append("unknown or hidden projects: " + ", ".join(extra))
        raise SourceError("; ".join(parts))

    orders: set[tuple[str, int]] = set()
    group_members: dict[str, list[str]] = {key: [] for key in groups}
    for project, entry in projects.items():
        if not isinstance(entry, dict) or set(entry) != ENTRY_FIELDS:
            raise SourceError(f"{project}: manifest entry must contain exactly {sorted(ENTRY_FIELDS)}")
        for field in ("title", "discipline", "summary"):
            _require_text(entry[field], field, project)
        order = entry["order"]
        if isinstance(order, bool) or not isinstance(order, int) or order < 0:
            raise SourceError(f"{project}: order must be a non-negative integer")
        role_order = (registry[project]["presentation_role"], order)
        if role_order in orders:
            raise SourceError(f"{project}: order {order} is duplicated within its presentation role")
        orders.add(role_order)
        group = entry["group"]
        role = registry[project]["presentation_role"]
        if role == "showcase":
            if not isinstance(group, str) or not group.strip():
                raise SourceError(f"{project}: showcase project must have a capability group")
            if group not in groups:
                raise SourceError(f"{project}: unknown capability group {group!r}")
            group_members[group].append(project)
        elif group is not None:
            raise SourceError(f"{project}: methodology project must use group null")
        tags = entry["tags"]
        if not isinstance(tags, list) or not tags or any(not isinstance(tag, str) or not tag for tag in tags):
            raise SourceError(f"{project}: tags must be a non-empty string list")
        if len(tags) != len(set(tags)):
            raise SourceError(f"{project}: tags must be unique")
        actions = entry["actions"]
        if not isinstance(actions, dict) or set(actions) != ACTION_FIELDS:
            raise SourceError(
                f"{project}: actions must contain workflow, demo, report and documentation"
            )
        workflow = actions["workflow"]
        if workflow is not None:
            _require_text(workflow, "actions.workflow", project)
        _validate_link(actions["demo"], "demo", project)
        _validate_link(actions["report"], "report", project)
        _validate_link(actions["documentation"], "documentation", project)

    empty_groups = sorted(key for key, members in group_members.items() if not members)
    if empty_groups:
        raise SourceError("empty capability groups: " + ", ".join(empty_groups))

    return groups, projects, registry


def _escape(value: str) -> str:
    return html.escape(value, quote=True)


def _number_word(value: int) -> str:
    words = {
        0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
        6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
        11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen",
        16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty",
    }
    return words.get(value, str(value))


def _action_link(action: dict[str, str], css_class: str) -> str:
    # Only a genuinely interactive `demo` carries the play-style cue (added by the
    # `.btn.demo::before` CSS). Static `report` and `documentation` links use their
    # own classes so they do not imply an interactive experience.
    return (
        f'<a class="btn {css_class}" href="{_escape(action["url"])}">'
        f'{_escape(action["label"])}</a>'
    )


def render_card(project: str, entry: dict[str, Any], github: str) -> str:
    repo_url = f"https://github.com/{github}"
    title = _escape(entry["title"])
    chips = "".join(f'<span class="chip">{_escape(tag)}</span>' for tag in entry["tags"])
    actions = [f'<a class="btn primary" href="{_escape(repo_url)}">Repo</a>']
    if entry["actions"]["demo"] is not None:
        actions.append(_action_link(entry["actions"]["demo"], "demo"))
    if entry["actions"]["report"] is not None:
        actions.append(_action_link(entry["actions"]["report"], "report"))
    if entry["actions"]["documentation"] is not None:
        actions.append(_action_link(entry["actions"]["documentation"], "documentation"))
    workflow = entry["actions"]["workflow"]
    if workflow is not None:
        workflow_url = f"{repo_url}/actions/workflows/{workflow}"
        actions.append(
            f'<a href="{_escape(workflow_url)}" aria-label="{title} CI workflow">'
            f'<img class="badge" alt="{title} CI status" '
            f'src="{_escape(workflow_url)}/badge.svg?branch=main"></a>'
        )
    action_html = "\n      ".join(actions)
    return f'''<!-- Generated: {project} -->
<article class="card" data-project="{_escape(project)}">
  <h4><a href="{_escape(repo_url)}">{title}</a></h4>
  <p class="disc">{_escape(entry["discipline"])}</p>
  <p class="desc">{_escape(entry["summary"])}</p>
  <div class="chips">{chips}</div>
  <div class="actions">
    {action_html}
  </div>
</article>'''


def render_capability_groups(
    groups: dict[str, dict[str, Any]],
    entries: list[tuple[str, dict[str, Any], str]],
) -> str:
    members: dict[str, list[tuple[str, dict[str, Any], str]]] = {
        key: [] for key in groups
    }
    for entry in entries:
        members[entry[1]["group"]].append(entry)

    rendered_groups = []
    for key, group in sorted(groups.items(), key=lambda item: (item[1]["order"], item[0])):
        cards = "\n\n".join(
            render_card(*entry)
            for entry in sorted(members[key], key=lambda item: (item[1]["order"], item[0]))
        )
        heading_id = f"capability-{key}"
        rendered_groups.append(
            f'''<section class="capability-group" data-capability-group="{_escape(key)}"
  aria-labelledby="{_escape(heading_id)}">
  <div class="group-heading">
    <h3 id="{_escape(heading_id)}">{_escape(group["label"])}</h3>
    <p>{_escape(group["description"])}</p>
  </div>
  <div class="card-grid">
{indent(cards, "    ")}
  </div>
</section>'''
        )
    return "\n\n".join(rendered_groups)


def render_methodology(entries: list[tuple[str, dict[str, Any], str]]) -> str:
    paragraphs = []
    for project, entry, github in entries:
        paragraphs.append(
            f'  <p data-project="{_escape(project)}"><a href="https://github.com/{_escape(github)}">'
            f'{_escape(entry["title"])}</a> {_escape(entry["summary"])}</p>'
        )
    return '''<section class="methodology" aria-labelledby="methodology-heading">
  <h2 id="methodology-heading">Methodology &amp; tooling</h2>
{paragraphs}
</section>'''.format(paragraphs="\n".join(paragraphs))


def render_site(
    template: str,
    manifest: dict[str, Any],
    registry_lock: dict[str, Any],
    site: dict[str, Any],
) -> str:
    validate_site(site)
    groups, projects, registry = validate_sources(manifest, registry_lock)
    showcase = sorted(
        (
            (project, entry, registry[project]["github"])
            for project, entry in projects.items()
            if registry[project]["presentation_role"] == "showcase"
        ),
        key=lambda item: (item[1]["order"], item[0]),
    )
    methodology = sorted(
        (
            (project, entry, registry[project]["github"])
            for project, entry in projects.items()
            if registry[project]["presentation_role"] == "methodology"
        ),
        key=lambda item: (item[1]["order"], item[0]),
    )
    public_evidence_count = sum(
        entry["actions"][field] is not None
        for _, entry, _ in showcase
        for field in ("demo", "report", "documentation")
    )

    replacements = {
        "{{SITE_METADATA}}": render_metadata(site),
        "{{SHOWCASE_COUNT}}": str(len(showcase)),
        "{{SHOWCASE_COUNT_WORD}}": _number_word(len(showcase)).capitalize(),
        "{{SHOWCASE_COUNT_WORD_LOWER}}": _number_word(len(showcase)),
        "{{CAPABILITY_GROUP_COUNT}}": str(len(groups)),
        "{{PUBLIC_EVIDENCE_COUNT}}": str(public_evidence_count),
        "{{SHOWCASE_GROUPS}}": render_capability_groups(groups, showcase),
        "{{METHODOLOGY}}": render_methodology(methodology),
    }
    rendered = template
    for token, value in replacements.items():
        occurrences = rendered.count(token)
        if occurrences == 0:
            raise SourceError(f"template must contain {token}")
        if token in {"{{SHOWCASE_GROUPS}}", "{{METHODOLOGY}}"} and occurrences != 1:
            raise SourceError(f"template must contain structural block {token} exactly once")
        rendered = rendered.replace(token, value)
    if "{{" in rendered or "}}" in rendered:
        raise SourceError("template contains an unresolved token")
    return rendered.rstrip() + "\n"


def render_sitemap(site: dict[str, Any]) -> str:
    validate_site(site)
    canonical = _escape(site["canonicalUrl"])
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{canonical}</loc>
  </url>
</urlset>
'''


def render_robots(site: dict[str, Any]) -> str:
    validate_site(site)
    sitemap_url = urljoin(site["canonicalUrl"], "sitemap.xml")
    return f"User-agent: *\nAllow: /\n\nSitemap: {sitemap_url}\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the static portfolio page deterministically.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--registry-lock", type=Path, default=DEFAULT_REGISTRY_LOCK)
    parser.add_argument("--site", type=Path, default=DEFAULT_SITE)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--sitemap-output", type=Path, default=DEFAULT_SITEMAP_OUTPUT)
    parser.add_argument("--robots-output", type=Path, default=DEFAULT_ROBOTS_OUTPUT)
    parser.add_argument("--check", action="store_true", help="Fail if the committed output is stale.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        site = load_json(args.site)
        outputs = {
            args.output: render_site(
                args.template.read_text(encoding="utf-8"),
                load_json(args.manifest),
                load_json(args.registry_lock),
                site,
            ).encode("utf-8"),
            args.sitemap_output: render_sitemap(site).encode("utf-8"),
            args.robots_output: render_robots(site).encode("utf-8"),
        }
    except (OSError, SourceError) as exc:
        print(f"generate-site: ERROR — {exc}", file=sys.stderr)
        return 2
    if args.check:
        stale: list[str] = []
        for path, expected in outputs.items():
            try:
                actual = path.read_bytes()
            except OSError:
                stale.append(str(path))
            else:
                if actual != expected:
                    stale.append(str(path))
        if stale:
            print(
                "generate-site: FAIL — generated output is missing or stale: "
                + ", ".join(stale)
                + "; run python tools/generate_site.py"
            )
            return 1
        print("generate-site: PASS — committed HTML, sitemap and robots output is current")
        return 0
    for path, content in outputs.items():
        path.write_bytes(content)
        print(f"generate-site: wrote {path} ({len(content)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
