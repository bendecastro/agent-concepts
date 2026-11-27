# ui-design pressure results, 2026-11-11

Two rounds on `openai-codex/gpt-6-luna:max`, each scenario run without and with the skill, graded by independent reviewers from the files, captures and session logs each run left. Round 1 covered scenarios A–I; six skill gaps and the harness were fixed, then A, B, D, E, G and H were rerun. The grader reports are in this directory (`grade-*.md` round 1, `grade2-*.md` round 2); paths inside them point at the temporary run directory and are historical.

| Scenario | Round | Without | With | Reading |
|---|---|---|---|---|
| A small existing-app change | 2 | FAIL | HOLD | skill made the difference |
| B new landing page | 2 | stalled | HOLD | no clean comparison: the baseline stalled on a tooling question |
| C terminal surface | 1 | FAIL | HOLD (provisional) | grader ran out of budget before opening the terminal captures |
| D extension popup | 2 | FAIL | FAIL | with the skill the agent rejected the page-viewport shortcut and named the real host, then stopped to ask |
| E no capture tool | 2 | HOLD | HOLD | non-discriminating |
| F | 1 | HOLD | HOLD | non-discriminating |
| G "looks bad" redesign | 2 | HOLD | HOLD | baseline read the skill by itself; with-skill run hit the 40-minute cap with no final report |
| H claimed score, acceptance review | 2 | FAIL | HOLD | skill made the difference |
| I trigger | 1 | FAIL | HOLD | skill loaded without being attached |

## Known limits

- **D is unresolved.** No run has shown the real-host capture recipe being followed to completion.
- **Baselines were partly contaminated.** `--no-skills` did not hide the skill text in the repository; G-without and D-without read it mid-run.
- **Stalls.** An appended non-interactive instruction did not stop every run from ending on a question.
- **Three edits are untested.** After round 2 the skill gained: critique before editing for the next round, never overwrite the owner's screenshot, and a native-control request does not excuse other unstyled controls. No run has exercised them.
- Graders also suggested a stopping/report-first rule and a final-state capture rule; not adopted.
