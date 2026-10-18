# Implementation Log — LAND-16: Publication closure

**Date:** 2026-10-18
**Backlog item:** LAND-16
**Repository:** `GBrooks1970/portfolio`
**Implementation PR:** [#74](https://github.com/GBrooks1970/portfolio/pull/74)
**Implementation head:** `2fdea1502a587bce8f0923881b3cc12d55a757eb`
**Merged revision:** `b8a2350b04de2b7d770b142845e9e36bb9bfe924`
**Closure branch:** `codex/land-16-publication-closure`

## Outcome

The Saleor card is published with its delivered capabilities, static Serenity report and CI actions. LAND-16 is DONE. This immutable record supplements the [pre-publication log](2026-10-18_land-16_saleor-report-links.md), whose pending statements describe that earlier capture.

## Captured verification

| Check | Result and evidence |
|---|---|
| Full local portfolio gate | Passed with 74 tests (1.575 seconds), no skips and external links enabled; see pre-publication log |
| PR quality | [39139132234](https://github.com/GBrooks1970/portfolio/actions/runs/39139132234), success at implementation head |
| Exact-merge quality | [39139175731](https://github.com/GBrooks1970/portfolio/actions/runs/39139175731), completed/success at merged revision |
| Exact-merge Pages | [39139175222](https://github.com/GBrooks1970/portfolio/actions/runs/39139175222), completed/success at merged revision |
| Live HTTP/content | Public landing page returned HTTP 200 at `2026-10-18T22:30:05.054368+00:00`; 36,676 bytes after CRLF-to-LF normalisation, equal to local merged `index.html` |
| Live SHA-256 | `6e050d3dc6be584fce755232b9eb3ac3b41557d41b625a239cd17b4e84f4bb4d` |
| Live browser | Saleor summary, five technology tags, report action, documentation action and `ci.yml` workflow link present |
| Live report navigation | Clicking Serenity reports reached the Saleor living-documentation page: 9 full API scenarios and 3 smoke scenarios, revision `abd506e38c0c3f1f7c56d0e17155545d1959069a`, explicit deterministic mock-SUT boundary |

The smoke suite is a subset, so the scenario counts are not additive. Desktop/mobile, overflow, keyboard and console checks are preserved in the implementation log. Live checks establish publication and navigation, not separate live-SUT acceptance or actual failure-notification delivery.

## Closure scope and validation

This documentation batch updates the backlog, plan outcome and plan index, and adds this record. It changes no generated output. Before publication, validate whitespace and local Markdown links; the documentation PR also runs the repository quality workflow. Verify its exact-main runs after merge without rewriting this immutable evidence record.

## Failures and remaining scope

No publication failure was observed. Saleor dependency maintenance remains tracked in its owning project. The older bfx landing PR #46 is outside this Saleor batch. Historical review and Learning Paths snapshots retain their original provenance.
