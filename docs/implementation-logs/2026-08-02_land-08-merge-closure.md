# Implementation Log — LAND-08: Merge and Publication Closure

**Date:** 2026-08-02
**Backlog item:** `LAND-08`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `codex/land-08-closure`
**Implementation commit:** `9e79ee645e99773ae2f7f8f8f9f947fb208ab911`
**Implementation pull request:** https://github.com/GBrooks1970/portfolio/pull/18
**Merge commit:** `728182e41cab2c062b270a228508fde4446bc7be`
**Closure evidence commit:** `0f352e0a1a550ffdee249a34809f6e3e9d1fd92b`
**Closure pull request:** https://github.com/GBrooks1970/portfolio/pull/19
**Pages run:** https://github.com/GBrooks1970/portfolio/actions/runs/30747708632

## Outcome

LAND-08 is complete. PR #18 merged as `728182e41cab2c062b270a228508fde4446bc7be`;
the exact merge commit passed the Portfolio quality workflow and GitHub Pages deployment. The
published `index.html` returns HTTP 200, is 23,218 bytes and exactly matches `main` at SHA-256
`B76F032FD98408CD58C9E23B594039799FD1AEB877AFB36E2D66E48F6DC1CD3C`.

The live page exposes four named capability regions containing 3/2/2/2 cards, nine card `h4`
headings, one methodology entry and the generated 9-project / 4-area / 4-public-demo-or-report
summary. Desktop and 390px browser checks show no horizontal, card, block or action overflow, all
22 project actions retain at least a 44px target, and the console is clean.

## Scope

- Mark draft PR #18 ready and merge only its validated head `b2e35dcf7861ce653d0d52c104d0640d72714b42`.
- Fast-forward the clean local landing checkout to the resulting `origin/main` merge commit.
- Observe exact-merge Portfolio quality and Pages workflows.
- Compare the deployed HTML byte-for-byte with committed `main` and verify LAND-08 inventory,
  grouping, statistics and heading markers.
- Recheck the published desktop and 390px layouts, action targets, overflow and console output.
- `docs/backlog.md` — check the final criterion and move LAND-08 from IN REVIEW to DONE.
- Explicit non-goal: do not promote or implement LAND-C03 or LAND-C04 without a new owner decision.

## Decisions

- Merge with an expected-head guard. A clean status is insufficient if the branch can move between
  validation and merge.
- Close against the exact merge commit and exact deployed bytes, not successful pull-request CI or
  a visually similar cached page.
- Keep the implementation log immutable. This separate closure record owns merge, publication and
  live-page evidence.
- Treat the Node.js 20 deprecation annotation in GitHub's generated Pages build as non-blocking and
  platform-owned: GitHub forced the referenced actions to Node.js 24 and the build/deploy/report jobs
  all passed. No repository workflow change can remove that generated-workflow annotation.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| Owner merge | PASS | PR #18 merged 2026-08-02 as `728182e41cab2c062b270a228508fde4446bc7be` |
| Exact-merge quality | PASS | [Run 30747708908](https://github.com/GBrooks1970/portfolio/actions/runs/30747708908) succeeded for `728182e`; 9 showcases, 1 methodology entry, 35 controls, 5 internal references, 34 external URLs, 20 contrast pairs and 43 tests |
| Exact-merge Pages | PASS | [Run 30747708632](https://github.com/GBrooks1970/portfolio/actions/runs/30747708632) completed build, deploy and status reporting for `728182e` |
| Local generated output | PASS | `python tools/generate_site.py --check` verifies HTML, sitemap and robots exact bytes on fast-forwarded `main` |
| Live HTML | PASS | HTTP 200; 23,218 bytes; exact `main` SHA-256 `B76F032FD98408CD58C9E23B594039799FD1AEB877AFB36E2D66E48F6DC1CD3C` |
| Live structure | PASS | 9 showcase cards, 4 capability regions, 9 card `h4`s, one methodology entry and one 9/4/4 count marker |
| Live desktop | PASS | 1440px override / 1425px content viewport; 3/2/2/2 cards; 9/4/4 statistics; zero horizontal or out-of-viewport card overflow |
| Live mobile | PASS | 390px override / 375px content viewport; nine 331px cards; 22 actions; zero document/card/block/action overflow; no action below 44px |
| Live console | PASS | No warning or error entries after desktop and mobile publication reloads |

## Failures and recovery

- The first live desktop screenshot exceeded the browser capture timeout. The already captured local
  viewport visual remained valid because deployed bytes exactly matched `main`; live DOM geometry,
  semantic snapshot and console inspection independently verified the published render.
- Viewport overrides were initially sampled before the browser had applied them, reversing the first
  desktop/mobile measurements. Waiting for the explicit override before reload produced stable
  1425px and 375px content widths and the expected results.
- GitHub's generated Pages build emitted a Node.js 20 deprecation annotation while explicitly
  forcing the referenced actions onto Node.js 24. All Pages jobs passed; the annotation is retained
  here rather than misreported as a repository-owned CI defect.

## Durable lessons

- Exact byte parity lets local visual evidence support a live deployment when the publication
  screenshot surface itself fails, provided live semantic and layout measurements are also taken.
- Responsive verification must record the actual content viewport, not only the requested override;
  browser chrome and scrollbars can make those values differ.
- Generated Pages-workflow annotations need an ownership check before entering the backlog. A
  platform-generated warning with successful forced runtime migration is not automatically an
  actionable repository task.

## Backlog reconciliation

- The final LAND-08 criterion is checked with pull-request CI, guarded owner merge, exact-merge
  quality, Pages, live/source byte parity and published desktop/mobile evidence.
- LAND-08 moves from IN REVIEW to DONE without exception.
- LAND-01 through LAND-08 are closed. LAND-C03 and LAND-C04 remain PROPOSED and unauthorised.
