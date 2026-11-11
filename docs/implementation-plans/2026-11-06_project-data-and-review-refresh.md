---
version: 1
created: 2026-11-06
project: portfolio-landing
type: implementation-plan
item: LAND-18 project-data and review-publication refresh
status: in-review
approved: 2026-11-07
delivered: 2026-11-07
language: en-GB
---

# Implementation plan: refresh project data and publish the new reviews

**Goal.** Bring every public project entry up to date with its owning evidence and make all newly published reviews discoverable from the landing page. Preserve the distinction between implementation, review findings, current CI, owner acceptance and published historical reports.

This instruction authorises preparation of this plan and the separate update of the workspace central index. Landing implementation and deployment remain proposed. The current central-index update is not a public-site release.

## Evidence gathered before planning

Read-only inspection covered the registry, current landing manifests, source generators, publication contracts, project review directories and relevant project documentation. Remote default-branch SHAs were compared with all 18 local project HEADs; they matched at capture. The canonical central generator was run in a separate staging root to protect existing landing changes.

| Finding | Consequence for implementation |
|---|---|
| The registry currently has 18 projects: 15 showcase, two methodology and one hidden. The landing manifest has 17 public entries. | Audit all 17 entries; retain the 15/2 public classification. Derive totals from the pinned registry. |
| The landing registry lock pins `78cda575c9b42c6cb8783eb719e6e67abd4f59f0`; the inspected registry checkout is `3a76747097084f525c9fec9fd7318d8aa47b89aa`. | Refresh the lock from an explicitly selected, merged registry commit and review the field-level diff. A newer SHA alone does not establish that membership changed. |
| The published reviews snapshot references central commit `69d258e6fa4a813f8309d8854979118739cc3621` and registry commit `cd628eadb26a6495ad60ea6bbb229a3feb932b7c`. | Import a new immutable snapshot after the updated central index is merged. |
| Eight new bundles across Sudoku, OrangeHRM, ParaBank, Credit Dashboard and portfolio-prompts are on their captured default branches. Sudoku, ParaBank and Credit each have two new independent reviews. | Publish all eight; retain parallel reviews even when only the latest timestamp supplies the primary summary. |
| Fifteen registered projects now have comprehensive bundles: 13 showcase and two methodology. TradeBlotter and Loan Origination have no such bundle. | Provide review actions only where a published review exists; state the two public coverage gaps accurately. |
| Credit Dashboard also has six October focused review/confirmation documents. The internal portfolio structural review is a different kind of assessment. | Preserve focused records alongside bundles. Keep the internal structural assessment outside public project-review content. |
| The canonical central generator writes directly to a sibling landing `reviews.html`, mis-resolves some summary links, can mistake a table heading for a grade, and omits coverage/parallel-review records. | Repair that source workflow before using it for repeatable publication. The current central refresh required documented reconciliation. |
| Landing `reviews.html` already has an unrelated uncommitted change. | Use a separate landing checkout; preserve and identify that change rather than overwriting or staging it. |
| The internal index names the hidden registry member and links to internal portfolio documents. | Generate an explicitly public export before importing into the public landing repository. Merely limiting the repository URL map is insufficient. |
| Existing `python -B tools/check_site.py` passed: 8 IDs, 70 named controls, 7 internal references, 66 external URLs and 20 contrast pairs. | This is a baseline for the current main page, including live URL checks. It is not validation of the proposed refresh or the modified reviews page. |
| Sudoku's November reviews identify dependency-policy and parity-evidence limits; the earlier merge did not remediate those findings. Credit's backlog remains closed with accepted residual limits. | Do not turn review publication into a claim of repaired product defects, green CI or reopened delivery. Recheck the current owning records during implementation. |

Owning contracts: [project contract](../project-contract.md), [generation](../generation.md), [review publication](../review-publication.md), [quality gate](../quality-gate.md) and [presentation ownership](../decisions/001-presentation-ownership.md). The updated [central index](../../../portfolio-reviews/README.md) contains the complete review inventory and source links.

## Project-by-project content audit

For each row, inspect the owning README, canonical backlog, current workflow/report evidence and latest relevant review. Record the reviewed commit, proposed copy/action delta, and the reason for retaining an unchanged field. Reviews inform limitations; the current backlog owns delivery status. Recheck facts at implementation time rather than treating this planning snapshot as continuously current.

