# Generated Portfolio Contract

The public page is a committed static artefact generated before deployment. Visitors load only
`index.html`; no browser-side code calls GitHub, reads the canonical registry or requires a build
tool.

## Ownership and source files

| File | Authority | Editing rule |
|---|---|---|
| `data/presentation.json` | Landing-owned capability groups and assignments plus public title, discipline, summary, order, tags and optional actions | Edit by hand and review as public presentation data |
| `data/registry-lock.json` | Generated snapshot of registry-owned project ID, GitHub slug and `presentation_role` | Never hand-edit; refresh from an exact canonical commit |
| `data/site.json` | Landing-owned canonical identity, author, social image and desired GitHub repository metadata | Edit by hand; keep claims aligned with visible evidence and repository settings |
| `index.template.html` | Landing-owned static layout, styling and count-bearing prose | Edit by hand; use generator tokens for derived content |
| `assets/` | Branded favicon and fixed-dimension preview assets | Commit reviewed source assets; do not substitute stale counts, badges or runtime evidence |
| `index.html`, `sitemap.xml`, `robots.txt` | Generated deployable output | Never hand-edit; commit with source changes |

This implements [decision 001](decisions/001-presentation-ownership.md). The lock is a reproducible
build input, not a second authority: its `source` object names the canonical repository, full commit
and path from which every row was extracted.

## Presentation manifest schema

`data/presentation.json` uses `schemaVersion: 2`, a `capabilityGroups` object and a `projects` object
keyed by the exact canonical registry project identifier. Every public `showcase` or `methodology`
row has one entry; `hidden` rows have none. Capability taxonomy is landing-owned presentation data,
not a canonical registry field.

```json
{
  "schemaVersion": 2,
  "capabilityGroups": {
    "stable-group-key": {
      "label": "Public capability label",
      "description": "Concise group narrative.",
      "order": 10
    }
  },
  "projects": {
    "registry-project-id": {
      "title": "Public title",
      "discipline": "Public discipline",
      "summary": "Evidence-backed public summary.",
      "order": 10,
      "group": "stable-group-key",
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

- group keys use stable lowercase kebab-case; labels and descriptions are non-empty; labels and
  non-negative display orders are unique;
- each showcase has exactly one known group, every group has at least one showcase, and methodology
  entries use `group: null` so they remain outside the showcase taxonomy;
- entries contain exactly the fields shown above and do not duplicate GitHub slug, lifecycle state,
  orchestration eligibility or presentation role;
- `order` is a non-negative integer unique within each presentation role;
- tags are non-empty and unique within an entry;
- `workflow` is a repository workflow filename or `null`;
- `demo` and `report` are `null` or an HTTPS URL with a truthful label;
- all public registry-lock rows have an entry and hidden/unknown rows do not; and
- repository and workflow URLs are derived from the registry-owned GitHub slug.

Capability sections, showcase cards, project/group/public-demo-or-report statistics, numeric/text
project counts and the methodology section are all derived. Group and project display order comes
only from their `order` values; JSON object order has no public meaning. A public-evidence statistic
counts each non-null `demo` or `report` action on a showcase. It does not claim CI health or project
freshness.

## Site manifest schema

`data/site.json` uses `schemaVersion: 1` and separates site identity from project presentation.
It owns the canonical HTTPS URL, title, description, `en-GB` language/`en_GB` Open Graph locale,
visible author identity, webpage social image and the desired public GitHub repository metadata.

The author record is deliberately evidence-limited: its URL equals the canonical page and each
`sameAs` value is an absolute HTTPS identity URL. The generated JSON-LD contains exactly one
`Person` and one `WebSite`; it does not claim `ProfilePage` while the visible product is primarily a
project catalogue. Social images use safe repository-relative `assets/` paths and positive declared
dimensions. Repository topics are lowercase, unique GitHub topic names.

The generator emits one consistent metadata block containing the document title/description,
canonical, Open Graph, minimal Twitter/X compatibility metadata, favicon links and JSON-LD. It also
emits a one-URL sitemap without a fabricated `lastmod` and a robots policy pointing to that sitemap.

## Generate and verify

From the repository root:

```powershell
python tools/generate_site.py
python tools/generate_site.py --check
python -B -m unittest discover -s tools/tests -p test_*.py
```

The generator uses only the Python standard library. It writes UTF-8 with LF endings and orders
projects deterministically. `--check` compares `index.html`, `sitemap.xml` and `robots.txt` byte for
byte and exits non-zero when any committed output is missing or stale, so unchanged input produces
unchanged output on every platform. `.gitattributes` keeps all three generated text files
LF-normalised in Windows working trees and marks PNG assets as binary.

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

## Verify canonical registry parity

`tools/check_registry_parity.py` closes the gap between the committed lock and its upstream source.
It rebuilds the lock from the exact `source.commit` and `source.path` recorded in
`data/registry-lock.json`, then verifies all four layers together:

1. canonical registry identifiers, GitHub slugs and presentation roles at the recorded commit;
2. the committed registry lock;
3. the landing-owned presentation manifest; and
4. the generated showcase/methodology inventory, count marker and exact `index.html` bytes.

The command requires a full-history checkout containing the recorded commit. From the normal
portfolio workspace layout:

```powershell
git -C ..\portfolio-prompts fetch origin
python tools/check_registry_parity.py --registry-repository ..\portfolio-prompts
```

The pull-request workflow checks out the public canonical repository with full history and runs the
same command. It uses the ordinary `pull_request` event, grants only `contents: read`, persists no
checkout credentials and reads no repository secrets. The recorded full commit—not a mutable
branch name—is the reproducible registry reference checked by the gate.

### Failure recovery

- **Missing, unknown, hidden, duplicate or misclassified entry:** update
  `data/presentation.json` to match the approved public roles, or correct the upstream registry and
  merge that change first. Do not weaken the check or edit the lock by hand.
- **Lock/source mismatch:** use `tools/lock_registry.py` against the intended merged canonical
  commit, review the lock diff, regenerate `index.html`, then rerun parity and unit tests.
- **Stale generated output/count:** run `python tools/generate_site.py`, review `index.html`, and
  rerun the parity command.
- **Transient checkout/network failure:** rerun the job. Do not replace the recorded commit merely
  to clear a transient failure.
- **Recorded commit genuinely unavailable:** confirm the canonical repository and history were not
  moved or rewritten. With owner approval, select a reachable merged canonical commit, refresh the
  lock and regenerate all dependent output in one PR; never silently fall back to an unpinned
  branch tip.
