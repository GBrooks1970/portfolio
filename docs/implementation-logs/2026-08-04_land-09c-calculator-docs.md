# Implementation Log — LAND-09C: calculator API reference (landing integration)

**Date:** 2026-08-04
**Backlog item:** `LAND-09C` (third slice of `LAND-09`)
**Repository:** `GBrooks1970/portfolio`
**Implementation branch:** `land-09c-calculator-docs`
**Implementation pull request:** https://github.com/GBrooks1970/portfolio/pull/25
**Merge commit:** `a4f991ccd8146b19a77a4cd05712fc73bb6ec797`
**Portfolio quality run:** https://github.com/GBrooks1970/portfolio/actions/runs/30885016294
**Pages deployment:** https://github.com/GBrooks1970/portfolio/actions/runs/30885015716
**Target repository:** `NeoCognitus70/calculator-screenplay-bdd` (CAL-21)
**Target PRs:** #30 (planning, merged `faee931`), #31 (implementation, merged `cd74df0`)
**Target Pages run:** https://github.com/NeoCognitus70/calculator-screenplay-bdd/actions/runs/30884443647

## Outcome

LAND-09C is complete. The landing page now links the calculator's published static API reference
through a **new typed `documentation` action**, and — as required by the LAND-09 rule that only a
genuinely interactive demo receives a play cue — the generator now distinguishes the three action
types so that reports and documentation are no longer styled as demos.

The live portfolio page (`https://gbrooks1970.github.io/portfolio/`) returns HTTP 200 with
`data-public-evidence-count="7"`, the "Public demos, reports and docs" statistic at 7, and the
Calculator card exposing an "API reference" `documentation` action linking the verified target URL.
The target page `https://neocognitus70.github.io/calculator-screenplay-bdd/` and its `openapi.json`
both return HTTP 200.

## Scope

- **New `documentation` action type** in `tools/generate_site.py` and `tools/check_registry_parity.py`:
  `ACTION_FIELDS`, per-entry validation, and the public-evidence count all include it; every entry in
  `data/presentation.json` carries the key.
- **Demo-only play cue.** `_action_link` is now type-aware: `demo` → `btn demo` (the `.btn.demo::before`
  play triangle), `report` → `btn report` (no cue), `documentation` → `btn documentation` (a small
  document glyph). This retroactively corrected the magento/orangehrm/parabank/hand-baked **report**
  buttons, which had rendered with the demo class and play cue.
- Calculator card gains an **"API reference"** documentation action → the verified target URL.
- Stat label → "Public demos, reports and docs"; count 5 → 7 across LAND-09B/09C (this slice 6 → 7).
- Regenerate `index.html`; `sitemap.xml`/`robots.txt` regenerate byte-identical.
- Tests: new `test_action_types_are_rendered_with_distinct_classes`; baselines public-evidence 6 → 7,
  external URLs 36 → 37, named controls 37 → 38; parity guard rebased 7 → 8. `docs/generation.md`
  documents the three action types and the demo-only cue policy.
- `docs/backlog.md`: LAND-09C completion evidence, DONE, promote LAND-09D to READY (final slice).

Explicit non-goals: no change to the target artefact, registry membership or `presentation_role`; no
work on LAND-09D beyond promoting it to READY.

## Decisions

- **A new typed action, not a re-used `report`/`demo`.** Per the LAND-09 common criterion, API
  documentation is neither a report nor an interactive demo, so it gets its own `documentation` type
  with truthful styling and an accessible "API reference" label.
- **Fix the play cue rather than paper over it.** The generator gave every non-primary link the `demo`
  class (and its ▶). Adding `documentation` was the moment to make the cue demo-only, which the spec
  requires ("only a genuinely interactive demo receives a play-style cue").
- **Custom dependency-free target renderer.** The target repository renders the OpenAPI contract with
  an in-repo renderer (no Redoc/Swagger CDN), keeping the visitor experience self-contained and the
  drift check simple.

## Validation

- `python tools/generate_site.py --check` — byte-stable committed output.
- `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts` — full gate PASS
  (9 showcase / 1 methodology, 38 named controls, 5 internal references, 37 external URLs, 20 contrast
  pairs, 44 tests).
- Browser-verified computed pseudo-element cues on the served page: demo → "▶", documentation → "📄",
  report → none; zero reports styled as demos; no console errors.
- Exact-merge Portfolio quality run 30885016294 and Pages deployment 30885015716 both succeeded; live
  page verified as above.

## Lessons

- The one-presentation-addition / three-derived-counts pattern held again (public-evidence, external
  URLs, named controls) plus the rebased parity guard — but this slice additionally required a
  generator/schema/CSS refactor because the action *type* was new, and every entry's `actions` object
  had to gain the key for the strict schema check.
- Computed `::before` cues are invisible to HTML-source and text checks; verifying the play-cue policy
  needed a `getComputedStyle(el, '::before')` read in the browser.
