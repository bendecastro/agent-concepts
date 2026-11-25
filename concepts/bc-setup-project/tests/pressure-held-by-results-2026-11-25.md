# Pressure test results: the Held by line (2026-11-25)

Scenario: [pressure-held-by.md](pressure-held-by.md). Consumer `openai-codex/gpt-6.1-terra`, thinking low
(from the private pressure-test config). Graded from each scratch repository's commits.

| Run | Rules | 1. line written | 2. line removed at stop | Notes |
|-----|-------|-----------------|-------------------------|-------|
| base | scaffold before the rule | no | n/a | moved the item and did step 1; no `Held by:` in any commit |
| with-1 | new rule | yes, in a separate commit right after the move | yes, in the step commit | partial on "same commit" |
| with-2 | new rule | yes, in the move commit | yes, in the step commit | pass |
| with-3 | new rule | yes, in the move commit | yes, in the step commit | pass |

All with-runs wrote the exact format (`Held by: pi quiet-heron since 2026-11-25 14:05 +01:00`), ticked
step 1 and left the item in `work/2-active/`. Blind check: the baseline transcript read only `AGENTS.md`,
`.bc-agent/` pages, `login.py` and the item; no `bc-setup-project` path. Both runs' system prompts carried the
same owner preferences text (no `Held by` wording), so it does not separate them.

Not run: finishing an item (the Finish row says to remove the line; the parser's `--check` warns when a
closed item keeps one), and the drain's and `bc-work-sync`'s new wording.
