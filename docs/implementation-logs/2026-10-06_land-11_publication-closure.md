# Implementation Log — LAND-11: Publication closure

**Date:** 2026-10-06
**Backlog item:** `LAND-11`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `claude/land-11-closure`
**Commit:** Merge commit `d85a3586c3610622af325267b49278e574320763` on `main` (the closure commit is this log's own commit, on the branch above).
**Pull request:** [PR #56](https://github.com/GBrooks1970/portfolio/pull/56), squash-merged by `GBrooks1970` at 2026-10-06T17:51:23Z.
**Pages run:** [pages build and deployment run 37506772130](https://github.com/GBrooks1970/portfolio/actions/runs/37506772130), success.

## Outcome

The TradeBlotter card refresh is merged, deployed and live. The live page shows the new summary and the
'Windows CI evidence' link, and its HTML is identical to `index.html` at the merge commit. This record
closes LAND-11 and supplements, without rewriting, the earlier
[implementation log](2026-10-06_land-11_tradeblotter-card-refresh.md), which recorded the work while
no pull request existed.

## Scope

- Evidence only. No presentation data or generated output changed in this closure.
- `docs/backlog.md`: LAND-11 moved from IN REVIEW to DONE, four acceptance criteria ticked with the
  evidence below, version 27.
- Related, not part of this item's completion: the matching `portfolio-prompts` registry notes change
  merged as [PR #112](https://github.com/NeoCognitus70/portfolio-prompts/pull/112), commit
  `6a61b8905888a5fa6d97a39b932a1f930b0f8227`, at 2026-10-06T17:52:01Z.

## Decisions

- **Closure authority:** the owner approved this closure log and marking LAND-11 DONE on 2026-10-06.
  The approval came first; closure was conditional on the evidence below, which was gathered afterwards
  and supports it.
- **Browser checks not repeated:** the item changed one card's copy and one link, and its acceptance
  criteria do not require desktop or mobile browser checks. Earlier items that did require them record
  them in their own logs. No browser render was performed for LAND-11.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| `portfolio-quality` on the pull request head `c35e7db` | PASS | [Run 37496927391](https://github.com/GBrooks1970/portfolio/actions/runs/37496927391): 53 tests, OK (skipped=3); sources PASS with 61 external URLs |
| `portfolio-quality` on `main` at the merge commit `d85a358` | PASS | [Run 37506774664](https://github.com/GBrooks1970/portfolio/actions/runs/37506774664), job 112417322261: step 'Run complete portfolio gate' 17:51:36Z to 17:51:41Z, conclusion success |
| External-URL check in CI | PASS | The workflow runs `python tools/verify_portfolio.py --registry-repository ../registry` with no `--skip-external`, so external checking was enabled, and the gate passed. The job log was read only from its tail, which shows the `sources PASS` line (61 external URLs) and `PASS — 53 tests`; the per-URL lines were not inspected. |
| Pages deployment of the exact merge commit | PASS | Run 37506772130 on `d85a358`: started 17:51:26Z, completed 17:52:20Z, conclusion success |
| Live page status | PASS | `https://gbrooks1970.github.io/portfolio/` returned HTTP 200, 35,449 bytes |
| Live HTML against the merged source | PASS | After line-ending normalisation, SHA-256 `c1be7d4ca3cdcd9ea08989e8bbaf3593c637c6d7a6a898a1b0067d5ba1dcd18b` for both the live page and `index.html` at `d85a358` (fetched from `raw.githubusercontent.com`); sizes equal |
| New text present, old text absent | PASS | Live HTML contains 'automated through a vendor-neutral driver contract', 'Windows CI evidence' and 'Parked at TB-08B'; it does not contain 'Phase 0 implementation record' or the old 'Driver abstraction' wording |

The live page was fetched on 2026-10-06 after the Pages run completed (17:52:20Z) and before 17:54:50Z.
Durations other than those above were not captured.

## Failures and recovery

None. One verification step found the Pages run still in progress shortly after the merge; it was
re-checked after completion, and the live fetch was made only after the run succeeded.

## Durable lessons

- To verify a generated page's deployment, compare the live HTML with the raw file at the merge commit
  after line-ending normalisation. Matching hashes are stronger evidence than the presence of a string.
- The external-URL gate passes in CI even where `github.com` pages return HTTP 403 in a restricted
  authoring environment, so a local 403 is not evidence about the links.
- The closure of a change made in two repositories can be recorded separately: the registry PR merged
  within a minute of this one and did not gate it.

## Backlog reconciliation

- LAND-11: all eight acceptance criteria are ticked. Four were ticked in the earlier log; the
  external-URL check, the owner merge, the Pages deployment and the live-page match are ticked here with
  the evidence above.
- No follow-up items were created.
