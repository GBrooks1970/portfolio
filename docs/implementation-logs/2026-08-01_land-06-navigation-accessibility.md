# Implementation Log — LAND-06: Navigation and Accessibility

**Date:** 2026-08-01
**Backlog item:** `LAND-06`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `codex/land-06-accessibility`
**Commit:** `c26dcf2794459c904d1fdf05feb778bcdd2dd89c`
**Pull request:** https://github.com/GBrooks1970/portfolio/pull/12
**Pages run:** Pending — public HTML/CSS changed; owner merge, exact-merge quality, Pages and live
verification remain required

## Outcome

The static portfolio now exposes a focusable skip link to a labelled showcase collection, a visible
section heading and a coherent H1/H2/H3 outline. Generated CI badge links and images identify their
projects, every project action has at least a 44px target, and light/dark themes expose explicit
high-contrast focus rings.

The complete local and pull-request gates pass with 35 named controls, two internal references, 33
external targets, 20 contrast pairs and 25 deterministic tests. Desktop rendering and the skip
target are verified. The available browser could not expose a 390px viewport, so that final
responsive criterion remains openly pending and PR #12 remains a draft.

## Scope

- `index.template.html` and generated `index.html` — add the skip link, labelled `main#projects`,
  visible showcase heading, H3 card titles, focus tokens/rings and 45px project-action targets.
- `tools/generate_site.py` — generate project-specific CI link names and badge alt text while
  retaining escaped manifest-owned titles.
- `tools/check_site.py` — enforce skip-target, visible-heading, heading-outline, CI-name,
  focus-style, minimum-target and focus-colour contrast contracts.
- `tools/tests/test_generate_site.py` and `tools/tests/test_site_quality.py` — add five LAND-06
  regression cases and generated-output assertions; the complete suite increases from 20 to 25.
- `README.md` and `docs/quality-gate.md` — document decision 002 and the expanded automated layer.
- `docs/implementation-logs/2026-08-01_land-05-merge-closure.md` — append LAND-05 merge,
  default-branch quality, Pages and live/source-parity closure evidence.
- `docs/backlog.md` — close LAND-05 and record the partially verified LAND-06 review state.
- Explicit non-goals: no public-copy, inventory, runtime-service or candidate LAND-C01–C04 work.

## Decisions

- Keep `main` as the project collection and make it the native fragment/focus target rather than
  introducing a second navigation wrapper.
- Insert one visible H2 before the generated cards and render each card title as H3. This preserves
  the methodology H2 as a peer section and avoids styling-only heading semantics.
- Apply project-specific names to both CI link and image because either may be exposed by assistive
  tooling; generic `CI` text is no longer accepted by the gate.
- Use light `#8a3000` and dark `#ffd166` focus tokens. Their surface contrast ranges from 7.95:1 to
  12.74:1, comfortably above the selected 4.5:1 text/focus baseline.
- Declare 45px action targets while validating a minimum of 44px. This absorbs fractional browser
  scaling without weakening the acceptance threshold.

These choices implement the explicit LAND-06 backlog contract within the static architecture
already accepted by decisions 001 and 002; no new structural ADR was required.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| Complete local command | PASS | 9 showcase, 1 methodology, 35 named controls, 2 internal references, 33 external targets and 20 contrast pairs |
| Python unit suite | PASS | 25/25 tests; five new LAND-06 regression cases plus generated-output assertions |
| Python compilation | PASS | `python -m compileall -q tools` |
| External targets | PASS | 33/33 unique HTTPS `href`/`src` targets returned HTTP 200–399 |
| Desktop browser | PASS | 1280 × 720 dark mode: 9 cards, 3 columns, no horizontal/action overflow or console errors |
| Action targets | PASS | 22/22 project actions rendered at 44.996px or greater |
| Heading / CI names | PASS | 1 H1, 2 H2s, 9 card H3s, 9 project-specific CI link/image pairs and no duplicate IDs |
| Skip/focus path | PARTIAL | First Tab exposed the skip link with a visible focus ring; activation moved focus to labelled `main#projects`, but direct Enter dispatch was not reliable in the available browser |
| 390px browser | PENDING | Browser exposes a fixed 1280 × 720 viewport; security policy rejected an embedded preview and no bypass was attempted |
| Markdown links / whitespace | PASS | All relative links across 21 Markdown files resolve; `git diff --check` clean |
| Pull-request CI | PASS | Run 30719723900 passed at exact implementation head `c26dcf2` |
| Owner merge / `main` / Pages / live | PENDING | Draft PR #12 remains for review |

## Failures and recovery

- CSS `min-height: 44px` computed correctly but the rendered browser rectangle measured 43.996px
  under fractional scaling. Raising the declaration to 45px produced a 44.996px minimum; the
  static gate now parses the value and accepts any declaration at or above 44px.
- The in-app browser exposes a fixed 1280 × 720 viewport. Its security policy rejected an embedded
  390px preview and explicitly prohibited workaround or alternate browser execution. The mobile
  check is recorded as pending rather than inferred from CSS or reported as passing.
- Direct Enter/Tab dispatch became unreliable after focus moved between the skip link and main
  target. The first real Tab focus, visible style, native link target and focus transfer on
  activation were observed; a clean keyboard-only activation pass remains part of final review.

## Durable lessons

- CSS pixel declarations can paint fractionally smaller under browser scaling; give minimum touch
  targets a small margin while keeping the validation threshold explicit.
- Accessibility requirements become durable when generator output and the committed HTML are
  validated together; changing markup alone would leave regressions easy to reintroduce.
- Link and image names should each carry context because assistive technologies may expose either
  surface.
- A fixed desktop browser cannot substantiate a mobile claim. Tool limitations belong in the
  evidence record, not behind an inferred pass.

## Backlog reconciliation

- Six LAND-06 criteria are implemented; skip link, heading hierarchy, CI names, focus treatment,
  action targets and both-theme contrast have automated and/or desktop evidence.
- The combined 390px/desktop criterion remains unchecked because only desktop is verified.
- LAND-06 remains IN REVIEW in draft PR #12 until 390px and keyboard-only activation checks pass,
  then requires owner merge, exact-merge quality, Pages and live verification before DONE.
- LAND-C01 through LAND-C04 remain unscheduled and unchanged.
