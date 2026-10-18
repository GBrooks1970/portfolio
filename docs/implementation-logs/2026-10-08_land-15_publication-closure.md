# Implementation Log — LAND-15: Publication closure

**Date:** 2026-10-08
**Backlog item:** `LAND-15`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `chore/land-15-closure`
**Commit:** Merge commit `b045dd63a20db9117bfba41d6a5e74f3c84bac7b` on `main` (the closure commit is this log's own commit, on the branch above).
**Pull request:** [PR #65](https://github.com/GBrooks1970/portfolio/pull/65), merged by `GBrooks1970` at 2026-10-08T00:24:45Z.
**Pages run:** [pages build and deployment run 37707630649](https://github.com/GBrooks1970/portfolio/actions/runs/37707630649), success.

## Outcome

The Learning Paths snapshot at document version 11 is merged, deployed and live. The live `learning-paths.html` is identical to the merged file after line-ending normalisation
and shows Version 11, the source commit `437e27f`, LAND-15 and the new 'Run record' section. `index.html`, `sitemap.xml` and `robots.txt` are unchanged. This record closes LAND-15
and supplements, without rewriting, the earlier [implementation log](2026-10-08_land-15_learning-paths-refresh.md), which recorded the work while no pull request existed.

## Scope

- Evidence only. No page, data or generator changed in this closure.
- `docs/backlog.md`: LAND-15 moved from IN PROGRESS to DONE, the three open acceptance criteria ticked with the evidence below, version 35.
- `docs/implementation-plans/2026-10-08_land-15-refresh-learning-paths-v11.md` and its `_index.md`: status set to implemented, `delivered` filled in and an Outcome appended; the approved body is unchanged.

## Decisions

- **Closure authority:** the owner approved the plan on 2026-10-08, merged the pull request, and the plan's step 7 provides for this closure.
- **Live browser run added.** LAND-12 and LAND-13 closed on status, hash and content checks, and LAND-14 added a live browser run for new behaviour. This change adds no behaviour but adds a 9-column table, so the 16 local
  browser checks were repeated against the live URL.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| `portfolio-quality` on the pull request head `d59d15b` | PASS | [Run 37706850153](https://github.com/GBrooks1970/portfolio/actions/runs/37706850153): 2026-10-08T00:16:04Z to 00:16:18Z, success |
| `portfolio-quality` on `main` at the merge commit `b045dd6` | PASS | [Run 37707631345](https://github.com/GBrooks1970/portfolio/actions/runs/37707631345): 00:24:48Z to 00:25:06Z, success |
| External-URL check in CI | PASS | The workflow runs `tools/verify_portfolio.py` and contains no `--skip-external`, so external checking was enabled and the gate passed. The job log was not read; the per-URL lines were not inspected. |
| Pages deployment of the exact merge commit | PASS | Run 37707630649 on `b045dd6`: 00:24:47Z to 00:25:27Z, success |
| Live `learning-paths.html` status | PASS | HTTP 200, 48,114 bytes; the new content ('Run record') appeared on the second poll, about 16 s after polling began (the Pages run was still in progress when polling started) |
| Live HTML against the merged source | PASS | After line-ending normalisation, SHA-256 `ffcbfee3f6951fbfe630c1efe0bb8d1f1fca3e93fa6bb85aef5ceb48b297c3b4` for both the live page and `learning-paths.html` at `origin/main` (before the change: `b715457b…a4ca6`) |
| Live `index.html` | PASS, unchanged | HTTP 200, 35,623 bytes; SHA-256 `b9565d1829fe993be42ac4c713e99dcdedc9bed3edcf1830f4d2d096ca5863c7` for the live page, `origin/main` and `7e792f6`; it links to `learning-paths.html` once |
| `sitemap.xml`, `robots.txt` | unchanged | `git diff 7e792f6 origin/main` over both is empty |
| New content present, old content absent | PASS | The live page contains 'Run record' (2 occurrences) and `437e27f` (2) and LAND-15 (1); it contains `6fe8133` 0 times and LAND-14 0 times. The metadata Version value is 11 and the 'Public snapshot' row reads 'Pinned from document commit 437e27f; refreshed 8 October 2026, 00:14 UTC (LAND-15)'. |
| Real Chromium (Playwright 1.61.1) against the live URL | PASS, 16 of 16 | The same checks as the local run: system light and dark; back link left of the switch; Version 11; the new commit and LAND-15; section 10 with 26 rows and 9 columns in a keyboard-focusable scroll region; the Status paragraph; 9 tables in scroll regions; click flips and saves; persistence across a reload; Tab order and a 3 px focus ring; Enter and Space; JavaScript off follows the system and hides the switch; no overflow at 375 px in either theme |

The live fetches were made on 2026-10-08 after the Pages run completed (00:25:27Z). Durations other than those above were not captured.

## Failures and recovery

None. The deployment was still running when the live page was first polled; the poll was repeated until the new content appeared, and the hash comparison was made after the Pages run succeeded.

## Durable lessons

- The first poll for new content can precede the Pages deployment. Poll until the new text appears, then compare hashes.
- The live checks for a content-only refresh are the same as the local ones; keeping the browser script means they cost one command.
- The snapshot remains unchecked against its private source: the next change to the document makes this page stale again.

## Backlog reconciliation

- LAND-15: all six acceptance criteria are ticked. Three were ticked in the earlier log; the CI quality run, the owner merge and the Pages deployment with the live-page match are ticked here with the evidence above.
- No follow-up items were created.
