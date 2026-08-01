# Implementation Log — LAND-05: Publication Quality Gate

**Date:** 2026-08-01
**Backlog item:** `LAND-05`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `codex/land-05-quality-gate`
**Commit:** `90a334b006a93e5703ba16cf3381af2f0569b15b`
**Pull request:** https://github.com/GBrooks1970/portfolio/pull/11
**Pages run:** Pending — a public colour token changed; owner merge, `main` quality, Pages and live
verification remain required

## Outcome

The portfolio now has one reproducible quality command for local development and pull-request CI.
It composes canonical registry parity with HTML structure, metadata, internal-reference, selected
accessibility, live external-target and deterministic-test checks. The complete run passed all 33
unique public HTTPS targets, 16 light/dark contrast pairs and 20 tests at the implementation head.

The first full run also found a real dark-theme defect: white text on the primary blue action had a
2.96:1 contrast ratio. The dark theme now uses `#0f151b` action text for a 6.20:1 ratio while the
public copy and layout remain unchanged. Draft PR #11 passed its exact-head read-only quality job.

## Scope

- `.github/workflows/registry-parity.yml` — extends the existing least-privilege parity workflow
  into the complete `portfolio-quality` pull-request/`main` job.
- `tools/check_site.py` — validates document structure, metadata, internal references, accessible
  names/focusability, declared theme contrast and external HTTPS targets with bounded retries.
- `tools/verify_portfolio.py` — exposes the single local/CI command and runs parity, site quality
  and all deterministic tests.
- `tools/tests/test_site_quality.py` — adds 10 focused quality-gate tests; the complete suite is now
  20 tests.
- `index.template.html` and generated `index.html` — correct the dark primary-action text token;
  public copy and layout geometry are unchanged.
- `README.md`, `docs/quality-gate.md`, `docs/project-contract.md` and
  `docs/decisions/002-publication-quality-gate.md` — document the command, policy, source/deployment
  boundary and durable decision.
- `docs/backlog.md` — reconciles LAND-04 closure and LAND-05 implementation evidence.
- Explicit non-goals: LAND-06 retains skip navigation, heading hierarchy, explicit focus styling,
  touch targets, project-specific CI labels and responsive layout contracts.

## Decisions

- Compose the earlier registry-parity control instead of creating independent commands that could
  drift or be selectively omitted.
- Use Python's standard-library HTML parser and HTTP client for the site layer, preserving the
  dependency-light repository while keeping tests deterministic through injected request behaviour.
- Check every unique public `href` and `src`; retry only explicitly transient status/network classes
  and fail after three bounded attempts rather than weakening evidence links.
- Treat the 4.5:1 text contrast threshold as a targeted automated baseline, not a full accessibility
  claim. Browser/keyboard checks remain required where the project contract assigns them.
- Keep Pages and unauthenticated live verification independent from pull-request quality.

The durable rationale and rejected alternatives are recorded in
[decision 002](../decisions/002-publication-quality-gate.md).

## Validation

| Gate | Result | Evidence |
|---|---|---|
| Complete local command | PASS | 9 showcase, 1 methodology, 34 named controls, 1 internal reference, 33 external targets and 16 contrast pairs |
| Python unit suite | PASS | 20/20 tests, including 10 LAND-05 site-quality cases |
| Python compilation | PASS | `python -m compileall -q tools` |
| External targets | PASS | 33/33 unique HTTPS `href`/`src` targets returned HTTP 200–399 |
| Theme contrast | PASS | 16/16 declared text pairs at or above 4.5:1; corrected dark primary action is 6.20:1 |
| Workflow security | PASS | `contents: read`; ordinary `pull_request`; no secrets; two non-persisted checkouts; three full-SHA action pins |
| Desktop browser | PASS | 1280 × 720 dark mode: 9 cards, 3 columns, 34 named/focusable links, no duplicate IDs, overflow or console errors |
| Markdown links / whitespace | PASS | Repository-relative documentation links resolve; `git diff --check` clean |
| Pull-request CI | PASS | Run 30717568452 completed `portfolio-quality` in 12 seconds at exact head `90a334b` |
| Owner merge / `main` / Pages / live | PENDING | Draft PR #11 remains for owner review |

## Failures and recovery

- The initial static-document test expected the 24 anchor-only targets used before LAND-05. The
  complete gate correctly discovered 33 unique `href` and `src` targets after badges were included;
  the assertion was corrected to the complete public surface.
- The first contrast run measured only 2.96:1 for the dark primary action's white-on-blue pair. A
  theme-specific `--accent-ink: #0f151b` token raised it to 6.20:1, and the generated output and all
  16 pair checks then passed.
- Port 8000 was already serving an older isolated worktree during browser review. The LAND-05
  worktree was served on fresh ports, its DOM/source token was confirmed and the final console log
  was empty; the unrelated server was left untouched.
- The in-app browser could not embed the local page in a mobile-width frame. No mobile result is
  claimed for this branch. LAND-05 changed only a dark text colour token, leaving the LAND-03 layout
  geometry intact; fresh 390px validation remains explicitly assigned to LAND-06.

## Durable lessons

- Link coverage must include image/badge sources as well as anchors or the public evidence surface
  is understated.
- A declared palette is useful only when the actual foreground/background roles are enumerated and
  tested in every supported theme.
- Network retry policy should be narrow, bounded and visible: it can distinguish a temporary outage
  without converting an unavailable evidence link into a false pass.
- Local browser evidence must identify the served worktree; a successful localhost response alone
  does not prove the intended branch is under review.
- Static accessibility automation and rendered keyboard/responsive review are complementary gates,
  not substitutes.

## Backlog reconciliation

- All six LAND-05 implementation criteria are checked with local and exact-head pull-request
  evidence.
- LAND-05 remains IN REVIEW until the owner merges PR #11 and exact-merge `main` quality, Pages and
  unauthenticated live checks pass.
- LAND-06's light/dark contrast criterion is pre-delivered by LAND-05. Its navigation, focus,
  touch-target, label and responsive acceptance criteria remain READY and out of this PR.
