import copy
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generate_reviews import ROOT, validate, render, check_reviews, digest, import_snapshot, load_snapshot


class ReviewPublicationTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = load_snapshot()
        self.lock = json.loads((ROOT / 'data/registry-lock.json').read_text(encoding='utf-8'))

    def test_committed_output_and_complete_parallel_inventory(self):
        check_reviews()
        self.assertEqual(len(self.snapshot['reviewProjects']), 15)
        self.assertEqual(len(self.snapshot['reviewBundles']), 18)
        self.assertEqual(len(self.snapshot['focusedReviews']), 6)
        new = [r for r in self.snapshot['reviewBundles'] if '20261105T' in r['bundle']]
        self.assertEqual(len(new), 8)
        for project in ['gb.automation.smoketests.sudoku.poc', 'parabank-bank-automation', 'credit-dashboard-sut']:
            self.assertEqual(sum(r['project'] == project for r in new), 2)

    def test_missing_parallel_record_is_rejected_even_when_primary_remains(self):
        record = next(r for r in self.snapshot['reviewBundles'] if r['project'] == 'credit-dashboard-sut' and 'Antigravity' in r['bundle'])
        self.snapshot['reviewBundles'].remove(record)
        with self.assertRaisesRegex(ValueError, 'parallel review'):
            validate(self.snapshot, self.lock)

    def test_hidden_repository_injection_is_rejected(self):
        self.snapshot['repositories']['private-evidence'] = 'example/private-evidence'
        with self.assertRaisesRegex(ValueError, 'public registry lock'):
            validate(self.snapshot, self.lock)

    def test_corrupt_anchor_fails_after_hash_is_recomputed(self):
        self.snapshot['html'] = self.snapshot['html'].replace('id="review-credit-dashboard-sut"', 'id="broken-anchor"')
        self.snapshot['htmlSha256'] = digest(self.snapshot['html'])
        with self.assertRaisesRegex(ValueError, 'anchor is corrupt'):
            validate(self.snapshot, self.lock)

    def test_source_substitution_is_rejected(self):
        self.snapshot['reviewBundles'][0]['commit'] = 'a' * 40
        with self.assertRaisesRegex(ValueError, 'published source'):
            validate(self.snapshot, self.lock)

    def test_table_wrappers_are_not_duplicated_and_navigation_is_present(self):
        output = render(self.snapshot)
        self.assertEqual(output.count('<table>'), output.count('<div class="table-scroll"'))
        self.assertIn('href="index.html">Back to portfolio', output)
        self.assertNotIn('Grade:</strong> Notes', output)

    def test_unpublished_central_commit_cannot_be_imported(self):
        with tempfile.TemporaryDirectory() as folder:
            repo = Path(folder)
            def git(*args):
                return subprocess.check_output(['git', '-C', str(repo), *args], stderr=subprocess.DEVNULL)
            git('init', '-q')
            (repo/'seed.txt').write_text('published', encoding='utf-8')
            git('add', '.')
            git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Published')
            git('update-ref','refs/remotes/origin/main','HEAD')
            (repo/'seed.txt').write_text('topic only', encoding='utf-8')
            git('add','.')
            git('-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','Not published')
            with self.assertRaises(subprocess.CalledProcessError):
                import_snapshot(repo, 'HEAD', self.lock)

    def test_stale_html_is_rejected_without_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'reviews.html').write_bytes(b'stale')
            with patch('generate_reviews.ROOT', root), patch('generate_reviews.load_snapshot', return_value=self.snapshot):
                with self.assertRaisesRegex(ValueError, 'stale'):
                    check_reviews()
            self.assertEqual((root/'reviews.html').read_bytes(), b'stale')
