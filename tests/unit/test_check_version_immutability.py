"""Tests for scripts.check_version_immutability."""

from scripts.check_version_immutability import get_removed_version_lines


def _fake_diff(monkeypatch, diff_output):
    calls = {}

    def fake_run(cmd, capture_output, text, check):
        calls["cmd"] = cmd

        class Result:
            returncode = 0
            stdout = diff_output
            stderr = ""

        return Result()

    monkeypatch.setattr("subprocess.run", fake_run)
    return calls


def test_version_line_change_detected(monkeypatch):
    diff = (
        "diff --git a/pyproject.toml b/pyproject.toml\n"
        "--- a/pyproject.toml\n"
        "+++ b/pyproject.toml\n"
        "@@ -2,1 +2,1 @@\n"
        '-version = "0.1.0"\n'
        '+version = "9.9.9"\n'
    )
    calls = _fake_diff(monkeypatch, diff)
    removed = get_removed_version_lines("origin/main")
    assert removed == ['-version = "0.1.0"']
    assert calls["cmd"][0:3] == ["git", "diff", "origin/main..HEAD"]


def test_version_line_addition_allowed(monkeypatch):
    diff = 'diff --git a/pyproject.toml b/pyproject.toml\n+version = "0.1.0"\n'
    _fake_diff(monkeypatch, diff)
    assert get_removed_version_lines("origin/main") == []


def test_version_line_removal_detected(monkeypatch):
    diff = 'diff --git a/SKILL.md b/SKILL.md\n-  version: "0.1.0"\n'
    _fake_diff(monkeypatch, diff)
    assert len(get_removed_version_lines("origin/main")) == 1


def test_regular_change_not_flagged(monkeypatch):
    diff = "diff --git a/README.md b/README.md\n-old text\n+new text\n"
    _fake_diff(monkeypatch, diff)
    assert get_removed_version_lines("origin/main") == []


def test_name_line_not_flagged(monkeypatch):
    diff = 'diff --git a/pyproject.toml b/pyproject.toml\n+name = "prose-style"\n'
    _fake_diff(monkeypatch, diff)
    assert get_removed_version_lines("origin/main") == []


def test_git_failure_exits(monkeypatch):
    def failing_run(cmd, capture_output, text, check):
        class Result:
            returncode = 128
            stdout = ""
            stderr = "fatal: bad revision"

        return Result()

    monkeypatch.setattr("subprocess.run", failing_run)
    try:
        get_removed_version_lines("bogus")
        assert False, "expected SystemExit"
    except SystemExit as exit_exc:
        assert exit_exc.code == 1
