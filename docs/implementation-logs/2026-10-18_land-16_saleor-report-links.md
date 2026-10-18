# Implementation Log — LAND-16: Saleor capabilities and report links

**Date:** 2026-10-18
**Backlog item:** `LAND-16`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `codex/land-16-saleor-reports`
**Commit:** Implementation follows plan commit `ac6e920`; exact publication commit belongs to the subsequent closure record.
**Pull request:** Pending creation at this pre-publication capture.
**Pages run:** Pending merge and deployment.

## Outcome

The Saleor card describes delivered catalogue, authentication, checkout and staff fulfilment journeys, published Serenity reports and daily upstream schema checks. It keeps dependency maintenance visible and distinguishes deterministic reports from separate live-SUT acceptance. New report and CI actions link to the owning project's public evidence.

## Scope

- Saleor entry in `data/presentation.json`, regenerated `index.html`, and three existing test baselines.
- The report uses a static report action; it is not a live application demo.
- Membership, registry lock, page layout, historical review and Learning Paths snapshots are unchanged. The unrelated bfx PR #46 is not part of this batch.

## Decisions

Public evidence count increases from 15 to 16; showcase count remains 15. Adding a report action and CI badge/action increases named controls from 66 to 68 and external URLs from 61 to 64. Existing expectations were deliberately updated. The wrong-count parity test now replaces 16 with 9 and still requires rejection, so the negative fixture cannot silently become a no-op.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| Complete portfolio gate | PASS | `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts`; 74 tests, 1.575 seconds for the test suite, no skips; external checks enabled |
| Source/static checks | PASS | 15 showcase, 2 methodology, 68 named controls, 7 internal references, 64 external URLs, 20 contrast pairs |
| Desktop browser | PASS | Requested 1280×800; inner width 1280, document scroll width 1265; readable card and visible actions |
| Mobile browser | PASS | Requested 390×844; browser rounding reported inner width 391, document scroll width 376; all four action heights approximately 44.99px, rightmost edge approximately 320.17px |
| Keyboard | PASS | Tab moved from title to Repo to Serenity reports; visible focus outline approximately 2.80px; Enter navigated to the real report page |
| Destinations | PASS | Report shows mock-SUT boundary, API 9 and smoke 3, revision `abd506e38c0c3f1f7c56d0e17155545d1959069a`; CI action reaches the project's `ci.yml` workflow page |
| Console | PASS | No warning/error entries during local layout inspection |
| Publication | Pending | Exact merged quality, Pages and live checks belong to the closure log |

## Failures and recovery

None in the implementation gate. Initial repository inspection found no root package.json; this repository uses the documented Python gate. Mobile browser viewport rounding is recorded above rather than reported as an exact 390px inner width.

## Durable lessons

Adding public actions affects evidence, control and external-link counts; update their independent oracles and keep the injected parity mismatch non-vacuous. Target reports are evidence for their stated execution environment, not proof of live Docker readiness.

## Backlog reconciliation

LAND-16 is IN REVIEW until exact-merge deployment and live publication have been verified. Historical snapshots retain their dated provenance.
