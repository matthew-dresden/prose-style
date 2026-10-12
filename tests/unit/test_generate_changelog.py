"""Tests for scripts.generate_changelog."""

import pathlib

from scripts.generate_changelog import (
    _format_entry,
    _group_commits,
    _write_changelog,
    generate_changelog,
)


def test_group_commits_sorts_by_section():
    commits = [
        "feat: add rule 11",
        "fix: stop crash on empty file",
        "docs: rewrite readme intro",
        "not-a-conventional-commit",
    ]
    sections = _group_commits(commits)
    assert sections["Added"] == ["add rule 11"]
    assert sections["Fixed"] == ["stop crash on empty file"]
    assert sections["Documentation"] == ["rewrite readme intro"]
    assert len(sections) == 3


def test_group_commits_breaking_goes_to_both_sections():
    sections = _group_commits(["feat!: new contract"])
    assert sections["Breaking Changes"] == ["new contract"]
    assert sections["Added"] == ["new contract"]


def test_format_entry_orders_sections():
    sections = {
        "Fixed": ["b fix"],
        "Added": ["a feat"],
        "Breaking Changes": ["z boom"],
    }
    entry = _format_entry("0.2.0", "2026-10-12", sections)
    lines = entry.splitlines()
    assert lines[0] == "## [0.2.0] - 2026-10-12"
    assert lines.index("### Breaking Changes") < lines.index("### Added")
    assert lines.index("### Added") < lines.index("### Fixed")
    assert "- a feat" in lines
    assert entry.endswith("\n")


def test_write_changelog_inserts_after_title(tmp_path):
    changelog = tmp_path / "CHANGELOG.md"
    changelog.write_text(
        "# Changelog\n\n## [0.1.0] - 2026-01-01\n\n### Added\n\n- old\n"
    )
    _write_changelog(changelog, "## [0.2.0] - 2026-10-12\n\n### Added\n\n- new\n")
    content = changelog.read_text()
    assert content.index("## [0.2.0]") < content.index("## [0.1.0]")
    assert content.startswith("# Changelog\n")


def test_write_changelog_creates_file_with_header(tmp_path):
    changelog = tmp_path / "sub" / "CHANGELOG.md"
    _write_changelog(changelog, "## [0.2.0] - 2026-10-12\n")
    content = changelog.read_text()
    assert content.startswith("# Changelog\n")
    assert "## [0.2.0]" in content


def test_generate_changelog_end_to_end(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "scripts.generate_changelog._find_last_tag", lambda prefix: "v0.1.0"
    )
    monkeypatch.setattr(
        "scripts.generate_changelog._get_commits",
        lambda last_tag: ["feat: change one", "fix: change two"],
    )
    path = generate_changelog(version="0.2.0", tag_prefix="v")
    assert path == "CHANGELOG.md"
    content = pathlib.Path("CHANGELOG.md").read_text()
    assert content.startswith("# Changelog\n")
    assert "## [0.2.0]" in content
    assert "- change one" in content
    assert "- change two" in content
