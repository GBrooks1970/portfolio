# Implementation Log — LAND-01: Portfolio Accuracy

**Date:** 2026-08-01
**Backlog item:** `LAND-01`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `codex/land-01-portfolio-accuracy`
**Commit:** Pending initial commit
**Pull request:** Pending publication workflow
**Pages run:** Pending owner merge

## Outcome

The landing source now presents all nine showcase projects, adds ParaBank with repository and CI
evidence but no unsupported demo claim, updates Sudoku to its 48-scenario contract, and exposes the
`portfolio-prompts` support repository as methodology rather than a showcase. The GitHub repository
homepage now points to the published portfolio URL.

The change is not yet publicly complete: owner merge, the exact Pages deployment, and live-page
verification remain required before LAND-01 can be marked DONE.

## Scope

- `index.html` — public card inventory, numeric claims, ParaBank evidence, Sudoku baseline, metadata,
  and methodology section.
- `README.md` — nine-showcase description and separate methodology link.
- GitHub repository metadata — homepage set to `https://gbrooks1970.github.io/portfolio/`.
- `docs/backlog.md` — LAND-01 acceptance evidence and IN REVIEW state.
- Explicit non-goals: generator/data ownership (LAND-02/03), registry parity (LAND-04), automated
  publication gates (LAND-05), and the broader accessibility contract (LAND-06).

## Decisions

- Insert ParaBank after OrangeHRM so related Docker-backed web-UI suites remain adjacent without
  redefining the existing overall order.
- Link only ParaBank's repository and default-branch CI. GitHub Pages cannot host its Docker-backed
  SUT, and no static report publication has been approved.
- Present `portfolio-prompts` in a dedicated methodology section outside the showcase grid so it is
  discoverable but does not become a tenth showcase.
- Keep the hand-authored hotfix deliberately small; the structured manifest and generator remain
  gated by LAND-02.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| Source assertions | PASS | 9 cards; no stale eight-project/46-scenario claim; ParaBank repo/CI only; methodology outside grid |
| Desktop browser | PASS | 1280 × 720; 3 equal columns; 9 visible cards; no horizontal overflow |
| Mobile browser | PASS | 390 × 844; 1 column; ParaBank card readable; actions inside viewport; no horizontal overflow |
| Browser console | PASS | No warnings or errors at either audited viewport |
| Changed destinations | PASS | ParaBank repository, `main` `ci.yml`, and `portfolio-prompts` repository confirmed through GitHub |
| Repository homepage | PASS | GitHub reports `https://gbrooks1970.github.io/portfolio/` |
| Markdown links | PASS | Every repository-relative Markdown link resolves |
| `git diff --check` | PASS | No whitespace errors before staging |
| GitHub Pages/live page | PENDING | Must be observed after owner merge |

Evidence baselines: registry `dd8d786`; ParaBank `76824a4`; Sudoku `05a9484`; landing base
`09398bd`.

## Failures and recovery

The in-app browser's mobile full-page screenshot stitched the long static page incorrectly and was
not used as an oracle. A normal 390 × 844 viewport screenshot rendered correctly, while direct DOM
bounds independently proved one-column layout and zero horizontal overflow. This matches the audit's
recorded limitation.

## Durable lessons

- Treat a long mobile full-page screenshot as supporting evidence only; use viewport captures and
  document/card bounds for responsive assertions.
- A public project card must distinguish evidence links from deployable demos. Repository and CI are
  truthful ParaBank actions today; a static report remains a separately governed candidate.
- Do not infer public membership from card count. LAND-04 must eventually compare stable registry
  identifiers with the landing manifest.

## Backlog reconciliation

- LAND-01 has seven locally verifiable acceptance criteria complete.
- The Pages-deployment/live-source criterion remains open until the owner merges the implementation
  PR and the exact deployment is observed.
- LAND-02 through LAND-06 and LAND-C01 through LAND-C04 remain unchanged and unscheduled according
  to their recorded status.
