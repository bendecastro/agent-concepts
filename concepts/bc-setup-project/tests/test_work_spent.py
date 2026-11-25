"""work_spent.py: the `Spent:` line from scrubbed, hand-made Pi, Claude Code and Codex session files."""
import json
import os
from pathlib import Path
import subprocess
import sys

SCRIPT = Path(__file__).resolve().parents[1] / "body/work_spent.py"
ITEM = "001-thing"
PLAN = "# Thing\n\nWhy: w.\nBlocked by: nothing\n\n## Steps\n\n- [ ] Step.\n\n## Outcome\n\n"


def git(root, *args, date="2026-11-01T10:00:00+00:00"):
    env = {**os.environ, "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date, "GIT_AUTHOR_NAME": "t",
           "GIT_AUTHOR_EMAIL": "t@example.com", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@example.com"}
    return subprocess.run(["git", *args], cwd=root, env=env, check=True, capture_output=True, text=True).stdout.strip()


def project(tmp_path):
    """An item active from 10:00 to 12:00 UTC on 2026-11-01, plus a git worktree of the project."""
    root = tmp_path / "proj"
    (root / "work/2-active").mkdir(parents=True)
    (root / f"work/2-active/{ITEM}.md").write_text(PLAN)
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "start", date="2026-11-01T10:00:00+00:00")
    (root / "work/3-done/2026-11").mkdir(parents=True)
    git(root, "mv", f"work/2-active/{ITEM}.md", f"work/3-done/2026-11/{ITEM}.md")
    git(root, "commit", "-qm", "finish", date="2026-11-01T12:00:00+00:00")
    git(root, "worktree", "add", "-q", str(tmp_path / "wt"))
    return root


def jsonl(path, records):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in records))


def pi_session(root, name, cwd, times, mention=ITEM, tokens=1000, cost=0.5):
    records = [{"type": "session", "id": name, "timestamp": times[0], "cwd": str(cwd)},
               {"type": "message", "timestamp": times[0], "message": {"role": "user", "content": f"work on {mention}"}}]
    records += [{"type": "message", "timestamp": t, "message": {"role": "assistant", "content": "ok",
                 "usage": {"totalTokens": tokens, "cost": {"total": cost}}}} for t in times[1:]]
    jsonl(root / "sessions" / name / f"{name}.jsonl", records)


def run(proj, roots, *flags):
    env = {**os.environ, **{f"WORK_SPENT_{tool.upper()}_SESSIONS": str(path) for tool, path in roots.items()}}
    return subprocess.run([sys.executable, str(SCRIPT), ITEM, *flags, str(proj / "work")],
                          capture_output=True, text=True, env=env)


def test_pi_sessions_in_period_folder_and_mentioning_the_item_are_summed(tmp_path):
    proj = project(tmp_path)
    pi = tmp_path / "pi"
    pi_session(pi, "main", proj, ["2026-11-01T10:05:00Z", "2026-11-01T10:10:00Z", "2026-11-01T10:40:00Z"])
    pi_session(pi, "worktree", tmp_path / "wt", ["2026-11-01T11:00:00Z", "2026-11-01T11:10:00Z"], cost=0.25)
    pi_session(pi, "unmentioned", proj, ["2026-11-01T10:05:00Z", "2026-11-01T10:10:00Z"], mention="002-other")
    pi_session(pi, "elsewhere", tmp_path, ["2026-11-01T10:05:00Z", "2026-11-01T10:10:00Z"])
    pi_session(pi, "later", proj, ["2026-11-02T10:05:00Z", "2026-11-02T10:10:00Z"])
    result = run(proj, {"pi": pi, "claude": tmp_path / "none-c", "codex": tmp_path / "none-x"})
    assert result.returncode == 0, result.stderr
    # main: 5 min + 30 min gap capped at 15 = 20 min; worktree: 10 min.
    assert result.stdout.strip() == ("Spent: 30m active, 3k tokens, $1.25 (estimated; pi 2 sessions, "
                                     "claude-code no files, codex no files; other tools not counted)")


