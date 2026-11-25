"""work_index.py `Review:` and `Gate:` lines in a step's Notes: --json parses them per step; --check warns on bad ones."""
import json
from pathlib import Path
import subprocess
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "body/work_index.py"
AGENTS = "# demo\n\nStages: now, next, later\n"
README = "# Work\n\n<!-- work-index:start -->\n<!-- work-index:end -->\n"
STEPS = """- [x] First step.
  Notes: done 2026-11-25.
  Review: changes requested by reviewer-subagent 2026-11-24
  Review: approved by reviewer-subagent 2026-11-25
  Gate: pass python3 -m pytest tests at 0123abc 2026-11-25
- [x] Second step. Notes: Gate: fail make check at 0123456789abcdef0123456789abcdef01234567 2026-11-25
- [ ] Third step.
"""
BAD = """- [x] First step.
  Notes: done.
  Review: looks good to me
  Gate: passed yesterday
- [x] Second step.
  Notes: Review: approved by owner 2026-11-25
"""


def plan(steps):
    return f"# Item\n\nWhy: w.\nBlocked by: nothing\n\n## Steps\n\n{steps}\n## Outcome\n\n"


def project(root, **files):
    for rel, text in {".bc-agent/AGENTS.md": AGENTS, "work/README.md": README, "work/0-ideas.md": "# Ideas\n", **files}.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)


def run(root, *flags):
    return subprocess.run([sys.executable, str(SCRIPT), *flags, str(root / "work")], capture_output=True, text=True)


def test_json_parses_review_and_gate_lines_per_step(tmp_path):
    project(tmp_path, **{"work/2-active/001-thing.md": plan(STEPS)})
    result = run(tmp_path, "--json")
    assert result.returncode == 0, result.stderr
    first, second, third = json.loads(result.stdout)["items"][0]["steps"]
    assert first["review"] == [
        {"result": "changes requested", "reviewer": "reviewer-subagent", "date": "2026-11-24",
         "text": "changes requested by reviewer-subagent 2026-11-24"},
        {"result": "approved", "reviewer": "reviewer-subagent", "date": "2026-11-25",
         "text": "approved by reviewer-subagent 2026-11-25"},
    ]
    assert first["gate"] == [{"result": "pass", "command": "python3 -m pytest tests", "commit": "0123abc",
                              "date": "2026-11-25", "text": "pass python3 -m pytest tests at 0123abc 2026-11-25"}]
    assert first["notes"].startswith("done 2026-11-25.")
    assert second["review"] == []
    assert second["gate"][0]["result"] == "fail" and second["gate"][0]["command"] == "make check"
    assert second["gate"][0]["commit"] == "0123456789abcdef0123456789abcdef01234567"
    assert third["review"] == [] and third["gate"] == []


def test_json_keeps_malformed_lines_with_null_fields(tmp_path):
    project(tmp_path, **{"work/2-active/001-thing.md": plan(BAD)})
    first, second = json.loads(run(tmp_path, "--json").stdout)["items"][0]["steps"]
    assert first["review"] == [{"result": None, "reviewer": None, "date": None, "text": "looks good to me"}]
    assert first["gate"] == [{"result": None, "command": None, "commit": None, "date": None, "text": "passed yesterday"}]
    assert second["review"][0]["reviewer"] == "owner"


def test_check_warns_on_malformed_review_and_gate_without_changing_exit(tmp_path):
    project(tmp_path, **{"work/2-active/001-bad.md": plan(BAD), "work/2-active/002-good.md": plan(STEPS),
                         "work/3-done/2026-11/003-done.md": plan(BAD)})
    assert run(tmp_path).returncode == 0
    result = run(tmp_path, "--check")
    assert result.returncode == 0, result.stderr
    warnings = [line for line in result.stderr.splitlines() if "Review:" in line or "Gate:" in line]
    assert any("001-bad" in w and "Review:" in w and "malformed" in w for w in warnings), result.stderr
    assert any("001-bad" in w and "Gate:" in w and "malformed" in w for w in warnings), result.stderr
    assert any("003-done" in w for w in warnings)
    assert not any("002-good" in w for w in warnings)
    assert len(warnings) == 4, result.stderr
