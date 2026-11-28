"""work_index.py --check: a ready item needs a `Dependencies:` line (error when planned on or after the ship date)."""
from pathlib import Path
import subprocess
import sys

import pytest

SCRIPTS = [Path(__file__).resolve().parents[1] / "body/work_index.py",
           Path(__file__).resolve().parents[3] / ".bc-agent/scripts/work_index.py"]
AGENTS = "# demo\n\nStages: now, next, later\n"
README = "# Work\n\n<!-- work-index:start -->\n<!-- work-index:end -->\n"


def plan(header):
    return f"# Item\n\nWhy: w.\nBlocked by: nothing\n{header}\n## Steps\n\n- [ ] First step.\n\n## Outcome\n\n"


def check(tmp_path, script, header):
    for rel, text in {".bc-agent/AGENTS.md": AGENTS, "work/README.md": README, "work/0-ideas.md": "# Ideas\n",
                      "work/order.md": "# Order\n\n1. 001-thing\n", "work/1-planned/001-thing.md": plan(header)}.items():
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / rel).write_text(text)
    subprocess.run([sys.executable, str(script), str(tmp_path / "work")], check=True)
    return subprocess.run([sys.executable, str(script), "--check", str(tmp_path / "work")], capture_output=True, text=True)


@pytest.mark.parametrize("script", SCRIPTS)
def test_new_ready_item_without_dependencies_fails(tmp_path, script):
    result = check(tmp_path, script, "Planned: bc-plan-to-pipeline 2026-11-28\nReady for agent: yes\n")
    assert result.returncode == 1
    assert "001-thing.md" in result.stderr and "Dependencies:" in result.stderr


@pytest.mark.parametrize("script", SCRIPTS)
def test_new_ready_item_with_dependencies_passes(tmp_path, script):
    result = check(tmp_path, script, "Planned: bc-plan-to-pipeline 2026-12-01\nReady for agent: yes\nDependencies: none new\n")
    assert result.returncode == 0, result.stderr
    assert "Dependencies" not in result.stderr


@pytest.mark.parametrize("script", SCRIPTS)
def test_older_ready_item_without_dependencies_only_warns(tmp_path, script):
    result = check(tmp_path, script, "Planned: bc-plan-to-pipeline 2026-11-27\nReady for agent: yes\n")
    assert result.returncode == 0, result.stderr
    assert "warning" in result.stderr and "Dependencies:" in result.stderr


@pytest.mark.parametrize("header", ["Planned: bc-plan-to-pipeline 2026-11-28\n",
                                    "Planned: bc-plan-to-pipeline 2026-11-28\nWaiting on owner: which package\n"])
@pytest.mark.parametrize("script", SCRIPTS)
def test_parked_item_is_not_checked(tmp_path, script, header):
    result = check(tmp_path, script, header)
    assert result.returncode == 0, result.stderr
    assert "Dependencies" not in result.stderr
