# Portfolio Landing — Backlog

**Version:** 5
**Last updated:** 2026-08-01
**Status:** ACTIVE — LAND-01 and LAND-02 complete; LAND-02R in review; LAND-05 and LAND-06 ready
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

## Current required cycle

| ID | Priority | Status | Depends on | Outcome |
|---|---|---|---|---|
| LAND-01 | P0 | DONE | — | Restore public inventory and factual accuracy |
| LAND-02 | P0 | DONE | LAND-01 | Define durable presentation ownership |
| LAND-02R | P1 | IN REVIEW | LAND-02 | Implement presentation roles in the canonical registry |
| LAND-03 | P1 | BLOCKED | LAND-02R | Generate cards and counts from structured data |
| LAND-04 | P1 | BLOCKED | LAND-02R, LAND-03 | Enforce registry-to-landing inventory parity in CI |
| LAND-05 | P1 | READY | — | Add publication-quality automated gates |
| LAND-06 | P1 | READY | LAND-01 | Strengthen navigation and accessibility contracts |

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
**Status:** IN REVIEW — registry owner merge and post-merge `main` CI pending
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
- [ ] Registry owner merges the PR and post-merge `main` CI is green.
- [ ] This backlog records the merged registry commit for LAND-03/04 to consume.

Completion evidence: implementation commit
[`d9ea5d0`](https://github.com/NeoCognitus70/portfolio-prompts/commit/d9ea5d02886bf518aaebd33f72f9e1cdbe31d1f5)
and implementation-log/evidence commits through current head `47f3c02db8d9ea508a3bed3090c4913351bab070`
are in draft [portfolio-prompts PR #50](https://github.com/NeoCognitus70/portfolio-prompts/pull/50).
The local self-gate passed with 13 tests; current-head PR integrity
[run 30710503211](https://github.com/NeoCognitus70/portfolio-prompts/actions/runs/30710503211)
also passed. Owner merge, the merged registry commit and post-merge `main` CI remain pending.
See the immutable
[LAND-02 closure / LAND-02R review log](implementation-logs/2026-08-01_land-02-closure_land-02r-review.md).

### LAND-03 — Generate cards and counts from structured data

**Priority:** P1
**Status:** BLOCKED — LAND-02R
**Type:** Code and generated HTML

Replace repeated hand-authored cards and numeric prose with a deterministic presentation manifest
and generator while retaining a static Pages output.

Acceptance criteria:

- [ ] Structured project data has a documented schema and stable registry identifier per entry.
- [ ] Card HTML, showcase count and methodology links are generated from that data.
- [ ] Display order is explicit and deterministic.
- [ ] Generated output is committed or deployed by the recorded strategy; contributors do not
      hand-edit generated regions.
- [ ] Generation is byte-stable for unchanged input and has an executable `--check` mode.
- [ ] All LAND-01 public content remains present after migration.

Completion evidence: **Blocked; none.**

### LAND-04 — Enforce registry-to-landing inventory parity

**Priority:** P1
**Status:** BLOCKED — LAND-02R and LAND-03
**Type:** CI and validation code

Make a missing or unknown public project a failing pull-request check rather than a visual-review
discovery.

Acceptance criteria:

- [ ] Validation compares registry identifiers and presentation roles with the landing manifest.
- [ ] It fails when a required showcase is absent, an unknown project is present or a methodology
      project is counted as a showcase.
- [ ] It fails when the displayed/generated showcase count differs from the manifest.
- [ ] Tests cover missing, extra, duplicate, hidden and methodology entries.
- [ ] The check runs on pull requests without write permissions or repository secrets.
- [ ] Registry source/ref and failure recovery are documented so the check is reproducible.

Completion evidence: **Blocked; none.**

### LAND-05 — Add publication-quality automated gates

**Priority:** P1
**Status:** READY
**Type:** CI and validation code

The repository currently relies on the Pages deployment alone. Add fast pull-request checks for
the static artefact.

Acceptance criteria:

- [ ] HTML structure and duplicate identifiers are validated.
- [ ] Repository, demo/report and workflow URLs are checked with a documented policy for transient
      failures.
- [ ] Internal links and required metadata are validated.
- [ ] Automated accessibility checks cover landmark structure, names, focusability and contrast.
- [ ] A local command reproduces the CI gate without requiring secrets.
- [ ] Pages deployment remains a separate post-merge signal; a successful deploy is not treated as
      proof that content is correct.

Completion evidence: **Not yet implemented.**

### LAND-06 — Strengthen navigation and accessibility contracts

**Priority:** P1
**Status:** READY — implement with or after LAND-01
**Type:** HTML and CSS

Acceptance criteria:

- [ ] A skip link targets the project collection.
- [ ] The project collection has a visible heading and coherent heading hierarchy.
- [ ] Every CI badge/link has a project-specific accessible name.
- [ ] Keyboard focus has an explicit, high-contrast `:focus-visible` treatment.
- [ ] Primary actions provide comfortable touch targets, aiming for 44px while retaining responsive
      wrapping.
- [ ] Light and dark colour schemes pass the chosen automated contrast checks.
- [ ] 390px and desktop layouts have no horizontal overflow or obscured actions.

Completion evidence: **Not yet implemented.**

## Candidate improvements — unscheduled

The following items are **PROPOSED**. They are not part of the current required cycle and must not be
implemented until promoted here by the owner.

### LAND-C01 — Search and social discoverability

Add a canonical URL, Open Graph/Twitter metadata, social-preview image, favicon and appropriate
structured data. Reconcile the GitHub repository description and homepage with the live site.

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

## Maintenance rules

- Update the version and date whenever item status or scope changes.
- Do not tick acceptance criteria without exact evidence.
- Record a completed development task in `docs/implementation-logs/` before marking it DONE.
- Preserve resolved items in this file or a linked archive; do not erase the decision trail.
- Keep en-GB spelling and avoid model-specific instructions.