| Public entry | Required assessment and proposed treatment | Source starting point |
|---|---|---|
| Magento Checkout Automation | Retain the guest-checkout/Screenplay scope. Replace the ambiguous `Live report` label with `Published report`. Recheck the structural review's inactive-e2e finding before making any current assurance claim. Keep the historical review available. | [README](../../../magento-checkout-automation/README.md) |
| OrangeHRM PIM Automation | Retain Docker-backed employee journeys and distinguish recorded report evidence from current workflow health. Add the November Antigravity review; reconcile any current CI diagnosis with owning project evidence before changing claims. | [README](../../../orangehrm-pim-automation/README.md) |
| ParaBank Bank Automation | Extend the current UI/API summary to acknowledge the delivered alternative test styles where useful. Verify the bounded performance lane separately before presenting it as performance evidence. Include both November reviews and their validation limits. | [README](../../../parabank-bank-automation/README.md) |
| Bitfinex WebSocket Screenplay | Retain the live protocol and Kanban links. Describe checksum checks without implying that a passing run closes every live-order-book issue. Reconcile maintenance claims with the existing LIVE-01 disposition. | [README](../../../bfx-ws-screenplay/README.md) |
| Hand-Baked Screenplay Pattern | Recheck the recorded 0.3.0 release, zero-dependency scope, event-fold reporter and mutation lane. Retain the existing summary where verified; do not equate a visibility-only mutation lane with a blocking quality threshold. | [README](../../../hand-baked-screenplay-pattern/README.md) |
| Markdown Renderer | Reconfirm offline behaviour, sanitisation, accessibility coverage and demo availability. Retain a product/demo action and keep test claims bounded to the implemented checks. | [README](../../../markdown-renderer/README.md) |
| Mobile Forex Automation | Keep browser-device emulation explicit; revise `on-device` wording if it implies execution on physical phones. Preserve the demo. Do not claim that pending local-runtime owner rehearsals are accepted. | [README](../../../mobile-forex-automation/README.md) |
| Calculator Screenplay BDD | Recheck the API, OpenAPI documentation and playwright-bdd scope. Retain API reference labelling and the existing review link when no newer review exists. | [README](../../../calculator-screenplay-bdd/README.md) |
| Sudoku Multi-Stack Parity POC | Describe three-stack checks over the common contract without an unqualified proof-of-completeness claim. Recheck the 55-scenario count, audit status and current parity evidence. Present both November reviews; retain solver and parity report actions with accurate labels. | [README](../../../gb.automation.smoketests.sudoku.poc/README.md) |
| OWASP Juice Shop DAST | Preserve intentionally vulnerable training-target framing, passive detection and separately controlled confirmation. Review scan date and maintenance state; never imply that a positive-detection gate establishes production security. | [README](../../../juice-shop-dast-automation/README.md) |
| Auth Separation | Keep it in methodology. Retain the specification-first and generated-skeleton boundary; generated 501 endpoints are not an implemented authentication service. Verify the board and existing review links. | [README](../../../auth-separation/auth-separation_README_v1.md) |
| Auth Separation Screenplay POC | Retain the implemented Node/Python/C# bounded interchangeability demonstration and living contract documentation. Verify current runtime claims and distinguish this executable POC from the methodology specification set. | [README](../../../auth-separation-screenplay-poc/README.md) |
| TradeBlotter WPF | Preserve the two delivered adapters and licensed Ranorex prerequisite. Keep Windows CI evidence and pending owner-acceptance boundaries distinct. Do not invent a comprehensive code-review action. | [README](../../../tradeblotter-wpf-screenplay/README.md) |
| Saleor GraphQL Automation | Retain delivered catalogue/authentication/checkout/fulfilment capabilities, report and schema-monitor links. Reconcile current dependency maintenance. The September review is historical and must not replace current delivery evidence. | [README](../../../saleor-graphql-automation/README.md) |
| Loan Origination Parity | Describe the four exercised surfaces and the actual parity assertions precisely. Recheck server-side authorisation and report evidence. Do not create a review action while no comprehensive bundle exists. | [README](../../../loan-origination-parity/README.md) |
| Credit Dashboard SUT | Condense the long card while retaining specification-first API/UI, shared harness, seeded defects, accessibility and visual coverage. Put dated counts and limitations in the evidence detail. Preserve closure on 23 October and accepted residual risks; remove blanket clean-run implications where exceptions exist. Include both November bundles and the six focused October records. | [README](../../../credit-dashboard-sut/README.md), [backlog](../../../credit-dashboard-sut/DOCS/backlog.md) |
| portfolio-prompts | Keep it in methodology. Describe lifecycle prompts, registry and evidence tooling accurately, with licence claims checked against owning files. Add the November Antigravity review; label the structural-review prompt as an approved proposal until separately installed. | [README](../../../portfolio-prompts/README.md) |

