# Publishing the reviews page

The root central index does not deploy this site's `reviews.html`. Its generator
writes an internal pair and a separate public HTML/manifest pair. The public pair
includes only showcase and methodology projects and reviews already present at
captured default-branch commits. It retains the latest summary per project, all
parallel bundles in the selected archive window, focused records and explicit
coverage gaps. It excludes private projects, internal structural reviews and local-only content.

Merge the generator prerequisite, then the root central-index PR. Fetch their
merged commits and refresh the public registry lock and review snapshot:

```text
python tools/lock_registry.py --repository <library-checkout> --commit <merged-library-SHA>
python tools/generate_reviews.py --import-repository <root-checkout> --commit <merged-root-SHA>
python tools/generate_site.py
python tools/verify_portfolio.py --registry-repository <library-checkout>
```

The importer rejects a root commit that is not an ancestor of the already-fetched
`origin/main`. It reads both files with `git show`, never the working tree.
`data/reviews.json` schema 2 records the root source, registry pin, public repository
map, review-project IDs, bundle/focused inventory, source manifest hash and exact
HTML hash. Validation compares inventories with rendered links/cards and the
public registry projection. A SHA is provenance, not evidence that review findings
are fixed. No visitor-side GitHub request or build runtime is added.

Each reviewed project's generated action points to
`reviews.html#review-<project-id>`. Projects without a comprehensive bundle receive
no review action. Review actions do not inflate the existing demo/report/documentation
statistic. The renderer preserves the source's table regions and adds only portfolio
navigation; grades come from explicit source judgements, with no landing heuristic.

`python tools/generate_reviews.py --check` rejects stale bytes. The full gate checks
all pinned review URLs in addition to existing main-page URLs. Snapshot, privacy,
parallel-inventory, anchor and unpublished-import tests run in standalone CI.

After merging the landing PR, observe quality and Pages for its exact merge commit,
compare unauthenticated live main/reviews HTML with the merged generated files,
and follow the new review links. Record publication separately from implementation.