def test_claude_code_counts_each_message_once_and_has_no_cost(tmp_path):
    proj = project(tmp_path)
    usage = {"input_tokens": 10, "output_tokens": 20, "cache_creation_input_tokens": 30, "cache_read_input_tokens": 40}
    base = {"cwd": str(tmp_path / "wt"), "sessionId": "c1"}
    jsonl(tmp_path / "claude/-proj/c1.jsonl", [
        {**base, "type": "user", "timestamp": "2026-11-01T10:00:30Z", "message": {"role": "user", "content": f"finish {ITEM}"}},
        {**base, "type": "assistant", "timestamp": "2026-11-01T10:01:00Z", "message": {"id": "m1", "usage": usage}},
        {**base, "type": "assistant", "timestamp": "2026-11-01T10:01:00Z", "message": {"id": "m1", "usage": usage}},
        {**base, "type": "assistant", "timestamp": "2026-11-01T10:03:30Z", "message": {"id": "m2", "usage": usage}}])
    result = run(proj, {"pi": tmp_path / "pi", "claude": tmp_path / "claude", "codex": tmp_path / "none"})
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == ("Spent: 3m active, 200 tokens, cost unknown (estimated; pi no files, "
                                     "claude-code 1 session without cost, codex no files; other tools not counted)")


def test_codex_sums_token_counts_and_has_no_cost(tmp_path):
    proj = project(tmp_path)
    count = lambda t, n: {"type": "event_msg", "timestamp": t,
                          "payload": {"type": "token_count", "info": {"last_token_usage": {"total_tokens": n}}}}
    jsonl(tmp_path / "codex/2026/11/01/rollout-x.jsonl", [
        {"type": "session_meta", "timestamp": "2026-11-01T11:00:00Z", "payload": {"cwd": str(proj)}},
        {"type": "response_item", "timestamp": "2026-11-01T11:00:10Z", "payload": {"type": "message", "content": ITEM}},
        count("2026-11-01T11:02:00Z", 1500), count("2026-11-01T11:04:00Z", 2500)])
    pi = tmp_path / "pi"
    pi_session(pi, "main", proj, ["2026-11-01T10:05:00Z", "2026-11-01T10:06:00Z"], tokens=500, cost=0.1)
    result = run(proj, {"pi": pi, "claude": tmp_path / "none", "codex": tmp_path / "codex"})
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == ("Spent: 5m active, 4.5k tokens, $0.10 (estimated; pi 1 session, "
                                     "claude-code no files, codex 1 session without cost; other tools not counted)")


def test_no_matching_session_gives_a_zero_line(tmp_path):
    proj = project(tmp_path)
    pi = tmp_path / "pi"
    pi_session(pi, "later", proj, ["2026-11-02T10:05:00Z", "2026-11-02T10:10:00Z"])
    (tmp_path / "claude").mkdir()
    result = run(proj, {"pi": pi, "claude": tmp_path / "claude", "codex": tmp_path / "none"})
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == ("Spent: 0m active, 0 tokens, cost unknown (estimated; pi 0 sessions, "
                                     "claude-code 0 sessions, codex no files; other tools not counted)")


def test_json_lists_the_period_and_matched_sessions(tmp_path):
    proj = project(tmp_path)
    pi = tmp_path / "pi"
    pi_session(pi, "main", proj, ["2026-11-01T10:05:00Z", "2026-11-01T10:10:00Z"])
    result = run(proj, {"pi": pi, "claude": tmp_path / "n", "codex": tmp_path / "n"}, "--json")
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["period"] == {"start": "2026-11-01T10:00:00+00:00", "end": "2026-11-01T12:00:00+00:00"}
    assert data["line"].startswith("Spent: 5m active")
    [session] = data["sessions"]
    assert (session["tool"], session["active_seconds"], session["tokens"], session["cost"]) == ("pi", 300, 1000, 0.5)
    assert session["file"].endswith("main.jsonl")
    assert not (SCRIPT.parent / "__pycache__").exists()


def test_uncommitted_item_has_no_active_period(tmp_path):
    root = tmp_path / "proj"
    (root / "work/2-active").mkdir(parents=True)
    (root / f"work/2-active/{ITEM}.md").write_text(PLAN)
    result = run(root, {"pi": tmp_path / "n", "claude": tmp_path / "n", "codex": tmp_path / "n"})
    assert result.returncode == 1
    assert "no committed move" in result.stderr


