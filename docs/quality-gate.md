# Portfolio Quality Gate

This gate implements the source, publication and deployment boundary accepted in
[`decision 002`](decisions/002-publication-quality-gate.md).

The repository exposes one complete, cross-platform pull-request gate. It requires a full-history
checkout of the public canonical registry repository and no credentials or repository secrets:

```powershell
python -m pip install -r requirements-dev.txt
python tools/verify_portfolio.py --registry-repository ..\portfolio-prompts
```

CI runs the same command on Python 3.13. The workflow uses the ordinary `pull_request` event,
`contents: read`, non-persisted checkout credentials and full commit-SHA pins for its Node 24-based
checkout/setup actions.

## Gate layers

1. **Canonical parity:** rebuild `data/registry-lock.json` from its recorded immutable registry
   commit and compare registry roles, the presentation manifest, grouped project assignments,
   generated inventory/statistics and committed bytes.
2. **HTML structure:** require one HTML5 document, head/body, header/main/footer and H1; balanced
   explicit tags; unique attributes/identifiers; and project articles inside the main landmark.
3. **Metadata, discoverability and internal links:** require `en-GB`, UTF-8, responsive viewport,
   title and description; enforce one matching HTTPS canonical, complete Open Graph and Twitter/X
   compatibility fields, a source-aligned `WebSite` + `Person` JSON-LD graph, favicon contracts,
   real PNG dimensions, a canonical one-URL sitemap and its robots policy; resolve every local
   target and same-document fragment inside the repository root.
4. **Static accessibility:** require a working skip target; a visible, labelled project collection;
   coherent H1/H2/H3/H4 structure and named capability sections; resolvable `aria-labelledby`
   references; non-empty image alt text;
   project-specific CI names; keyboard-focusable anchors and natural focus order; a 44px minimum
   project-action target; explicit `:focus-visible` styling; and a 4.5:1 minimum for 20 text/focus
   foreground/background pairs across the light and dark themes. The contrast formula follows
   [WCAG 2.2 contrast minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
   relative luminance. This remains a targeted automated baseline, not a claim of full WCAG
   conformance or a substitute for rendered keyboard and responsive review.
5. **External evidence:** verify every unique HTTPS `href` and `src`, including repositories,
   workflow pages, badges, demos, reports and the public canonical page. Absolute social-image URLs
   under the canonical site are mapped back to their local committed assets during pull-request
   validation, because a new asset cannot exist on the public `main` deployment before merge.
6. **Deterministic tests:** run every `tools/tests/test_*.py` test after the production checks.

## External-link policy

External checks issue bounded GET requests concurrently with a 15-second timeout and read only the
initial response bytes. HTTP 200–399 passes.

- Permanent client failures such as 400, 403 or 404 fail immediately.
- HTTP 408, 425, 429, 500, 502, 503 and 504 plus timeouts/network errors are treated as transient.
  They receive three total attempts with one- and three-second waits.
- A URL still transiently unavailable after the third attempt fails the gate with a distinct
  message. Rerun the job once; if it persists, investigate the target or service status. Do not
  delete evidence, weaken the policy or replace a URL merely to clear a transient outage.
- Redirects are followed by the standard HTTP client. Plain HTTP and protocol-relative public URLs
  are rejected; published evidence must use HTTPS.

For offline diagnosis only, skip live requests while retaining every deterministic check and test:

```powershell
python tools/verify_portfolio.py --registry-repository ..\portfolio-prompts --skip-external
```

This mode is deliberately labelled incomplete and is never used by CI.

## Pages remains independent

The quality workflow runs on pull requests and `main`; GitHub Pages deployment remains a separate
post-merge signal. A green gate proves the committed artefact meets the source and static quality
contracts. A green Pages run proves deployment succeeded. Closing public-output work requires both,
plus an unauthenticated check of the live page and newly published canonical assets when rendered
content changed. GitHub's repository description, homepage, topics and repository social preview
are settings-side evidence and must be verified separately from the committed HTML contract.
