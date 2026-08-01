# Decision 002 — Publication Quality Gate

**Status:** Accepted
**Date:** 2026-08-01
**Decision owner:** Portfolio owner
**Applies to:** `GBrooks1970/portfolio`
**Backlog:** LAND-05

## Context

The landing repository already generated deterministic static HTML and compared its public
inventory with the canonical portfolio registry. GitHub Pages also reported whether the committed
artefact deployed. Those controls did not establish that the document was structurally valid, its
references were reachable, its interactive content had accessible names or its light and dark
colour tokens met the selected contrast baseline.

Publication quality must be reproducible before merge without making the public page depend on a
runtime service, a browser-side GitHub API call, credentials or repository secrets. Deployment and
live verification must remain independent signals because they answer different questions.

## Decision

Adopt a single, composable pull-request command:

```powershell
python tools/verify_portfolio.py --registry-repository <portfolio-prompts-path>
```

The command runs these layers in order:

1. rebuild and validate the canonical registry lock, presentation manifest and generated output;
2. validate HTML document structure, metadata, internal targets and selected static accessibility
   properties;
3. check every unique public HTTPS `href` and `src` with a bounded retry policy; and
4. run the deterministic Python test suite.

The static accessibility layer covers landmark structure, accessible names, focusability and a
4.5:1 minimum contrast ratio for the site's declared light and dark text colour pairs. It is an
automated baseline, not a claim of full WCAG conformance. LAND-06 retains responsibility for skip
navigation, heading hierarchy, explicit focus treatment, touch targets and responsive browser
validation.

External targets pass on HTTP 200–399. Permanent client failures fail immediately. HTTP 408, 425,
429, 500, 502, 503 and 504, timeouts and network failures receive three total attempts with bounded
one- and three-second waits, then fail distinctly. An offline diagnostic may skip external requests
but cannot satisfy the complete gate or CI.

The repository-owned workflow uses the ordinary `pull_request` event, read-only contents
permission, non-persisted checkout credentials, no secrets and full commit-SHA action pins. Pages
continues independently after merge. Public-output work closes only after the complete gate,
deployment and unauthenticated live verification all pass when they apply.

## Consequences

Benefits:

- one local command reproduces the complete pull-request gate;
- common structural, reference and accessibility regressions fail before publication;
- transient link failures are retried predictably but never silently accepted;
- the static page keeps no runtime service dependency; and
- source quality, deployment and live-output evidence remain explicit and independently auditable.

Costs and constraints:

- the complete gate requires network access and can fail when a third-party evidence target remains
  unavailable after its bounded retries;
- static checks cannot replace keyboard, responsive or assistive-technology browser review; and
- each new colour role or interactive pattern must be added deliberately to the validation model.

## Rejected alternatives

### Treat a successful Pages deployment as publication proof

Rejected because Pages proves build and deployment success, not document correctness, link health,
registry parity or accessibility properties.

### Rely only on manual browser review

Rejected because it is not deterministic, is easy to omit and does not give pull requests a fast
regression signal. Browser review remains complementary for layout and interaction.

### Ignore or silently pass transient external failures

Rejected because portfolio evidence that is persistently unavailable is a real publication defect.
Bounded retries distinguish temporary service behaviour without concealing it.

### Add visitor-side link or registry checks

Rejected because runtime requests would expose visitors to rate limits and service failures and
would weaken the static delivery boundary accepted in
[decision 001](001-presentation-ownership.md).

### Introduce a full browser accessibility stack in LAND-05

Rejected for this item because the dependency-free static checks provide a fast foundation while
LAND-06 already owns the remaining navigation, focus, touch-target and responsive contracts.

## References

- [Portfolio quality gate](../quality-gate.md)
- [WCAG 2.2 — Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
