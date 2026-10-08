---
version: 1
created: 2026-10-08T00:30Z
project: portfolio-landing
type: implementation-plan
item: LAND-15
status: approved
approved: 2026-10-08, Gary Brooks ("approve with recommendations", every recommended option below); the owner merges
delivered: not yet
language: en-GB
---

# Implementation plan: LAND-15 Refresh the Learning Paths snapshot to version 11

**Goal.** Make the public page `learning-paths.html` match the Learning Paths document as it stands at
`437e27fb8c0ac00ff9191ba373eb13010593ec1c` in `GBrooks1970/test-automation-portfolio` (document version 11). The pinned snapshot (source
commit `6fe8133fea6a59accba608dfe77431f8f708b5bd`, version 10, published by LAND-14) lacks what EV-1 PR 1 added to the document
(`test-automation-portfolio` #301): the Status counts generated from run records, and a new section 10, 'Run record', a table of the latest
run record for each of the 26 stages. The change is a snapshot refresh, not a redesign, and follows
[`docs/learning-paths-refresh.md`](../learning-paths-refresh.md).

## Evidence gathered before planning

Read-only checks on 2026-10-08. The real repositories were not changed; the dry run below ran in a scratch copy of this repository.

| Finding | Consequence for the plan |
|---|---|
| `data/learning-paths.json` (schema 2) pins source commit `6fe8133…`, refreshed 2026-10-07T17:54Z by LAND-14. The document has changed once since: `437e27f` (#301, version 10 to 11). | That commit is the only content gap. |
| In the source repository at `7e794b2` (`origin/main`), `node build-docs-html.mjs ../PORTFOLIO_LEARNING_PATHS.md --check` and `node build-learning-paths-evidence.mjs --check` both pass. | The source page is current and its generated parts match its run records. |
| `python3 tools/refresh_learning_paths_snapshot.py --source <source html> --check` before any change exits 1: 'the snapshot differs from the source in: html'. | Only `html` differs; `style`, `scripts`, `title` and the top-bar button are unchanged, so the generator and its guards need no change. |
| Dry run in a scratch copy of this repository: the refresh script wrote the snapshot (`--commit 437e27f… --item LAND-15`), its `--check` then passed, and `generate_learning_paths.py`, `generate_learning_paths.py --check` and `generate_site.py --check` passed. `verify_portfolio.py --registry-repository ../portfolio-prompts --skip-external`: `sources PASS` with 15 showcase, 2 methodology, 66 named controls, 7 internal references, 61 external URLs and 20 contrast pairs; 74 tests, OK (skipped=3). | The pinned counts in `tools/tests/test_site_quality.py` need no change, and `index.html`, `sitemap.xml` and `robots.txt` do not change. |
| The dry-run diff of `learning-paths.html` is 317 insertions and 11 deletions; `data/learning-paths.json` changes `html`, `source.commit`, `snapshot.refreshed` and `snapshot.item`. The page's `href` set is unchanged (`index.html` only), scripts stay at 2, and tables go from 8 to 9. | The size is the new section 10 table (26 rows, 9 columns) and the changed metadata and Status text. No link is added or removed, so the generator's 'unknown link form' failure does not trigger. |
| Landing `main` at `7e792f6` is green: `Portfolio quality` run `37665080370` and `pages build and deployment` run `37665079717` both succeeded. | There is a green baseline, with no transient failure to re-run first. |
| Section 10 shows each stage's latest run record, including the platform label (for example 'Windows (owner machine)', 'Linux 6.18 (cloud container)'), the project commit and the record id. | The page publishes more run detail than before. All of it is already in the document's cells or in public project repositories; the owner is asked to confirm (decision 3). |
| The 9-column section 10 table is wide for a phone. The source page's own check showed no page-level overflow at 375 px because the table sits in a scroll region. | The browser check at 375 px and 1280 px, in both themes, must confirm the same on this page, which adds its own top bar. |

## Steps

0. Before starting: fetch both repositories; confirm the document is unchanged since `437e27f` (`git log 437e27f..origin/main -- portfolio-docs/PORTFOLIO_LEARNING_PATHS.md portfolio-docs/PORTFOLIO_LEARNING_PATHS.html`
   is empty) and the source page `--check` still passes. If the document has changed again, stop and re-plan against the newer commit.
1. Branch `chore/land-15-refresh-learning-paths-snapshot` from `origin/main`. Commit this plan and its index row first.
2. `docs/backlog.md` (v34): add LAND-15 (priority per decision 1, IN PROGRESS), its table row, the status line and the acceptance criteria, with a link to the runbook. It becomes DONE only with the Pages evidence, in the closure pull request.
3. Refresh the snapshot with the committed script:
   `python tools/refresh_learning_paths_snapshot.py --source <PORTFOLIO_LEARNING_PATHS.html> --commit 437e27fb8c0ac00ff9191ba373eb13010593ec1c --item LAND-15`,
   then the same command with `--check`, then `python tools/generate_learning_paths.py`. On the Windows machine use `python`.
4. Gates: `python tools/generate_learning_paths.py --check`, `python tools/generate_site.py --check`, and
   `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts --skip-external`. Expect `sources PASS` with the counts above, the same test count, and no change to `index.html`, `sitemap.xml` or `robots.txt`.
5. Look at it in Chromium at 1280 px and 375 px in the light and dark themes: no horizontal overflow, the switch at the top right beside 'Back to portfolio', the section 10 table in a scroll region with 26 rows, and the 'Public snapshot' row and metadata block showing version 11 and the new commit. Check the switch by keyboard and with JavaScript off.
6. Write `docs/implementation-logs/2026-10-08_land-15_learning-paths-refresh.md` with the evidence; commit; push; open a pull request. Not merged: the owner merges.
7. After the owner merges: confirm the exact-merge quality run and the Pages run succeeded; fetch the live `learning-paths.html` (a 404 shortly after a merge can mean the deployment is still running) and compare its SHA-256 with `origin/main` after normalising line endings; check the live text shows version 11 and the 'Run record' heading and not the version 10 wording; check the live `index.html` still links to the page and is unchanged. Then open the closure pull request: mark LAND-15 DONE with the evidence, add the `…_publication-closure.md` log, and append this plan's Outcome.
8. Afterwards, in `test-automation-portfolio`: a handover v5 recording EV-1 and LAND-15 (separate pull request, if the owner wants it).

## Verification

- `refresh_learning_paths_snapshot.py --check` exits 1 before the refresh and 0 after it (shown in the dry run). It would fail again if the snapshot were edited by hand.
- Both `generate_*` checks pass; `verify_portfolio` reports the same counts and test count; `index.html`, `sitemap.xml` and `robots.txt` are unchanged.
- The pull request's quality run passes in CI. The external-URL check can flake on a transient 5xx from GitHub; re-run it before treating it as a regression.
- The live page matches `origin/main` after merge and shows version 11 with section 10. This is the check that would fail if the refresh did not publish.

## Delivery

Branch `chore/land-15-refresh-learning-paths-snapshot`; pull request 1 carries the plan, the backlog item, the snapshot, the regenerated page and the implementation log; the owner merges. Pull request 2 (after Pages is confirmed) closes LAND-15 and adds the Outcome.

**Out of scope:** cards, groups, the registry, the sitemap and robots, the source repository's content, making the source repository public, automating the refresh (nothing can check the snapshot against a private repository), and any change to the generator or the refresh script.

## Decisions put to the owner

| Decision | Options | Recommended | Owner's answer |
|---|---|---|---|
| Priority | P1 or P2 | P2: the public page is behind, not wrong. Its Status counts are the same numbers (25 of 26 run, 21 as written, stage 4.2 not run), and it lacks the version 11 metadata and section 10. LAND-13 was P1 because it corrected a stale claim | As recommended, approved 2026-10-08 |
| `source.commit` | The document's last-change commit `437e27f…`; or the repository head | The document's last-change commit: it is what the snapshot contains (LAND-13's precedent) | As recommended, approved 2026-10-08 |
| Publish section 10 as generated | Publish the whole document; or hold section 10 back | Publish: it is the evidence behind the Status counts, and it contains nothing the document or the public project repositories do not already show | As recommended, approved 2026-10-08 |
| Pull requests | Two (change, then closure); or one | Two, as for LAND-11 to LAND-14 | As recommended, approved 2026-10-08 |
| Who does it | Directly; or a subagent | Directly: it is small and touches a public site | As recommended, approved 2026-10-08 |

## Outcome

Not yet delivered.
