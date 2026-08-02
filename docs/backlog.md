# Portfolio Landing — Backlog

**Version:** 15
**Last updated:** 2026-08-02
**Status:** ACTIVE — LAND-01 through LAND-07 closed; candidates await owner promotion
**Source evidence:** [`portfolio-page-audit-2026-08-01.md`](portfolio-page-audit-2026-08-01.md)

## Purpose and authority

This file is the authoritative source for outstanding work in the public portfolio landing-page
repository. It is deliberately model- and tool-agnostic: an engineer or agent must be able to
resume from the repository alone, without access to a prior conversation.

Source precedence:

1. This backlog defines approved work, priority, dependencies and completion.
2. Accepted records in [`decisions/`](decisions/) define architectural choices and ownership.
3. [`project-contract.md`](project-contract.md) defines gates and working norms.
4. The audit records evidence and recommendations; it does not authorise implementation by itself.
5. `README.md` and `index.html` describe the product but are not planning sources.

Do not promote a candidate improvement into required work without recording the decision here.

## Fixed facts

- Repository: `https://github.com/GBrooks1970/portfolio`
- Published page: `https://gbrooks1970.github.io/portfolio/`
- Current implementation: one static, dependency-free `index.html` published by GitHub Pages.
- Canonical portfolio membership: `portfolio-prompts/registry.yml` in
  `https://github.com/NeoCognitus70/portfolio-prompts`.
- Registry classification: `portfolio-landing` is a support repository, not a portfolio lifecycle
  `PROJECT=` value and not an orchestration target.
- Public presentation model accepted for this cycle: nine showcase projects; the registered
  `portfolio-prompts` meta-project appears under methodology/tooling rather than as a peer showcase
  card.
- All changes to `main`, including documentation-only changes, go through a branch and pull request.

## Priority and status model

- **P0:** public accuracy or credibility defect; complete first.
- **P1:** recurrence prevention or publication-quality control.
- **P2:** useful enhancement after the required control path exists.
- **READY:** approved and unblocked.
- **IN REVIEW:** implemented on a branch; owner merge and/or post-merge evidence is pending.
- **BLOCKED:** dependency or owner decision must be completed first.
- **PROPOSED:** unscheduled candidate; not authority to implement.
- **DONE:** acceptance criteria and completion evidence are recorded.
- **DONE WITH EXCEPTION:** the owner explicitly closed a documented evidence gap; this is not an
  unqualified pass and the exception remains visible in completion evidence.

## Current required cycle

| ID | Priority | Status | Depends on | Outcome |
|---|---|---|---|---|
| LAND-01 | P0 | DONE | — | Restore public inventory and factual accuracy |
| LAND-02 | P0 | DONE | LAND-01 | Define durable presentation ownership |
| LAND-02R | P1 | DONE | LAND-02 | Implement presentation roles in the canonical registry |
| LAND-03 | P1 | DONE | LAND-02R | Generate cards and counts from structured data |
| LAND-04 | P1 | DONE | LAND-02R, LAND-03 | Enforce registry-to-landing inventory parity in CI |
| LAND-05 | P1 | DONE | — | Add publication-quality automated gates |
| LAND-06 | P1 | DONE WITH EXCEPTION | LAND-01 | Strengthen navigation and accessibility contracts |
| LAND-07 | P2 | DONE | LAND-05, LAND-06 | Add search and social discoverability |

### LAND-01 — Restore public inventory and factual accuracy

**Priority:** P0
**Status:** DONE
**Type:** HTML, documentation and repository metadata

Add the missing ParaBank showcase and reconcile every public claim affected by the ninth showcase
project. This is an accuracy hotfix; do not wait for the future generator.

Acceptance criteria:

- [x] A **ParaBank Bank Automation** card links to the repository and default-branch CI.
- [x] The card describes the Docker-backed SUT, UI and stateful API BDD lanes, OpenAPI validation
      and REST–SOAP parity without claiming a Pages demo that does not exist.
