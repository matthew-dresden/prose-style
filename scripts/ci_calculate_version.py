"""CI wrapper for version calculation with GITHUB_OUTPUT.

Parses the squash commit message, calculates the next version from git
tags, and writes workflow outputs.

Usage:
    python3 -m scripts.ci_calculate_version \
        --commit-message "feat: add export (#3)" \
        --output "$GITHUB_OUTPUT"

Outputs written to $GITHUB_OUTPUT:
    next_version, bump_type, full_tag, is_initial

Exit code 0 on success, 1 on error.
"""

import argparse
import pathlib
import sys

from scripts.calculate_version import calculate_version
from scripts.constants import TAG_PREFIX
from scripts.validate_pr_title import parse_commit_message


def main() -> None:
    """CLI entry point for the CI version calculation wrapper."""
    parser = argparse.ArgumentParser(
        description="Calculate next version and emit GitHub Actions outputs."
    )
    parser.add_argument(
        "--commit-message",
        required=True,
        help="The squash commit message (PR title for squash merges).",
    )
    parser.add_argument(
        "--tag-prefix",
        default=TAG_PREFIX,
        help="Tag prefix for releases (default: v).",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Path to the GitHub Actions output file.",
    )
    args = parser.parse_args()

    parsed = parse_commit_message(args.commit_message)
    if not parsed["valid"]:
        print(f"::error::{parsed['error']}", file=sys.stderr)
        sys.exit(1)
    if not parsed["bump"]:
        print(
            f"::error::commit type '{parsed['type']}' does not map to a version bump",
            file=sys.stderr,
        )
        sys.exit(1)

    result = calculate_version(args.tag_prefix, parsed["bump"])

    with pathlib.Path(args.output).open("a") as f:
        f.write(f"next_version={result['next_version']}\n")
        f.write(f"bump_type={result['bump_type']}\n")
        f.write(f"full_tag={result['full_tag']}\n")
        f.write(f"is_initial={'true' if result['is_initial'] else 'false'}\n")

    print(
        f"version: {result['current_version']} -> {result['next_version']} "
        f"({result['bump_type']}, tag {result['full_tag']})"
    )


if __name__ == "__main__":
    main()
