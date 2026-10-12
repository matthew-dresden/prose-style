"""Tests for scripts.update_version_files."""

import pathlib

import pytest

from scripts.update_version_files import (
    update_pyproject_version,
    update_skill_version,
    update_version_files,
)

PYPROJECT = '[project]\nname = "prose-style"\nversion = "0.1.0"\n'
SKILL = '---\nname: prose-style\ndescription: test\nmetadata:\n  version: "0.1.0"\n  trigger: t\n---\n\n# Title\n'


@pytest.fixture
def repo_dir(tmp_path, monkeypatch):
    (tmp_path / "pyproject.toml").write_text(PYPROJECT)
    (tmp_path / "SKILL.md").write_text(SKILL)
    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_update_pyproject_version(repo_dir):
    update_pyproject_version("0.2.0")
    content = (repo_dir / "pyproject.toml").read_text()
    assert 'version = "0.2.0"' in content
    assert 'name = "prose-style"' in content


def test_update_skill_version(repo_dir):
    update_skill_version("0.2.0")
    content = (repo_dir / "SKILL.md").read_text()
    assert '  version: "0.2.0"' in content
    assert content.startswith("---\nname: prose-style")


def test_update_version_files_returns_both(repo_dir):
    files = update_version_files("1.0.0")
    assert files == ["pyproject.toml", "SKILL.md"]
    assert 'version = "1.0.0"' in (repo_dir / "pyproject.toml").read_text()
    assert '  version: "1.0.0"' in (repo_dir / "SKILL.md").read_text()


def test_missing_pyproject_exits(repo_dir):
    (repo_dir / "pyproject.toml").unlink()
    with pytest.raises(SystemExit):
        update_pyproject_version("0.2.0")


def test_missing_skill_exits(repo_dir):
    (repo_dir / "SKILL.md").unlink()
    with pytest.raises(SystemExit):
        update_skill_version("0.2.0")


def test_pyproject_without_version_line_exits(repo_dir):
    (repo_dir / "pyproject.toml").write_text('[project]\nname = "prose-style"\n')
    with pytest.raises(SystemExit):
        update_pyproject_version("0.2.0")


def test_skill_without_version_line_exits(repo_dir):
    (repo_dir / "SKILL.md").write_text("---\nname: prose-style\n---\n")
    with pytest.raises(SystemExit):
        update_skill_version("0.2.0")
