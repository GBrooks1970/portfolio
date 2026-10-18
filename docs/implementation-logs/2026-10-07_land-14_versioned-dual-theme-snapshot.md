# Implementation Log — LAND-14: Publish the versioned, dual-theme Learning Paths page

**Date:** 2026-10-07
**Backlog item:** `LAND-14`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `chore/land-14-versioned-dual-theme-snapshot`
**Base:** `c166e71` (`origin/main`). The plan was committed first as `4a7e448`.
**Pull request:** None opened yet when this log was written; the pull request description records the number.
**Pages run:** N/A until the change is merged.

## Outcome

`learning-paths.html` is regenerated from a snapshot rebuilt, by a committed script, from the source repository's new generated page
(`GBrooks1970/test-automation-portfolio` #297, document last-change commit `6fe8133fea6a59accba608dfe77431f8f708b5bd`, version 10). The page now
shows the document's version, dates, evidence cut-off and source revision, a 'Public snapshot' row (document commit, refresh time, backlog item), the house
light/dark switch at the top right beside 'Back to portfolio', and a dark palette. The change is on a branch and not merged, so the live page does not yet show it.
This is part B of the owner-approved plan LC-V1; part A merged in the source repository, and part C (the closure after Pages) follows this merge.

## Scope

- `data/learning-paths.json` (`schemaVersion` 2): rebuilt by `tools/refresh_learning_paths_snapshot.py`. New: `snapshot` (`refreshed`, `item`), `scripts` (`prePaint`,
  `toggle`) and `topbarButton`. `source.commit` is `6fe8133…`. The `html` is now the content between the source's `<!-- doc:begin -->` and `<!-- doc:end -->` markers.
- `tools/generate_learning_paths.py`: renders the top bar (back link left, switch right), the two scripts, a 'Public snapshot' row in the metadata block, private links
  as plain text (a bare relative `.html` name now counts as private, like `.md`), and **no table wrapping of its own** (the source already wraps each table).
- `tools/refresh_learning_paths_snapshot.py` (new) and its tests; the generator's tests extended.
- `docs/learning-paths-refresh.md` (new runbook), linked from `README.md` and the LAND-12, LAND-13 and LAND-14 backlog entries; `docs/backlog.md` v32.
- `docs/implementation-plans/` (the plan and its index row).
- Non-goals, unchanged: `index.html`, `sitemap.xml`, `robots.txt`, the registry, cards, groups, the hero link, and the source repository.

## Decisions

- **The page and its behaviour come from the source.** The snapshot carries the source's style, both scripts and the switch markup, so the landing page cannot drift
  from the source's behaviour. Only the top-bar layout is landing-specific (`EXTRA_CSS`).
- **A committed, tested refresh script**, replacing LAND-13's scratch one, so the procedure is findable and its guards are tested (missing or misordered markers,
  missing script, style or switch, bad SHA, bad item, bad timestamp).
- **No double wrapping.** The previous landing generator wrapped every table; the source now does, so the landing wrapping was removed. A test asserts the number of
  `<table>` equals the number of `table-scroll` wrappers.
- **The maintenance-guide link becomes plain text** (the guide is in the private repository), by extending `public_link()` to relative `.html` names; every other
  unknown relative form still fails closed.
- **The switch is at the top right**, as the owner specified and like the Markdown Renderer and the in-depth index.
- **Inline scripts on a previously script-free page** are the approved decision under LC-V1; the page follows the system colours and shows no dead control when JavaScript is off.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| Snapshot refresh | PASS | `refresh_learning_paths_snapshot.py --source ../portfolio-docs/PORTFOLIO_LEARNING_PATHS.html --commit 6fe8133… --item LAND-14` wrote commit `6fe8133`, `LAND-14`, `2026-10-07T17:54Z`; `--check` then reported 'the snapshot matches the source page' |
| `python tools/generate_learning_paths.py --check` and `python tools/generate_site.py --check` | PASS | 'learning-paths generation: PASS'; 'generate-site: PASS' |
| `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts --skip-external` | 73 of 74 tests pass; sources PASS | 'sources PASS — 15 showcase, 2 methodology, 66 named controls, 7 internal references, 61 external URLs, 20 contrast pairs': the same counts as LAND-13. 57 existing tests plus 17 new (8 for the page, 9 for the refresh script). The one failure, `test_all_registered_showcase_projects_present`, is the known local review-index failure (`credit-dashboard-sut` is missing from the sibling `portfolio-reviews/README.md`; CI skips the test) and is identical before and after |
| Page content | PASS | 8 tables and 8 `table-scroll` wrappers; 2 `<script>` blocks; 'Public snapshot' row present once; no `href` to the private repository or to a `PORTFOLIO_` file |
| Real Chromium (Playwright 1.61.1), `file://` | PASS, 13 of 13 | System light and system dark colours by default (dark `rgb(15, 23, 32)`, links `rgb(138, 184, 232)`); back link left and switch right on one row, 24 px from the column edge; the metadata block shows Version, Created, Last updated, Evidence cut-off, Source revision and Public snapshot; click flips and saves the choice; the choice persists across a reload while the system is dark; first Tab stop is the back link, second is the switch with a 3 px focus ring; Enter and Space both toggle; with JavaScript off the page follows the system (dark) and the switch stays hidden; at 375 px in both themes there is no horizontal overflow, 8 wrapped tables, and the back link and switch sit on one row without overlap |
| `index.html`, `sitemap.xml`, `robots.txt` | Unchanged | `git status` lists neither |
| `verify_portfolio.py` without `--skip-external`; remote CI on the pull request | Not run here | CI is the evidence for external URLs; recorded in the closure log |

Durations were not captured.

## Failures and recovery

- A shell command containing two long heredocs failed to parse before any of it ran (exit 2); the test files were then written with the file tool and applied with
  short commands. No partial state resulted.
- An edit to `README.md` left it in a state git no longer recognised as text, so the diff showed every line changed. The file was restored from `HEAD` and the one
  addition redone in the file's own CRLF working-copy endings; the diff is now two lines.
- My first browser run had one failing check of my own making: it compared the metadata labels in mixed case, but the CSS uppercases them. The comparison was corrected
  to use the text content; the page was right.

## Durable lessons

- Rebuilding a snapshot from markers the source emits is safer than rebuilding it by position. The extraction now fails loudly when a marker, script, style or the
  switch is missing, instead of silently dropping behaviour.
- When two generators both wrap the same elements, remove the duplicate and test for it; here a count of tables against wrappers does it.
- Check line endings after any scripted edit of an existing file (`git diff --stat` should show only the lines you meant to change).

## Backlog reconciliation

- Ticked, with evidence above: the refresh script and its guards, the page's version, snapshot row, switch and wrapping, the three gates with the same counts, and the real-browser
  checks.
- Left open: the pull request's quality run, the owner merge, and the Pages deployment and live-page check. LAND-14 stays IN PROGRESS until a closure log records them.
- No follow-up items were created. The `portfolio-reviews` index gap is reported to the owner separately.
