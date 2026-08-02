# Implementation Log — LAND-08: Information Architecture and Portfolio Narrative

**Date:** 2026-08-02
**Backlog item:** `LAND-08`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `codex/land-08-implementation`
**Implementation commit:** `9e79ee645e99773ae2f7f8f8f9f947fb208ab911`
**Pull request:** Pending
**Pages run:** Pending — public output requires owner merge, exact-merge quality, Pages and live
verification

## Outcome

The nine-showcase catalogue is now organised into four landing-owned primary capability groups:
Web UI and end-to-end; APIs, BDD and real-time protocols; multi-stack and framework design; and
mobile and shipped products. Every showcase appears once, while its existing tags retain secondary
technical scope. A compact 9/4/4 summary is generated from source data for showcase projects,
capability areas and non-null public demo/report actions.

The presentation manifest advances to schema version 2, grouped output is deterministic and
semantic, cards use `h4` beneath group `h3` headings, and the static visitor experience gains no
JavaScript, filtering, analytics or runtime API dependency. The complete local gate passes with 9
showcases, 1 methodology entry, 35 named controls, 5 internal references, 34 external URLs, 20
contrast pairs and 43 deterministic tests.

## Scope

- `data/presentation.json` — define four ordered capability groups and one group assignment for
  every showcase; keep the methodology entry outside the taxonomy with `group: null`.
- `tools/generate_site.py` — validate the schema, group keys, labels, orders, assignments and
  non-empty groups; render grouped sections and derive the 9/4/4 statistics.
- `index.template.html` and generated `index.html` — add a compact statistics summary, group
  narratives, responsive per-group card grids and the accepted H1/H2/H3/H4 hierarchy.
- `tools/check_registry_parity.py` — verify rendered group order, project assignments and all three
  generated counts against structured source data.
- `tools/check_site.py` — require named capability sections, `h4` card headings and cards nested
  within a capability section while retaining LAND-03 through LAND-07 controls.
- `tools/tests/` — extend generator, parity and site-quality regression coverage from 36 to 43
  tests, including invalid, missing, duplicate and drifting group/count cases.
- `README.md`, `docs/generation.md` and `docs/quality-gate.md` — document taxonomy ownership,
  schema version 2, derived-statistics semantics and grouped accessibility checks.
- Explicit non-goals: no filters, search, sorting, new evidence artefacts, freshness/CI summaries,
  browser-side API calls or registry-role changes.

## Decisions

- Store group definitions and assignments with landing-owned presentation data. Capability grouping
  is a public narrative choice and must not become a canonical lifecycle field in the registry.
- Give every showcase one primary group. Duplicating cross-cutting projects would break inventory
  counts, reading order and deterministic parity; tags continue to communicate secondary scope.
- Use stable kebab-case keys plus explicit numeric orders. JSON object order has no public meaning,
  and the generator can reject duplicate orders or empty groups before output is written.
- Count public evidence as each non-null showcase `demo` or `report` action. This is reproducible and
  does not imply that a linked artefact is fresh or that current CI is green.
- Keep all statistics generated and the page dependency-free. Nine cards do not justify visitor-side
  filtering or a client data layer.
- Use `h3` group headings and `h4` card titles beneath the existing `h2` showcase heading, preserving
  a meaningful outline without adding hidden labels.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| Complete local command | PASS | 9 showcase, 1 methodology, 35 controls, 5 internal references, 34 external URLs and 20 contrast pairs |
| Python unit suite | PASS | 43/43 tests; seven LAND-08 regressions added to the 36-test baseline |
| Generated outputs | PASS | `python tools/generate_site.py --check` confirms committed HTML, sitemap and robots bytes |
| Python compilation | PASS | `python -m compileall -q tools` |
| External targets | PASS | All 34 unique HTTPS `href`/`src` targets returned HTTP 200–399 |
| Desktop render | PASS | 1440px override / 1425px content viewport; four groups render 3/2/2/2 cards; 9/4/4 statistics; no horizontal or out-of-viewport card overflow |
| Mobile render | PASS | 390px override / 375px content viewport; all nine cards are 331px wide; zero document/card/action overflow; all 22 actions are at least 44px high |
| Accessibility/keyboard | PASS for LAND-08 scope | DOM exposes H1/H2/H3/H4 and four named regions; skip and card-title links show the explicit focus outline; LAND-08 adds no new interactive controls |
| Console | PASS | No warning or error entries after desktop and mobile reloads |
| Whitespace | PASS | `git diff --check` clean |
| Pull-request CI | PENDING | Implementation PR has not yet been opened |
| Owner merge / `main` / Pages / live page | PENDING | Required before LAND-08 can move from IN REVIEW to DONE |

## Failures and recovery

- The first unit run exposed a LAND-06 regression fixture still replacing `main.grid`. Updating the
  fixture to the new `main.portfolio` contract restored the 43-test pass without weakening the
  missing-landmark assertion.
- The browser's very tall full-page mobile capture repeated and clipped visual bands. Bounded
  viewport captures were clear, and DOM geometry independently proved zero document, card, block or
  action overflow at 390px.
- Browser-level raw Tab/Enter dispatch remains unreliable for the existing skip link, as already
  recorded by the accepted LAND-06 exception. Locator-driven keyboard focus confirmed the skip link
  reveal and project-link outline. LAND-08 introduces no new interactive path, so this inherited gap
  does not expand the exception or block the grouped information architecture.

## Durable lessons

- A portfolio taxonomy is safest as a primary presentation classification with tags for secondary
  capabilities; many-to-many card duplication makes both counts and navigation ambiguous.
- Generated statistics remain trustworthy only when their counting rule is explicit. In particular,
  “public demos and reports” counts source actions, not projects, availability or health.
- Semantic grouping changes the heading contract as well as the CSS. Generator, parity and static
  accessibility checks must move together so a visual refactor cannot silently flatten the outline.
- Browser screenshots and DOM geometry are complementary evidence. A capture backend can distort a
  tall page even when layout measurements and bounded screenshots are correct.

## Backlog reconciliation

- Nine implementation acceptance criteria are complete with source, generation, regression,
  external-link and rendered-browser evidence.
- LAND-08 moves from READY to IN REVIEW at implementation commit `9e79ee6`; current-head PR CI,
  owner merge, exact-merge quality, Pages and live-page parity remain open.
- LAND-C03 and LAND-C04 remain proposed and unchanged.
