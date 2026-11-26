# Implementation Log — LAND-19: Publication closure

**Date:** 2026-11-26
**Backlog item:** `LAND-19`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `chore/land-19-publication-closure`
**Commit:** Merge commit `af06a5327a14aee4a5bc8bcc0647cf4657f9a863` on `main` (the closure commit is this log's own commit, on the branch above).
**Pull request:** [PR #85](https://github.com/GBrooks1970/portfolio/pull/85) (commits `dc22c97`, `e4ad365`, `cdca301`), merged by `GBrooks1970` at 2026-11-26T21:00:04Z.
**Pages run:** [pages build and deployment run 45895018563](https://github.com/GBrooks1970/portfolio/actions/runs/45895018563), success.

## Outcome

The Learning Paths snapshot at document version 12 is merged, deployed and live. The live `learning-paths.html` is identical to the merged file after line-ending normalisation
and shows Version 12, the source commit `7fa013c` and LAND-19. `index.html`, `sitemap.xml` and `robots.txt` are unchanged. This record closes LAND-19 and supplements,
without rewriting, the earlier [implementation log](2026-11-25_land-19_learning-paths-refresh.md), which recorded the work while no pull request existed.

## Scope

- Evidence only. No page, data or generator changed in this closure.
- `docs/backlog.md`: LAND-19 moved from IN PROGRESS to DONE, the two open acceptance criteria ticked with the evidence below, version 44.
- `docs/implementation-plans/2026-11-24_land-19-refresh-learning-paths-v12.md` and its `_index.md`: status set to implemented, `delivered` filled in and an Outcome appended; the approved body is unchanged.

## Decisions

- **Closure authority:** the owner approved the plan on 2026-11-24, merged the pull request, asked for this closure ('Yes, after merge'), and the plan's step 8 provides for it.
- **Live browser run kept.** As for LAND-15, the 16 local browser checks were repeated against the live URL; it costs one command.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| `portfolio-quality` on the pull request head `cdca301` | PASS | [Run 45666023197](https://github.com/GBrooks1970/portfolio/actions/runs/45666023197): 2026-11-25T17:33:31Z to 17:33:58Z, success |
| `portfolio-quality` on `main` at the merge commit `af06a53` | PASS | [Run 45895020051](https://github.com/GBrooks1970/portfolio/actions/runs/45895020051): 2026-11-26T21:00:07Z to 21:00:33Z, success |
| External-URL check in CI | PASS | The workflow runs `tools/verify_portfolio.py` without `--skip-external`, so external checking was enabled. The job log was not read. |
| Pages deployment of the exact merge commit | PASS | Run 45895018563 on `af06a53`: 21:00:06Z to 21:00:50Z, success |
| Live `learning-paths.html` status | PASS | HTTP 200, 48,118 bytes, fetched after the Pages run succeeded (with a cache-busting query) |
| Live HTML against the merged source | PASS | After line-ending normalisation, SHA-256 `3881a66e8bf3036ec02c2cd8f75bc9599beee749ca8b77950a14c5119c4e3c41` for both the live page and `learning-paths.html` at `origin/main` (before the change: `ffcbfee3…`) |
| Live `index.html` | PASS, unchanged | HTTP 200, 37,944 bytes; SHA-256 `76ab5391…fc6c7f` for the live page and `origin/main`; it links to `learning-paths.html` once; `git diff 3cdf163 origin/main` over `index.html`, `sitemap.xml` and `robots.txt` is empty |
| New content present, old content absent | PASS | The live page contains `7fa013c` 3 times, LAND-19 once and 'Run record' twice; `437e27f` and LAND-15 0 times. The metadata Version value is 12 and the 'Public snapshot' row reads 'Pinned from document commit 7fa013c; refreshed 25 November 2026, 17:31 UTC (LAND-19)'. |
| Real Chromium 149.0.7827.55 against the live URL | PASS, 16 of 16 | The same checks as the local run, including Version 12, `7fa013c` and LAND-19 in the metadata, the outline as text, the only `href` being `index.html`, and no overflow at 375 px in either theme |

The live fetches and browser run were made on 2026-11-26 between 21:00:50Z (Pages success) and 21:01:19Z.

## Failures and recovery

None. The Pages run was waiting when first listed; it was watched to completion before any live fetch.

## Durable lessons

- Watching the Pages run to completion before the first fetch removes the stale-first-poll step LAND-15 needed.
- The snapshot remains unchecked against its private source: the next change to the document makes this page stale again.

## Backlog reconciliation

- LAND-19: all six acceptance criteria are ticked. Four were ticked in the earlier log; the CI quality run with the owner merge, and the Pages deployment with the live-page match, are ticked here.
- No follow-up items were created. The Windows `reviews.html` line-ending mismatch noted in the earlier log remains a candidate only.
