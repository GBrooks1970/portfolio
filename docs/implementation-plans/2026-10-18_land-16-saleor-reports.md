---
version: 1
created: 2026-10-18
project: portfolio-landing
type: implementation-plan
item: LAND-16
status: approved
approved: Owner requested merge PRs and update the landing page for the completed Saleor work on 2026-10-18
delivered: pending publication
language: en-GB
---

# LAND-16 — Publish current Saleor capabilities and report links

## Goal and evidence

The Saleor card has no CI or report action and describes only the earlier foundation. Saleor delivery is complete through project PR #23 (`abd506e38c0c3f1f7c56d0e17155545d1959069a`), with exact-main CI `39138528906`, published Serenity reports and scheduled schema-monitor evidence. Dependency maintenance remains tracked and actual failure-alert delivery is untested.

## Steps

1. Update only the Saleor entry in `data/presentation.json`: describe catalogue, authentication, checkout, staff fulfilment, reports and daily upstream schema checking; preserve the deterministic/live-SUT distinction; add `ci.yml` and a static report action to the published Serenity landing page.
2. Regenerate `index.html` using `tools/generate_site.py`. Retain registry membership, layout, historical review and Learning Paths snapshots.
3. Adjust existing inventory/link-count expectations and the deliberate wrong-count parity fixture for the new report and CI actions. Keep the negative parity test effective.
4. Run the complete portfolio gate with the canonical registry checkout, inspect desktop and 390px mobile presentation, check overflow, console errors and keyboard report navigation, then record implementation evidence.
5. Publish through a PR under the owner's merge instruction. Verify quality and Pages on the exact merge and inspect the live card/report link. Add an immutable publication-closure log and close the backlog item through a documentation PR.

## Scope and authority

This is Saleor presentation work in the landing repository. The owner approved updating the landing page following Saleor completion. The unrelated pre-existing bfx PR #46 is outside this batch. No registry fields, target-project code, baseline or notification settings change.

## Verification

Run `python tools/verify_portfolio.py --registry-repository ../portfolio-prompts`, including external links and the existing injected wrong-count test (which must still reject the altered count). Generated outputs must be byte-stable. Desktop/mobile checks must show usable actions and no horizontal overflow. A report is a static evidence action, not a live application demo.

## Delivery

Branch: `codex/land-16-saleor-reports`. Use exact-path staging. Keep initial implementation and post-deployment closure evidence separate, preserving history.
