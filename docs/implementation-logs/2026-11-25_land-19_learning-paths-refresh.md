# Implementation Log — LAND-19: Refresh the Learning Paths snapshot to version 12

**Date:** 2026-11-25
**Backlog item:** `LAND-19`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `chore/land-19-refresh-learning-paths-v12`
**Commit:** The plan was committed first (`dc22c97`, then `e4ad365` recording approval and the backlog item), based on `3cdf163`. The generator change, test, snapshot, page and this log are in the final commit on the branch.
**Pull request:** None opened yet.
**Pages run:** N/A until the change is merged.

## Outcome

`data/learning-paths.json` now pins the Learning Paths document at version 12, last-change commit `7fa013c470a2442d2a0c3c74ceb00db94ba1f823`
(`GBrooks1970/test-automation-portfolio` #380, the `portfolio-docs` reorganisation), and `learning-paths.html` is regenerated from it. The visible change is
the metadata: Version 12, the 'Last updated' time, the 'Public snapshot' row and the provenance commit. To publish it, `public_link()` in the generator now
also accepts an optional `reference-history/` prefix on a bare file name; such a link becomes text, as before. The change is not merged, so the live page
still shows version 11. Merge and publication evidence belong in a closure log.

## Scope

- `tools/generate_learning_paths.py`: one line, the `public_link()` pattern gains `(?:reference-history/)?`.
- `tools/tests/test_generate_learning_paths.py`: one test (6 lines): the outline path becomes text; `reference-history/../secret.md`, `reference-history/sub/x.md`, `other-folder/x.md` and `/reference-history/x.md` still raise.
- `data/learning-paths.json`: `html`, `source.commit`, `snapshot.refreshed` and `snapshot.item` (4 insertions, 4 deletions).
- `learning-paths.html`: regenerated (4 insertions, 4 deletions).
- `docs/backlog.md` v43: the LAND-19 row and section (P2, IN PROGRESS); the plan and its index row (approved 2026-11-24).
- Non-goals, unchanged: the refresh script, `index.html`, `sitemap.xml`, `robots.txt`, cards, the registry and the source repository.

## Decisions

All five were approved as recommended on 2026-11-24: priority P2; `source.commit` is the document's last-change commit; the generator admits the `reference-history/`
prefix only (option a); two pull requests; done directly.

## Validation

Run on 2026-11-25 in a worktree with `core.autocrlf=false`. Source repository `origin/main` `6d4e817`; source page SHA-256 `e6166bb1…f90cc61d`.

| Gate | Result | Evidence |
|---|---|---|
| Step 0: document unchanged since `7fa013c` | PASS | `git log 7fa013c..origin/main -- portfolio-docs/PORTFOLIO_LEARNING_PATHS.md portfolio-docs/PORTFOLIO_LEARNING_PATHS.html` is empty; landing `origin/main` still `3cdf163` |
| Step 0: the source page is current | PASS | `build-docs-html.mjs ../PORTFOLIO_LEARNING_PATHS.md --check`: 'is current (marked 18.1.0)' |
| `refresh_learning_paths_snapshot.py --source <html> --check`, before | exit 1 | 'the snapshot differs from the source in: html' |
| `refresh_learning_paths_snapshot.py … --commit 7fa013c… --item LAND-19` | PASS | 'wrote learning-paths.json (commit 7fa013c, LAND-19, 2026-11-25T17:31Z)' |
| The same script with `--check`, after | exit 0 | 'the snapshot matches the source page' |
| `generate_learning_paths.py`, then `--check`; `generate_site.py --check` | PASS | 'learning-paths generation: PASS' twice; 'generate-site: PASS — committed HTML, sitemap and robots output is current' |
| `verify_portfolio.py --registry-repository ../portfolio-prompts --skip-external` | PASS | 'review sources PASS — 105 pinned URLs'; 'sources PASS — 15 showcase, 2 methodology, 85 named controls, 22 internal references, 66 external URLs, 20 contrast pairs'; 'PASS — 80 tests', OK (skipped=3). Baseline on `main`: same counts, 79 tests |
| Must-fail control: test file against the `origin/main` generator | FAIL, as expected | 13 tests, errors=3: the new test and the two that render the committed page, each on `ValueError: Unsupported Learning Paths link: reference-history/…` |
| `index.html`, `sitemap.xml`, `robots.txt` | unchanged | `git diff --quiet HEAD` over the three files |
| Real Chromium 149.0.7827.55 (Playwright, `file://`) | PASS, 16 of 16 | Detail below |
| Browser control: the same checks on `origin/main`'s page | 14 of 16, as expected | Fails exactly 'metadata: Version 12' and 'snapshot row 7fa013c and LAND-19' |
| External-URL check and remote CI | Not run here | No pull request exists yet; CI is the evidence |

Real Chromium, 16 checks: system light (`rgb(255, 255, 255)`) and system dark (`rgb(15, 23, 32)`) colours by default; the back link is left of the switch on one row; the
metadata block reads Version 12 and shows `7fa013c` and LAND-19, not `437e27f` or LAND-15; the outline name appears as text and no link targets it; the only `href` is
`index.html`; 9 tables, each in a scroll region; section 10 has 26 rows and 9 columns; click flips the theme; the choice persists across a reload; the first Tab stop is the
back link, the second is the switch with a 3 px focus ring; Enter and Space both toggle; with JavaScript off the page follows the system (dark) and the switch is hidden;
at 375 px in light and in dark there is no horizontal overflow and the back link and switch share a row without overlap.

## Failures and recovery

- The first dry run (2026-11-24) stopped in `generate_learning_paths.py` with `Unsupported Learning Paths link: reference-history/PORTFOLIO_LEARNING_PATHS_OUTLINE_2026-10-06.md`.
  The generator fails closed on any relative path with a folder; the owner chose to admit `reference-history/` only.
- On the Windows checkout (`core.autocrlf=true`) `verify_portfolio.py` fails on `main` with 'reviews.html is stale': the committed generated pages are LF and the checkout
  converts them to CRLF. An LF clone of the same commit passes, and CI on `main` is green (`Portfolio quality` run `42250320882`). Not caused by this change; out of scope.

## Durable lessons

- A rename in the private source repository can break the public generator even when the visible text does not change: link targets, not labels, are what it validates.
- On Windows, run the landing gates in a checkout with `core.autocrlf=false`; `.gitattributes` pins LF only for `index.html`, `sitemap.xml` and `robots.txt`.

## Backlog reconciliation

- Ticked, with evidence above: the refresh and its `--check`, the new link-rule test, the three gates, and the real-browser checks.
- Left open: the CI quality run, the owner merge, and the Pages deployment with the live-page match. LAND-19 stays IN PROGRESS until a closure log records them.
- No follow-up items were created. A `.gitattributes` `eol=lf` rule for every generated page would remove the Windows mismatch, if the owner wants it as an item.
