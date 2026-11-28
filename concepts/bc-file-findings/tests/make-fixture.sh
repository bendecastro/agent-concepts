#!/usr/bin/env bash
# Build the find-bugs filing fixture (scenario C2) in a new folder: make-fixture.sh <dir> <agent-concepts>
# Scaffolded code project, a small dateparse package with a passing suite, two planned items,
# and a hunt branch carrying two failing reproductions and find-bugs-report.md.
set -euo pipefail
dir=$1; ac=$2
mkdir -p "$dir"; cd "$dir"
git init -q -b master
git config user.name tester; git config user.email tester@example.invalid
python3 "$ac/concepts/bc-setup-project/body/scaffold.py" --root . --slug dateparse --archetype code --date 2026-11-20 >/dev/null
cat >> AGENTS.md <<'EOF'

## This project

- Single agent: do not launch subagents.
- The owner sees questions only in `questions/` (one Markdown file per question, committed). Never ask in chat.
- Run tests with `python3 -m pytest -q`.
EOF
mkdir -p dateparse tests questions
touch questions/.gitkeep
cat > dateparse/__init__.py <<'EOF'
from .parse import parse_date, weekday_name
EOF
cat > dateparse/parse.py <<'EOF'
import datetime as dt

_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def parse_date(text):
    """Parse YYYY-MM-DD, optionally followed by a time part THH:MM, which is ignored."""
    year, month, day = text.split("-")
    return dt.date(int(year), int(month), int(day))


def weekday_name(date):
    return _DAYS[date.weekday() - 1]
EOF
cat > tests/test_parse.py <<'EOF'
import datetime as dt
from dateparse import parse_date


def test_parse_basic():
    assert parse_date("2026-03-04") == dt.date(2026, 3, 4)
EOF
cat > work/1-planned/004-fix-date-parse.md <<'EOF'
# Fix ambiguous slash dates

Why: `parse_date("03/04/2026")` raises; callers want slash dates.
Done when: slash dates parse.
Stage: now
Blocked by: nothing
Kind: bug
Source: owner
Planned: bc-plan-to-pipeline 2026-11-20

## Requirements

- Slash dates `MM/DD/YYYY` parse.

## Steps

- [ ] Accept `MM/DD/YYYY` in `parse_date`. Done when a test for `03/04/2026` passes.

## Outcome

_To be filled when finished or dropped._
EOF
cat > work/1-planned/005-add-weekday-long-names.md <<'EOF'
# Long weekday names

Why: reports want "Monday", not "Mon".
Done when: `weekday_name(d, long=True)` returns the long name.
Stage: next
Blocked by: nothing
Kind: feature
Source: owner
Planned: bc-plan-to-pipeline 2026-11-20

## Requirements

- `weekday_name(d, long=True)` returns the full English name.

## Steps

- [ ] Add the `long` flag. Done when a test for a Monday returns "Monday".

## Outcome

_To be filled when finished or dropped._
EOF
printf '1. 004-fix-date-parse\n2. 005-add-weekday-long-names\n' > work/order.md
python3 .bc-agent/scripts/work_index.py >/dev/null
git add -A; git commit -qm "dateparse: initial project"
base=$(git rev-parse --short HEAD)

git switch -qc find-bugs/2026-11-20-dateparse
cat > tests/test_find_bugs_repro.py <<'EOF'
import datetime as dt
from dateparse import parse_date, weekday_name


def test_parse_date_ignores_time_part():
    assert parse_date("2026-03-04T10:30") == dt.date(2026, 3, 4)


def test_weekday_name_monday():
    assert weekday_name(dt.date(2026, 11, 16)) == "Mon"
EOF
cat > find-bugs-report.md <<EOF
# Find bugs: dateparse

## Scope

Area: \`dateparse/\`. Commit hunted: $base. Branch: \`find-bugs/2026-11-20-dateparse\`.

## Confirmed

### B1 parse_date rejects a trailing time part
- Focus: inputs/edge cases
- Evidence: \`dateparse/parse.py\` \`year, month, day = text.split("-")\`; the docstring promises an optional \`THH:MM\` time part, which lands in \`day\`.
- Expected: \`parse_date("2026-03-04T10:30") == date(2026, 3, 4)\`. Actual: \`ValueError\` on \`"04T10:30"\`.
- Test: \`tests/test_find_bugs_repro.py::test_parse_date_ignores_time_part\`
- Failing output: \`ValueError: invalid literal for int() with base 10: '04T10:30'\`

### B2 weekday_name is off by one day
- Focus: contracts between modules
- Evidence: \`dateparse/parse.py\` \`_DAYS[date.weekday() - 1]\`; \`date.weekday()\` is already 0 for Monday.
- Expected: \`weekday_name(date(2026, 11, 16)) == "Mon"\` (a Monday). Actual: \`"Sun"\`.
- Test: \`tests/test_find_bugs_repro.py::test_weekday_name_monday\`
- Failing output: \`AssertionError: assert 'Sun' == 'Mon'\`

## Suspected

### S1 parse_date accepts two-digit years silently
- Evidence: \`int(year)\` on \`"26"\` gives year 26. Not attempted.

## Filing

Confirmed bugs are pre-selected for filing. Reply \`all\` to file them, or name the ones to file, the suspected ones to investigate, and any to reject with a reason.
EOF
git add -A; git commit -qm "find-bugs: two failing reproductions (suite fails exactly in tests/test_find_bugs_repro.py) and report"
git switch -q master
