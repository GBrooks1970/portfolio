import sys
import unittest
import json
import re
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS_DIR))

from generate_reviews import ROOT, public_link, render, check_reviews, validate_snapshot


class ReviewPublicationTests(unittest.TestCase):
    def test_nested_review_and_anchor_keep_their_path(self):
        self.assertEqual(public_link('../sudoku/DOCS/.review/v2/02.md#risk', {'sudoku': 'owner/sudoku'}),
                         'https://github.com/owner/sudoku/blob/main/DOCS/.review/v2/02.md#risk')

    def test_folder_uses_tree_and_registry_owner(self):
        self.assertEqual(public_link('../library/.review/v2/', {'library': 'OtherOwner/library'}),
                         'https://github.com/OtherOwner/library/tree/main/.review/v2/')

    def test_unknown_and_traversal_paths_fail_closed(self):
        for url in ['../../secret', '../project/../secret', 'file:///private', 'http://unsafe']:
            with self.assertRaises(ValueError):
                public_link(url, {'project': 'owner/project'})

    def test_committed_output_matches_snapshot(self):
        check_reviews()

    def test_latest_reviews_matrix_renders_expected_grades_and_identifiers(self):
        output = render(json.loads((ROOT / 'data/reviews.json').read_text(encoding='utf-8')))
        matrix_match = re.search(r'<h2>Latest Reviews Matrix</h2>.*?<table>(.*?)</table>', output, re.S)
        self.assertIsNotNone(matrix_match)
        matrix_table = matrix_match.group(1)

        # Credit Dashboard SUT has B+ grade from CODEX review
        row_cds = re.search(r'<tr>\s*<td><code>credit-dashboard-sut</code></td>.*?</tr>', matrix_table, re.S)[0]
        cells_cds = re.findall(r'<td>(.*?)</td>', row_cds, re.S)
        self.assertIn('CODE_REVIEW_CODEX_v1_20261105T0859Z', cells_cds[2])
        self.assertEqual(cells_cds[5], 'B+')

        # Sudoku has Claude Opus review as latest
        row_sudoku = re.search(r'<tr>\s*<td><code>gb.automation.smoketests.sudoku.poc</code></td>.*?</tr>', matrix_table, re.S)[0]
        cells_sudoku = re.findall(r'<td>(.*?)</td>', row_sudoku, re.S)
        self.assertIn('CODE_REVIEW_Claude_v2_20261105T1425Z', cells_sudoku[2])
        self.assertEqual(cells_sudoku[5], 'Not assigned')

    def test_all_15_review_projects_present_and_have_anchors(self):
        snapshot = json.loads((ROOT / 'data/reviews.json').read_text(encoding='utf-8'))
        self.assertEqual(len(snapshot['reviewProjects']), 15)
        output = render(snapshot)
        for project in snapshot['reviewProjects']:
            self.assertIn(f'id="review-{project}"', output)

    def test_hidden_project_rejected_in_reviews(self):
        snapshot = json.loads((ROOT / 'data/reviews.json').read_text(encoding='utf-8'))
        leaked = dict(snapshot)
        leaked['reviewProjects'] = list(snapshot['reviewProjects']) + ['azure-dotnet-platform']
        leaked['repositories'] = dict(snapshot['repositories'], **{'azure-dotnet-platform': 'GBrooks1970/azure-dotnet-platform'})
        with self.assertRaises(ValueError):
            validate_snapshot(leaked)


if __name__ == "__main__":
    unittest.main()
