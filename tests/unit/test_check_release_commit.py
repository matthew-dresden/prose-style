"""Tests for scripts.check_release_commit."""

from scripts.check_release_commit import parse_release_commit


def test_release_commit_detected_with_version():
    result = parse_release_commit("chore(release): v0.2.0 (#4)\n\nbody")
    assert result == {"should_skip": True, "release_version": "0.2.0"}


def test_release_commit_without_v_prefix():
    result = parse_release_commit("chore(release): 1.2.3")
    assert result == {"should_skip": True, "release_version": "1.2.3"}


def test_feature_commit_not_a_release():
    result = parse_release_commit("feat: add rule (#3)")
    assert result == {"should_skip": False, "release_version": ""}


def test_chore_without_release_prefix_not_a_release():
    result = parse_release_commit("chore: tidy scripts")
    assert result["should_skip"] is False


def test_release_prefix_without_version_not_matched():
    result = parse_release_commit("chore(release): notes")
    assert result["should_skip"] is False


def test_partial_version_not_matched():
    result = parse_release_commit("chore(release): v0.2")
    assert result["should_skip"] is False
