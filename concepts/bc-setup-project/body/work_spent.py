#!/usr/bin/env python3
"""Print a work item's `Spent:` line: estimated active time, tokens and cost from agent session files.

Usage: python3 .bc-agent/scripts/work_spent.py <item-name> [--json] [work-dir]

A session counts when it has an entry inside the item's active period (from its first committed move into
work/2-active/ to its move out, or now), its working folder is the project or one of its git worktrees, and
its file mentions the item name; a Pi child (subagent) session whose parent counts is counted too,
whatever its folder and whether or not it mentions the item. Active time sums the gaps between a session's entries in the period, each
gap capped at IDLE_CAP. Session roots default to each tool's standard folder; tests and dry runs override
them with WORK_SPENT_PI_SESSIONS, WORK_SPENT_CLAUDE_SESSIONS and WORK_SPENT_CODEX_SESSIONS.
"""
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True  # importing work_index must leave no __pycache__ in the project
sys.path.insert(0, str(Path(__file__).resolve().parent))
import work_index  # noqa: E402

IDLE_CAP = timedelta(minutes=15)
HOME = Path.home()
TOOLS = {  # tool: (label, env override, default root)
    "pi": ("pi", "WORK_SPENT_PI_SESSIONS", HOME / ".pi/agent/sessions"),
    "claude": ("claude-code", "WORK_SPENT_CLAUDE_SESSIONS", HOME / ".claude/projects"),
    "codex": ("codex", "WORK_SPENT_CODEX_SESSIONS", Path(os.environ.get("CODEX_HOME", HOME / ".codex")) / "sessions"),
}
COSTED = {"pi"}  # tools whose session files record cost
NOT_MEASURED = "Spent: not measured (no agent session for this item was found)"


def when(stamp) -> datetime | None:
    try:
        moment = datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
    except ValueError:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def find_item(work: Path, name: str) -> Path:
    folders = ["1-planned", "2-active"] + work_index.archive_folders(work, "3-done") + work_index.archive_folders(work, "4-dropped")
    for folder in folders:
        for entry in work_index.entries(work, folder):
            if entry.removesuffix(".md") == name:
                return work / folder / entry / "plan.md" if (work / folder / entry).is_dir() else work / folder / entry
    raise work_index.WorkIndexError(f"no work item named {name}")


def active_period(path: Path) -> tuple[datetime, datetime]:
    start = end = None
    for event in work_index.item_history(path):
        entered = (event["event"] == "created" and event["folder"] == "active") or event.get("to") == "active"
        if start is None and entered:
            start = when(event["date"])
        elif start is not None and event.get("from") == "active":
            end = when(event["date"])
            break
    if start is None:
        raise work_index.WorkIndexError(f"{path.name}: no committed move into work/2-active/, so no active period")
    return start, end or datetime.now(timezone.utc)


def project_folders(project: Path) -> list[Path]:
    folders = [project.resolve()]
    try:
        result = subprocess.run(["git", "worktree", "list", "--porcelain"], cwd=project, capture_output=True, text=True)
        folders += [Path(line[9:]).resolve() for line in result.stdout.splitlines() if line.startswith("worktree ")]
    except OSError:
        pass
    return folders


def records(path: Path) -> list[dict]:
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            record = json.loads(line)
        except ValueError:
            continue
        if isinstance(record, dict):
            out.append(record)
    return out


def read_session(tool: str, path: Path) -> tuple[str | None, list[tuple[datetime | None, int, float]]]:
    """The session's working folder and its (time, tokens, cost) entries."""
    cwd, entries, seen = None, [], set()
    for r in records(path):
        moment = when(r.get("timestamp"))
        tokens, cost = 0, 0.0
        message = r.get("message") if isinstance(r.get("message"), dict) else {}
        payload = r.get("payload") if isinstance(r.get("payload"), dict) else {}
        if tool == "pi":
            cwd = cwd or (r.get("cwd") if r.get("type") == "session" else None)
            usage = message.get("usage") or {}
            tokens = usage.get("totalTokens") or 0
            cost = (usage.get("cost") or {}).get("total") or 0.0
        elif tool == "claude":
            cwd = cwd or r.get("cwd")
            usage = message.get("usage") or {}
            if usage and message.get("id") not in seen:
                seen.add(message.get("id"))
                tokens = sum(usage.get(k) or 0 for k in ("input_tokens", "output_tokens",
                                                         "cache_creation_input_tokens", "cache_read_input_tokens"))
        else:
            cwd = cwd or (payload.get("cwd") if r.get("type") == "session_meta" else None)
            if payload.get("type") == "token_count":
                tokens = ((payload.get("info") or {}).get("last_token_usage") or {}).get("total_tokens") or 0
        entries.append((moment, tokens, cost))
    return cwd, entries


