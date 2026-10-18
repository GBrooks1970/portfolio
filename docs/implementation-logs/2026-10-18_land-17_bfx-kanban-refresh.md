# Implementation Log — LAND-17: BFX Kanban link refresh

**Date:** 2026-10-18
**Backlog item:** LAND-17
**Repository:** `GBrooks1970/portfolio`
**Branch:** `feat/link-bfx-kanban-board`
**Commit:** Refresh follows plan commit `441adaa`; reconciles main `3fa9109e4e7c95ee0955815890ef96e54e256fa9` with original PR head `5e789004b9e7a4a7154db1da0c93239c0b05f8f8`.
**Pull request:** [#46](https://github.com/GBrooks1970/portfolio/pull/46)
**Pages run:** Pending merge; subsequent immutable closure record will capture publication.

## Outcome and scope

The BFX showcase card links its published Interactive Kanban board. Existing PR #46 is refreshed against current main without rewriting branch history. The source manifest, generated HTML and three existing test baselines carry the change; recent Saleor content and all other public cards are preserved. LAND-17 planning and evidence are added to landing documentation. No BFX repository content changes.

## Decisions

The board supports filtering, search and ticket details, so the demo action type and explicit Interactive Kanban board label remain appropriate under the generation contract. Public evidence count rises from 16 to 17, external URLs from 64 to 65 and named controls from 68 to 69. The negative parity fixture now replaces 17 with 9 and still requires rejection.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| Full local gate | PASS | `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts`; 74 tests in 1.425 seconds, no skips, external checks enabled |
| Source/static checks | PASS | 15 showcase, 2 methodology, 69 named controls, 7 internal references, 65 external URLs, 20 contrast pairs |
| Board source | PASS | HTTP 200; 20,668 normalised bytes match `bfx-ws-screenplay_implementation-kanban_v1.html` at BFX main `b90dba4b71eea34bd18ecad9821721e3c168ad1c`; SHA-256 `1106209cb070756c0ce980c36e9a3bafc745c2c751239a06edb9d30469ab6f81` |
| Desktop | PASS | Requested 1280×800; inner width 1280, document width 1265; readable card and unobscured action |
| Mobile | PASS | Requested 390×844; rounded inner width 391, document width 376; new action 183.43×44.99px, right edge 292.70px; no horizontal overflow |
| Keyboard | PASS | Title → Repo → board action; visible gold focus outline approximately 2.80px; Enter navigates to the board |
| Board interactions | PASS | 21 tickets: 2 backlog and 19 done; MEDIUM filter shows 1/21; search RISK-1 shows 2/21; opening the pinned-trio ticket displays description/status/acceptance criteria and Close dismisses it; clearing filters restores 21/21 |
| Console | PASS | No captured warning/error entries during landing and board checks |
| Publication | Pending | Refreshed PR quality, exact merge CI/Pages and live checks follow this capture |

## Failures and recovery

Merging current main exposed conflicts in generated `index.html` and three test files. Resolve tests against main, apply the new one-action counts and regenerate HTML from merged source data. The full gate then passes, including the deliberate wrong-count test. The September PR's sibling-review failure did not recur in this full workspace run.

## Durable lessons and boundaries

Refresh old PR descriptions and numerical assertions from current evidence: the published board now has 21 tickets, not the original 17. Its own generation timestamp is 2026-09-15; linking it does not assert that it is a live backlog feed. The existing BFX CI badge displayed a failing status during inspection; this landing change neither alters nor claims to repair that independent workflow.

## Backlog reconciliation

LAND-17 remains IN REVIEW pending current PR CI, exact-merge publication and the closure record. Local/browser acceptance evidence is complete.
