# Implementation Log — LAND-17: Publication closure

**Date:** 2026-10-18
**Backlog item:** LAND-17
**Repository:** `GBrooks1970/portfolio`
**Implementation PR:** [#46](https://github.com/GBrooks1970/portfolio/pull/46)
**Refreshed head:** `95bf9fe26737d41ab2c3de5a07a9b889f9d5e871`
**Merge:** `61af8cb4f28454860e87ee2c4dd5a58e55f1a810`
**Closure branch:** `codex/land-17-publication-closure`

## Outcome

The live BFX card now links its Interactive Kanban board. LAND-17 is DONE. This record supplements the immutable [implementation log](2026-10-18_land-17_bfx-kanban-refresh.md), preserving its pre-publication capture.

## Captured verification

| Check | Evidence |
|---|---|
| Full local gate | 74 tests passed in 1.425 seconds, no skips, external links enabled; desktop/mobile, keyboard and board interaction evidence is in the implementation log |
| Refreshed PR CI | [39173104533](https://github.com/GBrooks1970/portfolio/actions/runs/39173104533), success, quality job 13 seconds |
| Exact-merge quality | [39173135247](https://github.com/GBrooks1970/portfolio/actions/runs/39173135247), success at merge above, quality job 13 seconds |
| Exact-merge Pages | [39173135151](https://github.com/GBrooks1970/portfolio/actions/runs/39173135151), success at merge above; build 22 seconds, deploy 8 seconds |
| Public content | HTTP 200 at `2026-10-18T22:39:42.476777+00:00`; 36,791 bytes after CRLF-to-LF normalisation; equal to merged `index.html` |
| Live SHA-256 | `39b1693a88730b104d206b44b4a976b8aaf772948e929eba4c138ee631103bad` |
| Live navigation | After browser refresh, the BFX card shows Interactive Kanban board; clicking it opens the correct published board with 21 tickets, 2 backlog and 19 done |

## Decisions, failures and recovery

The first browser navigation reused cached pre-deployment HTML. An explicit reload displayed the deployed action, consistent with the unauthenticated byte comparison. No deployment failure occurred. Existing GitHub-managed Pages action/runtime annotations did not prevent successful deployment.

The board is a dated published snapshot, and the independent BFX CI badge was failing during implementation verification. This publication establishes link availability and functionality only; it changes no BFX code or CI behaviour.

## Closure scope and validation

Update the backlog, plan outcome and plan index, and add this immutable record. Generated output remains unchanged. Validate whitespace and relative Markdown links before committing; verify closure PR CI and exact-main quality/Pages after merge. Retain this capture unchanged rather than recursively rewriting publication history.

## Durable lesson

For older presentation PRs, refresh source-derived counts and negative fixtures against current main, then distinguish successful deployment from browser-cache freshness and target-project health.
