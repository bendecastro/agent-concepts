"""work_index.py `Replanning:` and `Rounds:` lines: Folder column state, the ready-line error, and --json fields."""
import json
from pathlib import Path
import subprocess
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "body/work_index.py"
AGENTS = "# demo\n\nStages: now, next, later\n"
README = "# Work\n\n<!-- work-index:start -->\n<!-- work-index:end -->\n"


def plan(*lines):
    header = "".join(f"{line}\n" for line in lines)
    return f"# Item\n\nWhy: w.\nBlocked by: nothing\n{header}\n## Steps\n\n- [x] First step.\n- [ ] Second step.\n\n## Outcome\n\n"


def fixture(root, files):
    for rel, text in {"work/README.md": README, "work/0-ideas.md": "# Ideas\n", ".bc-agent/AGENTS.md": AGENTS, **files}.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)


def run(root, *flags):
    return subprocess.run([sys.executable, str(SCRIPT), *flags, str(root / "work")], capture_output=True, text=True)


def test_replanning_item_is_marked_in_the_folder_column(tmp_path):
    fixture(tmp_path, {
        "work/2-active/001-replanned.md": plan("Replanning: second review found a new ordering — decides: owner",
                                               "Waiting on owner: replan or split?"),
        "work/2-active/002-agent-replan.md": plan("Replanning: pressure test failed — decides: agent"),
    })
    result = run(tmp_path)
    assert result.returncode == 0, result.stderr
    readme = (tmp_path / "work/README.md").read_text()
    row1 = next(r for r in readme.splitlines() if "001-replanned" in r)
    row2 = next(r for r in readme.splitlines() if "002-agent-replan" in r)
    assert "active, replanning, waiting on owner" in row1
    assert "active, replanning" in row2 and "waiting" not in row2
    assert run(tmp_path, "--check").returncode == 0


def test_replanning_item_that_is_also_ready_is_an_error(tmp_path):
    fixture(tmp_path, {
        "work/2-active/001-both.md": plan("Ready for agent: yes", "Replanning: new sequence — decides: owner"),
    })
    result = run(tmp_path)
    assert result.returncode == 1
    assert "2-active/001-both.md" in result.stderr
    assert "Replanning" in result.stderr and "Ready for agent" in result.stderr


def test_json_parses_replanning_and_rounds(tmp_path):
    fixture(tmp_path, {
        "work/2-active/001-replanned.md": plan("Replanning: second review found a new ordering — decides: owner",
                                               "Rounds: 3 blocking reviews, 1 replan"),
        "work/2-active/002-malformed.md": plan("Replanning: no decider given", "Rounds: lots"),
        "work/2-active/003-plain.md": plan(),
    })
    result = run(tmp_path, "--json")
    assert result.returncode == 0, result.stderr
    items = {i["name"]: i for i in json.loads(result.stdout)["items"]}
    replanned = items["001-replanned"]
    assert replanned["header"]["replanning"] == "second review found a new ordering — decides: owner"
    assert replanned["header"]["rounds"] == "3 blocking reviews, 1 replan"
    assert replanned["replanning"] == {"reason": "second review found a new ordering", "decider": "owner",
                                       "text": "second review found a new ordering — decides: owner"}
    assert replanned["rounds"] == {"blocking_reviews": 3, "replans": 1, "text": "3 blocking reviews, 1 replan"}
    malformed = items["002-malformed"]
    assert malformed["replanning"] == {"reason": None, "decider": None, "text": "no decider given"}
    assert malformed["rounds"] == {"blocking_reviews": None, "replans": None, "text": "lots"}
    assert items["003-plain"]["replanning"] is None and items["003-plain"]["rounds"] is None
