---
version: 1
created: 2026-10-07T14:11Z
project: portfolio-landing
type: implementation-plan
item: LAND-13
status: implemented
approved: 2026-10-07, Gary Brooks ("Approved, go with recommendations", every recommended option below); the owner merges
delivered: PR #61, squash commit 43d6fb8, merged 2026-10-07T14:49:34Z by the owner
language: en-GB
---

# Implementation plan: LAND-13 Refresh the Learning Paths snapshot to the current edition

**Goal.** Make the public page `learning-paths.html` match the Learning Paths document as it stands at
`13d102a336d5acbdbb2267fcc0c7f84962e27e2a` in `GBrooks1970/test-automation-portfolio`. The pinned snapshot (source commit
`2b83c40`, published by LAND-12) still says stage 4.4 'failed to start' and that the probe 'has no result', although stage 4.4
now passes after the juice-shop probe fix. The change is a snapshot refresh, not a redesign.

## Evidence gathered before planning

Read-only checks on 2026-10-07. Nothing in either repository was changed.

| Finding | Consequence for the plan |
|---|---|
| `data/learning-paths.json` pins source commit `2b83c40`. The paths document has changed once since then: #289 (`13d102a`). | That commit is the only content gap. |
| The delta between the snapshot HTML and the current document body is 4 changed lines (the Status paragraph, the 4.4 row, finding 7 and one section 9 bullet). The stylesheet is identical. The document has 2 hrefs, unchanged, with none added or removed. | The generator's 'unknown link form' failure will not trigger, and the pinned counts in `tools/tests/test_site_quality.py` (66 interactive, 7 internal references, 61 external URLs) should not move. |
| LAND-12 recorded the repository head at the time (`2b83c40`) as the source commit. The last commit that changed the document is `13d102a336d5acbdbb2267fcc0c7f84962e27e2a`. | Record the document's last-change commit: it is what the snapshot contains, and it stays accurate if unrelated commits land later. |
| `generate_site.py --check` and `generate_learning_paths.py --check` pass on landing `main` (`a49da0a`). | Those two gates are green before the change. |
| `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts --skip-external` exits 1 locally: 56 of 57 tests pass; `test_all_registered_showcase_projects_present` fails because `credit-dashboard-sut` is absent from the sibling `portfolio-reviews/README.md`. The test skips in CI, where that folder is absent. | Unrelated to this change. Record it, do not hide it, and raise the review-index gap separately. |
| The landing push run on `main` (`37628017743`, on `a49da0a`) failed in the external-URL check: `https://github.com/GBrooks1970/gb.automation.smoketests.sudoku.poc (HTTP 500)` after 3 attempts. The Pages build for that commit succeeded. | A transient external failure, not code. Re-run it before starting. |
| On the authoring machine `python3` is the Microsoft Store stub; `python` is 3.13.1. | Use `python` for every command. |
| The repository has no `docs/implementation-plans/` folder. LAND-11 and LAND-12 each used two pull requests: the change, then a publication closure. | Create the folder, its index and the template copy. Use the same two-pull-request pattern. |

## Steps

0. Before starting: fetch both repositories; confirm the paths document is unchanged since `13d102a`
   (`git log 13d102a..origin/main -- portfolio-docs/PORTFOLIO_LEARNING_PATHS.*` is empty); re-run the failed run `37628017743`.
1. Branch `chore/land-13-refresh-learning-paths-snapshot` from `origin/main`. Create `docs/implementation-plans/` with this plan and an
   `_index.md`; copy `templates/implementation-plan.template.md` into `docs/templates/`. Commit these first.
2. `docs/backlog.md` (v30): add LAND-13 (P1, IN PROGRESS), its table row, the status line and the acceptance criteria. It becomes DONE
   only with the Pages evidence, in the closure pull request.
3. Update `data/learning-paths.json` with a throw-away script: `html` from the body between `<div class="wrap">` and
   `<footer class="doc">` of `portfolio-docs/PORTFOLIO_LEARNING_PATHS.html`; `style` from its stylesheet (unchanged); `source.commit` set to
   `13d102a336d5acbdbb2267fcc0c7f84962e27e2a`. First prove that loading and writing the old file reproduces it byte for byte, so the diff is
   only the intended lines. Preserve the working copy's line endings.
4. `python tools/generate_learning_paths.py`, then `python tools/generate_learning_paths.py --check`, `python tools/generate_site.py --check`
   and `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts --skip-external`. Expect the same counts (15 showcase, 2
   methodology, 66 named controls, 7 internal references, 61 external URLs, 20 contrast pairs) and only the one known local test failure.
   `learning-paths.html` should differ by the four content lines and the commit reference; `index.html`, `sitemap.xml` and `robots.txt` must be unchanged.
