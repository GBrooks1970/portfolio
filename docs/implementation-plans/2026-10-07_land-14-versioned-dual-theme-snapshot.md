---
version: 1
created: 2026-10-07T17:53Z
project: portfolio-landing
type: implementation-plan
item: LAND-14
status: implemented
approved: 2026-10-07, Gary Brooks (plan LC-V1, "agreed as recommended", with the switch at the top right); the owner merges
delivered: PR #63, merge commit 9537d83, merged 2026-10-07T18:00:56Z by the owner
language: en-GB
---

# Implementation plan: LAND-14 Publish the versioned, dual-theme Learning Paths page

**Goal.** The public `learning-paths.html` shows the version and snapshot it is, carries the house light/dark switch at the top right, and is rebuilt
from the source repository's new generated page by a committed script instead of a scratch one. This is part B of the owner-approved plan LC-V1
(`docs/implementation-plans/2026-10-07_lc-v1-versioned-dual-theme-learning-paths.md` in `GBrooks1970/test-automation-portfolio`); part A (that repository's
frontmatter, generator, dark theme and maintenance guide) merged as #297, and the document's last-change commit is `6fe8133fea6a59accba608dfe77431f8f708b5bd`
(version 10).

## Evidence gathered before planning

Read-only checks on 2026-10-07. Nothing in this repository was changed.

| Finding | Consequence for the plan |
|---|---|
| The source page now has YAML-derived metadata (a `.doc-meta` block under the title), a dark palette in `<style>`, a pre-paint theme script in `<head>`, a `<header class="topbar">` with the 🌓 switch, a toggle script at the end of `<body>`, and `<!-- doc:begin -->` and `<!-- doc:end -->` markers around the document content. Tables are already wrapped in `.table-scroll` regions. | The snapshot takes the content between the markers, plus the style, the two scripts and the switch markup from the same source, so the landing page cannot drift from the source's behaviour. |
| `tools/generate_learning_paths.py` wraps `<table>` itself and has its own `.table-scroll` CSS and its own light-only `extra` rules. | Remove its table wrapping and duplicate CSS, or every table would be wrapped twice. Keep a landing override so the switch sits at the top right beside the back link. |
| `public_link()` raises on a relative `.html` link. The source's metadata block links to its maintenance guide, `PORTFOLIO_LEARNING_PATHS_MAINTENANCE.html`, which is in the private repository. | A bare relative `.html` name becomes plain text, as private `.md` names already do; every other unknown form still fails closed. |
| Only `generate_learning_paths.py`, `tools/tests/test_generate_learning_paths.py` (4 tests) and one call in `verify_portfolio.py` touch this page. No landing test forbids an inline script; the page and the site have no JavaScript today except one JSON-LD block in `index.html`. | The change is contained. The inline scripts are the owner-approved decision (the house switch needs them), with system colours when JavaScript is off. |
| The existing test requires `<a href="index.html">Back to portfolio</a>` verbatim. | Keep that link text and markup. |
| LAND-13's snapshot rewrite used a scratch script that was not committed. | Commit `tools/refresh_learning_paths_snapshot.py` with tests, and a runbook `docs/learning-paths-refresh.md`, so the procedure is findable. |
| `python3` on the authoring machine is the Microsoft Store stub; `python` is 3.13.1. The working copies are CRLF and the index LF. | Use `python` in the runbook's Windows notes; write the JSON with LF and let git normalise. |

## Design

