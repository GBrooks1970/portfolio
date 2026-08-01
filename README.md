# Test Automation Portfolio — landing page

A static, self-contained landing page for Gary Brooks's test-automation portfolio, published via
GitHub Pages: **https://gbrooks1970.github.io/portfolio/**

It links nine showcase projects (mobile-web device emulation, E2E and banking web UI, API/BDD,
multi-stack parity, real-time WebSocket, a Screenplay teaching library, and a shipped product)
with their repositories, live demos, and CI status. The supporting
[`portfolio-prompts`](https://github.com/NeoCognitus70/portfolio-prompts) methodology and tooling
repository is linked separately and is not counted as a showcase.

`index.html` is the committed, generated site — it has no visitor-side build step, dependency or
runtime data fetch. Public copy and display order live in `data/presentation.json`; canonical
membership, GitHub slugs and presentation roles come from the exact registry commit recorded in
`data/registry-lock.json`. The static output is generated from `index.template.html`:

```powershell
python tools/generate_site.py
python tools/generate_site.py --check
python -B -m unittest discover -s tools/tests -p test_*.py
```

To verify the committed registry lock against its exact canonical source as well as the manifest
and generated page, provide a full-history checkout of the public prompt-library repository:

```powershell
python tools/check_registry_parity.py --registry-repository ..\portfolio-prompts
```

The complete local pull-request gate adds HTML, internal/external link, metadata, accessibility and
test validation:

```powershell
python tools/verify_portfolio.py --registry-repository ..\portfolio-prompts
```

Pull requests run that same command with read-only permissions and no repository secrets. See
[`docs/quality-gate.md`](docs/quality-gate.md) for its coverage, live-URL retry policy and offline
diagnostic mode.

Do not edit `index.html` directly. See [`docs/generation.md`](docs/generation.md) for the schema,
registry-lock refresh and reproducibility contract. Merge changes to `main` through a pull request;
Pages redeploys the committed output automatically.

## Contributor entry point

Before changing the landing page, read these repository-owned control records:

1. [`docs/project-contract.md`](docs/project-contract.md) — scope, validation and working norms.
2. [`docs/backlog.md`](docs/backlog.md) — authoritative priorities, dependencies and acceptance
   criteria.
3. [`docs/portfolio-page-audit-2026-08-01.md`](docs/portfolio-page-audit-2026-08-01.md) — evidence
   behind the current remediation cycle.
4. [`docs/decisions/001-presentation-ownership.md`](docs/decisions/001-presentation-ownership.md) —
   ownership of portfolio membership, public copy and generated output.
5. [`docs/decisions/002-publication-quality-gate.md`](docs/decisions/002-publication-quality-gate.md)
   — the boundary between source quality, deployment and live verification.
6. [`docs/generation.md`](docs/generation.md) — deterministic source files, commands and registry
   pinning/parity procedure.
7. [`docs/quality-gate.md`](docs/quality-gate.md) — reproducible PR gate, accessibility scope and
   external-link failure policy.

Record completed development in [`docs/implementation-logs/`](docs/implementation-logs/) before
closing its backlog item. These documents use ordinary Markdown and repository-relative paths so
they can be followed by a human or any AI-assisted engineering tool.

## Licence

[MIT](LICENSE) — © 2026 Gary Brooks.

The MIT licence applies only to the landing-page source in this repository. Portfolio projects and
support material stored elsewhere may use different terms; each owning repository is authoritative.
