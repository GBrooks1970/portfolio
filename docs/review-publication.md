# Publishing the reviews page

The portfolio root's central index is a local workspace artefact. Merging that
repository does not deploy this repository's `reviews.html`.

`data/reviews.json` holds the exact merged central HTML snapshot, its repository,
commit and source path, and registry-derived repository slugs. Refresh that snapshot
only after the project review PRs and central-index PR have merged. Preserve the
source commit and registry commit when importing; do not copy uncommitted output.

Run `python tools/generate_reviews.py`, then the complete portfolio quality gate.
The renderer converts workspace-relative links to GitHub blob/tree URLs, preserves
fragments, rejects unknown/traversing paths and adds portfolio navigation and a
keyboard-scrollable responsive table. `python tools/generate_reviews.py --check`
rejects stale output and is included in the main quality gate. No visitor-side
GitHub requests or build runtime are introduced.

Review the snapshot and generated output together in a landing PR. After merge,
observe Pages for the exact merge commit, compare the unauthenticated live HTML
with the generated output, and check the new full-review and executive-summary
links. Only then report that the public reviews page is current.
