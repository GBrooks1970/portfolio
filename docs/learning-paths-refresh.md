# Refreshing the Learning Paths snapshot

The public page `learning-paths.html` is a **pinned snapshot** of a generated page in the private repository `GBrooks1970/test-automation-portfolio`
(`portfolio-docs/PORTFOLIO_LEARNING_PATHS.html`). That repository is private, so CI here cannot read it: nothing detects that the snapshot has gone stale.
**Every merged edit to the source document makes this page stale.** This is the landing-side procedure for refreshing it. The source-side procedure (editing
the document, its frontmatter, building and checking its HTML) is in that repository's `portfolio-docs/PORTFOLIO_LEARNING_PATHS_MAINTENANCE.md`.

Backlog history: LAND-12 (publication), LAND-13 (a refresh), LAND-14 (versioned, dual-theme page and this runbook) in [`backlog.md`](backlog.md).

## What is stored where

| File | Role |
| --- | --- |
| `data/learning-paths.json` (`schemaVersion` 2) | The snapshot: `source` (repository, path, the document's last-change `commit`), `snapshot` (`refreshed` UTC time and the backlog `item`), and the extracted `title`, `style`, `scripts` (`prePaint`, `toggle`), `topbarButton` and `html` |
| `tools/refresh_learning_paths_snapshot.py` | Rewrites the snapshot from the source page. Guards: both `doc:` markers exactly once and in order, the style, one script in the head and one after it, the switch (`id="theme-toggle"`); a full 40-character SHA; an item like `LAND-14`; a timestamp like `2026-10-07T18:00Z` |
| `tools/generate_learning_paths.py` | Renders `learning-paths.html` from the snapshot: the top bar (back link left, the house light/dark switch right), a 'Public snapshot' row in the metadata block, private links as plain text, and no wrapping of its own (the source already wraps tables) |
| `learning-paths.html` | Generated. Never edit by hand |

## Procedure

1. **Check what changed.** In the source repository, `git fetch` and `git log <snapshot commit>..origin/main -- portfolio-docs/PORTFOLIO_LEARNING_PATHS.md portfolio-docs/PORTFOLIO_LEARNING_PATHS.html`.
   The snapshot commit is `source.commit` in `data/learning-paths.json`. If nothing changed, stop. If the new version adds or removes a link, expect the pinned counts in
   `tools/tests/test_site_quality.py` to need a deliberate update.
2. **Check the source page is current.** In the source repository, `cd portfolio-docs/tools && node build-docs-html.mjs ../PORTFOLIO_LEARNING_PATHS.md --check`.
3. **Branch and plan first.** In this repository: branch from `origin/main` (`chore/land-<n>-…`), write the plan in `docs/implementation-plans/` (copy the shape of the latest
   one), add its index row, and commit it before anything else. Landing rules: every change, including documentation-only, goes through a branch and a pull request, and
   the owner approves the plan and merges.
4. **Backlog item.** Add the next `LAND-<n>` to `backlog.md` (bump its version) as IN PROGRESS, with acceptance criteria and a link to this runbook.
5. **Refresh the snapshot.** The source's last-change commit is `git log -1 --format=%H -- portfolio-docs/PORTFOLIO_LEARNING_PATHS.md` in the source repository.
   ```
   python tools/refresh_learning_paths_snapshot.py --source <path to PORTFOLIO_LEARNING_PATHS.html> --commit <that SHA> --item LAND-<n>
   python tools/refresh_learning_paths_snapshot.py --source <path to PORTFOLIO_LEARNING_PATHS.html> --check
   python tools/generate_learning_paths.py
   ```
   On the Windows authoring machine use `python`; `python3` there is the Microsoft Store stub and fails. `--refreshed` defaults to the current UTC time.
6. **Gates.**
   ```
   python tools/generate_learning_paths.py --check
   python tools/generate_site.py --check
   python tools/verify_portfolio.py --registry-repository ../portfolio-prompts --skip-external
   ```
   Expect `sources PASS` with the same counts as before (15 showcase, 2 methodology, 66 named controls, 7 internal references, 61 external URLs, 20 contrast pairs). Locally one
   test, `test_all_registered_showcase_projects_present`, fails when a showcase project is missing from the sibling `portfolio-reviews/README.md`; it is skipped in CI, where
   that folder is absent, and is not caused by a refresh. `index.html`, `sitemap.xml` and `robots.txt` must not change.
7. **Look at it.** Open the page in a real browser at 1280 px and 375 px, in the light and the dark theme: no horizontal overflow, the switch at the top right beside
   'Back to portfolio', every table in a scroll region, the 'Public snapshot' row showing the new commit. Check the switch by keyboard and with JavaScript off (the page
   follows the system colours and the button stays hidden).
8. **Implementation log and pull request.** Write `docs/implementation-logs/<date>_land-<n>_<slug>.md` with the evidence, commit, push, and open the pull request. Not merged: the owner merges.
   The external-URL check in CI can fail on a transient 5xx from GitHub; re-run it before treating it as a regression.
9. **After the merge (the closure).** Confirm the exact-merge quality run and the Pages run (`pages build and deployment`) succeeded on the merge commit; fetch the live page
   (a 404 shortly after a merge can mean the deployment is still running), compare its SHA-256 with `learning-paths.html` at `origin/main` after normalising line endings, check
   that it shows the new version and snapshot row and not the old wording, and check that the live `index.html` still links to it. Then open the closure pull request: mark the
   backlog item DONE with the evidence, add a `…_publication-closure.md` log, and append the plan's Outcome.

## Limits

- Staleness cannot be detected here. The only safeguards are this runbook, the source repository's maintenance guide, and the backlog entries.
- The page and its scripts come from the source page; to change the look of the page, change the source generator (`portfolio-docs/tools/` there) and refresh, rather than patching
  this repository's `learning-paths.html`. Only the top-bar layout (`EXTRA_CSS` in `generate_learning_paths.py`) is landing-specific.
- The site has otherwise no JavaScript. The two inline scripts on this page are the house theme switch; they do nothing when JavaScript is off, and the page then follows the system colours.
