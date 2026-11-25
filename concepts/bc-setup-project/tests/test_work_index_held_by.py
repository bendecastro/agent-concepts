"""work_index.py `Held by:` line: --json parses it and gives its age; --check warns on bad or leftover lines."""
import json
import os
from pathlib import Path
import subprocess
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "body/work_index.py"
AGENTS = "# demo\n\nStages: now, next, later\n"
README = "# Work\n\n<!-- work-index:start -->\n<!-- work-index:end -->\n"


def plan(held=None):
    line = f"Held by: {held}\n" if held is not None else ""
    return f"# Item\n\nWhy: w.\nBlocked by: nothing\n{line}\n## Steps\n\n- [ ] First step.\n\n## Outcome\n\n"


def git(root, *args, date="2026-11-01T10:00:00+00:00"):
    env = {**os.environ, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date, "GIT_AUTHOR_NAME": "t",
           "GIT_AUTHOR_EMAIL": "t@example.com", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com"}
    return subprocess.run(["git", *args], cwd=root, env=env, check=True, capture_output=True, text=True).stdout.strip()


def write(root, rel, text):
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text(text)


def run(root, *flags):
    return subprocess.run([sys.executable, str(SCRIPT), *flags, str(root / "work")], capture_output=True, text=True)


def items(root):
    result = run(root, "--json")
    assert result.returncode == 0, result.stderr
    return {i["name"]: i for i in json.loads(result.stdout)["items"]}


def test_json_parses_held_by_and_gives_age_from_last_commit(tmp_path):
    write(tmp_path, ".bc-agent/AGENTS.md", AGENTS)
    write(tmp_path, "work/README.md", README)
    write(tmp_path, "work/0-ideas.md", "# Ideas\n")
    git(tmp_path, "init", "-q")
    write(tmp_path, "work/2-active/001-thing/plan.md", plan())
    write(tmp_path, "work/2-active/002-other.md", plan())
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "start", date="2026-11-01T10:00:00+00:00")
    write(tmp_path, "work/2-active/001-thing/plan.md", plan("pi worker-3 since 2026-11-02 09:30 +01:00"))
    git(tmp_path, "commit", "-qam", "claim", date="2026-11-02T08:30:00+00:00")
    write(tmp_path, "work/2-active/002-other.md", plan("claude-code abc123 since 2026-11-03 10:00 UTC"))

    data = items(tmp_path)
    held = data["001-thing"]["held_by"]
    assert data["001-thing"]["header"]["held_by"] == "pi worker-3 since 2026-11-02 09:30 +01:00"
    assert held["tool"] == "pi" and held["session"] == "worker-3" and held["since"] == "2026-11-02 09:30 +01:00"
    assert held["committed"].startswith("2026-11-02T08:30:00")
    assert held["age_seconds"] > 0
    uncommitted = data["002-other"]["held_by"]
    assert uncommitted["tool"] == "claude-code" and uncommitted["since"] == "2026-11-03 10:00 UTC"
    assert uncommitted["committed"] is None and uncommitted["age_seconds"] is None


def test_json_held_by_is_null_without_line_and_unparsed_when_malformed(tmp_path):
    write(tmp_path, ".bc-agent/AGENTS.md", AGENTS)
    write(tmp_path, "work/README.md", README)
    write(tmp_path, "work/0-ideas.md", "# Ideas\n")
    write(tmp_path, "work/2-active/001-thing.md", plan())
    write(tmp_path, "work/2-active/002-other.md", plan("someone, yesterday"))
    data = items(tmp_path)
    assert data["001-thing"]["held_by"] is None
    assert data["002-other"]["held_by"]["tool"] is None
    assert data["002-other"]["header"]["held_by"] == "someone, yesterday"


def test_check_warns_on_malformed_and_closed_held_by_without_changing_exit(tmp_path):
    write(tmp_path, ".bc-agent/AGENTS.md", AGENTS)
    write(tmp_path, "work/README.md", README)
    write(tmp_path, "work/0-ideas.md", "# Ideas\n")
    write(tmp_path, "work/2-active/001-good.md", plan("pi s1 since 2026-11-02 09:30 +01:00"))
    write(tmp_path, "work/2-active/002-bad.md", plan("someone, yesterday"))
    write(tmp_path, "work/3-done/2026-11/003-done.md", plan("pi s2 since 2026-11-02 09:30 UTC"))
    write(tmp_path, "work/4-dropped/004-dropped.md", plan("pi s3 since 2026-11-02 09:30 UTC"))
    assert run(tmp_path).returncode == 0
    result = run(tmp_path, "--check")
    assert result.returncode == 0, result.stderr
    warnings = [line for line in result.stderr.splitlines() if "Held by" in line]
    assert len(warnings) == 3, result.stderr
    assert any("002-bad" in w and "malformed" in w for w in warnings)
    assert any("003-done" in w for w in warnings) and any("004-dropped" in w for w in warnings)
    assert not any("001-good" in w for w in warnings)
