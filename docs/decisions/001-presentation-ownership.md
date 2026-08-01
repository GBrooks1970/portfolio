# Decision 001 — Portfolio Presentation Ownership

**Status:** Accepted
**Date:** 2026-08-01
**Decision owner:** Portfolio owner
**Applies to:** `GBrooks1970/portfolio` and the public-presentation contract with
`NeoCognitus70/portfolio-prompts`
**Backlog:** LAND-02

## Context

The public landing page historically repeated portfolio membership, project counts and display copy
inside hand-authored HTML. ParaBank joined the canonical registry after the last landing update, so
the public page remained at eight projects until LAND-01 corrected it. The audit identified split,
unvalidated ownership as the root cause.

The existing registry already owns lifecycle status and orchestration eligibility. Those concepts
must remain independent from public presentation: a resting project is still a showcase, a meta
project may appear as methodology, and orchestration eligibility must never decide visibility.

## Decision

Adopt a hybrid, build-time ownership model.

### Canonical registry ownership

`portfolio-prompts/registry.yml` owns:

- the stable project identifier (`project`);
- the canonical GitHub repository slug (`github`);
- portfolio membership;
- lifecycle status and orchestration eligibility under their existing meanings; and
- a required `presentation_role` for each `projects:` row.

`presentation_role` is an enum with these meanings:

| Role | Public treatment |
|---|---|
| `showcase` | Requires a landing manifest entry, produces one showcase card and contributes to the showcase count |
| `methodology` | Requires a landing manifest entry, appears in methodology/tooling and never contributes to the showcase count |
| `hidden` | Remains a registry member but must not have public presentation content or affect public counts |

Lifecycle `status`, `orchestration_target` and `presentation_role` are orthogonal. Tooling must not
derive one from another.

The `portfolio-landing` support repository remains outside `projects:` and is not assigned a
presentation role. It hosts the presentation surface; it is not content presented by that surface.

### Landing repository ownership

This repository will own a versioned JSON presentation manifest, introduced by LAND-03 and keyed by
the exact registry project identifier. For every `showcase` or `methodology` project it will own:

- public title, discipline and concise summary;
- deterministic display order;
- presentation tags;
- optional workflow path used to construct a CI action; and
- optional demo or report URLs and their truthful public labels.

The repository action URL is derived from the registry-owned `github` slug. The manifest must not
duplicate membership, GitHub slugs, lifecycle state, orchestration eligibility or presentation role.
Hidden projects must not have manifest entries. Unknown, missing, duplicate or role-incompatible
entries are validation failures.

The initial manifest schema will use this shape; LAND-03 may add backwards-compatible validation
metadata but must not move the ownership boundary:

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
        "workflow": null,
        "demo": null,
        "report": null
      }
    }
  }
}
```

### Build and deployment boundary

- Generation and parity validation happen before deployment, never in a visitor's browser.
- CI may check out the public registry repository or read a caller-supplied local registry path; the
  exact registry commit used must be visible in validation evidence.
- The generator produces deterministic static HTML and numeric summaries from registry roles plus
  the landing manifest.
- Generated output is committed and verified by a byte-stable `--check` mode unless a later recorded
  decision deliberately changes the Pages build strategy.
- The deployed page has no runtime dependency on GitHub APIs, registry availability, credentials or
  cross-origin requests.

## Current classification

This table is normative for the LAND-02R registry change:

| Registry project | Presentation role |
|---|---|
| `magento-checkout-automation` | `showcase` |
| `hand-baked-screenplay-pattern` | `showcase` |
| `calculator-screenplay-bdd` | `showcase` |
| `gb.automation.smoketests.sudoku.poc` | `showcase` |
| `bfx-ws-screenplay` | `showcase` |
| `orangehrm-pim-automation` | `showcase` |
| `markdown-renderer` | `showcase` |
| `mobile-forex-automation` | `showcase` |
| `parabank-bank-automation` | `showcase` |
| `portfolio-prompts` | `methodology` |

There are no hidden projects at the time of this decision.

## Lifecycle procedures

### Make a new project visible

1. Onboard the project into the canonical registry with its stable identifier, GitHub slug and
   explicit presentation role.
2. Merge and validate that registry change in `portfolio-prompts`.
3. In a separate landing PR, add the required public manifest entry, update the recorded registry
   commit, regenerate static output and pass parity/publication gates.
4. Merge the landing PR, observe Pages and verify the live output before claiming publication.

A project is not publicly presented merely because a repository exists or because it is an
orchestration target.

### Hide or retire a project

- Set `presentation_role: hidden` when membership and lifecycle records must remain but public
  presentation should stop. Remove its landing manifest entry and generated output in the linked
  landing PR.
- Use lifecycle `status: resting` only to mean zero outstanding project work; it does not hide the
  project.
- Remove a registry row only when the project is no longer a portfolio member. The landing manifest
  entry and generated output must be removed in the coordinated landing PR.
- A methodology project moved to hidden must disappear from methodology/tooling and must never alter
  the showcase count.

## Delivery sequence

The ownership decision is implemented in separate repositories and review units:

1. **LAND-02R:** add and validate `presentation_role` in `portfolio-prompts`.
2. **LAND-03:** add the landing manifest, deterministic generator and committed generated output.
3. **LAND-04:** enforce registry-to-manifest/output parity in pull-request CI.

LAND-03 is blocked by LAND-02R. LAND-04 is blocked by LAND-02R and LAND-03.

## Consequences

Benefits:

- membership and public roles have one canonical owner;
- public editorial copy remains with the site that presents it;
- counts and cards become deterministic rather than repeated prose;
- CI can fail on omissions before publication; and
- GitHub Pages stays static, fast and resilient.

Costs and constraints:

- onboarding and retirement require coordinated PRs in two repositories;
- CI needs an explicit, reproducible registry input;
- generated HTML must not be hand-edited; and
- a registry change can intentionally block landing work until public copy is supplied.

## Rejected alternatives

### Keep all data in `index.html`

Rejected because LAND-01 proved that manual membership and counts drift without a machine contract.

### Put all public copy in the canonical registry

Rejected because lifecycle tooling should not own marketing prose, visual order, tags or demo/report
presentation. It would couple registry maintenance to landing-page design.

### Fetch GitHub or registry data at runtime

Rejected because it introduces visitor-visible network/authentication/rate-limit failures, weakens
determinism and is unnecessary for a static portfolio.

### Derive presentation role from lifecycle status or orchestration eligibility

Rejected because the concepts have different meanings. Resting projects remain public showcases,
while the meta project is methodology and deliberately excluded from orchestration fan-outs.
