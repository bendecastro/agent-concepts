"""The published starter items can be filed in a freshly scaffolded work folder."""
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

BODY = Path(__file__).resolve().parents[1] / "body"


@pytest.fixture
def project(tmp_path):
    root = tmp_path / "demo"
    root.mkdir()
    try:
        subprocess.run(
            [sys.executable, str(BODY / "scaffold.py"), "--root", str(root),
             "--slug", "demo", "--date", "2026-01-02", "--archetype", "code"],
            check=True, capture_output=True, text=True,
        )
        yield root
    finally:
        shutil.rmtree(root)


def published_starters():
    reference = (BODY / "starter-items.md").read_text(encoding="utf-8")
    return dict(re.findall(
        r"^## ([a-z-]+)\n\nApplies when: [^\n]+\n\n```markdown\n(.*?)^```$",
        reference, re.MULTILINE | re.DOTALL,
    ))


def file_starters(project, expected):
    """File each expected starter item in order and run the project's index check."""
    starters = published_starters()
    work = project / "work"
    items = []
    for number, (slug, (kind, owner_command)) in enumerate(expected.items(), 1):
        item = starters[slug].replace("{{stage}}", "next").replace("{{date}}", "2026-01-02")
        header, steps_and_outcome = item.split("\n## Steps\n")
        steps, _ = steps_and_outcome.split("\n## Outcome\n")
        assert f"Kind: {kind}" in header.splitlines(), slug
        assert "Source: bc-setup-project" in header.splitlines(), slug
        assert "Planned: bc-setup-project 2026-01-02" in header.splitlines(), slug
        if owner_command:
            assert any(line.startswith("Needs owner: ") and owner_command in line
                       for line in header.splitlines()), slug
            assert not any(line.startswith("Ready for agent:") for line in header.splitlines()), slug
        else:
            assert "Ready for agent: yes" in header.splitlines(), slug
            step_blocks = re.split(r"(?m)^- \[ \] ", steps.strip())[1:]
            assert step_blocks, slug
            for step in step_blocks:
                assert "Done when" in step and "Out of scope" in step, (slug, step)
        name = f"{number:03d}-{slug}"
        items.append(name)
        (work / "1-planned" / f"{name}.md").write_text(item, encoding="utf-8")

    (work / "order.md").write_text(
        "# Work order\n\n" + "".join(f"{i}. {name}\n" for i, name in enumerate(items, 1)),
        encoding="utf-8",
    )
    index = [sys.executable, str(project / ".bc-agent/scripts/work_index.py")]
    for args in ([], ["--check"]):
        result = subprocess.run(index + args, capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
        assert "warning" not in result.stderr, result.stderr


def test_starter_items_pass_work_index_check(project):
    # Architecture is a top kind in the scaffold's ordering rules.
    expected = {
        "architecture-review": ("architecture", "/bc-improve-codebase-architecture"),
        "design-inventory": ("design", None),
        "guardrails-setup-checks": ("performance", None),
        "issue-triage": ("none", "/bc-triage"),
    }
    file_starters(project, expected)


def test_new_project_starter_items_pass_work_index_check(project):
    # The scaffold alone holds no source code: the new or empty project case.
    expected = {
        "guardrails-for-new-project": ("performance", None),
        "design-for-new-project": ("design", None),
    }
    file_starters(project, expected)
    for slug in expected:
        item = published_starters()[slug]
        # Each waits for code without blocking other work.
        assert "no code yet" in item.split("\n## Steps\n")[1], slug
        assert "Blocked by: nothing" in item.splitlines(), slug


def test_published_starter_items_are_all_covered():
    assert published_starters().keys() == {
        "architecture-review", "design-inventory", "guardrails-setup-checks",
        "issue-triage", "design-for-new-project", "guardrails-for-new-project",
    }


def test_setup_offers_new_project_starter_items():
    skill = (BODY / "SKILL.md").read_text(encoding="utf-8")
    assert "Skip starter items for new or empty projects" not in skill
    assert "guardrails-for-new-project" in skill
    assert "design-for-new-project" in skill
