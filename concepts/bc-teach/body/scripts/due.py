#!/usr/bin/env python3
"""Print review items that are due, with next-interval suggestions.

Usage: due.py [path/to/REVIEW.md]

Parses the markdown table in REVIEW.md (columns: #, Prompt, Source,
Last reviewed, Interval, Due) and prints items due today or earlier.
Date arithmetic lives here so the agent never has to do it in its head.
Items under a "## Retired" heading are ignored.
"""

import re
import sys
from datetime import date, timedelta
from pathlib import Path

CAP_DAYS = 60
RESET_DAYS = 2

def parse(path: Path):
    items, retired = [], False
    for line in path.read_text().splitlines():
        if line.startswith("#"):
            retired = "retired" in line.lower()
            continue
        if retired or not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not cells[0].isdigit():
            continue  # header, separator, or malformed row
        m_int = re.match(r"(\d+)\s*d", cells[4])
        m_due = re.match(r"\d{4}-\d{2}-\d{2}", cells[5])
        if not (m_int and m_due):
            print(f"warning: row {cells[0]} has unparseable interval/due, skipping", file=sys.stderr)
            continue
        items.append({
            "num": cells[0], "prompt": cells[1], "source": cells[2],
            "interval": int(m_int.group(1)),
            "due": date.fromisoformat(m_due.group(0)),
        })
    return items

def main():
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "REVIEW.md")
    if not path.exists():
        sys.exit(f"no review queue at {path} — nothing is due")
    today = date.today()
    due = sorted((i for i in parse(path) if i["due"] <= today), key=lambda i: i["due"])
    print(f"today: {today}")
    if not due:
        print("nothing due — proceed to the session")
        return
    print(f"{len(due)} item(s) due:\n")
    for i in due:
        overdue = (today - i["due"]).days
        passed = min(max(i["interval"] * 2, RESET_DAYS), CAP_DAYS)
        print(f"#{i['num']} (due {i['due']}, {overdue}d overdue) [{i['source']}]")
        print(f"  prompt: {i['prompt']}")
        print(f"  if recalled: interval {passed}d, due {today + timedelta(days=passed)}")
        print(f"  if hard:     interval {i['interval']}d, due {today + timedelta(days=i['interval'])}")
        print(f"  if failed:   interval {RESET_DAYS}d, due {today + timedelta(days=RESET_DAYS)}")
        print()

if __name__ == "__main__":
    main()
