#!/usr/bin/env python3
"""Self-checks for the prose-style repository.

Fails on any prose em dash, en dash, or double-hyphen substitute in the
repository's own markdown, and on skill frontmatter that disagrees with the
directory name or carries an empty description. Code fences and inline code
spans are skipped: a "--" inside a command example is an argument, not a
dash standing in for punctuation.

Usage: check_prose.py [file ...]

With no arguments, checks every markdown file in the repository except the
LICENSE and NOTICE legal files.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FENCE = re.compile(r"^\s*```")
INLINE_CODE = re.compile(r"`[^`]*`")
PROSE_DASH = re.compile(r"(?<= )--(?= )|(?<= )--$|^--(?= )")
DASH_CHARACTERS = ("\u2014", "\u2013")


def markdown_files(roots: list[Path]) -> list[Path]:
    if roots:
        return [r for r in roots if r.suffix == ".md"]
    repo = Path(__file__).resolve().parent.parent
    skip = {"LICENSE", "NOTICE"}
    return sorted(p for p in repo.rglob("*.md") if p.name not in skip and ".git" not in p.parts)


def prose_dashes(text: str) -> list[str]:
    findings: list[str] = []
    in_fence = False
    for number, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = INLINE_CODE.sub("", line)
        if PROSE_DASH.search(stripped) or any(c in stripped for c in DASH_CHARACTERS):
            findings.append(f"  line {number}: {line.strip()[:100]}")
    return findings


def frontmatter_problems(path: Path, text: str) -> list[str]:
    if path.name != "SKILL.md":
        return []
    problems: list[str] = []
    if not text.startswith("---\n"):
        problems.append("SKILL.md carries no frontmatter block")
        return problems
    end = text.find("\n---", 4)
    block = text[4:end]
    name = re.search(r"^name:\s*(\S+)\s*$", block, re.MULTILINE)
    description = re.search(r"^description:\s*(.+)$", block, re.MULTILINE)
    if name is None or name.group(1) != path.parent.name:
        problems.append(f"frontmatter name must match the directory name ({path.parent.name})")
    if description is None or not description.group(1).strip():
        problems.append("frontmatter description is missing or empty")
    return problems


def main(argv: list[str]) -> int:
    files = markdown_files([Path(a) for a in argv])
    failed = False
    for path in files:
        text = path.read_text(encoding="utf-8")
        dashes = prose_dashes(text)
        front = frontmatter_problems(path, text)
        if dashes or front:
            failed = True
            print(f"ERROR: {path}")
            for finding in dashes + front:
                print(finding)
    if failed:
        print("\nProse must carry no em dash, en dash, or double-hyphen substitute.")
        print("Rewrite the sentence with the punctuation it calls for.")
        return 1
    print(f"checked {len(files)} markdown file(s): no prose dashes, frontmatter sane")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
