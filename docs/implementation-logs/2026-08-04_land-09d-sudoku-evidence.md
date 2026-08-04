# Implementation Log — LAND-09D: sudoku browser-only evidence (landing integration)

**Date:** 2026-08-04
**Backlog item:** `LAND-09D` (fourth and final slice of `LAND-09`)
**Repository:** `GBrooks1970/portfolio`
**Implementation branch:** `land-09d-sudoku-demo`
**Implementation pull request:** https://github.com/GBrooks1970/portfolio/pull/27
**Merge commit:** `19a87975f21141daf2fe46b74099322dba6c9c3d`
**Portfolio quality run:** https://github.com/GBrooks1970/portfolio/actions/runs/30927279911
**Pages deployment:** https://github.com/GBrooks1970/portfolio/actions/runs/30927332426
**Target repository:** `GBrooks1970/gb.automation.smoketests.sudoku.poc` (BACKLOG-071 / DR-040)
**Target PRs:** #52 (planning: BACKLOG-071 + DR-040, merged `619016f`), #53 (implementation, merged `4e504b3`)
**Target Pages run:** https://github.com/GBrooks1970/gb.automation.smoketests.sudoku.poc/actions/runs/30926946232

## Outcome

LAND-09D is complete, and with it the entire **LAND-09 public-evidence programme (09A–09D)**. The
landing page now links the sudoku DEMOAPP001 static, browser-only solver visualisation as a `demo`
action.

The live portfolio page (`https://gbrooks1970.github.io/portfolio/`) returns HTTP 200 with
`data-public-evidence-count="8"`, the "Public demos, reports and docs" statistic at 8, and the Sudoku
card exposing a "Solver visualisation" `demo` action linking the verified target URL. The target page
`https://gbrooks1970.github.io/gb.automation.smoketests.sudoku.poc/` returns HTTP 200 and was verified
live on its real Pages base path (banner, 5 puzzles, "✓ SOLVED", full step playback filling all 81
cells, no console errors).

## Scope

- `data/presentation.json` — set the sudoku `demo` action from `null` to
  `{ "label": "Solver visualisation", "url": "https://gbrooks1970.github.io/gb.automation.smoketests.sudoku.poc/" }`.
- Regenerate `index.html` (the Sudoku card gains the demo action; generated public-evidence count
  7 → 8). `sitemap.xml`/`robots.txt` regenerate byte-identical.
- Update the deterministic test count baselines for the added external link: public-evidence 7 → 8,
  external URLs 37 → 38, named controls 38 → 39; rebase the parity guard's injected mismatch 8 → 9.
- Verify the target Pages URL as an unauthenticated visitor before adding the landing link.
- `docs/backlog.md`: LAND-09D completion evidence, DONE, and mark the LAND-09 programme complete.

## Decisions

- **`demo`, not `report`/`documentation`.** The sudoku artefact is a genuinely interactive browser
  viewer (select a puzzle, step/play through the solve), so it is a `demo` and correctly receives the
  play-style cue — unlike LAND-09A/09B (`report`) and 09C (`documentation`).
- **Truthful, bounded framing.** The target page and DR-040 keep the evidence surface explicitly
  separate from the advanced-technique, tutor and generator ideas (BACKLOG-014/015/016), and from any
  three-stack parity claim. The link label ("Solver visualisation") reflects exactly what it shows.
- **Link only a verified, merged URL.** Added only after the target merged (`4e504b3`), its Pages
  deploy succeeded, and the live viewer was verified on the real base path.

## Validation

- `python tools/generate_site.py --check` — byte-stable committed output.
- `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts` — full gate PASS
  (9 showcase / 1 methodology, 39 named controls, 5 internal references, 38 external URLs, 20 contrast
  pairs, 44 tests).
- Exact-merge Portfolio quality run 30927279911 and Pages deployment 30927332426 both succeeded; live
  page verified as above.

## Lessons

- The one-presentation-addition / three-derived-counts + parity-guard pattern held for the fourth
  time — a reliable shape for each evidence slice.
- The target side was the hardest of the four: the live viewer was API-coupled, so it needed a
  mandated viability gate plus an offline precompute path reusing the maintained solve/visualise logic.
  Isolating that as a target-owned BACKLOG-071/DR-040 (not landing work) kept the landing change a
  simple, verified one-line link — the LAND-09 delivery contract working as intended.
