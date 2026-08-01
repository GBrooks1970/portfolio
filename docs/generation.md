# Generated Portfolio Contract

The public page is a committed static artefact generated before deployment. Visitors load only
`index.html`; no browser-side code calls GitHub, reads the canonical registry or requires a build
tool.

## Ownership and source files

| File | Authority | Editing rule |
|---|---|---|
| `data/presentation.json` | Landing-owned public title, discipline, summary, order, tags and optional actions | Edit by hand and review as public copy |
| `data/registry-lock.json` | Generated snapshot of registry-owned project ID, GitHub slug and `presentation_role` | Never hand-edit; refresh from an exact canonical commit |
| `index.template.html` | Landing-owned static layout, styling and count-bearing prose | Edit by hand; use generator tokens for derived content |
| `index.html` | Generated deployable output | Never hand-edit; commit with its source changes |

This implements [decision 001](decisions/001-presentation-ownership.md). The lock is a reproducible
build input, not a second authority: its `source` object names the canonical repository, full commit
and path from which every row was extracted.

## Presentation manifest schema

`data/presentation.json` uses `schemaVersion: 1` and a `projects` object keyed by the exact canonical
registry project identifier. Every public `showcase` or `methodology` row has one entry; `hidden`
rows have none.

```json
{
  "schemaVersion": 1,
  "projects": {
    "registry-project-id": {
      "title": "Public title",
      "discipline": "Public discipline",
      "summary": "Evidence-backed public summary.",
      "order": 10,
      "tags": ["Tag"],
      "actions": {
        "workflow": "ci.yml",
        "demo": {"label": "Live demo", "url": "https://example.test/"},
        "report": null
      }
    }
  }
}
```

Rules enforced by `tools/generate_site.py`:

- entries contain exactly the fields shown above and do not duplicate GitHub slug, lifecycle state,
  orchestration eligibility or presentation role;
- `order` is a non-negative integer unique within each presentation role;
- tags are non-empty and unique within an entry;
- `workflow` is a repository workflow filename or `null`;
- `demo` and `report` are `null` or an HTTPS URL with a truthful label;
- all public registry-lock rows have an entry and hidden/unknown rows do not; and
- repository and workflow URLs are derived from the registry-owned GitHub slug.

Showcase cards, their numeric/text counts and the methodology section are all derived. Display order
comes only from `order`; JSON object order has no public meaning.

## Generate and verify

From the repository root:

```powershell
python tools/generate_site.py
python tools/generate_site.py --check
python -B -m unittest discover -s tools/tests -p test_*.py
```

The generator uses only the Python standard library. It writes UTF-8 with LF endings and orders
projects deterministically. `--check` compares exact bytes and exits non-zero when committed output
is stale, so an unchanged input produces unchanged output on every platform.

## Refresh the canonical registry lock

Lock refresh requires PyYAML only for reading the upstream YAML; generated-site checks remain
dependency-free.

```powershell
python -m pip install -r requirements-dev.txt
python tools/lock_registry.py `
  --repository ..\portfolio-prompts `
  --commit <full-merged-portfolio-prompts-commit>
python tools/generate_site.py
python tools/generate_site.py --check
```

`lock_registry.py` reads `registry.yml` directly from the supplied Git commit using `git show`; it
does not trust the checkout's working tree. Review the full commit recorded in
`data/registry-lock.json` and commit the lock, manifest and regenerated HTML together.

LAND-04 will add pull-request CI that independently fetches/checks the recorded canonical source
and exercises negative parity cases. Until that work lands, the generator enforces the locked
source-to-manifest/output contract locally while keeping the upstream enforcement gap explicit.
