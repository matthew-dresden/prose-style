"""Tests for scripts.validate_pr_title."""

import pytest

from scripts.validate_pr_title import parse_commit_message


def test_valid_feat_maps_to_minor():
    result = parse_commit_message("feat: add dash rule")
    assert result == {
        "valid": True,
        "type": "feat",
        "scope": None,
        "breaking": False,
        "description": "add dash rule",
        "bump": "minor",
    }


def test_valid_fix_with_scope_maps_to_patch():
    result = parse_commit_message("fix(checker): handle empty line")
    assert result["valid"] is True
    assert result["type"] == "fix"
    assert result["scope"] == "checker"
    assert result["bump"] == "patch"


@pytest.mark.parametrize(
    "commit_type",
    ["feat", "perf", "build", "ci", "revert", "release", "meta", "module"],
)
def test_minor_types(commit_type):
    assert parse_commit_message(f"{commit_type}: something")["bump"] == "minor"


@pytest.mark.parametrize(
    "commit_type", ["fix", "chore", "docs", "style", "refactor", "test"]
)
def test_patch_types(commit_type):
    assert parse_commit_message(f"{commit_type}: something")["bump"] == "patch"


def test_bang_marks_breaking_and_major():
    result = parse_commit_message("feat!: rewrite the rules")
    assert result["breaking"] is True
    assert result["bump"] == "major"


def test_release_commit_title_is_valid_conventional():
    result = parse_commit_message("chore(release): v0.2.0")
    assert result["valid"] is True
    assert result["type"] == "chore"
    assert result["scope"] == "release"
    assert result["bump"] == "patch"


def test_empty_message_is_invalid():
    result = parse_commit_message("")
    assert result["valid"] is False
    assert "Empty" in result["error"]


def test_non_conventional_message_is_invalid():
    result = parse_commit_message("updated some stuff")
    assert result["valid"] is False
    assert "conventional commit format" in result["error"]


def test_only_first_line_is_parsed():
    result = parse_commit_message("fix: first line wins\n\nbody text here")
    assert result["valid"] is True
    assert result["description"] == "first line wins"
