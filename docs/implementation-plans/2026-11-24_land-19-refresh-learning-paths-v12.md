---
version: 1
created: 2026-11-24T22:53Z
project: portfolio-landing
type: implementation-plan
item: LAND-19
status: approved
approved: 2026-11-24, Gary Brooks ("Approve as recommended", every recommended option below); the owner merges
language: en-GB
---

# Implementation plan: LAND-19 Refresh the Learning Paths snapshot to version 12

**Goal.** Make the public page `learning-paths.html` match the Learning Paths document as it stands at
`7fa013c470a2442d2a0c3c74ceb00db94ba1f823` in `GBrooks1970/test-automation-portfolio` (document version 12). The pinned snapshot (source
commit `437e27fb8c0ac00ff9191ba373eb13010593ec1c`, version 11, published by LAND-15) predates the `portfolio-docs` reorganisation
(`test-automation-portfolio` #380), which moved the outline into `portfolio-docs/reference-history/` and changed two links to it. The change
is a snapshot refresh, following [`docs/learning-paths-refresh.md`](../learning-paths-refresh.md), plus one narrow change to the generator,
which currently refuses the new link form.

## Evidence gathered before planning

Read-only checks on 2026-11-24. The dry runs below ran in scratch clones of this repository; nothing real was changed.

| Finding | Consequence for the plan |
|---|---|
| `data/learning-paths.json` pins source commit `437e27f…`, refreshed 2026-10-08T00:14Z by LAND-15. Since then the document has changed once: `7fa013c` (#380, version 11 to 12). Its diff is the frontmatter (`version`, `updated`), one path in a comment, and one link target, `PORTFOLIO_LEARNING_PATHS_OUTLINE_2026-10-06.md` to `reference-history/PORTFOLIO_LEARNING_PATHS_OUTLINE_2026-10-06.md`. `source-revision` is unchanged: the evidence was not re-checked. | That commit is the only content gap, and the visible text barely changes. |
| In the source repository at `6d4e817` (`origin/main`), `node build-docs-html.mjs ../PORTFOLIO_LEARNING_PATHS.md --check` passes (marked 18.1.0). | The source page is current. |
| `refresh_learning_paths_snapshot.py --check` before any change exits 1: 'the snapshot differs from the source in: html'. After `--commit 7fa013c… --item LAND-19` it exits 0. | The refresh script and its guards need no change. |
| `generate_learning_paths.py` then fails: `ValueError: Unsupported Learning Paths link: reference-history/PORTFOLIO_LEARNING_PATHS_OUTLINE_2026-10-06.md`. `public_link()` turns only bare file names (`[A-Za-z0-9_.-]+\.(md|html)`) into text and fails closed on anything else; its tests require `dir/file.md` and `dir/guide.html` to fail. | The generator needs a deliberate change (decision 3). Without it the refresh cannot be published. |
| With the recommended change (an optional `reference-history/` prefix, nothing else) and one new test, in an LF clone: the refresh `--check`, both `generate_*` checks and `verify_portfolio.py --registry-repository ../portfolio-prompts --skip-external` pass: `sources PASS` with 15 showcase, 2 methodology, 85 named controls, 22 internal references, 66 external URLs and 20 contrast pairs; 80 tests, OK (skipped=3). The baseline on `main` is the same counts and 79 tests. | The pinned counts in `tools/tests/test_site_quality.py` need no change. One test is added. |
| The dry-run diff is 4 lines of `learning-paths.html` (Version 11 to 12, the 'Last updated' time, the 'Public snapshot' row and the provenance commit), 4 lines of `data/learning-paths.json`, 1 line of the generator and 6 lines of tests. The page's `href` set stays `index.html` only, and the string `reference-history` does not appear in the page (the link becomes its label text, as before). | `index.html`, `sitemap.xml` and `robots.txt` do not change. Nothing private is exposed. |
| On the Windows checkout (`core.autocrlf=true`) the baseline gate fails: 'reviews.html is stale'. The committed files are LF; checked out as CRLF they no longer match byte for byte. In an LF clone the same commit passes, and CI on `main` (`Portfolio quality` run `42250320882`) is green. | Not caused by this change and out of scope. The work is done in a worktree with `core.autocrlf=false`, and the log records the cause. |

## Steps

0. Before starting: fetch both repositories; confirm the document is unchanged since `7fa013c` and the source page `--check` still passes. If it has changed again, stop and re-plan.
1. Branch `chore/land-19-refresh-learning-paths-v12` from `origin/main` (worktree with `core.autocrlf=false`). Commit this plan and its index row first.
2. `docs/backlog.md` (v43): add LAND-19 (priority per decision 1, IN PROGRESS), its table row, the status line and acceptance criteria, with a link to the runbook. DONE only in the closure pull request.
3. `tools/generate_learning_paths.py`: in `public_link()`, accept an optional `reference-history/` prefix on the bare-file-name form. Add a test that the outline path becomes text and that `reference-history/../secret.md`, `reference-history/sub/x.md`, `other-folder/x.md` and `/reference-history/x.md` still fail. The existing `dir/file.md` and `dir/guide.html` failures stay.
4. Refresh the snapshot: `python tools/refresh_learning_paths_snapshot.py --source <PORTFOLIO_LEARNING_PATHS.html> --commit 7fa013c470a2442d2a0c3c74ceb00db94ba1f823 --item LAND-19`, then `--check`, then `python tools/generate_learning_paths.py`.
5. Gates: `generate_learning_paths.py --check`, `generate_site.py --check`, `verify_portfolio.py --registry-repository ../portfolio-prompts --skip-external`. Expect the counts above, 80 tests, and no change to `index.html`, `sitemap.xml` or `robots.txt`.
6. Look at it in Chromium at 1280 px and 375 px in the light and dark themes: no horizontal overflow, the switch at the top right beside 'Back to portfolio', and the metadata block showing Version 12 and the 'Public snapshot' row with `7fa013c` and LAND-19.
7. Write `docs/implementation-logs/2026-11-24_land-19_learning-paths-refresh.md` with the evidence; commit; push; open a pull request. Not merged: the owner merges.
8. After the owner merges: confirm the exact-merge quality run and the Pages run succeeded; fetch the live page and compare its SHA-256 with `origin/main` after normalising line endings; check it shows Version 12, `7fa013c` and LAND-19 and not `437e27f` or LAND-15; check the live `index.html` still links to it. Then open the closure pull request: LAND-19 DONE with the evidence, a `…_publication-closure.md` log, and this plan's Outcome.

## Verification

- `refresh_learning_paths_snapshot.py --check` exits 1 before the refresh and 0 after it (shown in the dry run).
- The new generator test fails without the generator change: the unpatched generator raised the `ValueError` above on exactly that path.
- Both `generate_*` checks pass; `verify_portfolio` reports the same counts and 80 tests; `index.html`, `sitemap.xml` and `robots.txt` are unchanged.
- The pull request's quality run passes in CI (re-run the external-URL check once on a transient 5xx before treating it as a regression).
- The live page matches `origin/main` after merge and shows Version 12. This is the check that would fail if the refresh did not publish.

## Delivery

Branch `chore/land-19-refresh-learning-paths-v12`; pull request 1 carries the plan, the backlog item, the generator change and test, the snapshot, the regenerated page and the implementation log; the owner merges. Pull request 2 (after Pages is confirmed) closes LAND-19 and adds the Outcome.

**Out of scope:** the `reviews.html` CRLF mismatch on Windows checkouts (a `.gitattributes` `eol=lf` rule for every generated page would fix it; separate item if wanted), cards, the registry, the source document's content, and automating the refresh.

## Decisions put to the owner

| Decision | Options | Recommended | Owner's answer |
|---|---|---|---|
| Priority | P1 or P2 | P2: the public page is behind by metadata only; its content is the same as version 11 | As recommended, approved 2026-11-24 |
| `source.commit` | The document's last-change commit `7fa013c…`; or the repository head | The document's last-change commit, as for LAND-13 and LAND-15 | As recommended, approved 2026-11-24 |
| Generator link rule | (a) accept an optional `reference-history/` prefix only; (b) accept any one-folder relative `.md`/`.html` path; (c) no change, and refresh later | (a): it admits exactly the one form the document uses and keeps the fail-closed rule for every other folder; a future link into another folder fails loudly and is decided then | As recommended, approved 2026-11-24 |
| Pull requests | Two (change, then closure); or one | Two, as for LAND-11 to LAND-18 | As recommended, approved 2026-11-24 |
| Who does it | Directly; or a subagent | Directly: it is small and touches a public site | As recommended, approved 2026-11-24 |