- [x] Header, footer, README and metadata say **nine showcase projects**, not eight.
- [x] The Sudoku card states the current **48-scenario** three-stack baseline.
- [x] `portfolio-prompts` is linked from a methodology/tooling area and is not counted as a showcase
      card.
- [x] The GitHub repository homepage is set to `https://gbrooks1970.github.io/portfolio/`.
- [x] Desktop and 390px mobile checks show every card, no horizontal overflow and no console errors.
- [x] GitHub Pages deploys the merged commit successfully and the live page matches the source.

Completion evidence: implementation commit `fe30c92058317564ac2bf07a0c96e29b75701e28` merged through
[PR #5](https://github.com/GBrooks1970/portfolio/pull/5) as
`69811285eead431290d5c70f3ee3d7288206a33c`. The exact merge commit was published successfully by
[Pages run 30706419372](https://github.com/GBrooks1970/portfolio/actions/runs/30706419372).
The live URL returned HTTP 200 and its line-ending-normalised HTML exactly matched `origin/main`
(SHA-256 `CE1EA5B76D73058D0CAD75798025C11E9B838B43038DE5D8E03CC141149D21DB`). Live browser checks at
1280 × 720 (3 columns) and 390 × 844 (1 column) found 9 cards, no horizontal overflow and no console
warnings/errors. See the original
[implementation log](implementation-logs/2026-08-01_land-01_portfolio-accuracy.md) and immutable
[publication closure](implementation-logs/2026-08-01_land-01_publication-closure.md).

### LAND-02 — Define durable presentation ownership

**Priority:** P0
**Status:** DONE
**Type:** Decision and design documentation

Record a durable boundary between canonical portfolio membership and public-facing presentation
copy before building a generator.

Recommended decision:

- `portfolio-prompts/registry.yml` owns membership and an explicit presentation role such as
  `showcase`, `methodology` or `hidden`.
- This repository owns titles, public summaries, display order, tags and demo/report URLs in a
  structured manifest keyed by the registry project identifier.
- CI compares the two sources. Runtime browser code must not call the GitHub API or fetch the
  registry.

Acceptance criteria:

- [x] A versioned decision record defines membership, presentation roles and ownership of public
      copy.
- [x] The decision states how future projects become visible and how retired projects are removed.
- [x] `portfolio-prompts` is classified as methodology; all nine current non-meta projects are
      classified as showcases.
- [x] The decision preserves a static deployable artefact and avoids runtime GitHub/API coupling.
- [x] The backlog dependencies are reconciled if the chosen design differs from the recommendation.

Completion evidence: [`decision 001`](decisions/001-presentation-ownership.md) records the accepted
hybrid boundary, full current classification, lifecycle procedures and static-generation contract.
The separate registry-schema implementation is explicit as LAND-02R; LAND-03/04 dependencies are
reconciled accordingly. Decision commit `2dcb5868d6959c42112233bc987acf5acb08eef2` and evidence
commit `baa9a21607ac1034e3f9a4b57c4b234195e45902` merged through
[PR #7](https://github.com/GBrooks1970/portfolio/pull/7) as
`3f4f77f456fc372f6f1da813a807e48beafda5dd`. The exact merge commit was published successfully by
[Pages run 30710048684](https://github.com/GBrooks1970/portfolio/actions/runs/30710048684).
See the original
[implementation log](implementation-logs/2026-08-01_land-02_presentation-ownership.md).

### LAND-02R — Implement presentation roles in the canonical registry

**Priority:** P1
**Status:** DONE
**Type:** Cross-repository schema, validation and documentation (`NeoCognitus70/portfolio-prompts`)

Implement decision 001's registry-owned `presentation_role` without mixing the change into this
landing repository.

Acceptance criteria:

- [x] Every `projects:` row in `portfolio-prompts/registry.yml` declares exactly one
      `presentation_role`: `showcase`, `methodology` or `hidden`.
- [x] The nine current non-meta projects are `showcase`; `portfolio-prompts` is `methodology`.
- [x] Registry validation rejects missing and unsupported roles and proves lifecycle status and
      `orchestration_target` remain independent.
- [x] Registry field documentation and tests cover showcase, methodology and hidden cases.
- [x] `python tools/check-library.py` passes locally and on the current PR head.
- [x] Registry owner merges the PR and post-merge `main` CI is green.
- [x] This backlog records the merged registry commit for LAND-03/04 to consume.

Completion evidence: implementation commit
[`d9ea5d0`](https://github.com/NeoCognitus70/portfolio-prompts/commit/d9ea5d02886bf518aaebd33f72f9e1cdbe31d1f5)
and implementation-log/evidence commits through head `47f3c02db8d9ea508a3bed3090c4913351bab070`
merged through [portfolio-prompts PR #50](https://github.com/NeoCognitus70/portfolio-prompts/pull/50)
as `78a7a3e40c3ea614674dee106d78854471cee571`.
The local self-gate passed with 13 tests; current-head PR integrity
[run 30710503211](https://github.com/NeoCognitus70/portfolio-prompts/actions/runs/30710503211)
and post-merge `main` integrity
[run 30710731714](https://github.com/NeoCognitus70/portfolio-prompts/actions/runs/30710731714)
both passed. LAND-03/04 must consume the merged commit above, never the topic-branch commit.
See the immutable
[LAND-02 closure / LAND-02R review log](implementation-logs/2026-08-01_land-02-closure_land-02r-review.md)
and final [LAND-02R registry closure log](implementation-logs/2026-08-01_land-02r-registry-closure.md).

### LAND-03 — Generate cards and counts from structured data

**Priority:** P1
**Status:** DONE
**Type:** Code and generated HTML

Replace repeated hand-authored cards and numeric prose with a deterministic presentation manifest
and generator while retaining a static Pages output.

Acceptance criteria:

- [x] Structured project data has a documented schema and stable registry identifier per entry.
- [x] Card HTML, showcase count and methodology links are generated from that data.
- [x] Display order is explicit and deterministic.
- [x] Generated output is committed by the recorded strategy; contributors do not
      hand-edit generated regions.
- [x] Generation is byte-stable for unchanged input and has an executable `--check` mode.
- [x] All LAND-01 public content remains present after migration.
- [x] Every generated external link resolves for an unauthenticated visitor.
- [x] Owner merges the PR; the exact Pages deployment succeeds and the live output is verified.

Completion evidence: branch `codex/land-03-generated-portfolio` pins canonical registry merge
`78a7a3e40c3ea614674dee106d78854471cee571`; `python tools/generate_site.py --check` PASS;
3/3 deterministic tests PASS; desktop 1280 × 720 and mobile 390 × 844 checks found 9 showcase
cards, one methodology entry, 3/1 columns, no horizontal overflow, contained actions and no console
warnings/errors; all 24 external links and `LICENSE` resolve. Implementation commit
[`12d502d`](https://github.com/GBrooks1970/portfolio/commit/12d502db8f9dee1d4c0e34f0dec4d6e3c57357a9)
and evidence commit `6d2537423da4965fcf7dc0e67fd54d16308deee7` merged through
[PR #9](https://github.com/GBrooks1970/portfolio/pull/9) as
`b7037b3e2e2932b87eca5294594dc29f238be5d5`. Exact-merge
[Pages run 30716076304](https://github.com/GBrooks1970/portfolio/actions/runs/30716076304)
passed. The live URL returned HTTP 200 with 9 showcase cards, ParaBank and the methodology entry;
its line-ending-normalised HTML exactly matched the merge commit at SHA-256
`4C964DF58AF80166E0B94BA4B66E9D2900522F2855492CC74F08F9F7CD0B3326`. See the immutable
[implementation log](implementation-logs/2026-08-01_land-03-generated-portfolio.md) and
[publication closure](implementation-logs/2026-08-01_land-03-publication-closure.md).

### LAND-04 — Enforce registry-to-landing inventory parity

**Priority:** P1
**Status:** DONE
**Type:** CI and validation code

Make a missing or unknown public project a failing pull-request check rather than a visual-review
discovery.

Acceptance criteria:

- [x] Validation compares registry identifiers and presentation roles with the landing manifest.
- [x] It fails when a required showcase is absent, an unknown project is present or a methodology
      project is counted as a showcase.
- [x] It fails when the displayed/generated showcase count differs from the manifest.
- [x] Tests cover missing, extra, duplicate, hidden and methodology entries.
- [x] The check runs on pull requests without write permissions or repository secrets.
- [x] Registry source/ref and failure recovery are documented so the check is reproducible.

Completion evidence: implementation commit
[`70dec95`](https://github.com/GBrooks1970/portfolio/commit/70dec9554a7b2c098fb1ab67dd59396fe2c00c07)
on branch `codex/land-04-ci-parity`; `tools/check_registry_parity.py` rebuilt the lock from canonical
commit `78a7a3e40c3ea614674dee106d78854471cee571` and passed with 9 showcase / 1 methodology projects;
deterministic unit suite passed 10/10, including seven explicit LAND-04 parity cases; generator
`--check`, workflow least-privilege assertions, Markdown links and `git diff --check` passed.
Read-only pull-request
[run 30716526046](https://github.com/GBrooks1970/portfolio/actions/runs/30716526046)
passed at the exact implementation head. Owner merged [PR #10](https://github.com/GBrooks1970/portfolio/pull/10)
as `c70855af2c2ebbe287f2496c98704a8b554bad22`; exact-merge `main`
[parity run 30716866062](https://github.com/GBrooks1970/portfolio/actions/runs/30716866062) and
[Pages run 30716865649](https://github.com/GBrooks1970/portfolio/actions/runs/30716865649)
both passed. The live page returned HTTP 200, retained 9 cards and exactly matched `main` at
normalised SHA-256 `4C964DF58AF80166E0B94BA4B66E9D2900522F2855492CC74F08F9F7CD0B3326`.
See the immutable [implementation log](implementation-logs/2026-08-01_land-04-registry-parity.md)
and [merge closure](implementation-logs/2026-08-01_land-04-merge-closure.md).

### LAND-05 — Add publication-quality automated gates

**Priority:** P1
**Status:** DONE
**Type:** CI and validation code

The repository currently relies on the Pages deployment alone. Add fast pull-request checks for
the static artefact.

Acceptance criteria:

- [x] HTML structure and duplicate identifiers are validated.
- [x] Repository, demo/report and workflow URLs are checked with a documented policy for transient
      failures.
- [x] Internal links and required metadata are validated.
- [x] Automated accessibility checks cover landmark structure, names, focusability and contrast.
- [x] A local command reproduces the CI gate without requiring secrets.
- [x] Pages deployment remains a separate post-merge signal; a successful deploy is not treated as
      proof that content is correct.

Completion evidence: implementation commit
[`90a334b`](https://github.com/GBrooks1970/portfolio/commit/90a334b006a93e5703ba16cf3381af2f0569b15b)
on branch `codex/land-05-quality-gate`; complete local command passed canonical parity for 9
showcase / 1 methodology projects, 34 named controls, all 33 unique external link/resource targets,
16 light/dark contrast pairs and 20/20 deterministic tests. The first quality run found the dark
primary action at 2.96:1; the theme-specific text token raises it to 6.20:1. Read-only pull-request
[run 30717568452](https://github.com/GBrooks1970/portfolio/actions/runs/30717568452)
passed at the exact implementation head in [PR #11](https://github.com/GBrooks1970/portfolio/pull/11).
Owner merged PR #11 as `16c2cf2f6f83d84b1c50eb64fea3049a06f6b549`; exact-merge
[quality run 30719108064](https://github.com/GBrooks1970/portfolio/actions/runs/30719108064)
and [Pages run 30719107654](https://github.com/GBrooks1970/portfolio/actions/runs/30719107654)
both passed. The live page returned HTTP 200 with nine showcase cards and one methodology entry;
normalised live and `main` SHA-256 both equal
`455FDFA2EFF6B1F41AA01225FB1C4238D69CDE6E23019D75F4B240ED5D049F94`. See
[decision 002](decisions/002-publication-quality-gate.md), the immutable
[implementation log](implementation-logs/2026-08-01_land-05-publication-quality-gate.md) and
[merge closure](implementation-logs/2026-08-01_land-05-merge-closure.md).

Platform observation: exact-merge Pages run 30716076304 passed but reported that GitHub's generated
Pages workflow still invokes Node 20-based `actions/checkout@v4` and `actions/upload-artifact@v4`
under a forced Node 24 runtime. LAND-05 must use current Node 24 action releases for any
repository-owned workflow; the GitHub-managed Pages warning remains an external platform signal.

### LAND-06 — Strengthen navigation and accessibility contracts

**Priority:** P1
**Status:** DONE WITH EXCEPTION — owner accepted documented 390px/keyboard evidence gaps
**Type:** HTML and CSS

Acceptance criteria:

- [x] A skip link targets the project collection.
- [x] The project collection has a visible heading and coherent heading hierarchy.
- [x] Every CI badge/link has a project-specific accessible name.
- [x] Keyboard focus has an explicit, high-contrast `:focus-visible` treatment.
- [x] Primary actions provide comfortable touch targets, aiming for 44px while retaining responsive
      wrapping.
- [x] Light and dark colour schemes pass the chosen automated contrast checks — pre-delivered by
      LAND-05's 16-pair gate and dark primary-button token correction.
- [x] 390px and desktop layouts have no horizontal overflow or obscured actions — closed by owner
      acceptance of LAND-03's verified 390px baseline plus unchanged horizontal geometry; no fresh
      390px render was obtained in LAND-06.

Completion evidence: implementation commit
[`c26dcf2`](https://github.com/GBrooks1970/portfolio/commit/c26dcf2794459c904d1fdf05feb778bcdd2dd89c)
on branch `codex/land-06-accessibility`; complete local gate passed with 35 named controls, two
internal references, 33 external targets, 20 light/dark text/focus pairs and 25/25 tests.
At 1280 × 720 dark mode, browser inspection found nine cards, three columns, no horizontal/action
overflow, no console errors, nine project-specific CI name pairs and a 44.996px minimum action
height. First keyboard focus exposed the skip link with its visible ring; activating it moved focus
to labelled `main#projects`. Exact-head pull-request
[run 30719723900](https://github.com/GBrooks1970/portfolio/actions/runs/30719723900)
passed in [draft PR #12](https://github.com/GBrooks1970/portfolio/pull/12).

The available browser could not expose a 390px viewport and its security policy rejected an
embedded preview; direct keyboard activation dispatch also remained unreliable. After these gaps
were reported, the owner explicitly instructed merge. PR #12 merged as
`628b58c8cae8423d4c2d13fb6d3da66343a003a4`; exact-merge
[quality run 30720104041](https://github.com/GBrooks1970/portfolio/actions/runs/30720104041)
and [Pages run 30720103723](https://github.com/GBrooks1970/portfolio/actions/runs/30720103723)
both passed. The live page returned HTTP 200 with all LAND-06 structural markers and exactly
matched `main` at normalised SHA-256
`19D40D49BEF3FAFC9586D013015199D2196CE7689124BE873968A371ABDADC8F`.

LAND-06 is therefore DONE WITH EXCEPTION. The 390px conclusion uses LAND-03's verified one-column
390px result plus the fact that LAND-06 did not widen the grid, cards, wrapper or action padding;
this is an accepted inference, not a fresh viewport pass. See the immutable
[implementation log](implementation-logs/2026-08-01_land-06-navigation-accessibility.md) and
[merge closure](implementation-logs/2026-08-01_land-06-merge-closure.md).

### LAND-07 — Search and social discoverability

**Priority:** P2
**Status:** DONE
**Type:** Generated HTML metadata, static assets, validation and repository settings

Give the portfolio one consistent, evidence-backed identity for search engines, link previews,
browsers and its GitHub repository. Preserve the static, dependency-free visitor experience: this
item must not add analytics, cookies, client-side API calls or runtime service dependencies.

Accepted design:

- Add a versioned `data/site.json` as the landing repository's single source for the canonical URL,
  site title, public description, author identity and social-image metadata. Keep site identity
  separate from project presentation data.
- Generate an absolute HTTPS canonical URL, Open Graph metadata and minimal Twitter/X compatibility
  metadata from that source.
- Describe the visible site with a JSON-LD `WebSite` and `Person` graph. Do not claim `ProfilePage`
  while the page is primarily a project catalogue, and do not add employers, qualifications,
  locations or other identity claims that are absent from visible, verified content.
- Use an evergreen, solid-background design without a project count. Export a 1200 × 630 webpage
  preview and a separate 1280 × 640 GitHub repository preview from the same visual design.
- Publish a concise sitemap and robots policy for the one canonical public page.

Acceptance criteria:

- [x] `data/site.json` has a documented, validated schema and is the authoritative source for site
      identity metadata used by generated output.
- [x] Generated HTML contains exactly one HTTPS canonical link, and its URL agrees with `og:url`,
      the JSON-LD website URL, sitemap and configured public homepage.
- [x] Open Graph includes `og:type=website`, title, description, URL, site name, `en_GB` locale and
      an absolute image URL with MIME type, actual dimensions and meaningful alternative text.
- [x] Minimal Twitter/X compatibility metadata uses a large-image card and agrees with the Open
      Graph title, description, image and image alternative text.
- [x] Valid JSON-LD links a `WebSite` to a `Person` whose name, role, URL and `sameAs` values are
      supported by visible portfolio content; automated validation rejects malformed or drifting
      data.
- [x] A simple branded SVG favicon, 32 × 32 PNG fallback and Apple touch icon are committed,
      generated into the document head and validated as resolvable internal assets.
- [x] `assets/portfolio-social-preview-1200x630.png` and
      `assets/github-social-preview-1280x640.png` exist at their declared dimensions, remain legible
      at preview size and contain no dynamic project count or stale CI evidence.
- [x] `sitemap.xml` contains the canonical page without a fabricated freshness date; `robots.txt`
      allows public crawling and points to the sitemap.
- [x] The deterministic generator and publication-quality gate cover missing or duplicate
      canonicals, URL disagreement, required preview fields, asset existence and dimensions,
      malformed structured data, icons, sitemap and robots policy. Before merge, absolute URLs
      under the canonical site map back to local assets instead of requiring the asset to exist on
      the current public `main` deployment.
- [x] The GitHub repository description is reconciled to “Static portfolio of test-automation
      projects spanning UI, API, mobile web, WebSocket and multi-stack parity.”; the homepage stays
      `https://gbrooks1970.github.io/portfolio/`; discoverability topics include
      `test-automation`, `quality-engineering`, `portfolio`, `playwright`, `serenity-js`, `bdd` and
      `github-pages`; and the dedicated GitHub social-preview image is uploaded and verified.
- [x] The documented local gate and current-head pull-request CI pass. After owner merge, exact-merge
      quality and Pages runs pass, the live HTML matches `main`, and canonical, favicon, sitemap and
      social-image URLs return successfully.

Implementation evidence: commit `00f827a2cbdaf81241f8ab1029000e9acdc141cc` on branch
`codex/land-07-implementation`; byte-stable HTML/sitemap/robots check PASS; complete local gate PASS
for 9 showcase / 1 methodology projects, 35 named controls, 5 internal references, 34 external URLs,
20 contrast pairs and 36/36 tests. Repository description, homepage and seven topics match
`data/site.json`; the 1280 × 640 repository preview was uploaded and visually verified in GitHub
settings. See the immutable
[implementation log](implementation-logs/2026-08-02_land-07-discoverability.md). That implementation
was reviewed in [PR #15](https://github.com/GBrooks1970/portfolio/pull/15); closure evidence follows.

Completion evidence: [PR #15](https://github.com/GBrooks1970/portfolio/pull/15) merged as
`6c71e00f7ba98572945e2acb664b45a9c5fe9945`. Exact-merge
[Portfolio quality run 30734100251](https://github.com/GBrooks1970/portfolio/actions/runs/30734100251)
and [Pages run 30734099813](https://github.com/GBrooks1970/portfolio/actions/runs/30734099813)
both passed. The public HTML and six referenced supporting outputs returned HTTP 200; deployed HTML,
social PNG, PNG icons, sitemap and robots exactly matched `main`, while the SVG exactly matched the
commit-pinned raw blob after excluding Windows working-tree line-ending conversion. Live metadata
contained exactly one canonical, matching Open Graph URL/image, one `Person`, one `WebSite` and no
`ProfilePage`. Repository description, homepage, seven topics and the uploaded repository preview
remain reconciled. See the immutable
[merge closure](implementation-logs/2026-08-02_land-07-merge-closure.md).

## Candidate improvements — unscheduled

The following items are **PROPOSED**. They are not part of the current required cycle and must not be
implemented until promoted here by the owner. LAND-C01 was promoted as LAND-07 on 2026-08-02; its
accepted scope and provenance are retained above.

### LAND-C02 — Information architecture and portfolio narrative

Evaluate grouping showcases by capability—UI/E2E, API/protocols, multi-stack/libraries and
products—and add concise, generated portfolio statistics. Avoid filters until the number of cards
creates a real navigation problem.

### LAND-C03 — Expand public evidence

Provide consistent evidence links where useful. Candidate outputs include a static ParaBank
Serenity report snapshot, a hand-baked Screenplay sample report, calculator API documentation and
Sudoku interactive evidence. Do not attempt to host Docker-backed SUTs on GitHub Pages.

### LAND-C04 — Generated freshness information

Generate a last-updated value and optional CI/evidence summary during deployment. Do not call GitHub
APIs from visitors' browsers and do not imply that a stale timestamp means a project is unhealthy.

## Owner decisions

| Decision | State | Recorded outcome |
|---|---|---|
| OD-LAND-01 — Hotfix before generator | Accepted for this cycle | LAND-01 precedes LAND-03 so the missing ParaBank card is not delayed |
| OD-LAND-02 — Meta-project presentation | Accepted for this cycle | `portfolio-prompts` appears as methodology/tooling, not as the tenth showcase card |
| OD-LAND-03 — Durable data ownership | Accepted 2026-08-01 | Hybrid boundary recorded in decision 001: registry owns membership/role; landing owns public copy/order |
| OD-LAND-04 — ParaBank public artefact | Pending candidate promotion | Repository + CI now; consider a static Serenity snapshot later, never the Docker SUT |
| OD-LAND-05 — Public methodology target | Accepted 2026-08-01 | Make `NeoCognitus70/portfolio-prompts` public after a repository/history/log scan; unauthenticated access now returns 200 and secret scanning/push protection are enabled |
| OD-LAND-06 — Browser evidence exception | Accepted 2026-08-01 | Merge LAND-06 with no fresh 390px render or reliable keyboard-only Enter dispatch; retain the gaps and inherited-evidence rationale permanently |
| OD-LAND-07 — Search/social scope | Accepted 2026-08-02 | Promote LAND-C01 as LAND-07/P2 with `data/site.json`, `WebSite` + `Person`, evergreen dual preview assets, favicons, sitemap/robots, repository metadata/topics and automated plus post-merge live verification |

## Maintenance rules

- Update the version and date whenever item status or scope changes.
- Do not tick acceptance criteria without exact evidence.
- Record a completed development task in `docs/implementation-logs/` before marking it DONE.
- Preserve resolved items in this file or a linked archive; do not erase the decision trail.
- Keep en-GB spelling and avoid model-specific instructions.
