# Implementation Log — LAND-13: Publication closure

**Date:** 2026-10-07
**Backlog item:** `LAND-13`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `chore/land-13-closure`
**Commit:** Merge commit `43d6fb8d23f1e66e9ba95be4d080e3880553db48` on `main` (the closure commit is this log's own commit, on the branch above).
**Pull request:** [PR #61](https://github.com/GBrooks1970/portfolio/pull/61), squash-merged by `GBrooks1970` at 2026-10-07T14:49:34Z.
**Pages run:** [pages build and deployment run 37639968207](https://github.com/GBrooks1970/portfolio/actions/runs/37639968207), success.

## Outcome

The refreshed Learning Paths page is merged, deployed and live. `learning-paths.html` on the live site is identical to the merged file after
line-ending normalisation, and it now says stage 4.4 'Failed on 6 October 2026; passes after a fix' and no longer says the probe 'has no
result'. This record closes LAND-13 and supplements, without rewriting, the earlier
[implementation log](2026-10-07_land-13_learning-paths-refresh.md), which recorded the work while no pull request existed.

## Scope

- Evidence only. No page, data or generator changed in this closure.
- `docs/backlog.md`: LAND-13 moved from IN PROGRESS to DONE, the three open acceptance criteria ticked with the evidence below, version 31.
- `docs/implementation-plans/2026-10-07_land-13-refresh-learning-paths-snapshot.md` and its `_index.md`: status set to implemented, `delivered`
  filled in and an Outcome appended; the approved body is unchanged.

## Decisions

- **Closure authority:** the owner merged the pull request and asked for this closure on 2026-10-07, after the plan was approved with every
  recommended option.
- **Browser checks not repeated:** the pre-merge Chromium render (no horizontal overflow at 1280 px and 375 px) is in the earlier log. No browser
  render of the live page was performed for this closure; the live checks below are an HTTP fetch, a hash comparison and a content search.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| `portfolio-quality` on the pull request head `1521ec7` | PASS | [Run 37639374795](https://github.com/GBrooks1970/portfolio/actions/runs/37639374795), job 112853931126: 14:45:25Z to 14:45:37Z; step 'Run complete portfolio gate' 14:45:30Z to 14:45:35Z, success |
| `portfolio-quality` on `main` at the merge commit `43d6fb8` | PASS | [Run 37639969505](https://github.com/GBrooks1970/portfolio/actions/runs/37639969505), job 112855997701: 14:49:39Z to 14:49:56Z; step 'Run complete portfolio gate' 14:49:46Z to 14:49:51Z, success |
| External-URL check in CI | PASS | No workflow file contains `--skip-external` (a search of `.github/workflows/*.yml` returned 0 matches), so the gate ran with external checking enabled and passed |
| Pages deployment of the exact merge commit | PASS | Run 37639968207 on `43d6fb8`: 14:49:36Z to 14:50:23Z, conclusion success |
| Live `learning-paths.html` status | PASS | HTTP 200, 37,767 bytes, fetched with a cache-busting query after the Pages run completed |
| Live HTML against the merged source | PASS | After line-ending normalisation, SHA-256 `dcf810d919bedce5530009c64e0f21d186ae01cccb429c432f2fd4954a0b31d3` for the live page and `learning-paths.html` at `origin/main` |
| Live `index.html` against the merged source | PASS | SHA-256 `b9565d1829fe993be42ac4c713e99dcdedc9bed3edcf1830f4d2d096ca5863c7` for both; 35,623 bytes; the live page still carries `href="learning-paths.html"` with the text 'Learning Paths' |
| Page content | PASS | The live page contains 'passes after a fix', 'has been fixed' and the commit reference `13d102a`, and does not contain 'has not produced a result here' or 'Failed on Windows, Node 24.18.0.' |
| The red `main` push run before the work (`37628017743`) | PASS on re-run | Attempt 2 completed successfully (updated 14:40:50Z); the first attempt had failed on an external HTTP 500 from GitHub |

The live `learning-paths.html` fetch was made on 2026-10-07 after the Pages run completed (14:50:23Z); the `index.html` fetch was made at about
14:55Z. Fetch times were not otherwise captured, and neither were durations other than those above.

## Failures and recovery

None. The first attempt of the earlier `main` push run had failed on a transient external HTTP 500 and passed on re-run, before this change began.

## Durable lessons

- The refresh worked as the earlier lessons predicted: prove a regeneration recipe against the old inputs first, then compare the live file with
  the merged one by hash. Matching hashes are stronger evidence than the presence of a string, and the string checks add the human-meaningful part.
- The pinned page is stale whenever its source document changes, and nothing can check that in CI. Any edit to
  `PORTFOLIO_LEARNING_PATHS.md` in `test-automation-portfolio` should be followed by a refresh of `data/learning-paths.json` here.
- A snapshot's `source.commit` is best set to the commit that last changed the source document, not to the repository head.

## Backlog reconciliation

- LAND-13: all seven acceptance criteria are ticked. Four were ticked in the earlier log; the pull request's CI run, the owner merge, and the
  Pages deployment with live-page match are ticked here with the evidence above.
- No follow-up items were created. The `portfolio-reviews` index gap (`credit-dashboard-sut` missing from the sibling
  `portfolio-reviews/README.md`, which makes one test fail locally) is reported to the owner separately.
