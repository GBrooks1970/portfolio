import json
import unittest

from refresh_learning_paths_snapshot import build_snapshot, dumps, extract, matches_source, validate_arguments

SHA = "6fe8133fea6a59accba608dfe77431f8f708b5bd"
WHEN = "2026-10-07T17:54Z"
SOURCE = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<title>Doc &amp; Title</title>
<style>
  :root { --ink: #111; }
</style>
<script>(function () { var pre = 1; })();</script>
</head>
<body>
<div class="wrap">
<header class="topbar"><button type="button" id="theme-toggle" hidden>X</button></header>
<!-- doc:begin -->
<h1>Doc</h1>
<section class="doc-meta"><dl>
<div><dt>Version</dt><dd>10</dd></div>
</dl></section>
<!-- doc:end -->
<footer class="doc">generated</footer>
</div>
<script>
(function () { var toggle = 1; })();
</script>
</body>
</html>
"""
OLD = {
    "schemaVersion": 1,
    "source": {"repository": "GBrooks1970/test-automation-portfolio", "path": "portfolio-docs/X.md", "commit": "a" * 40, "note": "n"},
    "title": "old",
    "style": "old",
    "html": "old",
}


class ExtractTests(unittest.TestCase):
    def test_extracts_every_field_from_the_source_page(self):
        got = extract(SOURCE)
        self.assertEqual(got["title"], "Doc & Title")
        self.assertEqual(got["style"], ":root { --ink: #111; }")
        self.assertEqual(got["scripts"], {"prePaint": "(function () { var pre = 1; })();", "toggle": "(function () { var toggle = 1; })();"})
        self.assertIn('id="theme-toggle"', got["topbarButton"])
        self.assertTrue(got["html"].startswith("<h1>Doc</h1>"))
        self.assertTrue(got["html"].endswith("</section>\n"))
        self.assertNotIn("doc:begin", got["html"])
        self.assertNotIn("<footer", got["html"])

    def test_windows_line_endings_give_the_same_result(self):
        self.assertEqual(extract(SOURCE.replace("\n", "\r\n")), extract(SOURCE))

    def test_missing_or_duplicate_markers_fail(self):
        with self.assertRaises(ValueError):
            extract(SOURCE.replace("<!-- doc:end -->", ""))
        with self.assertRaises(ValueError):
            extract(SOURCE.replace("<!-- doc:begin -->", "<!-- doc:begin --><!-- doc:begin -->"))

    def test_markers_in_the_wrong_order_fail(self):
        swapped = SOURCE.replace("<!-- doc:begin -->", "@@").replace("<!-- doc:end -->", "<!-- doc:begin -->").replace("@@", "<!-- doc:end -->")
        with self.assertRaises(ValueError):
            extract(swapped)

    def test_a_missing_script_switch_or_style_fails(self):
        with self.assertRaises(ValueError):
            extract(SOURCE.replace("<script>(function () { var pre = 1; })();</script>\n", ""))
        with self.assertRaises(ValueError):
            extract(SOURCE.replace('id="theme-toggle"', 'id="other"'))
        with self.assertRaises(ValueError):
            extract(SOURCE.replace("<style>", "<styl>").replace("</style>", "</styl>"))


class BuildTests(unittest.TestCase):
    def test_builds_the_version_2_snapshot_in_the_expected_key_order(self):
        snap = build_snapshot(OLD, extract(SOURCE), SHA, "LAND-14", WHEN)
        self.assertEqual(list(snap), ["schemaVersion", "source", "snapshot", "title", "style", "scripts", "topbarButton", "html"])
        self.assertEqual(snap["schemaVersion"], 2)
        self.assertEqual(snap["source"]["commit"], SHA)
        self.assertEqual(snap["source"]["repository"], OLD["source"]["repository"])
        self.assertEqual(snap["snapshot"], {"refreshed": WHEN, "item": "LAND-14"})

    def test_bad_arguments_fail(self):
        cases = [
            ("6fe8133", "LAND-14", WHEN),
            (SHA.upper(), "LAND-14", WHEN),
            (SHA, "land-14", WHEN),
            (SHA, "LAND-", WHEN),
            (SHA, "LAND-14", "2026-10-07 17:54"),
        ]
        for commit, item, when in cases:
            with self.assertRaises(ValueError, msg=(commit, item, when)):
                validate_arguments(commit, item, when)

    def test_the_file_layout_is_one_space_indent_with_a_trailing_newline_and_round_trips(self):
        snap = build_snapshot(OLD, extract(SOURCE), SHA, "LAND-14", WHEN)
        text = dumps(snap)
        self.assertTrue(text.startswith('{\n "schemaVersion": 2,'))
        self.assertTrue(text.endswith("}\n"))
        self.assertEqual(json.loads(text), snap)

    def test_matches_source_names_the_differing_fields(self):
        snap = build_snapshot(OLD, extract(SOURCE), SHA, "LAND-14", WHEN)
        self.assertEqual(matches_source(snap, extract(SOURCE)), [])
        changed = dict(snap, html="other", style="other")
        self.assertEqual(matches_source(changed, extract(SOURCE)), ["style", "html"])


if __name__ == "__main__":
    unittest.main()
