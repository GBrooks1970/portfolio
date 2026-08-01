from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "data" / "presentation.json"
DEFAULT_REGISTRY_LOCK = ROOT / "data" / "registry-lock.json"
DEFAULT_TEMPLATE = ROOT / "index.template.html"
DEFAULT_OUTPUT = ROOT / "index.html"
PUBLIC_ROLES = {"showcase", "methodology"}
ALLOWED_ROLES = PUBLIC_ROLES | {"hidden"}
ENTRY_FIELDS = {"title", "discipline", "summary", "order", "tags", "actions"}
ACTION_FIELDS = {"workflow", "demo", "report"}
LINK_FIELDS = {"label", "url"}


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


def validate_sources(
    manifest: dict[str, Any], registry_lock: dict[str, Any]
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, str]]]:
    if manifest.get("schemaVersion") != 1 or not isinstance(manifest.get("projects"), dict):
        raise SourceError("presentation manifest must use schemaVersion 1 and a projects object")
    if registry_lock.get("schemaVersion") != 1:
        raise SourceError("registry lock must use schemaVersion 1")

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
        tags = entry["tags"]
        if not isinstance(tags, list) or not tags or any(not isinstance(tag, str) or not tag for tag in tags):
            raise SourceError(f"{project}: tags must be a non-empty string list")
        if len(tags) != len(set(tags)):
            raise SourceError(f"{project}: tags must be unique")
        actions = entry["actions"]
        if not isinstance(actions, dict) or set(actions) != ACTION_FIELDS:
            raise SourceError(f"{project}: actions must contain workflow, demo and report")
        workflow = actions["workflow"]
        if workflow is not None:
            _require_text(workflow, "actions.workflow", project)
        _validate_link(actions["demo"], "demo", project)
        _validate_link(actions["report"], "report", project)

    return projects, registry


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


def _action_link(action: dict[str, str]) -> str:
    return (
        f'<a class="btn demo" href="{_escape(action["url"])}">'
        f'{_escape(action["label"])}</a>'
    )


def render_card(project: str, entry: dict[str, Any], github: str) -> str:
    repo_url = f"https://github.com/{github}"
    title = _escape(entry["title"])
    chips = "".join(f'<span class="chip">{_escape(tag)}</span>' for tag in entry["tags"])
    actions = [f'<a class="btn primary" href="{_escape(repo_url)}">Repo</a>']
    if entry["actions"]["demo"] is not None:
        actions.append(_action_link(entry["actions"]["demo"]))
    if entry["actions"]["report"] is not None:
        actions.append(_action_link(entry["actions"]["report"]))
    workflow = entry["actions"]["workflow"]
    if workflow is not None:
        workflow_url = f"{repo_url}/actions/workflows/{workflow}"
        actions.append(
            f'<a href="{_escape(workflow_url)}" aria-label="{title} CI workflow">'
            f'<img class="badge" alt="{title} CI status" '
            f'src="{_escape(workflow_url)}/badge.svg?branch=main"></a>'
        )
    action_html = "\n      ".join(actions)
    return f'''  <!-- Generated: {project} -->
  <article class="card" data-project="{_escape(project)}">
    <h3><a href="{_escape(repo_url)}">{title}</a></h3>
    <p class="disc">{_escape(entry["discipline"])}</p>
    <p class="desc">{_escape(entry["summary"])}</p>
    <div class="chips">{chips}</div>
    <div class="actions">
      {action_html}
    </div>
  </article>'''


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


def render_site(template: str, manifest: dict[str, Any], registry_lock: dict[str, Any]) -> str:
    projects, registry = validate_sources(manifest, registry_lock)
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

    replacements = {
        "{{SHOWCASE_COUNT}}": str(len(showcase)),
        "{{SHOWCASE_COUNT_WORD}}": _number_word(len(showcase)).capitalize(),
        "{{SHOWCASE_COUNT_WORD_LOWER}}": _number_word(len(showcase)),
        "{{SHOWCASE_CARDS}}": "\n\n".join(render_card(*item) for item in showcase),
        "{{METHODOLOGY}}": render_methodology(methodology),
    }
    rendered = template
    for token, value in replacements.items():
        occurrences = rendered.count(token)
        if occurrences == 0:
            raise SourceError(f"template must contain {token}")
        if token in {"{{SHOWCASE_CARDS}}", "{{METHODOLOGY}}"} and occurrences != 1:
            raise SourceError(f"template must contain structural block {token} exactly once")
        rendered = rendered.replace(token, value)
    if "{{" in rendered or "}}" in rendered:
        raise SourceError("template contains an unresolved token")
    return rendered.rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the static portfolio page deterministically.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--registry-lock", type=Path, default=DEFAULT_REGISTRY_LOCK)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="Fail if the committed output is stale.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        rendered = render_site(
            args.template.read_text(encoding="utf-8"),
            load_json(args.manifest),
            load_json(args.registry_lock),
        )
    except (OSError, SourceError) as exc:
        print(f"generate-site: ERROR — {exc}", file=sys.stderr)
        return 2
    expected = rendered.encode("utf-8")
    if args.check:
        try:
            actual = args.output.read_bytes()
        except OSError as exc:
            print(f"generate-site: ERROR — cannot read {args.output}: {exc}", file=sys.stderr)
            return 2
        if actual != expected:
            print("generate-site: FAIL — index.html is stale; run python tools/generate_site.py")
            return 1
        print("generate-site: PASS — committed output is current")
        return 0
    args.output.write_bytes(expected)
    print(f"generate-site: wrote {args.output} ({len(expected)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