5. Render `learning-paths.html` in Chromium at 375 px and 1280 px and confirm no horizontal overflow, as LAND-12 did.
6. Write `docs/implementation-logs/2026-10-07_land-13_learning-paths-refresh.md` with the evidence; commit; push; open a pull request. Not merged.
7. After the owner merges: confirm the Pages run on the exact merge commit succeeded; confirm the live `learning-paths.html` returns 200 and
   its SHA-256 matches `origin/main` after line-ending normalisation; confirm the live text contains the new wording ('passes after a fix')
   and not the old ('has not produced a result here'). Then open the closure pull request: close LAND-13 with the evidence, add a
   publication-closure log, and append this plan's Outcome.
8. Afterwards, in `test-automation-portfolio`: a handover v4 recording the refresh and correcting v3's stale rows (separate pull request).

## Verification

- The snapshot diff is limited to the four content lines and the commit reference; both `generate_*` checks pass.
- `verify_portfolio` reports the same counts; the one known local failure is recorded, not hidden.
- The pull request's quality run passes in CI. If the external-URL check flakes with a transient 5xx, re-run it rather than treat it as a code failure.
- The live page matches `origin/main` after merge and shows the new wording. This is the check that would fail if the refresh did not publish.

## Delivery

Branch `chore/land-13-refresh-learning-paths-snapshot`; pull request 1 carries the plan, backlog item, snapshot, regenerated page and
implementation log; the owner merges. Pull request 2 (after Pages is confirmed) closes LAND-13 and adds the Outcome. The handover v4 is a
separate pull request in `test-automation-portfolio`.

**Out of scope:** cards, groups, the registry, the sitemap and robots, the source repository's content, making the source repository public,
automating the refresh (nothing can check the snapshot against a private repository), and the missing `credit-dashboard-sut` entry in
`portfolio-reviews/README.md`.

## Decisions put to the owner

| Decision | Options | Recommended | Owner's answer |
|---|---|---|---|
| Priority | P1 or P2 | P1: the public page makes a stale claim. LAND-12 was P2 as an enhancement, LAND-11 (a card refresh) was P0 | P1, approved 2026-10-07 |
| `source.commit` | The commit that last changed the document; or the repository head at refresh time (LAND-12's precedent) | The document's last-change commit `13d102a…`: it is what the snapshot contains | `13d102a…`, approved 2026-10-07 |
| The red push run on `main` | Re-run now; or leave | Re-run: a transient external 500, and a green baseline helps the pull request | Re-run, approved 2026-10-07 |
| Pull requests | Two (change, then closure); or one | Two, as for LAND-11 and LAND-12 | Two, approved 2026-10-07 |
| Who does it | Directly; or a subagent | Directly: it is small and touches a public site | Directly, approved 2026-10-07 |

## Outcome

Delivered as planned. [PR #61](https://github.com/GBrooks1970/portfolio/pull/61) (two commits: `df591be` the plan, `1521ec7` the snapshot, page, backlog item and log) was merged by the
owner as `43d6fb8d23f1e66e9ba95be4d080e3880553db48` on 2026-10-07 at 14:49:34Z. The logs are
[`docs/implementation-logs/2026-10-07_land-13_learning-paths-refresh.md`](../implementation-logs/2026-10-07_land-13_learning-paths-refresh.md) and
[`2026-10-07_land-13_publication-closure.md`](../implementation-logs/2026-10-07_land-13_publication-closure.md).

- **Change:** `data/learning-paths.json` `html` and `source.commit` (now `13d102a336d5acbdbb2267fcc0c7f84962e27e2a`) refreshed; `learning-paths.html` regenerated. Only four content lines and the footer commit reference changed; `style`, `title`, the other `source` fields, `index.html`, `sitemap.xml` and `robots.txt` did not.
- **Verification, as planned:** both recipes were proved against the old snapshot first; `generate_learning_paths.py --check` and `generate_site.py --check` passed; `verify_portfolio.py --skip-external` reported the same counts (15 showcase, 2 methodology, 66 controls, 7 internal references, 61 external URLs, 20 contrast pairs) with the one known local test failure; Chromium showed no overflow at 1280 px or 375 px. PR quality run `37639374795` and exact-merge run `37639969505` passed; Pages run `37639968207` on the merge commit succeeded.
- **The check that would have failed if the refresh had not published:** the live page returned HTTP 200, its SHA-256 equals `origin/main` after line-ending normalisation (`dcf810d9…b31d3`), it contains 'passes after a fix' and does not contain 'has not produced a result here'.
- **Differences from the plan:** none in design or scope. The re-run of the red `main` push run (step 0) succeeded on attempt 2, as expected from a transient external HTTP 500.
- **Not done, as stated in the plan:** the missing `credit-dashboard-sut` entry in the sibling `portfolio-reviews/README.md` (a content gap in `test-automation-portfolio`), and any automation of the refresh.
