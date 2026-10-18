---
version: 1
created: 2026-10-18
project: portfolio-landing
type: implementation-plan
item: LAND-17
status: approved
approved: Owner approved updating PR 46, verification, merge and deployment on 2026-10-18
delivered: pending
language: en-GB
---

# LAND-17 — Refresh and publish the BFX Kanban link

## Goal and evidence

Resume existing [PR #46](https://github.com/GBrooks1970/portfolio/pull/46) to add the Interactive Kanban board action to the BFX showcase card. Its head `5e789004b9e7a4a7154db1da0c93239c0b05f8f8` conflicts with current main `3fa9109e4e7c95ee0955815890ef96e54e256fa9`; September test evidence and count baselines need refreshing.

Read-only checks found the public board returns HTTP 200 and matches the board file at BFX main `b90dba4b71eea34bd18ecad9821721e3c168ad1c` after newline normalisation (20,668 bytes; SHA-256 `1106209cb070756c0ce980c36e9a3bafc745c2c751239a06edb9d30469ab6f81`). The BFX repository remains read-only in this task.

## Steps

1. Merge current main into the existing PR branch, preserving history. Resolve stale generated content and count baselines against current main, retaining the single BFX action in `data/presentation.json`.
2. Regenerate `index.html`; adjust existing count assertions in `test_generate_site.py`, `test_registry_parity.py` and `test_site_quality.py`. Preserve the injected mismatch test as an effective negative check.
3. Add LAND-17 to `docs/backlog.md` and this plan to its index. Run the complete portfolio gate with the canonical registry checkout and external links enabled.
4. Inspect the card at desktop and 390px mobile widths, keyboard order/focus, overflow and console. Follow its link and exercise board filtering, search and ticket details.
5. Add an immutable implementation log, refresh the existing PR description and push normally. Merge after current PR CI passes; verify exact-main quality, Pages and live output.
6. Record deployment evidence and close LAND-17 through a documentation PR, also verifying its CI and exact-main deployment.

## Verification

Run `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts`. The intentional wrong-evidence-count fixture must still be rejected. Check changed Markdown links and whitespace. Live generated HTML must match committed output after newline normalisation; board navigation must reach its stated destination.

## Delivery and owner decision

Continue `feat/link-bfx-kanban-board` and PR #46 without rewriting history. Owner's “continue as recommended” authorises refresh, verification and merge. Preserve all recent Saleor and other landing changes. No BFX code, board content, registry or notification changes are included.
