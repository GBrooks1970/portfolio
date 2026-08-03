# Implementation Log — LAND-09B: hand-baked sample report (landing integration)

**Date:** 2026-08-03
**Backlog item:** `LAND-09B` (second slice of `LAND-09`)
**Repository:** `GBrooks1970/portfolio`
**Implementation branch:** `land-09b-hand-baked-report`
**Implementation pull request:** https://github.com/GBrooks1970/portfolio/pull/23
**Merge commit:** `d94787befac3d3bd63f3995eff88e6c05d39f2a5`
**Portfolio quality run:** https://github.com/GBrooks1970/portfolio/actions/runs/30863597028
**Pages deployment:** https://github.com/GBrooks1970/portfolio/actions/runs/30863596646
**Target repository:** `NeoCognitus70/hand-baked-screenplay-pattern` (HBSP-27)
**Target PRs:** #42 (planning, merged `be03329`), #43 (implementation, merged `ae33a66`)
**Target Pages run:** https://github.com/NeoCognitus70/hand-baked-screenplay-pattern/actions/runs/30863382627

## Outcome

LAND-09B is complete. The landing page now links the hand-baked Screenplay library's published
static-reporter sample. The landing change is presentation data plus regenerated output only — the
artefact, its generation, tests, workflow and Pages configuration are wholly owned by the target
repository.

The live portfolio page (`https://gbrooks1970.github.io/portfolio/`) returns HTTP 200 with
`data-public-evidence-count="6"`, the "Public demos and reports" statistic at 6, and the Hand-Baked
Screenplay Pattern card exposing a "Sample report" action linking the verified target URL. The
target page `https://neocognitus70.github.io/hand-baked-screenplay-pattern/` returns HTTP 200, is
self-contained, and shows an illustrative-sample provenance banner plus three scenes (two passing,
one failing) with a rendered assertion error.

## Scope

- `data/presentation.json` — set the hand-baked `report` action from `null` to
  `{ "label": "Sample report", "url": "https://neocognitus70.github.io/hand-baked-screenplay-pattern/" }`.
- Regenerate `index.html` (the hand-baked card gains the report action; generated public-evidence
  count 5 → 6). `sitemap.xml` and `robots.txt` regenerate byte-identical.
- Update the deterministic test count baselines for the added external link: public-evidence 5 → 6,
  external URLs 35 → 36, named controls 36 → 37; rebase the parity guard's injected mismatch 6 → 7.
- Verify the target Pages URL as an unauthenticated visitor before adding the landing link.
- `docs/backlog.md` — record LAND-09B completion evidence, mark it DONE, promote LAND-09C to READY,
  and **correct the LAND-09B/09C target-repository owners** from `GBrooks1970/...` to
  `NeoCognitus70/...` (both repositories are owned by `NeoCognitus70`).

Explicit non-goals: no change to the target artefact, registry membership or `presentation_role`;
no work on LAND-09C/09D beyond promoting 09C to READY.

## Decisions

- **"Sample report", not "Live report".** The label signals an illustrative sample (independent of
  Serenity/JS, not current CI), matching the target's provenance banner and OD-LAND-10.
- **Link only a verified, merged URL.** Added only after the target merges (`ae33a66`), the target
  Pages deploy succeeded and a live HTTP 200 check passed.
- **Fixed a latent target-owner error.** The LAND-09B (and LAND-09C) slices named
  `GBrooks1970/hand-baked-screenplay-pattern` / `GBrooks1970/calculator-screenplay-bdd`; the
  registry owns both under `NeoCognitus70`. Corrected so the recorded Pages base and repository URLs
  are right.

## Validation

- `python tools/generate_site.py --check` — byte-stable committed output.
- `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts` — full gate PASS
  (9 showcase / 1 methodology, 37 named controls, 5 internal references, 36 external URLs, 20
  contrast pairs, 43 tests).
- Exact-merge Portfolio quality run 30863597028 and Pages deployment 30863596646 both succeeded;
  live page verified as above.

## Known limitations

- The published target sample is a fixed illustrative artefact, deliberately not a live or current
  CI result; its determinism is guaranteed by the target's injected-clock design and gated by the
  target's own `spec/sample-report.spec.ts`.

## Lessons

- The one-presentation-addition / three-derived-counts pattern (public-evidence, external URLs,
  named controls) plus the rebased parity guard recurred exactly as in LAND-09A — a reliable,
  repeatable shape for each evidence slice.
- Cross-repository target owners in the landing backlog must be checked against `registry.yml`;
  two slices carried the wrong owner until this pass.
