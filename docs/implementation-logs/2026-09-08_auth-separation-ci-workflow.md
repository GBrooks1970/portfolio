# Implementation Log — Link auth-separation-screenplay-poc CI Workflow

**Date:** 2026-09-08  
**Repository:** `GBrooks1970/portfolio` (`portfolio-landing`)  
**Project Updated:** `auth-separation-screenplay-poc`  

## Outcome

`auth-separation-screenplay-poc` delivered its Phase 3 continuous integration workflow (`.github/workflows/ci.yml`) on `main` (`34facb3`, PR #7), executing the unified 6-stage verification gate across Node 20 and Node 22 matrix jobs. `portfolio-landing` has now been updated to link this workflow and display its active status badge on the public showcase card.

With this update, **all 11 showcase projects** in the portfolio now feature automated GitHub Actions CI workflow badges.

## Scope of Changes

1. **`data/presentation.json`**:
   - Updated `auth-separation-screenplay-poc` action:
     - Changed `"workflow": null` to `"workflow": "ci.yml"`.

2. **Generated Site Outputs (`index.html`, `sitemap.xml`, `robots.txt`)**:
   - Regenerated via `python tools/generate_site.py`.
   - Card for `auth-separation-screenplay-poc` now includes workflow link and live status badge:
     `https://github.com/GBrooks1970/auth-separation-screenplay-poc/actions/workflows/ci.yml`.

3. **Landing Test Baselines**:
   - `tools/tests/test_generate_site.py`: Updated CI workflow and CI status count assertions from 10 to 11.
   - `tools/tests/test_site_quality.py`: Updated `external_urls` (45 → 47) and `interactive_elements` (48 → 49) to account for the new badge link and SVG source.

## Validation Evidence

- `python tools/generate_site.py --check` — PASS (committed HTML, sitemap and robots output is current).
- `python tools/check_registry_parity.py --registry-repository ../portfolio-prompts` — PASS (11 showcase and 2 methodology projects match canonical registry).
- `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts` — PASS (11 showcase, 2 methodology, 49 named controls, 6 internal references, 47 external URLs, 20 contrast pairs, 48/48 tests green).
- `python -B -m unittest discover -s tools/tests -p "test_*.py"` — PASS (48/48 tests green).
