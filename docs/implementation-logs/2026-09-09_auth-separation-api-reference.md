# Implementation Log — Link auth-separation-screenplay-poc Static API Reference

**Date:** 2026-09-09  
**Repository:** `GBrooks1970/portfolio` (`portfolio-landing`)  
**Project Updated:** `auth-separation-screenplay-poc`  
**Target Repository:** `GBrooks1970/auth-separation-screenplay-poc` (PR #11, merged `50efcd6`)  
**Target Pages URL:** https://gbrooks1970.github.io/auth-separation-screenplay-poc/ (HTTP 200 OK)  
**Target Pages Run:** https://github.com/GBrooks1970/auth-separation-screenplay-poc/actions/runs/34292365565  

## Outcome

`auth-separation-screenplay-poc` authored and deployed a self-contained, multi-spec static API reference site documenting all 4 microservice and event contracts (AuthN, AuthZ, User Profile, Domain & Audit Events) via GitHub Actions (`.github/workflows/pages.yml`) to GitHub Pages.

`portfolio-landing` has now integrated this URL on the `auth-separation-screenplay-poc` card under the typed `documentation` action. The card renders an **API reference** button with `btn documentation` styling and document glyph, matching the established pattern from `calculator-screenplay-bdd`.

With this addition, the portfolio public evidence metric increments from **9 to 10** public demos, reports, and documentation sites.

## Scope of Changes

1. **`data/presentation.json`**:
   - Added `documentation` action for `auth-separation-screenplay-poc`:
     ```json
     "documentation": {
       "label": "API reference",
       "url": "https://gbrooks1970.github.io/auth-separation-screenplay-poc/"
     }
     ```

2. **Generated Site Outputs (`index.html`)**:
   - Regenerated via `python tools/generate_site.py`.
   - Card for `auth-separation-screenplay-poc` renders `<a class="btn documentation" href="https://gbrooks1970.github.io/auth-separation-screenplay-poc/">API reference</a>`.
   - Public evidence count statistic updated from 9 to 10 (`data-public-evidence-count="10"`).

3. **Landing Test Baselines**:
   - `tools/tests/test_generate_site.py`: Updated public evidence count assertions from 9 to 10 and added assertion for the rendered `auth-separation-screenplay-poc` documentation button.
   - `tools/tests/test_site_quality.py`: Updated `external_urls` (47 → 48) and `interactive_elements` (49 → 50).
   - `tools/tests/test_registry_parity.py`: Updated evidence count parity assertion baseline (9 → 10).

## Validation Evidence

- `curl -I https://gbrooks1970.github.io/auth-separation-screenplay-poc/` — HTTP 200 OK (Content-Length: 74,538 bytes).
- `python tools/generate_site.py --check` — PASS (committed HTML, sitemap and robots output is current).
- `python -B -m unittest discover -s tools/tests -p "test_*.py"` — PASS (48/48 tests green).
- `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts` — PASS (11 showcase, 2 methodology, 50 named controls, 6 internal references, 48 external URLs, 20 contrast pairs, 48/48 tests green).
