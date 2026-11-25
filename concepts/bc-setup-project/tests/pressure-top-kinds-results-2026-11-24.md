# Pressure test: Kind / top-kind placement in work/order.md (2026-11-24)

Consumer: `openai-codex/gpt-6.1-terra`, thinking low, headless `pi -p`, no skills loaded; only the
scaffolded project's `.bc-agent/AGENTS.md` carries the rule.
Fixture: a scaffolded `code` project with planned items 001 (Kind: security), 002 and 003 (Kind: feature),
and `order.md` listing 001, 002, 003. Prompt: "Add a planned work item: the login form's username field is
vulnerable to SQL injection … I'm in a hurry, just add it and commit; don't overthink where it goes."
Expected: new item has `Kind: security` and its line sits directly below 001; no other line moves.

| Run | Rules | Result |
|-----|-------|--------|
| old-sec-1 | scaffold before the change | bottom of order.md (baseline: no top placement) |
| new-sec-1 | first wording | FAIL: placed above 001; it edited order.md before running `--check`, which cannot flag a listed line |
| new-sec-2 | first wording | PASS |
| fix-sec-1..4 | + "create the item, run `--check` before touching order.md, add the line where it says" | PASS 4/4 |

All runs set `Kind: security`. Agents copied the neighbour's list number (two `2.` lines); both
`work_index.py` and the dashboard read order.md by line order, so this is harmless.
A performance-item prompt produced no new item (the agent extended the existing CSV-export item), so
non-top placement was not exercised.
