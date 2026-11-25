"""The contributor installer never replaces a skill it did not create, and --uninstall removes only its own links.

Each test loads the script with HOME and XDG_CONFIG_HOME pointed at pytest's tmp_path, so the real
home folder is never read or written. The script still deploys this repository's real concepts, as
relative links inside that temporary home.
"""

import importlib.util
import os
from pathlib import Path
import sys

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "deploy-local-skills.py"
REPO = SCRIPT.parents[1]
NAME = "guardrails"  # a deployed public concept


@pytest.fixture
def deploy(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(home / ".config"))
    spec = importlib.util.spec_from_file_location("deploy_local_skills_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.HOME == home, "the script must read the temporary home, never the real one"
    return module


@pytest.fixture
def run(deploy, monkeypatch, capsys):
    def invoke(*args):
        monkeypatch.setattr(sys, "argv", ["deploy-local-skills.py", *args])
        assert deploy.main() == 0
        return capsys.readouterr().out
    return invoke


def report_lines(out, verb):
    return [line for line in out.splitlines() if line.startswith(verb)]


def foreign_skill(tmp_path, name=NAME):
    """A skill folder that belongs to someone else, outside this repository."""
    folder = tmp_path / "their-collection" / name
    folder.mkdir(parents=True)
    (folder / "SKILL.md").write_text("---\nname: theirs\n---\n")
    return folder


def test_foreign_symlink_with_a_concept_name_is_kept(deploy, run, tmp_path):
    foreign = foreign_skill(tmp_path)
    link = deploy.GLOBAL_SKILLS / NAME
    link.parent.mkdir(parents=True)
    link.symlink_to(foreign)

    out = run()

    assert link.resolve() == foreign.resolve()
    assert any(NAME in line for line in report_lines(out, "skip")), out


def test_own_stale_link_into_this_repo_is_replaced(deploy, run):
    link = deploy.GLOBAL_SKILLS / NAME
    link.parent.mkdir(parents=True)
    retired = REPO / "concepts" / "retired-concept" / "body"  # no longer in the repository
    link.symlink_to(deploy.rel_target(retired, link.parent))

    out = run()

    assert link.resolve() == (REPO / "concepts" / NAME / "body").resolve()
    assert report_lines(out, "update"), out


def test_private_concept_link_is_own_and_uninstalled(deploy, run):
    private_body = deploy.PRIVATE_CONCEPTS / "zz-private-check" / "body"
    private_body.mkdir(parents=True)
    (private_body / "SKILL.md").write_text("---\nname: zz-private-check\n---\n")
    run()
    link = deploy.GLOBAL_SKILLS / "zz-private-check"
    assert link.is_symlink()

    run("--uninstall")

    assert not os.path.lexists(link)


def test_uninstall_removes_only_own_links(deploy, run, tmp_path):
    run()
    foreign = foreign_skill(tmp_path)
    clash = deploy.GLOBAL_SKILLS / NAME
    clash.unlink()
    clash.symlink_to(foreign)
    other = foreign_skill(tmp_path, "their-other-skill")
    (deploy.GLOBAL_SKILLS / "their-other-skill").symlink_to(other)
    own_folder = deploy.GLOBAL_SKILLS / "their-folder"
    own_folder.mkdir()
    (own_folder / "SKILL.md").write_text("theirs\n")

    out = run("--uninstall")

    assert clash.resolve() == foreign.resolve()
    assert (deploy.GLOBAL_SKILLS / "their-other-skill").resolve() == other.resolve()
    assert (own_folder / "SKILL.md").read_text() == "theirs\n"
    remaining = {entry.name for entry in deploy.GLOBAL_SKILLS.iterdir() if entry.is_symlink()}
    assert remaining == {NAME, "their-other-skill"}
    for target in (deploy.PI_SKILLS, deploy.CLAUDE_SKILLS):
        assert not any(entry.is_symlink() for entry in target.iterdir()), target
    assert report_lines(out, "remove"), out


def test_uninstall_dry_run_changes_nothing(deploy, run):
    run()
    link = deploy.GLOBAL_SKILLS / NAME

    out = run("--uninstall", "--dry-run")

    assert link.is_symlink()
    assert report_lines(out, "remove"), out


def test_uninstall_rejects_deploy_only_flags(deploy, run, capsys):
    run()

    with pytest.raises(SystemExit) as refused:
        run("--uninstall", "--force")

    assert refused.value.code == 2
    assert "--uninstall" in capsys.readouterr().err
