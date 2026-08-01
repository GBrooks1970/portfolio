# Portfolio Page Audit — 2026-08-01

**Subject:** `https://gbrooks1970.github.io/portfolio/`
**Repository:** `https://github.com/GBrooks1970/portfolio`
**Landing source baseline:** `8eee1bacc262b5736715f9e88c430a231ff6631e`
**Registry baseline:** `dd8d7864c0c8f14576b96a328e170ea39a0ac85c`
**Purpose:** Preserve the evidence and recommendations behind backlog v1 for cold resumption.

## Scope and method

The audit compared:

- the live GitHub Pages DOM and visual layout;
- the repository's `index.html`, README and Pages history;
- the registered project set in `portfolio-prompts/registry.yml`;
- current project facts needed to identify stale public claims.

The live page was inspected at a 1280 × 720 desktop viewport and a 390 × 844 mobile viewport. The
audit checked card inventory, landmark structure, link semantics, document overflow and captured
console warnings/errors. It did not mutate the page, repositories or GitHub settings.

## Executive finding

The page is a clean, fast and responsive static showcase, but its inventory is maintained manually
and has drifted from the portfolio registry. Eight showcase cards are published. ParaBank—the ninth
showcase project—is missing, and the registered `portfolio-prompts` meta-project is mentioned only
indirectly rather than linked as methodology/tooling.

The defect is systemic rather than a one-off card omission: counts, cards and summaries are repeated
in hand-authored HTML and Markdown, and no pull-request check compares them with the registry.

## Evidence

| ID | Severity | Finding | Evidence |
|---|---|---|---|
| AUD-01 | HIGH | ParaBank is missing from the public showcase | Live DOM has 8 articles; registry has 9 non-meta showcase projects |
| AUD-02 | HIGH | Project totals are hard-coded | Header, footer and README independently say “eight projects” |
| AUD-03 | HIGH | No inventory parity gate exists | Repository contains `index.html`, README and licence only; Actions history is Pages deployment |
| AUD-04 | MEDIUM | Sudoku evidence is stale | Card says 46 scenarios; authoritative backlog baseline says 48 scenarios / 267 steps |
| AUD-05 | MEDIUM | Meta-project ownership is not discoverable | Hero says “Library work under @NeoCognitus70” as plain text; `portfolio-prompts` is not linked |
| AUD-06 | MEDIUM | Repeated CI links have weak accessible names | Every badge image uses the same `alt="CI"`; no project-specific link label |
| AUD-07 | MEDIUM | Navigation/accessibility can be stronger | No skip link, project-section heading or explicit `:focus-visible` style |
| AUD-08 | LOW | Discoverability metadata is incomplete | No canonical/social metadata; GitHub repository homepage field is empty |

## Chronology and root cause

- Landing commit `8eee1ba` and its successful Pages deployment were published on 2026-07-14.
- The ParaBank repository was created on 2026-07-22 and subsequently registered as the ninth
  showcase project.
- No onboarding step or CI contract required the support repository to change when registry
  membership changed.
- Consequently the page, README and repeated numeric prose remained at the eight-project baseline.

Root cause: **the registry owns portfolio membership, while the landing page independently owns an
unvalidated manual copy of that membership.**

## Current inventory comparison

| Registry project | Public treatment | Audit result |
|---|---|---|
| `magento-checkout-automation` | Showcase card | Present |
| `hand-baked-screenplay-pattern` | Showcase card | Present |
| `calculator-screenplay-bdd` | Showcase card | Present |
| `gb.automation.smoketests.sudoku.poc` | Showcase card | Present; scenario count stale |
| `bfx-ws-screenplay` | Showcase card | Present |
| `orangehrm-pim-automation` | Showcase card | Present |
| `markdown-renderer` | Showcase card | Present |
| `mobile-forex-automation` | Showcase card | Present |
| `parabank-bank-automation` | Showcase card | **Missing** |
| `portfolio-prompts` | Methodology/tooling | Mentioned indirectly; repository link missing |

`portfolio-landing` itself remains a support repository and is not counted as a showcase or
registered lifecycle project.

## Visual and technical strengths to preserve

- Static, dependency-free delivery with no runtime API dependency.
- Responsive grid: three columns at the audited desktop width and one column at 390px.
- No horizontal document overflow at either audited width.
- Correct `lang="en-GB"`, page title, description and major header/main/footer landmarks.
- Automatic light/dark colour-scheme support.
- No console warnings or errors during the live audit.
- Clear cards, concise technology chips and direct repository/evidence actions.

## Recommended target model

Use a hybrid ownership model:

1. The portfolio registry owns stable membership identifiers and an explicit presentation role.
2. The landing repository owns public title, description, tags, display order and evidence URLs in
   a structured manifest keyed by those identifiers.
3. A deterministic generator produces card HTML and all numeric summaries.
4. Pull-request CI compares registry membership/roles with the landing manifest, validates the
   generated output and checks publication quality.
5. GitHub Pages deploys only the static generated artefact. Visitor browsers do not call GitHub or
   registry APIs.

This avoids duplicating membership authority while keeping marketing copy and presentation design
inside the repository that owns them.

## ParaBank presentation recommendation

Suggested card:

- **Title:** ParaBank Bank Automation
- **Discipline:** Banking UI + API BDD
- **Summary:** Docker-backed ParaBank automation combining Serenity/JS and Playwright UI journeys
  with stateful API BDD, live OpenAPI validation and REST–SOAP parity.
- **Tags:** Serenity/JS, Playwright, OpenAPI, Docker
- **Actions:** Repository and CI

Do not claim a live demo. A later, separately approved improvement may publish a static Serenity
report snapshot, but GitHub Pages cannot host the Docker-backed ParaBank SUT.

## Improvement catalogue

Required control work is defined in backlog LAND-01…06. Future candidates are LAND-C01…04:

- social and search metadata;
- clearer capability-based information architecture;
- expanded static evidence/report links;
- generated freshness and portfolio statistics.

The backlog, not this audit, determines whether and when those improvements are authorised.

## Audit limitations

- Link destinations were inspected structurally; this audit is not a long-running availability
  monitor.
- CI badges reflect their owning repositories and may legitimately change after capture.
- The mobile full-page screenshot mechanism was not used as an oracle; layout conclusions use live
  DOM bounds and overflow measurements.
- No accessibility statement here replaces automated and manual checks required by LAND-05/06.
