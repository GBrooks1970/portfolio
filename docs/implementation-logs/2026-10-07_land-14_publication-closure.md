# Implementation Log — LAND-14: Publication closure

**Date:** 2026-10-07
**Backlog item:** `LAND-14`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `chore/land-14-closure`
**Commit:** Merge commit `9537d83e0ed962ea3dde2d103f75a541cbd571ed` on `main` (the closure commit is this log's own commit, on the branch above).
**Pull request:** [PR #63](https://github.com/GBrooks1970/portfolio/pull/63), merged by `GBrooks1970` at 2026-10-07T18:00:56Z.
**Pages run:** [pages build and deployment run 37663545393](https://github.com/GBrooks1970/portfolio/actions/runs/37663545393), success.

## Outcome

The versioned, dual-theme Learning Paths page is merged, deployed and live. The live `learning-paths.html` is identical to the merged file after line-ending
normalisation, shows the document's version, dates, evidence cut-off, source revision and a 'Public snapshot' row, and carries the house light/dark switch at the
top right. The same real-browser suite that passed locally passes against the live URL. This record closes LAND-14 and supplements, without rewriting, the earlier
[implementation log](2026-10-07_land-14_versioned-dual-theme-snapshot.md), which recorded the work while no pull request existed. It completes part C of the
owner-approved plan LC-V1.

## Scope

- Evidence only. No page, data or generator changed in this closure.
- `docs/backlog.md`: LAND-14 moved from IN PROGRESS to DONE, the three open acceptance criteria ticked with the evidence below, version 33.
- `docs/implementation-plans/2026-10-07_land-14-versioned-dual-theme-snapshot.md` and its `_index.md`: status set to implemented, `delivered` filled in and an Outcome
  appended; the approved body is unchanged.

## Decisions

- **Closure authority:** the owner merged the pull request and asked for part C on 2026-10-07, after the plan was approved under LC-V1.
- **Live browser run added.** LAND-12 and LAND-13 closed on status, hash and content checks. Because this change adds behaviour (a theme switch and two scripts), the closure also
  ran the real-browser suite against the live URL.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| `portfolio-quality` on the pull request head `6c234a9` | PASS | [Run 37663223836](https://github.com/GBrooks1970/portfolio/actions/runs/37663223836): 17:58:29Z to 17:58:45Z |
| `portfolio-quality` on `main` at the merge commit `9537d83` | PASS | [Run 37663545958](https://github.com/GBrooks1970/portfolio/actions/runs/37663545958): 18:00:58Z to 18:01:54Z |
| External-URL check in CI | PASS | No workflow file contains `--skip-external` (a search of `.github/workflows/*.yml` returned 0 matches), so external checking was enabled and the gate passed |
| Pages deployment of the exact merge commit | PASS | Run 37663545393 on `9537d83`: 18:00:58Z to 18:01:47Z, conclusion success |
| Live `learning-paths.html` status | PASS | HTTP 200, 41,622 bytes, fetched with a cache-busting query at about 18:02:50Z, after the Pages run completed |
| Live HTML against the merged source | PASS | After line-ending normalisation, SHA-256 `b715457bf14dfa3835d01812f585e6436af482f316866a648d7c3da0d11a4ca6` for the live page and `learning-paths.html` at `origin/main` |
| Live `index.html` against the merged source | PASS | SHA-256 `b9565d1829fe993be42ac4c713e99dcdedc9bed3edcf1830f4d2d096ca5863c7` for both (35,623 bytes), the same hash recorded after LAND-13, so the change did not alter it; it still carries `href="learning-paths.html"` |
| Live page content | PASS | Contains `<dt>Version</dt>`, `<dt>Public snapshot</dt>`, the document commit `6fe8133`, `LAND-14`, the switch (`id="theme-toggle"`, 'Toggle light/dark theme'), the dark palette (`data-theme="dark"`, `prefers-color-scheme: dark`) and the stage 4.4 wording 'Failed on 6 October 2026; passes after a fix'; 2 `<script>` blocks; 8 tables in 8 `table-scroll` wrappers |
| Real Chromium (Playwright 1.61.1) against `https://gbrooks1970.github.io/portfolio/learning-paths.html` | PASS, 13 of 13 | System light and dark colours by default; back link left and switch right on one row, 24 px from the column edge; the metadata block shows Version, Created, Last updated, Evidence cut-off, Source revision and Public snapshot (version 10); 8 tables, 8 wrappers, no private hrefs, 2 scripts; click flips and saves the choice; the choice persists across a reload while the system is dark; first Tab stop is the back link, second the switch with a 3 px focus ring; Enter and Space both toggle; with JavaScript off the page follows the system (dark) and the switch stays hidden; no horizontal overflow at 375 px in either theme |

Durations of the local gates were not captured; the live fetches and the browser run were made on 2026-10-07 after the Pages run completed (18:01:47Z).

## Failures and recovery

None in the closure. While setting up the live browser run, my first two edits of the scratch test script's URL line were rejected or broke on a backslash in a regular expression; the
line was rewritten without one and the suite then ran. No page was affected.

## Durable lessons

- A change that adds behaviour should be closed with a behaviour check against the live URL, not only a hash: the hash proves the bytes are the merged ones, and the browser run proves they work.
- The pinned page is stale whenever its source document changes. Refreshing it is now one documented procedure (`docs/learning-paths-refresh.md`) with a tested script; the remaining risk is
  remembering to do it, since nothing can detect staleness from CI.
- Record the hash of an unchanged file too (`index.html` here): it shows by comparison that a change touched only what it was meant to.

## Backlog reconciliation

- LAND-14: all seven acceptance criteria are ticked. Four were ticked in the earlier log; the pull request's CI run, the owner merge, and the Pages deployment with live-page match are ticked here with the evidence above.
- No follow-up items were created. The `portfolio-reviews` index gap (`credit-dashboard-sut` missing from the sibling `portfolio-reviews/README.md`, which makes one test fail locally) is reported to the owner separately.