INDEX = Path(__file__).resolve().parents[1] / "body/work_index.py"
LINE = ("Spent: 1h 5m active, 2.5M tokens, $3.10 (estimated; pi 2 sessions, claude-code no files, "
        "codex 0 sessions; other tools not counted)")


def test_work_index_json_parses_the_spent_line_and_check_warns_on_a_malformed_one(tmp_path):
    work = tmp_path / "work"
    (tmp_path / ".bc-agent").mkdir()
    (tmp_path / ".bc-agent/AGENTS.md").write_text("Stages: now\n")
    (work / "3-done/2026-11").mkdir(parents=True)
    (work / "README.md").write_text("# Work\n\n<!-- work-index:start -->\n<!-- work-index:end -->\n")
    (work / "0-ideas.md").write_text("# Ideas\n")
    (work / "3-done/2026-11/001-good.md").write_text(PLAN + f"Landed.\n\n{LINE}\n")
    (work / "3-done/2026-11/002-bad.md").write_text(PLAN + "Spent: about an hour\n")
    (work / "3-done/2026-11/003-none.md").write_text(PLAN + "Landed.\n")
    result = subprocess.run([sys.executable, str(INDEX), "--json", str(work)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    items = {i["name"]: i for i in json.loads(result.stdout)["items"]}
    assert items["001-good"]["spent"] == {
        "active": "1h 5m", "tokens": "2.5M", "cost": "$3.10",
        "sources": "pi 2 sessions, claude-code no files, codex 0 sessions; other tools not counted", "text": LINE[7:]}
    assert items["002-bad"]["spent"] == {"active": None, "tokens": None, "cost": None, "sources": None,
                                         "text": "about an hour"}
    assert items["003-none"]["spent"] is None
    subprocess.run([sys.executable, str(INDEX), str(work)], check=True)
    check = subprocess.run([sys.executable, str(INDEX), "--check", str(work)], capture_output=True, text=True)
    assert check.returncode == 0, check.stderr
    assert "3-done/2026-11/002-bad.md has a malformed Spent: line" in check.stderr
    assert "001-good" not in check.stderr


def test_pi_child_sessions_of_a_matched_parent_count_in_any_folder_within_the_period(tmp_path):
    proj = project(tmp_path)
    pi = tmp_path / "pi"
    pi_session(pi, "main", proj, ["2026-11-01T10:05:00Z", "2026-11-01T10:10:00Z"])
    gone = tmp_path / "worktrees/removed"  # a worker's worktree, removed after integration
    children = pi / "sessions/main/main"  # Pi keeps children in a folder named after the parent file
    pi_session(children, "step", gone, ["2026-11-01T10:20:00Z", "2026-11-01T10:30:00Z"], mention="the step")
    (children / "sessions/step/step.jsonl").rename(children / "sessions/step/run-0.jsonl")
    pi_session(children, "own", proj, ["2026-11-01T11:00:00Z", "2026-11-01T11:05:00Z"])
    pi_session(children, "late", gone, ["2026-11-02T10:20:00Z", "2026-11-02T10:30:00Z"], mention="the step")
    pi_session(pi, "orphan", gone, ["2026-11-01T10:20:00Z", "2026-11-01T10:30:00Z"], mention="the step")
    roots = {"pi": pi, "claude": tmp_path / "n", "codex": tmp_path / "n"}
    result = run(proj, roots)
    assert result.returncode == 0, result.stderr
    # main 5m + step 10m + own 5m; late is outside the period, orphan has no matched parent.
    assert result.stdout.strip() == ("Spent: 20m active, 3k tokens, $1.50 (estimated; pi 3 sessions, "
                                     "claude-code no files, codex no files; other tools not counted)")
    sessions = {Path(s["file"]).name: s for s in json.loads(run(proj, roots, "--json").stdout)["sessions"]}
    assert sessions["run-0.jsonl"]["via"] == "child of main.jsonl"
    assert sessions["main.jsonl"]["via"] == "match"
    assert sessions["own.jsonl"]["via"] == "match"  # counted once, on its own match