## Steps

1. **Reserve scope and write the publication contract.** Create isolated `codex/` branches in each owning repository. Recheck status and reserve a new landing backlog ID on approval. Update landing `docs/generation.md` and `docs/review-publication.md` to define: public-role filtering, latest-versus-parallel review treatment, immutable source pins, stable project anchors, focused-review records and provenance. Preserve the existing uncommitted landing output and unrelated root work.

2. **Make central generation reproducible in portfolio-prompts.** Change `tools/build-portfolio-reviews.py` and add focused tests under `tools/tests/`. Add explicit workspace/output selection and a non-writing `--check` mode. Remove the automatic sibling-landing write. Correct bundle-relative/source-relative links, explicit grade/date extraction, matrix escaping and HTML table rendering. Preserve coverage gaps and all newer parallel bundles deterministically. Emit both the internal central index and a public HTML export, proposed as `portfolio-reviews/public-index.html`, that contains only visible registry projects and public project sources. The public export must omit the hidden member, internal structural-review section, local absolute paths and local-only review content. Update the canonical summary prompt and tool documentation to describe these outputs and checks. This is a tooling prerequisite, not a change implemented by the present planning task.

3. **Publish the central artefacts in the root support repository.** Regenerate `portfolio-reviews/README.md` and `portfolio-reviews/index.html` and add the public export from the reviewed generator. Verify all eight new bundles, all six focused records and every latest-summary selection. Confirm that all intended public source files exist on their repositories' default branches. Preserve exact captured source commits. Merge the central-index PR before importing it into landing; the current uncommitted refresh cannot be used as a claimed merged source.

4. **Refresh landing source data from merged inputs.** Run `tools/lock_registry.py --repository <canonical-checkout> --commit <selected-merged-SHA>` and review `data/registry-lock.json`. Update all required fields in `data/presentation.json` using the project audit above. Update `data/site.json` only if the verified capability description changes. Import the exact merged public-export HTML into `data/reviews.json`; set its central repository, full source commit, public-export path and registry commit accurately. Derive the public repository map from the same registry pin. Add a validated `reviewProjects` list derived from the public export's project cards, rather than hand-maintaining another membership list.

5. **Generate review navigation and content.** Update `tools/generate_reviews.py` to consume the public export, validate `reviewProjects`, preserve `review-<project-id>` anchors and avoid duplicating existing table wrappers or applying obsolete grade heuristics. Update `tools/generate_site.py` to derive a `Code reviews` action to `reviews.html#review-<project-id>` for each project with a published bundle. Keep the current presentation schema's ownership boundary; the review action comes from the pinned review snapshot, not duplicated editorial URLs. Preserve the global Reviews navigation. Adjust `index.template.html` only as needed for the extra action's wrapping and keyboard treatment. Generate `reviews.html` and `index.html`; regenerate `sitemap.xml`/`robots.txt` only through their generator when its inputs require it. The proposed snapshot has 15 review destinations: 13 showcase and two methodology entries. The remaining two showcase entries receive no invented review destination.

6. **Validate the complete result and review it in a browser.** Extend the relevant existing tests in `tools/tests/test_generate_reviews.py`, `test_reviews_summary.py`, `test_generate_site.py`, `test_registry_parity.py` and `test_site_quality.py` for the changed contracts. Run the complete gate, then inspect the main and reviews pages at desktop and 390px widths, in both landing themes where supported. Exercise the changed project actions, both links for each new review, parallel-review inventory, focused records, keyboard focus and horizontal table scrolling. Record real counts and output; do not reuse this plan's baseline counts as results.

7. **Publish and close with evidence.** Open a landing PR containing source data, generated output, tests and documentation together. Merge only with owner authority. Observe quality and Pages for the exact merge commit; compare unauthenticated live main/reviews HTML with the merged generated files and follow the new review links. Record immutable implementation/publication logs under `docs/implementation-logs/`, reconcile the landing backlog and append the plan outcome. Mark the task implemented only after publication is verified.

