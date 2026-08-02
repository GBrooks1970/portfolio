# Implementation Log — LAND-07: Search and Social Discoverability

**Date:** 2026-08-02
**Backlog item:** `LAND-07`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `codex/land-07-implementation`
**Commit:** `00f827a2cbdaf81241f8ab1029000e9acdc141cc`
**Pull request:** Pending
**Pages run:** Pending — public metadata and assets require owner merge, exact-merge quality, Pages
and live verification

## Outcome

The portfolio now has one generated identity contract for search engines, link previews, browser
icons and repository discovery. A validated `data/site.json` drives the canonical URL, document
identity, complete Open Graph and Twitter/X compatibility metadata, an evidence-backed JSON-LD
`WebSite` + `Person` graph, favicon links, a one-page sitemap and robots policy. Two evergreen social
assets use the existing dark palette without a project count or volatile CI evidence.

The GitHub repository description, homepage, seven discoverability topics and dedicated 1280 × 640
repository social preview are reconciled. The complete local gate passes with 9 showcase and 1
methodology project, 35 named controls, 5 internal references, 34 live HTTPS targets, 20 contrast
pairs and 36 deterministic tests.

## Scope

- `data/site.json` — add the versioned canonical identity, author, webpage preview and desired
  repository-metadata contract.
- `tools/generate_site.py`, `index.template.html` and generated `index.html` — validate the site
  source and generate canonical, social, icon and `WebSite` + `Person` metadata.
- `sitemap.xml` and `robots.txt` — add byte-stable generated crawler outputs without an unverified
  freshness date.
- `assets/` — add a source-aligned SVG favicon, 32 × 32 fallback, 180 × 180 touch icon, 1200 × 630
  webpage preview and separate 1280 × 640 GitHub repository preview.
- `tools/check_site.py`, `tools/check_registry_parity.py` and deterministic tests — validate metadata
  uniqueness/consistency, structured data, local canonical-asset mapping, real PNG dimensions,
  icons, sitemap/robots and all three generated text artefacts.
- `.gitattributes`, `README.md`, `docs/generation.md` and `docs/quality-gate.md` — document binary/LF
  handling, source ownership, local commands, pre-merge URL policy and settings-side evidence.
- GitHub settings — update description/homepage/topics and upload the dedicated repository preview.
- Explicit non-goals: no analytics, cookies, runtime API calls, dynamic freshness, project-count
  artwork, `ProfilePage` claim or visible card/layout changes.

## Decisions

- Keep site identity in `data/site.json`, separate from project copy in `data/presentation.json`.
  This prevents canonical and social metadata from drifting without mixing site and project schemas.
- Use exactly one JSON-LD `WebSite` linked to one `Person`. The portfolio is primarily a project
  catalogue, so claiming `ProfilePage` would overstate the current visible information architecture.
- Generate the abstract technical background with the built-in image workflow but render all words
  deterministically. This retains visual originality while preventing generated spelling errors.
- Export 1200 × 630 and 1280 × 640 assets from the same evergreen design. The artwork omits project
  totals and badges so adding or changing showcases does not invalidate cached previews.
- Map canonical absolute image URLs back to committed local files during pull-request validation.
  Requiring the new URL to exist on the current `main` deployment would make a correct PR fail
  before it could publish the asset.
- Generate sitemap and robots output with the same standard-library command as `index.html`; the
  complete gate compares all three exact byte streams and then validates their semantics.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| Complete local command | PASS | 9 showcase, 1 methodology, 35 named controls, 5 internal references, 34 external URLs and 20 contrast pairs |
| Python unit suite | PASS | 36/36 tests; 11 LAND-07 generator/quality cases added to the prior 25-test baseline |
| Generated outputs | PASS | `python tools/generate_site.py --check` verifies HTML, sitemap and robots bytes |
| Python compilation | PASS | `python -m compileall -q tools` |
| External targets | PASS | All 34 unique HTTPS `href`/`src` targets returned HTTP 200–399 |
| Preview assets | PASS | Web preview visually inspected at 1200 × 630; GitHub preview at 1280 × 640; PNG header dimensions enforced by the gate |
| Repository metadata | PASS | Description and homepage exactly match `data/site.json`; topics are `bdd`, `github-pages`, `playwright`, `portfolio`, `quality-engineering`, `serenity-js`, `test-automation` |
| Repository social preview | PASS | 1280 × 640 preview uploaded through GitHub settings and visually verified after upload |
| Whitespace | PASS | `git diff --check` clean |
| Pull-request CI | PENDING | Branch has not yet been pushed or opened for review |
| Owner merge / `main` / Pages / live assets | PENDING | Required before LAND-07 can move from IN REVIEW to DONE |

## Failures and recovery

- The local Python environment did not contain Pillow. The generated, text-free background was
  resized and given deterministic Segoe UI typography with Windows `System.Drawing`; the final PNGs
  were then inspected at original resolution and validated from their binary IHDR dimensions.
- Updating the generator signature initially exposed one stale caller in the registry-parity test
  fixture. Passing the new site source through that caller restored the complete suite and ensured
  parity validation uses the same identity input as normal generation.
- The webpage preview URL cannot return its new asset until this branch merges. The gate deliberately
  validates same-site absolute images against local files before merge; exact live HTTP checks remain
  a closure requirement.

## Durable lessons

- Search metadata is only durable when every representation—canonical, Open Graph, compatibility
  fields, structured data, sitemap and repository settings—has one reviewed source value.
- A repository social preview and a webpage Open Graph image are separate publication surfaces with
  different preferred dimensions; committing one file does not configure the other surface.
- Generated art should not own factual words or volatile counts. Deterministic overlays and binary
  dimension checks make visual assets reviewable without turning them into runtime content.
- Third-party preview caches may lag a successful deployment; closure should verify public asset
  availability, not promise immediate cache refresh across every sharing platform.

## Backlog reconciliation

- Ten LAND-07 implementation/settings criteria are complete with local, binary, visual and GitHub
  settings evidence.
- LAND-07 moves from READY to IN REVIEW at implementation commit `00f827a`; current-head PR CI,
  owner merge, exact-merge quality, Pages and live canonical-asset checks remain open.
- LAND-C02 through LAND-C04 remain proposed and unchanged.
