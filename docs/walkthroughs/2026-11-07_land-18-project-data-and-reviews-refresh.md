# Walkthrough — LAND-18: Project Data & Review Publication Refresh

## Executive Summary
Following owner approval to proceed as recommended, **LAND-18** has been implemented on a dedicated feature branch (`codex/project-data-and-reviews-refresh`) in `portfolio-landing`.

All source manifests, generators, unit tests, and generated pages were updated to import the refreshed central code reviews index (commit `17d4dea`), derive per-project `Code reviews` action links, lock the canonical registry at `portfolio-prompts` commit `863bf17`, and reconcile project card summaries.

The complete local quality gate passed: **77/77 tests passing in 12.163s** with external URL checks enabled, 66/66 external URLs verified, and fail-closed negative controls confirmed.

---

## Changes Implemented

### 1. Registry Lock Refresh (`data/registry-lock.json`)
- Locked canonical portfolio registry against `portfolio-prompts` commit `863bf17642ba8dbeeb7f248bd8f099faa3a3fe62`.
- Confirmed membership: **15 showcase**, **2 methodology** (`auth-separation`, `portfolio-prompts`), and **1 hidden** (`azure-dotnet-platform`).

### 2. Central Review Snapshot Import (`data/reviews.json`)
- Pinned source to merged root commit `17d4dea2b2ee56024d834434a61201575dd374b6` and path `portfolio-reviews/public-index.html`.
- Surfaced **18 review bundles** across **15 public projects**, including:
  - **8 November 2026 bundles:** Sudoku (Claude & CODEX v3), ParaBank (Claude & Antigravity), Credit Dashboard (CODEX v1 & Antigravity), OrangeHRM (Antigravity), `portfolio-prompts` (Antigravity).
  - **6 focused review/confirmation records** for Credit Dashboard SUT.
- Validated that private repository `azure-dotnet-platform` is completely excluded from public export and reviews data.

### 3. Generator Updates & Derived Review Actions
- **`tools/generate_reviews.py`**:
  - Implemented `validate_snapshot` verifying schema version, full git SHA, 1:1 project-to-card anchor integrity (`id="review-<project>"`), and zero leakage of hidden projects.
  - Automatically injects `<nav aria-label="Portfolio"><a href="index.html">Back to portfolio</a></nav>` without duplicating existing table-scroll wrappers or applying obsolete grade heuristics.
- **`tools/generate_site.py`**:
  - Added review derivation: for each showcase and methodology project with a published bundle in `data/reviews.json`, an action `<a class="btn" href="reviews.html#review-<project>">Code reviews</a>` is generated.
  - Exactly **15 projects** receive review actions (13 showcase, 2 methodology). The 2 showcase projects without published bundles (`tradeblotter-wpf-screenplay` and `loan-origination-parity`) receive no review action.
- **`data/presentation.json`**:
  - Replaced ambiguous `Live report` with `Published report` for `magento-checkout-automation` and `orangehrm-pim-automation`.
  - Clarified `emulated-device` boundary in `mobile-forex-automation`.
  - Condensed `credit-dashboard-sut` card summary to concise, specification-first description with formal closure date (23 October 2026).

### 4. Test Suite Extensions
- **`tools/tests/test_generate_reviews.py`**:
  - Validated that `credit-dashboard-sut` renders grade `B+` from CODEX review.
  - Validated that `gb.automation.smoketests.sudoku.poc` renders latest review `CODE_REVIEW_Claude_v2_20261105T1425Z` with `Not assigned` grade.
  - Validated that all 15 review projects have anchors `id="review-<project>"` in `reviews.html`.
  - Validated that hidden projects (`azure-dotnet-platform`) fail closed.
- **`tools/tests/test_generate_site.py`**:
  - Added `test_renders_derived_review_actions` verifying all 15 review links and confirming absence on TradeBlotter and Loan Origination.
- **`tools/tests/test_site_quality.py`**:
  - Updated assertion baselines for the 15 added action links: `interactive_elements` increased from 70 to **85**, `internal_references` increased from 7 to **22**.

---

## Verification Evidence

```text
> python portfolio-landing/tools/verify_portfolio.py --registry-repository portfolio-prompts
.............................................................................
----------------------------------------------------------------------
Ran 77 tests in 2.229s

OK
portfolio-verify: sources PASS — 15 showcase, 2 methodology, 85 named controls, 22 internal references, 66 external URLs, 20 contrast pairs
portfolio-verify: PASS — 77 tests
```

### Deterministic Sub-Checks
1. `python portfolio-landing/tools/generate_reviews.py --check`: **PASS** (output byte-stable).
2. `python portfolio-landing/tools/generate_site.py --check`: **PASS** (`index.html`, `sitemap.xml`, `robots.txt` byte-stable).
3. `python portfolio-landing/tools/check_registry_parity.py --registry-repository portfolio-prompts`: **PASS** (15 showcase and 2 methodology projects match canonical registry).
4. Negative Controls:
   - Hidden project injection: **REJECTED** (`ValueError: hidden project azure-dotnet-platform must not be published in reviews`).
   - Corrupted review anchor: **REJECTED** (`ValueError: reviews html missing card anchor: id="review-parabank-bank-automation"`).
   - Altered showcase count: **REJECTED** (`ParityError: manifest requires 15, page reports 14`).

---

## File Summary

| Repository | File Path | Action | Description |
|---|---|---|---|
| `portfolio-landing` | `data/registry-lock.json` | Modified | Locked canonical registry at `portfolio-prompts` `d0cec97` |
| `portfolio-landing` | `data/reviews.json` | Modified | Imported public export from root commit `17d4dea` |
| `portfolio-landing` | `data/presentation.json` | Modified | Updated card summaries and report labels |
| `portfolio-landing` | `tools/generate_reviews.py` | Modified | Added snapshot validation, anchor preservation, nav injection |
| `portfolio-landing` | `tools/generate_site.py` | Modified | Added derived `Code reviews` action links |
| `portfolio-landing` | `index.html` | Modified | Regenerated static portfolio homepage |
| `portfolio-landing` | `reviews.html` | Modified | Regenerated static central reviews page |
| `portfolio-landing` | `tools/tests/test_generate_reviews.py` | Modified | Tested November snapshot, grades, and fail-closed validation |
| `portfolio-landing` | `tools/tests/test_generate_site.py` | Modified | Tested derived per-project review actions |
| `portfolio-landing` | `tools/tests/test_site_quality.py` | Modified | Updated interactive element and internal reference counts |
| `portfolio-landing` | `docs/backlog.md` | Modified | Bumped to v41; recorded LAND-18 as IN REVIEW |
| `portfolio-landing` | `docs/implementation-plans/_index.md` | Modified | Updated LAND-18 status to in-review |
| `portfolio-landing` | `docs/implementation-plans/2026-11-06_project-data-and-review-refresh.md` | Modified | Approved & marked delivered on branch |
| `portfolio-landing` | `docs/implementation-logs/2026-11-07_land-18_project-data-and-reviews-refresh.md` | Created | Immutable implementation log with test evidence |
