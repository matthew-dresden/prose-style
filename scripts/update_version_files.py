"""Update version fields in pyproject.toml and the SKILL.md frontmatter.

The release pipeline owns both version fields. Manual edits are rejected
by scripts/check_version_immutability.py.

Usage:
    python3 scripts/update_version_files.py --version 0.2.0

Output (JSON to stdout):
    {"files_updated": ["pyproject.toml", "SKILL.md"]}

Exit code 0 on success, 1 on error.
"""

import argparse
import json
import pathlib
import re
import sys

PYPROJECT_VERSION_PATTERN = re.compile(r'^(version\s*=\s*)"[^"]*"', re.MULTILINE)
SKILL_VERSION_PATTERN = re.compile(r'^(  version:\s*)"[^"]*"', re.MULTILINE)


def update_pyproject_version(version: str) -> str:
    """Update the version field in pyproject.toml under the [project] section.

    Args:
        version: New semver version string (e.g. "0.2.0").

    Returns:
        The file path that was updated.

    Raises:
        SystemExit: If pyproject.toml is not found or the version line cannot be located.
    """
    pyproject_path = pathlib.Path("pyproject.toml")

    if not pyproject_path.exists():
        sys.stderr.write(
            f"ERROR: pyproject.toml not found at {pyproject_path.resolve()}\n"
        )
        sys.exit(1)

    content = pyproject_path.read_text()
    new_content, count = PYPROJECT_VERSION_PATTERN.subn(
        f'\\1"{version}"', content, count=1
    )

    if count == 0:
        sys.stderr.write("ERROR: Could not find version field in pyproject.toml\n")
        sys.exit(1)

    pyproject_path.write_text(new_content)

    return str(pyproject_path)


def update_skill_version(version: str) -> str:
    """Update the metadata.version field in the SKILL.md frontmatter.

    Args:
        version: New semver version string (e.g. "0.2.0").

    Returns:
        The file path that was updated.

    Raises:
        SystemExit: If SKILL.md is not found or the version line cannot be located.
    """
    skill_path = pathlib.Path("SKILL.md")

    if not skill_path.exists():
        sys.stderr.write(f"ERROR: SKILL.md not found at {skill_path.resolve()}\n")
        sys.exit(1)

    content = skill_path.read_text()
    new_content, count = SKILL_VERSION_PATTERN.subn(f'\\1"{version}"', content, count=1)

    if count == 0:
        sys.stderr.write(
            "ERROR: Could not find '  version:' field in SKILL.md frontmatter\n"
        )
        sys.exit(1)

    skill_path.write_text(new_content)

    return str(skill_path)


def update_version_files(version: str) -> list[str]:
    """Update every version file owned by the release pipeline.

    Args:
        version: New semver version string (e.g. "0.2.0").

    Returns:
        List of file paths (relative to repo root) that were updated.
    """
    return [
        update_pyproject_version(version),
        update_skill_version(version),
    ]


def main() -> None:
    """CLI entry point for updating version files.

    Outputs a JSON object with the list of files updated to stdout.
    Exits with code 0 on success, code 1 on error.
    """
    parser = argparse.ArgumentParser(
        description="Update version fields in pyproject.toml and the SKILL.md frontmatter"
    )
    parser.add_argument(
        "--version",
        required=True,
        help="New semver version string (e.g. '0.2.0')",
    )
    args = parser.parse_args()

    files_updated = update_version_files(version=args.version)

    output = json.dumps({"files_updated": files_updated})
    sys.stdout.write(output + "\n")


if __name__ == "__main__":
    main()