1. **Snapshot** (`data/learning-paths.json`, `schemaVersion` 2): `source` (repository, path, `commit` = the document's last-change commit, note), a new `snapshot`
   object (`refreshed` UTC timestamp, `item` = the backlog item), `title`, `style`, `scripts` (`prePaint`, `toggle`), `topbarButton` (the switch markup), and
   `html` (the content between the markers).
2. **Page** (`learning-paths.html`, generated): a top bar with the 'Back to portfolio' link on the left and the switch on the right; the source's metadata block
   with one extra row, 'Public snapshot', saying which document commit this is pinned from and when and under which item it was refreshed; the pre-paint script
   in `<head>` and the toggle script at the end; private links as plain text, as before.
3. **Refresh script** `tools/refresh_learning_paths_snapshot.py --source <generated .html> --commit <sha> --item <LAND-N>` rewrites the snapshot from the source page. It
   fails if a marker, script, style or the switch is missing, if the commit is not a full 40-character SHA, or if the item is not `LAND-<n>`. `--check` re-derives
   the extractable fields from a source and compares them with the committed snapshot.
4. **Runbook** `docs/learning-paths-refresh.md`: the landing-side procedure, linked from the LAND-12, LAND-13 and LAND-14 backlog entries, `README.md` and the
   generator's docstring.

## Steps

0. Fetch; confirm #297 merged and the document's last-change commit; confirm this repository's `main` is current and the unrelated open PR #46 is left alone.
1. Branch `chore/land-14-versioned-dual-theme-snapshot` from `origin/main`. Commit this plan, its index row and nothing else first.
2. `docs/backlog.md` (v32): add LAND-14 (P1, IN PROGRESS), its table row and the status line; link the runbook from the LAND-12 and LAND-13 entries.
3. Code: `tools/generate_learning_paths.py` (new snapshot shape, top bar, scripts, snapshot row, no table wrapping, `.html` private-link rule);
   `tools/refresh_learning_paths_snapshot.py`; tests for both (the 4 existing tests updated, new ones added).
4. Refresh the snapshot from the merged source with the committed script (`--commit 6fe8133fea6a59accba608dfe77431f8f708b5bd --item LAND-14`), regenerate the page.
5. Gates: `generate_learning_paths.py --check`, `generate_site.py --check`, and `verify_portfolio.py --registry-repository ../portfolio-prompts --skip-external`
   (expect the same counts as LAND-13: 15 showcase, 2 methodology, 66 named controls, 7 internal references, 61 external URLs, 20 contrast pairs; locally
   56 of the 57 existing tests plus the new ones, with the one known local review-index failure).
6. Real Chromium (Playwright from `markdown-renderer`): light and dark by system setting, no `data-theme` until used, the switch at the top right beside the back
   link, click and persistence, Tab, Enter and Space, JavaScript off (system colours, no dead control), no horizontal overflow at 1280 px and 375 px in both themes,
   8 tables in 8 scroll regions (not 16), the snapshot row visible, nothing private linked.
7. Write the runbook and `docs/implementation-logs/2026-10-07_land-14_versioned-dual-theme-snapshot.md`; commit, push, open a pull request. Not merged.
8. After the owner merges (part C): exact-merge quality run and Pages run; live `learning-paths.html` status, SHA-256 against `origin/main` (line endings
   normalised) and content (the version and snapshot block, the switch, the old wording absent); close LAND-14 with a publication-closure log and this plan's Outcome.

## Verification

- The committed page equals what the generator renders from the committed snapshot (`--check`), and the snapshot equals what the refresh script extracts from the source.
- The refresh script and the generator tests pass, including a failing case for each guard (missing marker, bad SHA, unknown link form).
- The real-browser checks above pass in both themes; the live page after the merge matches `origin/main` by hash and shows the new content.
- `index.html`, `sitemap.xml` and `robots.txt` are unchanged.

## Delivery

One pull request for part B on the branch above; the owner merges. Part C is a second pull request after Pages is confirmed. No change to the source repository.

**Out of scope:** the registry, cards, groups, the hero link, `index.html`, `sitemap.xml`, `robots.txt`, the source repository, other landing pages, and the unrelated
open pull request #46.

## Decisions put to the owner

| Decision | Options | Recommended | Owner's answer |
|---|---|---|---|
| Switch position, version scheme, inline script, persistence, build tool, procedure location, who does it | Set by LC-V1 | As recommended in LC-V1; the switch at the top right | Approved 2026-10-07 under LC-V1 |
| Commit the snapshot refresh script, rather than keep a scratch one | A committed script with tests; or a scratch script as in LAND-13 | A committed script: the procedure must be findable and testable | Within LC-V1's 'procedure in findable places'; no separate decision needed |

## Outcome

Delivered as planned. [PR #63](https://github.com/GBrooks1970/portfolio/pull/63) (two commits: `4a7e448` the plan, `6c234a9` the change) was merged by the owner as `9537d83e0ed962ea3dde2d103f75a541cbd571ed` on 2026-10-07 at 18:00:56Z. The logs are
[`docs/implementation-logs/2026-10-07_land-14_versioned-dual-theme-snapshot.md`](../implementation-logs/2026-10-07_land-14_versioned-dual-theme-snapshot.md) and
[`2026-10-07_land-14_publication-closure.md`](../implementation-logs/2026-10-07_land-14_publication-closure.md).

- **Change:** the snapshot (`schemaVersion` 2) is rebuilt by the committed `tools/refresh_learning_paths_snapshot.py` from the source's generated page (document commit `6fe8133fea6a59accba608dfe77431f8f708b5bd`, version 10); the generator renders the top bar with the switch at the top right, the two scripts, a 'Public snapshot' row and no table wrapping of its own. `index.html`, `sitemap.xml` and `robots.txt` did not change.
- **Verification, as planned:** the generator and site checks passed; `verify_portfolio.py --skip-external` gave the same counts as LAND-13 with 74 tests (the one failure is the known local review-index test that CI skips); real Chromium passed 13 of 13 checks locally in both themes. PR quality run `37663223836` and exact-merge run `37663545958` passed; the Pages run `37663545393` on the merge commit succeeded.
- **The check that would have failed if the change had not published:** the live `learning-paths.html` returned HTTP 200, its SHA-256 equals `origin/main` after line-ending normalisation (`b715457b…a4ca6`), it carries the version and 'Public snapshot' rows and the switch, and the same 13 real-browser checks pass against the live URL. The live `index.html` equals `origin/main` and is byte-identical to its pre-change hash.
- **Differences from the plan:** none in design or scope. One addition: the closure also ran the browser suite against the live URL, not only the hash and content checks.
- **Not done, as stated in the plan:** the registry, cards, groups, the hero link, and the unrelated open pull request #46; the `portfolio-reviews` index gap (a content gap in `test-automation-portfolio`).
