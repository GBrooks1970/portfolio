"""Validate and publish the immutable, public central-review snapshot."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SNAPSHOT = ROOT / 'data/reviews.json'
SOURCE_REPOSITORY = 'GBrooks1970/test-automation-portfolio'
SOURCE_PATH = 'portfolio-reviews/public-index.html'
MANIFEST_PATH = 'portfolio-reviews/public-manifest.json'
SHA = re.compile(r'[0-9a-f]{40}')


def digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


class ReviewHTML(HTMLParser):
    def __init__(self, document):
        super().__init__()
        self.ids, self.projects, self.links = [], [], set()
        self.feed(document)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {'script', 'iframe', 'object', 'embed', 'base'} or any(key.startswith('on') for key in attrs):
            raise ValueError('Executable content in review snapshot')
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if attrs.get('data-review-project'):
            project = attrs['data-review-project']
            if attrs.get('id') != 'review-' + project:
                raise ValueError('Review project anchor is corrupt')
            self.projects.append(project)
        if attrs.get('href'):
            self.links.add(attrs['href'])


def validate(snapshot: dict, registry_lock: dict | None = None) -> ReviewHTML:
    if snapshot.get('schemaVersion') != 2:
        raise ValueError('Review snapshot schemaVersion must be 2')
    source = snapshot['source']
    if (source.get('repository') != SOURCE_REPOSITORY or source.get('path') != SOURCE_PATH
            or source.get('manifestPath') != MANIFEST_PATH or not SHA.fullmatch(source.get('commit', ''))):
        raise ValueError('Review snapshot requires an exact central source commit and public paths')
    if not SHA.fullmatch(snapshot.get('registryCommit', '')):
        raise ValueError('Review snapshot requires a full registry commit')
    if digest(snapshot['html']) != snapshot['htmlSha256']:
        raise ValueError('Review HTML hash differs from its source manifest')
    repositories = snapshot['repositories']
    if registry_lock is not None:
        expected = {r['project']: r['github'] for r in registry_lock['projects'] if r['presentation_role'] in {'showcase', 'methodology'}}
        if repositories != expected or snapshot['registryCommit'] != registry_lock['source']['commit']:
            raise ValueError('Review repository inventory or registry pin differs from public registry lock')
        hidden = [r['project'] for r in registry_lock['projects'] if r['presentation_role'] not in {'showcase', 'methodology'}]
        if any(project in snapshot['html'] for project in hidden):
            raise ValueError('Hidden project in public snapshot')
    parsed = ReviewHTML(snapshot['html'])
    if len(parsed.ids) != len(set(parsed.ids)) or len(parsed.projects) != len(set(parsed.projects)):
        raise ValueError('Duplicate review project or anchor')
    if parsed.projects != snapshot['reviewProjects'] or not set(parsed.projects) <= repositories.keys():
        raise ValueError('Review project inventory differs from public cards')
    expected_links, bundle_keys = set(), set()
    for record in snapshot['reviewBundles']:
        project, bundle, commit = record['project'], record['bundle'], record['commit']
        key = (project, bundle)
        if project not in repositories or not SHA.fullmatch(commit) or key in bundle_keys:
            raise ValueError('Invalid review bundle source or duplicate bundle')
        bundle_keys.add(key)
        prefix = f'https://github.com/{repositories[project]}/blob/{commit}/'
        for kind, filename in [('index', r'00_[^/]+\.md'), ('executive', '01_EXECUTIVE_SUMMARY.md')]:
            url = record[kind]
            if not url.startswith(prefix) or not re.search('/' + re.escape(bundle) + '/' + filename + '$', url):
                raise ValueError('Review link differs from its published source')
            expected_links.add(url)
    actual_bundle_links = {url for url in parsed.links if re.search(r'/CODE_REVIEW_[^/]+/(?:00_[^/]+|01_EXECUTIVE_SUMMARY)\.md$', url)}
    if expected_links != actual_bundle_links:
        raise ValueError('Review bundle inventory differs from HTML; a parallel review may be missing')
    if {project for project, _ in bundle_keys} != set(parsed.projects):
        raise ValueError('Review bundle coverage differs from project cards')
    focused = {r['url'] for r in snapshot['focusedReviews']}
    actual_focused = {url for url in parsed.links if re.search(r'/\.review/\d{4}-\d{2}-\d{2}_[^/]+\.md$', url)}
    if focused != actual_focused or len(focused) != len(snapshot['focusedReviews']):
        raise ValueError('Focused review inventory differs from HTML')
    for record in snapshot["focusedReviews"]:
        project = record["project"]
        if project not in repositories or not record["url"].startswith(f"https://github.com/{repositories[project]}/blob/"):
            raise ValueError("Focused review source differs from its project")
    allowed_repos = set(repositories.values())
    for url in parsed.links:
        match = re.match(r'https://github.com/([^/]+/[^/]+)/(?:blob|tree)/([0-9a-f]{40})/', url)
        if not match or match[1] not in allowed_repos:
            raise ValueError(f'Review link is not a pinned public source: {url}')
    manifest = {key: value for key, value in snapshot.items() if key not in {"source", "html"}}
    manifest["schemaVersion"] = 1
    if digest(json.dumps(manifest, indent=2, ensure_ascii=False)+"\n") != source.get("manifestSha256"):
        raise ValueError("Review source manifest hash differs from the imported metadata")
    return parsed


def load_snapshot(path: Path = DEFAULT_SNAPSHOT, registry_lock: dict | None = None) -> dict:
    snapshot = json.loads(path.read_text(encoding='utf-8'))
    if registry_lock is None:
        registry_lock = json.loads((ROOT / 'data/registry-lock.json').read_text(encoding='utf-8'))
    validate(snapshot, registry_lock)
    return snapshot


def render(snapshot: dict) -> str:
    validate(snapshot)
    # The source already supplies accessible table regions and escaped review prose.
    return snapshot['html'].replace('<main class="container">', '<main class="container"><nav aria-label="Portfolio"><a href="index.html">Back to portfolio</a></nav>', 1)


def check_reviews() -> None:
    expected = render(load_snapshot())
    if (ROOT / 'reviews.html').read_bytes() != expected.encode('utf-8'):
        raise ValueError('reviews.html is stale; run python tools/generate_reviews.py')


def import_snapshot(repository: Path, commit: str, registry_lock: dict) -> dict:
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repository), *args])
    full_commit = git('rev-parse', f'{commit}^{{commit}}').decode().strip()
    # A topic-branch commit is not a published central source.
    subprocess.run(['git', '-C', str(repository), 'merge-base', '--is-ancestor', full_commit, 'origin/main'], check=True, capture_output=True)
    manifest_bytes = git('show', f'{full_commit}:{MANIFEST_PATH}')
    manifest = json.loads(manifest_bytes)
    snapshot = {**manifest, 'schemaVersion': 2, 'source': {'repository': SOURCE_REPOSITORY, 'commit': full_commit, 'path': SOURCE_PATH, 'manifestPath': MANIFEST_PATH, 'manifestSha256': hashlib.sha256(manifest_bytes).hexdigest()}, 'html': git('show', f'{full_commit}:{SOURCE_PATH}').decode('utf-8')}
    validate(snapshot, registry_lock)
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--import-repository', type=Path)
    parser.add_argument('--commit')
    args = parser.parse_args()
    if bool(args.import_repository) != bool(args.commit) or (args.check and args.import_repository):
        parser.error('--import-repository and --commit must be paired, without --check')
    if args.import_repository:
        lock = json.loads((ROOT / 'data/registry-lock.json').read_text(encoding='utf-8'))
        snapshot = import_snapshot(args.import_repository, args.commit, lock)
        DEFAULT_SNAPSHOT.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')
    if args.check:
        check_reviews()
    else:
        (ROOT / 'reviews.html').write_text(render(load_snapshot()), encoding='utf-8', newline='\n')
    print('reviews generation: PASS')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