## Verification

| Check | Required result |
|---|---|
| Public inventory parity | Exactly the visible registry projects; currently 15 showcase plus two methodology. The hidden member appears nowhere in public HTML or public snapshot data. |
| Review completeness | All eight new bundles are reachable, including both reviews for Sudoku, ParaBank and Credit. All six October focused records remain accessible. All 15 latest selections match the timestamp rule. |
| Source identity | Central export is read from a merged full SHA; registry pins agree; public review targets exist at recorded source commits. No untracked review is labelled published. |
| Generator isolation | Running the central generator leaves a sentinel sibling `portfolio-landing/reviews.html` byte-for-byte unchanged. |
| Grade and link correctness | A `Grade`/`Notes` table header never becomes an overall grade. Bundle-relative and repository-relative examples resolve to the intended source. Matrix columns remain valid. |
| Determinism | A second build produces identical bytes. `--check` fails when an output byte is deliberately changed and passes after regeneration. |
| Required negative controls | Inject a hidden project into public data, omit one parallel review, corrupt a review anchor, substitute an unpublished source, and alter a generated count. Each corresponding gate must fail for the stated reason. Restore fixtures before the final run. |
| Full local/PR gate | `python tools/verify_portfolio.py --registry-repository <full-history-canonical-checkout>` passes with external URL checks enabled. `--skip-external` is diagnostic only. The tooling PR also passes `python tools/check-library.py`. |
| Browser | No page-level overflow, hidden actions, duplicate IDs or console errors at desktop/390px; tables may scroll within their labelled region. Keyboard navigation and all changed review paths work. |
| Publication | Exact-merge quality and Pages pass; live bytes and review destinations match the merged artefacts. A merge alone is not publication evidence. |

The public-export and navigation tests must run in isolated CI too. Tests that skip because sibling checkouts are absent cannot be the only protection for hidden-project exclusion or review completeness.

## Delivery

| Repository | Proposed branch | Review unit and dependency |
|---|---|---|
| portfolio-prompts | `codex/review-index-generation-refresh` | Generator/prompt fixes and focused tests; merge before final root regeneration. |
| test-automation-portfolio | `codex/central-reviews-refresh-20261106` | Updated central index and generated public export; merge before landing snapshot import. |
| portfolio-landing | `codex/project-data-and-reviews-refresh` | Project copy, pinned review/registry data, navigation, generated pages and tests. Owner-authorised merge, then publication evidence. |

Do not stage other agents' files, reset their checkouts, change target-project application code, accept audit exceptions or close their review findings as part of this presentation work. New project fixes require their owning workflows. Preserve current Learning Paths content unless its separately verified source has changed and the owner adds that refresh to scope.

## Decisions put to the owner

| Decision | Options | Recommendation | Owner's answer |
|---|---|---|---|
| Review discoverability | Global Reviews page only; or global page plus per-project actions | Add derived per-project `Code reviews` actions while keeping all parallel reviews in the reviews page. | Accepted 2026-11-07: Per-project action links implemented on cards with published reviews. |
| Card detail | Retain all historical counts in card prose; or use concise capability summaries with dated detail in evidence | Use concise summaries and date-bound detailed evidence, especially for Credit Dashboard. | Accepted 2026-11-07: Concise summaries and precise lifecycle/report labels implemented. |
| Publication sequence | Publish the current internal index directly; or produce a filtered, merged public export | Use the public export and the three-repository sequence above. | Accepted 2026-11-07: Pinned public export imported from root commit 17d4dea. |
| Delivery authority | Prepare PRs for owner merge; or separately authorise agent merges after checks | Prepare reviewable PRs, with merge authority confirmed for this new implementation batch. | Accepted 2026-11-07: Prepared on branch `codex/project-data-and-reviews-refresh` for owner review and PR. |

## Outcome

Implemented on branch `codex/project-data-and-reviews-refresh` on 2026-11-07 under backlog item LAND-18. All acceptance criteria and verification gates passed (77/77 tests, external URLs verified, negative controls passed). Implementation log: [`docs/implementation-logs/2026-11-07_land-18_project-data-and-reviews-refresh.md`](../implementation-logs/2026-11-07_land-18_project-data-and-reviews-refresh.md).
