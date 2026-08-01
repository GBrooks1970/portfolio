# Implementation Log — LAND-02: Presentation Ownership

**Date:** 2026-08-01
**Backlog item:** `LAND-02`
**Repository:** `GBrooks1970/portfolio`
**Branch:** `codex/land-02-presentation-ownership`
**Commit:** `2dcb5868d6959c42112233bc987acf5acb08eef2`
**Pull request:** https://github.com/GBrooks1970/portfolio/pull/7
**Pages run:** N/A — documentation-only; no `index.html` or public-page behaviour change

## Outcome

Decision 001 establishes a hybrid presentation contract before generator work begins. The canonical
`portfolio-prompts` registry owns membership, GitHub slugs and an explicit presentation role; the
landing repository owns evidence-backed public copy, order, tags and optional public actions. All
generation and parity work happens before static deployment, with no visitor-side GitHub or registry
API dependency.

The decision classifies nine current projects as showcases and `portfolio-prompts` as methodology.
It also defines how projects become visible, hidden or removed.

## Scope

- `docs/decisions/001-presentation-ownership.md` — accepted ownership, schema and lifecycle decision.
- `docs/backlog.md` — LAND-02 evidence, LAND-02R cross-repository work and reconciled dependencies.
- `docs/project-contract.md` — accepted decision records added to source boundaries.
- `README.md` — decision record added to the contributor entry point.
- Explicit non-goals: no registry mutation, manifest, generator, CI parity or public HTML change.

## Decisions

- Add a registry-owned `presentation_role` enum: `showcase`, `methodology` or `hidden`.
- Keep lifecycle `status`, orchestration eligibility and presentation role orthogonal.
- Use a landing-owned JSON manifest keyed by the exact registry identifier without duplicating
  membership, GitHub slugs or roles.
- Derive repository actions from registry GitHub slugs; keep workflow/demo/report presentation in
  the landing manifest.
- Commit deterministic static HTML and enforce it with a future byte-stable check; never fetch
  registry or GitHub data in visitors' browsers.
- Deliver the registry schema in a separate repository/PR as LAND-02R before LAND-03.

## Validation

| Gate | Result | Evidence |
|---|---|---|
| Registry orientation | PASS | `portfolio-prompts` baseline `dd8d786`; lifecycle/orchestration semantics inspected independently |
| Current classification | PASS | 9 `showcase`, 1 `methodology`, 0 `hidden` rows in decision 001 |
| Acceptance coverage | PASS | Membership/copy ownership, visibility, retirement and static deployment are explicit |
| Dependency reconciliation | PASS | LAND-02R added; LAND-03 depends on it; LAND-04 depends on LAND-02R and LAND-03 |
| Markdown links | PASS | All repository-relative links resolve |
| Exact staged scope | PASS | README, backlog, project contract and decision 001 only |
| `git diff --cached --check` | PASS | No whitespace errors |
| Owner merge | PENDING | LAND-02 remains IN REVIEW until PR #7 merges |

## Failures and recovery

None.

## Durable lessons

- Lifecycle state cannot safely stand in for public visibility: resting showcases remain public,
  while the meta project is methodology and excluded from fan-outs.
- A cross-repository contract needs an explicit implementation item and commit evidence; burying the
  registry change inside generator work would make cold resumption ambiguous.
- Static generation can use external canonical data at build/check time without imposing a runtime
  dependency on visitors.

## Backlog reconciliation

- LAND-02 is IN REVIEW with all content acceptance criteria checked; owner merge is the final gate.
- LAND-02R is BLOCKED on LAND-02 owner merge.
- LAND-03 is BLOCKED on LAND-02R; LAND-04 is BLOCKED on LAND-02R and LAND-03.
- LAND-05 and LAND-06 remain READY and can proceed independently.
