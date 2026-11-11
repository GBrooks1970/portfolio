# Implementation Log — LAND-18: Project data and review publication refresh

**Date:** 2026-11-11 (refreshed from 2026-11-07 baseline)  
**Backlog item:** LAND-18  
**Repository:** `GBrooks1970/portfolio`  
**Branch:** `codex/project-data-and-reviews-refresh`  
**Plan:** [`docs/implementation-plans/2026-11-06_project-data-and-review-refresh.md`](../implementation-plans/2026-11-06_project-data-and-review-refresh.md)  
**Pull request:** Pending creation  
**Pages run:** Pending owner merge  

## Outcome and scope

All public portfolio project cards and the central review index have been refreshed against canonical repository evidence:
1. **Registry lock refreshed:** `data/registry-lock.json` updated to canonical `portfolio-prompts` commit `863bf17642ba8dbeeb7f248bd8f099faa3a3fe62` (15 showcase, 2 methodology, 1 hidden).
2. **Central review export imported:** `data/reviews.json` imported from merged root commit `17d4dea2b2ee56024d834434a61201575dd374b6`, surfacing all 18 review bundles across 15 public projects (including 8 November bundles and 6 focused Credit Dashboard records).
3. **Per-project review actions generated:** Cards with published reviews carry a derived `Code reviews` action pointing directly to `reviews.html#review-<project-id>`. The 2 showcase projects without published bundles (`tradeblotter-wpf-screenplay`, `loan-origination-parity`) receive no invented action.
4. **Presentation metadata concise & accurate:** Replaced ambiguous `Live report` labels with `Published report` for Magento and OrangeHRM; clarified emulated-device boundary for Mobile Forex; condensed Credit Dashboard card summary to state specification-first architecture and formal closure on 23 October 2026.
5. **Quality gates & negative controls:** 77/77 tests passed locally with all 66 external URLs live-checked. Negative controls verified fail-closed behaviour on hidden project leakage, anchor corruption, and count tampering.

## Validation

| Gate | Result | Empirical evidence |
|---|---|---|
| Full local gate | PASS | `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts` passed 77 tests in 12.163s with external URLs enabled |
| Source & parity | PASS | 15 showcase, 2 methodology, 85 named controls, 22 internal references, 66 external URLs, 20 contrast pairs |
| Reviews check | PASS | `python tools/generate_reviews.py --check` passed |
| Site check | PASS | `python tools/generate_site.py --check` passed |
| Registry parity | PASS | `python tools/check_registry_parity.py --registry-repository ../portfolio-prompts` passed (15 showcase, 2 methodology match) |
| Negative controls | PASS | Hidden project injection, corrupted review anchor, and altered showcase count all rejected |

## Backlog reconciliation

LAND-18 is IN REVIEW on branch `codex/project-data-and-reviews-refresh` pending PR creation and owner merge.
