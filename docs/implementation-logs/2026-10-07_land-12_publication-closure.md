# Implementation Log — LAND-12: Publication closure

**Date:** 2026-10-07
**Backlog item:** `LAND-12`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `claude/land-12-closure`
**Commit:** Merge commit `6e9907b6fd619eea04735936a809d0b900c3c61f` on `main` (the closure commit is this log's own commit, on the branch above).
**Pull request:** [PR #58](https://github.com/GBrooks1970/portfolio/pull/58), squash-merged by `GBrooks1970` at 2026-10-07T13:06:00Z.
**Pages run:** [pages build and deployment run 37625885376](https://github.com/GBrooks1970/portfolio/actions/runs/37625885376), success.

## Outcome

The Learning Paths page is merged, deployed and live. The hero link and `learning-paths.html` are on the live site,
and both files are identical to the merged sources after line-ending normalisation. This record closes LAND-12 and
supplements, without rewriting, the earlier [implementation log](2026-10-07_land-12_learning-paths-page.md), which
recorded the work while no pull request existed.

## Scope

- Evidence only. No page, data or generator changed in this closure.
- `docs/backlog.md`: LAND-12 moved from IN REVIEW to DONE, the three open acceptance criteria ticked with the
  evidence below, version 29.

## Decisions

- **Closure authority:** the owner asked for this closure log and for LAND-12 to be marked DONE on 2026-10-07,
  after the merge and after the evidence below was reported to them.
- **Browser checks not repeated:** the pre-merge Chromium render (no horizontal overflow at 1280 px and 375 px) is
  in the earlier log. No browser render of the live page was performed for this closure.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| `portfolio-quality` on the pull request head `d84f58b` | PASS | [Run 37623616244](https://github.com/GBrooks1970/portfolio/actions/runs/37623616244), job 112799733134: started 12:47:59Z, completed 12:48:11Z, conclusion success |
| `portfolio-quality` on `main` at the merge commit `6e9907b` | PASS | [Run 37625886411](https://github.com/GBrooks1970/portfolio/actions/runs/37625886411), job 112807396125: step 'Run complete portfolio gate' 13:06:19Z to 13:06:25Z, conclusion success |
| External-URL check in CI | PASS | The workflow runs `tools/verify_portfolio.py` and contains no `--skip-external` (the file has no such string), so external checking was enabled and the gate passed. The job log was not read; the per-URL lines were not inspected. |
| Pages deployment of the exact merge commit | PASS | Run 37625885376 on `6e9907b`: started 13:06:07Z, completed 13:06:52Z, conclusion success |
| Live `learning-paths.html` status | PASS | HTTP 200, 36,162 bytes, first returned within 32 seconds of polling (404 on a check made about a minute earlier, before the deployment finished) |
| Live HTML against the merged source | PASS | After line-ending normalisation, SHA-256 `32ae3c533a3f5507424a126013d031c7adbe23dfd0f49188b64fab4a351f3458` for the live page and `learning-paths.html` at `origin/main`; size 36,162 bytes for both |
| Live `index.html` against the merged source | PASS | SHA-256 `3653a01f8ea026eca2beea75b2203e29f1ee39ac299c57c61169c6ce76f4df04` for both; 35,511 bytes; the live page contains exactly one `href="learning-paths.html"` |
| Page content | PASS | The live page's `<h1>` is 'Portfolio Learning Paths' |

The live fetches were made on 2026-10-07 after the Pages run completed (13:06:52Z). Durations other than those
above were not captured.

## Failures and recovery

None. An early fetch of the live page, made while the Pages run was still in progress, returned HTTP 404. It was
repeated until the page returned 200, and the content comparison was made only after the Pages run succeeded.

## Durable lessons

- The pinned page cannot be drift-checked against its private source in CI. A new edition of the Learning Paths
  document needs a deliberate refresh of `data/learning-paths.json` and a landing pull request.
- A 404 shortly after a merge can mean the Pages deployment is still running; confirm the run's conclusion before
  treating it as a failure.
- Matching hashes of the live file and the file at the merge commit are stronger evidence than the presence of a
  string.

## Backlog reconciliation

- LAND-12: all nine acceptance criteria are ticked. Six were ticked in the earlier log; the external-URL check, the
  owner merge and the Pages deployment with live-page match are ticked here with the evidence above.
- No follow-up items were created.
