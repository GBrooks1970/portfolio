# Project Contract — Portfolio Landing

## Purpose

This repository owns the public, static presentation of the test-automation portfolio. It does not
own portfolio membership, project health or the behaviour of linked projects.

## Source boundaries

- `docs/backlog.md` is the source of truth for approved work and completion.
- Accepted records in `docs/decisions/` define architectural choices and ownership boundaries.
- `portfolio-prompts/registry.yml` is the source of truth for portfolio membership.
- This repository owns public copy, layout, presentation metadata and Pages deployment.
- `data/presentation.json` owns public copy and order; `data/registry-lock.json` is a generated,
  reviewable snapshot of canonical registry fields at its recorded commit.
- `index.template.html` is the layout source and `index.html` is generated, committed output.
- A GitHub Pages deployment proves publication only; it does not prove inventory or content
  correctness.

## Gates

Apply every relevant gate before committing.

### Documentation-only changes

```powershell
git diff --check
```

Also confirm every new repository-relative Markdown link resolves.

### HTML, CSS or generated-content changes

Until LAND-05 supplies the complete publication-quality local gate:

1. Run `python tools/check_registry_parity.py --registry-repository <portfolio-prompts-path>` using
   a full-history canonical checkout.
2. Run `python tools/generate_site.py --check`.
3. Run `python -B -m unittest discover -s tools/tests -p test_*.py`.
4. Run `python -m http.server 8000` from the repository root.
5. Inspect `http://127.0.0.1:8000/` at desktop and 390px mobile widths.
6. Confirm no horizontal overflow, obscured actions or console errors.
7. Exercise every changed repository, CI, demo/report and internal link.
8. Confirm keyboard focus order and visible focus treatment.
9. Run `git diff --check`.

When LAND-05 adds an executable validation command, update this contract in the same PR and make
that command the first gate.

### Post-merge publication

- Observe the exact GitHub Pages run for the merged commit.
- Verify the live URL renders the merged content.
- Record the commit, PR and Pages run in the backlog and implementation log.

## Working norms

- All `main` changes go through a branch and pull request; the owner authorises merges.
- Preserve the static, dependency-light delivery model unless an approved decision changes it.
- Edit `data/presentation.json` or `index.template.html`, then regenerate; never hand-edit
  `index.html` or `data/registry-lock.json`.
- Do not call GitHub or registry APIs from visitors' browsers; generate data before deployment.
- Never hard-code a project total when it can be derived from structured source data.
- Keep registry identifiers stable and public display copy separate.
- Do not claim a demo, report, test count or green CI state without exact evidence.
- Use semantic HTML, keyboard-accessible actions, explicit focus states and en-GB prose.
- Treat external pages and CI badges as evidence links, not as content or availability guarantees.
- Keep secrets, private identifiers and runtime credentials out of the static artefact.
- Reconcile `docs/backlog.md` and add an implementation log before closing development work.

## Pull-request scope

- Prefer one reviewable backlog item per implementation PR.
- A target-project change and a landing-page presentation change belong in separate repositories and
  PRs, even when they describe the same project.
- Generated files and their source data must be reviewed together.
- Do not mix unrelated portfolio-root or project-repository changes into this repository.
- Pull-request workflows must use the `pull_request` event, least-privilege read permissions, no
  repository secrets, and non-persisted checkout credentials when executing proposed code.

## Completion evidence

A task is DONE only when:

- every acceptance criterion is checked with evidence;
- applicable local/CI gates pass;
- the owner merges the PR;
- the exact Pages deployment succeeds when public output changed;
- the live page is verified; and
- an immutable implementation log records what changed, decisions, failures and lessons.
