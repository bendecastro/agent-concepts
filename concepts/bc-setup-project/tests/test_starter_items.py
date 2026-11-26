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


def test_starter_items_pass_work_index_check(project):
    reference = (BODY / "starter-items.md").read_text(encoding="utf-8")
    starters = dict(re.findall(
        r"^## ([a-z-]+)\n\nApplies when: [^\n]+\n\n```markdown\n(.*?)^```$",
        reference, re.MULTILINE | re.DOTALL,
    ))
    # Architecture is a top kind in the scaffold's ordering rules.
    expected = {
        "architecture-review": ("architecture", "/bc-improve-codebase-architecture"),
        "design-inventory": ("design", None),
        "guardrails-setup-checks": ("performance", None),
        "issue-triage": ("none", "/bc-triage"),
    }
    assert starters.keys() == expected.keys()
    work = project / "work"
    items = []
    for number, (slug, (kind, owner_command)) in enumerate(expected.items(), 1):
        item = starters[slug].replace("{{stage}}", "next").replace("{{date}}", "2026-01-02")
        header, steps_and_outcome = item.split("\n## Steps\n")
        steps, _ = steps_and_outcome.split("\n## Outcome\n")
        assert f"Kind: {kind}" in header.splitlines(), slug
        assert "Source: bc-setup-project" in header.splitlines(), slug
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
