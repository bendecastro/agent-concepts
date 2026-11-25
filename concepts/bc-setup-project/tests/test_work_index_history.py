"""work_index.py --json `history`: folder moves and step ticks read from git, following renames."""
import json
from pathlib import Path
import os
import subprocess
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "body/work_index.py"
AGENTS = "# demo\n\nStages: now, next, later\n"
PLAN = "# Item\n\nWhy: w.\nBlocked by: nothing\n\n## Steps\n\n- [ ] First step.\n- [ ] Second step. Notes: later.\n\n## Outcome\n\n"


def git(root, *args, date="2026-11-01T10:00:00+00:00"):
    env = {**os.environ, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date, "GIT_AUTHOR_NAME": "t",
           "GIT_AUTHOR_EMAIL": "t@example.com", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com"}
    return subprocess.run(["git", *args], cwd=root, env=env, check=True, capture_output=True, text=True).stdout.strip()


def write(root, rel, text):
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text(text)


def project(root):
    write(root, ".bc-agent/AGENTS.md", AGENTS)
    write(root, "work/README.md", "# Work\n")
    return root


def items(root):
    result = subprocess.run([sys.executable, str(SCRIPT), "--json", str(root / "work")], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    return {i["name"]: i for i in json.loads(result.stdout)["items"]}


def strip(history):
    return [{k: v for k, v in e.items() if k != "commit"} for e in history]


def test_history_records_moves_and_ticks_following_renames(tmp_path):
    project(tmp_path)
    git(tmp_path, "init", "-q")
    write(tmp_path, "work/1-planned/001-thing.md", PLAN)
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "plan", date="2026-11-01T10:00:00+00:00")
    # Single-file item becomes a folder item while moving to active: a rename.
    (tmp_path / "work/2-active/001-thing").mkdir(parents=True)
    git(tmp_path, "mv", "work/1-planned/001-thing.md", "work/2-active/001-thing/plan.md")
    git(tmp_path, "commit", "-qm", "start", date="2026-11-02T10:00:00+00:00")
    plan = tmp_path / "work/2-active/001-thing/plan.md"
    plan.write_text(plan.read_text().replace("- [ ] First step.", "- [x] First step.\n  Notes: done."))
    git(tmp_path, "commit", "-qam", "tick", date="2026-11-03T10:00:00+00:00")
    (tmp_path / "work/3-done/2026-11").mkdir(parents=True)
    git(tmp_path, "mv", "work/2-active/001-thing", "work/3-done/2026-11/001-thing")
    plan = tmp_path / "work/3-done/2026-11/001-thing/plan.md"
    plan.write_text(plan.read_text().replace("- [ ] Second step. Notes: later.", "- [x] Second step. Notes: done too."))
    git(tmp_path, "commit", "-qam", "close", date="2026-11-04T10:00:00+00:00")

    history = items(tmp_path)["001-thing"]["history"]
    assert strip(history) == [
        {"event": "created", "folder": "planned", "date": "2026-11-01T10:00:00Z"},
        {"event": "moved", "from": "planned", "to": "active", "date": "2026-11-02T10:00:00Z"},
        {"event": "ticked", "step": "First step.", "date": "2026-11-03T10:00:00Z"},
        {"event": "moved", "from": "active", "to": "done", "date": "2026-11-04T10:00:00Z"},
        {"event": "ticked", "step": "Second step.", "date": "2026-11-04T10:00:00Z"},
    ]
    assert all(len(e["commit"]) == 40 for e in history)


def test_uncommitted_item_has_empty_history(tmp_path):
    project(tmp_path)
    git(tmp_path, "init", "-q")
    write(tmp_path, "work/1-planned/001-old.md", PLAN)
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "old")
    write(tmp_path, "work/1-planned/002-new.md", PLAN)
    data = items(tmp_path)
    assert data["002-new"]["history"] == []
    assert len(data["001-old"]["history"]) == 1


def test_no_git_repository_gives_empty_history(tmp_path):
    project(tmp_path)
    write(tmp_path, "work/1-planned/001-thing.md", PLAN)
    env = {**os.environ, "GIT_CEILING_DIRECTORIES": str(tmp_path.parent)}
    result = subprocess.run([sys.executable, str(SCRIPT), "--json", str(tmp_path / "work")], capture_output=True, text=True, env=env)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["items"][0]["history"] == []
