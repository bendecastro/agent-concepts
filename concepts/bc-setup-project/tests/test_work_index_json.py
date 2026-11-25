"""work_index.py --json: the work data a dashboard reads (reference page: body/work-data.md)."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

from hypothesis import given, strategies as st

SCRIPT = Path(__file__).resolve().parents[1] / "body/work_index.py"
README = "# Work\n\nIntro.\n\n<!-- work-index:start -->\n<!-- work-index:end -->\n"
AGENTS = "# demo\n\nStages: now, next, later\n"
ACTIVE = """# Dashboard data

Why: people want a dashboard. Second sentence.
Done when: it prints JSON.
Stage: now
Blocked by: 001-base
Kind: feature
Source: bc-plan-to-pipeline
Planned: bc-plan-to-pipeline 2026-11-25
Ready for agent: yes

## Steps

- [x] First step: does a thing.
  Notes: done 2026-11-25; see the test.
- [ ] Second step. Blocked by: First step. Notes: inline note here.
- [X] Third step
  spans two lines.

## Outcome

<Filled when the item is finished or dropped.>
"""
DONE = "# Base\n\nWhy: base.\nDone when: x.\n\n## Steps\n\n- [x] only\n\n## Outcome\n\nShipped it.\nTwo lines.\n"


def fixture(root):
    files = {
        "work/README.md": README,
        "work/0-ideas.md": "# Ideas\n",
        ".bc-agent/AGENTS.md": AGENTS,
        "work/2-active/025-dashboard-data/plan.md": ACTIVE,
        "work/1-planned/030-waiting.md": "# Waiting\n\nWhy: w.\nBlocked by: nothing\nWaiting on owner: which colour?\n",
        "work/3-done/2026-11/001-base/plan.md": DONE,
        "work/4-dropped/002-gone.md": "# Gone\n\nWhy: g.\n\n## Outcome\n\nNot needed.\n",
    }
    for path, text in files.items():
        (root / path).parent.mkdir(parents=True, exist_ok=True)
        (root / path).write_text(text)
    return root


def run(root, *args):
    return subprocess.run([sys.executable, str(SCRIPT), *args, str(root / "work")], capture_output=True, text=True)


def snapshot(root):
    return {p: p.read_bytes() for p in sorted(root.rglob("*")) if p.is_file()}


def test_json_prints_every_item_with_header_steps_and_outcome(tmp_path):
    fixture(tmp_path)
    result = run(tmp_path, "--json")
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["format_version"] == 1
    assert data["stages"] == ["now", "next", "later"]
    assert [(i["folder"], i["name"]) for i in data["items"]] == [
        ("planned", "030-waiting"), ("active", "025-dashboard-data"), ("done", "001-base"), ("dropped", "002-gone")]
    active = data["items"][1]
    assert active == {
        "number": "025", "slug": "dashboard-data", "name": "025-dashboard-data", "folder": "active",
        "path": "2-active/025-dashboard-data/plan.md", "title": "Dashboard data",
        "header": {
            "why": "people want a dashboard. Second sentence.", "done_when": "it prints JSON.", "stage": "now",
            "blocked_by": "001-base", "kind": "feature", "source": "bc-plan-to-pipeline",
            "planned": "bc-plan-to-pipeline 2026-11-25", "ready_for_agent": "yes", "waiting_on_owner": None,
            "held_by": None,
        },
        "steps": [
            {"text": "First step: does a thing.", "checked": True, "notes": "done 2026-11-25; see the test."},
            {"text": "Second step. Blocked by: First step.", "checked": False, "notes": "inline note here."},
            {"text": "Third step\nspans two lines.", "checked": True, "notes": None},
        ],
        "outcome": "<Filled when the item is finished or dropped.>",
        "history": [], "held_by": None,
    }
    done, dropped = data["items"][2], data["items"][3]
    assert done["path"] == "3-done/2026-11/001-base/plan.md"
    assert done["outcome"] == "Shipped it.\nTwo lines."
    assert dropped["header"]["blocked_by"] is None and dropped["steps"] == []
    assert data["items"][0]["header"]["waiting_on_owner"] == "which colour?"


def test_json_writes_no_files(tmp_path):
    fixture(tmp_path)
    before = snapshot(tmp_path)
    assert run(tmp_path, "--json").returncode == 0
    assert snapshot(tmp_path) == before


def test_check_and_default_ignore_closed_items_as_before(tmp_path):
    fixture(tmp_path)
    assert run(tmp_path).returncode == 0
    assert "025-dashboard-data" in (tmp_path / "work/README.md").read_text()
    assert run(tmp_path, "--check").returncode == 0


def load_module():
    spec = importlib.util.spec_from_file_location("work_index", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


WORK_INDEX = load_module()
LINE = st.text(st.characters(blacklist_categories=("Cc", "Cs", "Zl", "Zp")), min_size=1, max_size=30).map(
    lambda s: s.strip()).filter(lambda s: s and "Notes:" not in s and not s.startswith(("-", "#")))


@given(st.lists(st.tuples(LINE, st.booleans(), st.one_of(st.none(), LINE)), max_size=6))
def test_steps_parse_inverts_plan_format(steps):
    body = "".join(f"- [{'x' if c else ' '}] {t}\n" + (f"  Notes: {n}\n" if n else "") for t, c, n in steps)
    text = f"# T\n\nWhy: w.\n\n## Steps\n\n{body}\n## Outcome\n\n"
    parsed = WORK_INDEX.parse_steps(text)
    assert [(s["text"], s["checked"], s["notes"]) for s in parsed] == steps
