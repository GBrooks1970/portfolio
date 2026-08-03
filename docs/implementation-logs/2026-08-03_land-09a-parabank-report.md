# Implementation Log — LAND-09A: ParaBank static Serenity report (landing integration)

**Date:** 2026-08-03
**Backlog item:** `LAND-09A` (first slice of `LAND-09`)
**Repository:** `GBrooks1970/portfolio`
**Implementation branch:** `land-09a-parabank-report`
**Implementation pull request:** https://github.com/GBrooks1970/portfolio/pull/21
**Merge commit:** `9b4be696b108ea4394778db2f8f8a915884a0086`
**Portfolio quality run:** https://github.com/GBrooks1970/portfolio/actions/runs/30840610612
**Pages deployment:** https://github.com/GBrooks1970/portfolio/actions/runs/30840601153
**Target (ParaBank) implementation PR:** https://github.com/GBrooks1970/parabank-bank-automation/pull/27 (merged `d9aba95`)

## Outcome

LAND-09A is complete. The landing page now links ParaBank's content-verified static Serenity
report, published from the target repository under PB-EVID-01. The landing change is presentation
data plus regenerated output only — no build coupling to the target repository.

The live portfolio page (`https://gbrooks1970.github.io/portfolio/`) returns HTTP 200 with
`data-public-evidence-count="5"`, the "Public demos and reports" statistic at 5, and the ParaBank
card exposing a "Serenity report" action linking the verified target URL; the render console is
clean. The target report `https://gbrooks1970.github.io/parabank-bank-automation/`, its
`serenity/index.html` entry page and `evidence.json` all return HTTP 200, and `evidence.json`
records the merged source commit.

## Scope

- `data/presentation.json` — set ParaBank's `report` action from `null` to
  `{ "label": "Serenity report", "url": "https://gbrooks1970.github.io/parabank-bank-automation/" }`.
- Regenerate `index.html` (ParaBank card gains the report action; generated public-evidence count
  4 → 5). `sitemap.xml` and `robots.txt` regenerate byte-identical.
- Update the deterministic test count baselines for the added external link: public-evidence 4 → 5,
  external URLs 34 → 35, named controls 35 → 36; rebase the parity guard's injected mismatch 5 → 6
  so it still exercises genuine drift rather than passing vacuously.
- Verify the target Pages URL as an unauthenticated visitor before adding the landing link.
- `docs/backlog.md` — record LAND-09A completion evidence, mark it DONE and promote LAND-09B to READY.

Explicit non-goals: no change to the target report content, the pinned SUT, registry membership or
`presentation_role`; no work on LAND-09B–09D beyond promoting 09B to READY.

## Decisions

- **Report semantics, snapshot wording.** The action uses the typed `report` action (not `demo`),
  and the "Serenity report" label deliberately avoids implying live CI health or a hosted service —
  consistent with OD-LAND-04, OD-LAND-10 and PB-EVID-01's snapshot contract.
- **Link only a verified, merged URL.** Per the cross-repository delivery contract step 3, the
  landing link was added only after the target merge (`d9aba95`), its post-merge `main` CI/Pages
  success and a live HTTP 200 check — never a proposed or branch-only URL.
- **Counts are generated, tests assert them.** The public-evidence statistic is derived by the
  generator; the test baselines were updated to match rather than being hand-set in the template.

## Validation

- `python tools/generate_site.py --check` — byte-stable committed output.
- `python -B -m unittest discover -s tools/tests -p "test_*.py"` — 43 tests OK.
- `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts` — full gate PASS
  (9 showcase / 1 methodology, 36 named controls, 5 internal references, 35 external URLs, 20
  contrast pairs, 43 tests).
- Exact-merge Portfolio quality run 30840610612 and Pages deployment 30840601153 both succeeded;
  live page verified as above.

## Known limitations

- The published target `evidence.json` `sourceRef` advances to whichever commit produced the latest
  successful ParaBank `main` deployment; it is the newest published snapshot, not a fixed pin. The
  report content (the eight UI scenarios) is gated by `check:pages` at publish time.
- No fresh 390px render of the ParaBank Serenity report body was taken this session; the landing
  page's own responsive/accessibility contracts are covered by the quality gate.

## Lessons

- A single presentation-data addition still moves three derived counts (public-evidence, external
  URLs, named controls); update every asserting baseline in one change or the gate fails piecemeal.
- Guard tests that inject a deliberate mismatch must be rebased when the real baseline moves, or they
  silently stop testing anything.
