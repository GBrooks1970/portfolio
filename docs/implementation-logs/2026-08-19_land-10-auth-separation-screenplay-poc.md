# Implementation Log — Onboard auth-separation-screenplay-poc showcase project

**Date:** 2026-08-19  
**Repository:** `GBrooks1970/portfolio` (`portfolio-landing`)  
**Project Onboarded:** `auth-separation-screenplay-poc` (Thirteenth Portfolio Project)  

## Outcome

`auth-separation-screenplay-poc` is now onboarded into the public portfolio landing page as the 11th showcase project, located in the **Multi-stack and framework design** capability group.

The generated portfolio page (`index.html`) now renders 11 showcase cards across 5 capability groups plus 2 methodology entries (`portfolio-prompts`, `auth-separation`), with all parity, quality, and unit test suites passing.

## Scope of Changes

1. **`data/registry-lock.json`**:
   - Refreshed from canonical `portfolio-prompts/registry.yml` at commit `d0a330e529ddc08810312c650bf63677cf64f0f2`.
   - Added `auth-separation-screenplay-poc` row with `presentation_role: "showcase"`.

2. **`data/presentation.json`**:
   - Added `auth-separation-screenplay-poc` configuration:
     - Title: `Auth Separation Screenplay POC`
     - Discipline: `Multi-stack SDD + Screenplay BDD`
     - Summary: `Demonstrates specification-driven development and Screenplay BDD proving microservice interchangeability across Node.js, Python FastAPI, and C# .NET 9 with living OpenAPI and AsyncAPI contracts.`
     - Group: `multi-stack-frameworks` (order `110`)
     - Tags: `Screenplay`, `OpenAPI 3.1`, `AsyncAPI 3.0`, `Polyglot`
     - Actions: `workflow: null, demo: null, report: null, documentation: null`

3. **Generated Site Outputs (`index.html`, `sitemap.xml`, `robots.txt`)**:
   - Regenerated via `python tools/generate_site.py`.
   - Showcase count updated to 11 (`data-showcase-count="11"`).

4. **Landing Test Baselines**:
   - `tools/tests/test_generate_site.py`: Updated showcase count assertions (10 → 11).
   - `tools/tests/test_registry_parity.py`: Updated parity test assertions for 11 showcase projects.
   - `tools/tests/test_site_quality.py`: Updated `external_urls` (44 → 45) and `interactive_elements` (46 → 48).

## Validation Evidence

- `python tools/generate_site.py --check` — PASS (committed HTML, sitemap and robots output is current).
- `python tools/check_registry_parity.py --registry-repository ../portfolio-prompts` — PASS (11 showcase and 2 methodology projects match canonical registry).
- `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts --skip-external` — PASS (11 showcase, 2 methodology, 48 named controls, 6 internal references, 45 external URLs, 20 contrast pairs, 48/48 tests green).
- `python -B -m unittest discover -s tools/tests -p "test_*.py"` — PASS (48/48 tests green).
