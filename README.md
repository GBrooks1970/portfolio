# Test Automation Portfolio — landing page

A static, self-contained landing page for Gary Brooks's test-automation portfolio, published via
GitHub Pages: **https://gbrooks1970.github.io/portfolio/**

It links nine showcase projects (mobile-web device emulation, E2E and banking web UI, API/BDD,
multi-stack parity, real-time WebSocket, a Screenplay teaching library, and a shipped product)
with their repositories, live demos, and CI status. The supporting
[`portfolio-prompts`](https://github.com/NeoCognitus70/portfolio-prompts) methodology and tooling
repository is linked separately and is not counted as a showcase.

`index.html` is the whole site — no build step, no dependencies. Merge changes to `main` through a
pull request; Pages redeploys automatically.

## Contributor entry point

Before changing the landing page, read these repository-owned control records:

1. [`docs/project-contract.md`](docs/project-contract.md) — scope, validation and working norms.
2. [`docs/backlog.md`](docs/backlog.md) — authoritative priorities, dependencies and acceptance
   criteria.
3. [`docs/portfolio-page-audit-2026-08-01.md`](docs/portfolio-page-audit-2026-08-01.md) — evidence
   behind the current remediation cycle.

Record completed development in [`docs/implementation-logs/`](docs/implementation-logs/) before
closing its backlog item. These documents use ordinary Markdown and repository-relative paths so
they can be followed by a human or any AI-assisted engineering tool.

## Licence

[MIT](LICENSE) — © 2026 Gary Brooks.

The MIT licence applies only to the landing-page source in this repository. Portfolio projects and
support material stored elsewhere may use different terms; each owning repository is authoritative.
