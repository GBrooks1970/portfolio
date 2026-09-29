import unittest
import json
import re
from generate_reviews import ROOT

from generate_reviews import public_link, render, check_reviews


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

    def test_overall_grade_does_not_replace_bundle_identifier(self):
        output = render(json.loads((ROOT / 'data/reviews.json').read_text(encoding='utf-8')))
        row = re.search(r'<tr>\s*<td><code>gb.automation.smoketests.sudoku.poc</code></td>.*?</tr>', output, re.S)[0]
        cells = re.findall(r'<td>(.*?)</td>', row, re.S)
        self.assertIn('CODE_REVIEW_CODEX_v2_20260929T0633Z', cells[2])
        self.assertEqual(cells[5], '<code>B</code>')