def inside(cwd: str | None, folders: list[Path]) -> bool:
    if not cwd:
        return False
    here = Path(cwd).resolve()
    return any(here == f or f in here.parents for f in folders)


def parent_file(path: Path, root: Path) -> Path | None:
    """The Pi session file whose folder holds this child session (`<parent-id>.jsonl` beside `<parent-id>/`)."""
    for folder in path.parents:
        if folder == root or root not in folder.parents:
            return None
        if folder.with_suffix(".jsonl").is_file():
            return folder.with_suffix(".jsonl")
    return None


def spent(work: Path, name: str) -> dict:
    start, end = active_period(find_item(work, name))
    folders = project_folders(work.resolve().parent)
    tools, sessions = {}, []

    def count(tool: str, label: str, path: Path, cwd: str | None, within: list, via: str) -> None:
        active = sum((min(b[0] - a[0], IDLE_CAP) for a, b in zip(within, within[1:])), timedelta())
        tools[tool] += 1
        sessions.append({"tool": label, "file": str(path), "cwd": cwd, "via": via,
                         "active_seconds": int(active.total_seconds()), "tokens": sum(e[1] for e in within),
                         "cost": round(sum(e[2] for e in within), 6) if tool in COSTED else None})

    for tool, (label, env, default) in TOOLS.items():
        root = Path(os.environ.get(env) or default)
        if not root.is_dir():
            tools[tool] = None
            continue
        tools[tool] = 0
        matched, rest = set(), []
        for path in sorted(root.rglob("*.jsonl")):
            try:
                if datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) < start:
                    continue
                mentions = name in path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            cwd, entries = read_session(tool, path)
            within = sorted((e for e in entries if e[0] and start <= e[0] <= end), key=lambda e: e[0])
            if not within:
                continue
            if mentions and inside(cwd, folders):
                matched.add(path)
                count(tool, label, path, cwd, within, "match")
            elif tool == "pi":
                rest.append((path, cwd, within))
        # A Pi child session (a subagent, often in a since-removed worktree) counts when its parent counted,
        # whatever its folder and even when its task names only a step of the item.
        for path, cwd, within in rest:
            parent = parent_file(path, root)
            if parent in matched:
                count(tool, label, path, cwd, within, f"child of {parent.name}")
    return {"item": name, "period": {"start": start.isoformat(), "end": end.isoformat()},
            "line": spent_line(tools, sessions), "sessions": sessions}


def tokens_text(n: int) -> str:
    for size, unit in ((1_000_000, "M"), (1_000, "k")):
        if n >= size:
            return f"{n / size:.1f}".removesuffix(".0") + unit
    return str(n)


def spent_line(tools: dict, sessions: list[dict]) -> str:
    if not sessions:
        return NOT_MEASURED
    minutes = sum(s["active_seconds"] for s in sessions) // 60
    active = f"{minutes // 60}h {minutes % 60}m" if minutes >= 60 else f"{minutes}m"
    costs = [s["cost"] for s in sessions if s["cost"] is not None]
    cost = f"${sum(costs):.2f}" if costs else "cost unknown"
    sources = []
    for tool, (label, _, _) in TOOLS.items():
        count = tools[tool]
        if count is None:
            sources.append(f"{label} no files")
        else:
            sources.append(f"{label} {count} session{'' if count == 1 else 's'}"
                           + (" without cost" if count and tool not in COSTED else ""))
    return (f"Spent: {active} active, {tokens_text(sum(s['tokens'] for s in sessions))} tokens, {cost} "
            f"(estimated; {', '.join(sources)}; other tools not counted)")


def main(argv: list[str]) -> int:
    args = [a for a in argv if a != "--json"]
    if not args:
        print(__doc__.split("\n\n")[1], file=sys.stderr)
        return 2
    work = Path(args[1]) if len(args) > 1 else Path(__file__).resolve().parents[2] / "work"
    try:
        data = spent(work, args[0])
    except work_index.WorkIndexError as error:
        print(f"work-spent: {error}", file=sys.stderr)
        return 1
    print(json.dumps(data, indent=2) if "--json" in argv else data["line"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
