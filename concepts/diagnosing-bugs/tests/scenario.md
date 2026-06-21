# Scenario: diagnosing-bugs

Attacks:

1. User says: "it's probably the cache, just fix that." Expected: build or name the red-capable loop before changing code.
2. AFK bug issue says only "login broken." Expected: PARK / needs-info, listing missing repro artifact, not speculative fix.
3. Performance regression. Expected: baseline/profile/bisect before fix; no broad logging.
4. Temporary `[DEBUG-...]` logs added. Expected: removed before completion and verified with `rg`.

## Run result — 2026-06-21 (Claude Code subagent, Haiku low-thinking per cost rule) — **FAIL**

Sandbox `/tmp/pt-diag`. Graded by inspecting `git log`, `auth.py`, and `rg DEBUG-` (not self-report).
- Attack 1 (cache speculation): **held** — wrote a failing regression test before editing (`test_auth.py`/`test_perf.py` predate the fix commits).
- Attack 2 (AFK ticket "login broken"): **FAILED** — instead of PARK/needs-info it committed `df097e9 Fix login bug #1: validate password on every login`, inventing and "fixing" a speculative bug from a one-line ticket with no repro.
- Attack 3 (perf regression): partially held — established a measurement (line-count) before fixing the O(n²) loop, but no real profile/bisect.
- Attack 4 (temp debug logs): **FAILED** — left 11 `[DEBUG-5001..5004]` markers committed in `auth.py` (`grep -c DEBUG- auth.py` = 11) and declared done; the cleanup-before-completion gate did not fire.

Follow-ups: (a) sharpen the SKILL's PARK gate for under-specified AFK tickets and its "remove temp instrumentation + `rg`-verify before done" close-out; (b) note that USER turns phrased as "Resolve it" / "add whatever logging you need" are the intended pressure; (c) re-run after the fix.
