"""Tests for scripts.calculate_version."""

import pytest

from scripts.calculate_version import (
    _apply_bump,
    _find_latest_version,
    _parse_semver,
    calculate_version,
)


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("1.2.3", (1, 2, 3)), ("0.0.0", (0, 0, 0)), ("10.20.30", (10, 20, 30))],
)
def test_parse_semver_valid(raw, expected):
    assert _parse_semver(raw) == expected


@pytest.mark.parametrize("raw", ["1.2", "1.2.3.4", "a.b.c", "1.x.3", ""])
def test_parse_semver_invalid(raw):
    assert _parse_semver(raw) is None


def test_apply_bump_major_resets():
    assert _apply_bump((1, 2, 3), "major") == (2, 0, 0)


def test_apply_bump_minor_resets_patch():
    assert _apply_bump((1, 2, 3), "minor") == (1, 3, 0)


def test_apply_bump_patch_increments():
    assert _apply_bump((1, 2, 3), "patch") == (1, 2, 4)


def test_find_latest_version_returns_max():
    tags = ["v0.0.9", "v0.1.0", "v0.0.10"]
    version, is_initial = _find_latest_version(tags, "v")
    assert version == (0, 1, 0)
    assert is_initial is False


def test_find_latest_version_initial_when_no_tags():
    version, is_initial = _find_latest_version([], "v")
    assert version == (0, 0, 0)
    assert is_initial is True


def test_find_latest_version_ignores_non_semver_tags():
    tags = ["v0.1.0", "v-not-a-version"]
    version, is_initial = _find_latest_version(tags, "v")
    assert version == (0, 1, 0)


def test_calculate_version_computes_next_tag(monkeypatch):
    monkeypatch.setattr(
        "scripts.calculate_version._git_tags_for_prefix", lambda prefix: ["v0.1.0"]
    )
    monkeypatch.setattr("scripts.calculate_version._git_tag_exists", lambda tag: False)
    result = calculate_version("v", "minor")
    assert result == {
        "tag_prefix": "v",
        "current_version": "0.1.0",
        "next_version": "0.2.0",
        "bump_type": "minor",
        "full_tag": "v0.2.0",
        "is_initial": False,
    }


def test_calculate_version_rejects_existing_tag(monkeypatch):
    monkeypatch.setattr(
        "scripts.calculate_version._git_tags_for_prefix", lambda prefix: ["v0.1.0"]
    )
    monkeypatch.setattr("scripts.calculate_version._git_tag_exists", lambda tag: True)
    with pytest.raises(SystemExit):
        calculate_version("v", "patch")


def test_calculate_version_rejects_invalid_bump_type():
    with pytest.raises(SystemExit):
        calculate_version("v", "mega")
