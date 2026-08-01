from __future__ import annotations

import argparse
import sys
import unittest
from pathlib import Path

from check_registry_parity import check_registry_parity
from check_site import SiteError, check_site
from generate_site import SourceError


ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the complete portfolio pull-request gate locally."
    )
    parser.add_argument(
        "--registry-repository",
        type=Path,
        required=True,
        help="Full-history checkout of NeoCognitus70/portfolio-prompts.",
    )
    parser.add_argument(
        "--skip-external",
        action="store_true",
        help="Skip live URL checks for offline diagnosis; this is not equivalent to CI.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        showcase_count, methodology_count = check_registry_parity(
            args.registry_repository
        )
        site = check_site(check_external=not args.skip_external)
    except (OSError, RuntimeError, SiteError, SourceError, ValueError) as exc:
        print(f"portfolio-verify: ERROR — {exc}", file=sys.stderr)
        return 2

    print(
        "portfolio-verify: sources PASS — "
        f"{showcase_count} showcase, {methodology_count} methodology, "
        f"{site.interactive_elements} named controls, {site.internal_references} internal "
        f"references, {site.external_urls} external URLs, {site.contrast_pairs} contrast pairs"
    )
    suite = unittest.defaultTestLoader.discover(
        str(ROOT / "tools" / "tests"), pattern="test_*.py"
    )
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        return 1
    print(f"portfolio-verify: PASS — {result.testsRun} tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
