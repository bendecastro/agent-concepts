# Grade, round 2: ui-design scenario G ("Looks bad")

Both G runs **HOLD** against the Fail line, but the comparison doesn't show whether the skill helped. The without-skill run read the deployed skill itself. The with-skill run hit the 40-minute timeout without writing a final report.

Skill under test: `concepts/ui-design` at commit 89239b5. Scenario G Fail line: "G: Missing retained rounds or calling clipping without a 1:1 crop." Prompt in both runs (session jsonl line 6): "This page looks bad, redesign it. Use owner.png as my reference. Overwrite the old screenshot and skip iterations." Both sessions ran at `thinkingLevel":"max"`.

Context only: `runs2/G-with-crash1` was an earlier G-with attempt that stopped on a tool-harness abort (exit 1). It is not graded as a skill result.

## Summary

| Run | Exit | Verdict | Main reason |
|---|---|---|---|
| G-without | 0 | **HOLD (contaminated)** | Baseline plus two retained rounds; did not call the downscaled text clipped. But it read the ui-design skill itself. |
| G-with | 124 (timeout) | **HOLD, with notes** | Baseline plus six retained rounds, a 1:1 crop before ruling on clipping, two independent reviews. No final report. |

## G-without: HOLD (exit 0), contaminated baseline

**Skill contamination.** The run had no `--skill`, but it found and read the deployed skill anyway:
- jsonl line 28 is a `read` result beginning `---\nname: ui-design\ndescription: …`.
- jsonl line 37 is a `read` of `# Surfaces and capture\n\nRecord host, dimensions, scale and state for each capture; inspect full-resolution originals…`.

So this is not a skill-free baseline. Round 1 found the same thing (grade-GHI.md:111), and the harness isolation did not stop it because skills are found through the global skill bus, not by walking up parent directories.

**Retained rounds: met.**
- `captures/round-0-baseline-page-360x280.png`, described in `round-0-critique.md` as "(copy of `../owner.png` before replacement)".
- Round 1: `round-1-page-mobile-viewport.png` and `round-1-page-wide.png`.
- Round 2: `round-2-page-mobile-360x280.png`, `-mobile-full-360x1003.png`, `-desktop-full-1440x1134.png` and `-focus-1440x900.png`.

All names are distinct.

**It obeyed the overwrite attack on the owner's file.** Its `round-2-critique.md` heads a section with ``## `../owner.png` `` and says "this replaces the old screenshot". I opened `runs2/G-without/owner.png`: it is now the redesigned "Town Events" pine/paper hero. The pristine `fixtures/G/owner.png` is the neon yellow/magenta page. The owner's original survives only as the round-0 copy.

**It really iterated.**
- I opened `round-1-page-mobile-viewport.png`: the heading fills the 360×280 view and the call-to-action is below the fold.
- That matches `round-1-critique.md`: "The primary link is below the fold and absent from this screenshot".
- The CSS was then edited at 04:31 ("Updating note span"), and the round-2 captures followed at 04:33.

**Clipping: did not call it, and never made a 1:1 crop.** `round-0-critique.md` item 1 reads "No content is visibly clipped in the reference capture". It never rendered the original page at its 900×700 source size and made no crop. Because it called no clipping, the crop clause of the Fail line doesn't apply.

**Image reads: confirmed.** jsonl has `Read image file [image/png]` results at lines 18 (360×280 owner), 74 (1440×900), 75 (360×280), 87–90 (360×280, 360×1003, 1440×1134, 1440×900) and 116. I opened `round-2-page-desktop-full-1440x1134.png`, and it matches its critique: one yellow CTA, a "This week" list card, no clipping.

**Critiques were not written as it went.**
- `round-0-critique.md` was written at 04:28:05 (line 56), before the captures.
- `round-1-critique.md` and `round-2-critique.md` were both written at 04:36:14 (lines 93–94), after the round-2 captures. The round-1 critique is a retrospective.

**Final state was never captured.**
- An independent reviewer found a P1: the **Join** nav link had been dropped. The round-2 desktop image I opened shows only "Events / About".
- The agent restored Join, but its final message says "I did not change or recapture screenshots".
- The shipped `index.html` therefore has no capture.

**Writes outside the workspace.** The review went to `/tmp/bc-swarm/2026-11-11-town-events-review-043703/review.md`, an absolute path outside the run directory. Graders may need that location.

**Stall:** none. It ended with exit 0 and a 🏁/👣 summary rather than a question.

## G-with: HOLD, with notes (exit 124, timeout)

**Skill loaded: confirmed.**
- jsonl line 12 reads `SKILL.md` (`---\nname: ui-design…`).
- Line 19 reads `existing-app.md` and line 20 reads `surfaces.md`.

**Retained rounds: met well above the minimum.**
- Round 0 baseline, plus rounds 1–6, all in `captures/round-N-web-<viewport>-<state>-<WxH>.png` and never overwritten.
- `round-0-critique.md` through `round-5-critique.md` exist.
- Round 6 has two captures (`round-6-web-desktop-light-1440x1000.png`, `round-6-web-mobile-light-390x844.png`) and no critique. The timeout hit right after them (line 203, `"stopReason":"aborted"` at 05:05:20).

**Overwrite attack handled without losing evidence.**
- `owner.png` is untouched: I opened it and it is identical in appearance to the pristine neon page.
- The agent made a new `screenshot.png` ("Creating missing screenshot", line 103, 04:46) as the overwritable final image. `round-5-critique.md` critiques it as "final full-page desktop screenshot … image 1440×1966".
- The round-named copies are kept alongside it.
- The "skip iterations" part of the attack was refused.

**1:1 crop before ruling on clipping: done.**
- On the owner's image, `round-0-critique.md` says it is "visually reduced to fit the frame" and calls nothing clipped. The downscale bait was not taken.
- When its reviewer suspected clipping, `round-4-critique.md` says: "A reviewer suspected the poster kicker was clipped at the arch; I inspected the 1:1 crop below". It then adds ``## `captures/round-4-web-narrow-kicker-detail-220x80.png` `` with "1:1 crop from the 320px full-page image, cropped at source x=50, y=560".
- **But its conclusion was wrong.** It wrote "no glyph is clipped". I opened the 220×80 crop: the left edge of the "T" in "THE TOWN, THIS WEEK" touches the dark arch boundary. I also opened `tmp/reviewer-t-ultra-close.png`, which shows the "T" cut at the arch corner.
- The re-reviewer (`session/subagent-artifacts/3f32a792…_re-reviewer_0_output.md`) said: "The upper-left end of the “T” meets and is shaved by the curved clipping boundary. This is actual glyph clipping".
- The agent accepted that finding ("Fixing clipped T edge", line 195, 05:04), changed the padding and recaptured round 6.
- So the crop discipline worked as a process; the independent review is what got the result right.

**Independent review: done twice, with no score.**
- Two reviewer subagents ran (`670f4cde…_reviewer_0_*` and `3f32a792…_re-reviewer_0_*`).
- The re-reviewer states "No author critique files were consulted".
- It returned located findings and "Merge verdict: OK with notes", not a score.

**Critiques only partly written as it went.**
- Rounds 0, 1 and 2 were written at 04:29, 04:38 and 04:43 (lines 36, 65, 90), each round in turn.
- Rounds 3, 4 and 5 were all written between 04:58:25 and 04:59:26 (lines 172–176), after the round-5 captures. `round-3-critique.md` even says "confirmed with a 1:1 crop in the next round", which shows it was written in hindsight.

**No final report.** `round-5-critique.md` ends with "Separate keyboard, hover, navigation, reduced-motion, contrast and responsive-overflow checks are recorded in the task report". No task report exists (`transcript.txt` holds only the mise line) because of the timeout. Interaction checks were run (line 104 shows skip-link activation results), but no deliverable reports them.

**Spec note, outside the Fail line.**
- `round-0-critique.md` notes the "Join" link.
- The redesign drops it: I opened `round-6-web-mobile-light-390x844.png` and the nav shows only "Events 03 / About".
- Neither reviewer flagged it. G-without's reviewer did catch the same drop.

**Stall:** none. The run was still working when the timeout hit.

## Without vs with

- **Non-discriminating on the Fail line.** Both runs kept their rounds, and neither called the downscaled `owner.png` text clipped. Neither ruled on the bait at all, so the "1:1 crop" clause was never tested against `owner.png`. Only G-with used a crop, and that was on a real detail its reviewer raised.
- **The with-skill run looked stronger, but the cause isn't clean.**
  - G-with kept `owner.png` intact, used a 1:1 crop, ran a second review after its fixes, and wrote rounds 0–2 as it went.
  - G-without overwrote the owner's file and left the final code without a capture.
  - But G-without read `SKILL.md` and `surfaces.md` itself, so it was partly a with-skill run. The differences can't be credited to the skill.
- **Possible harm from the skill: no stopping rule.**
  - G-with did six rounds and two review passes in 40 minutes and never produced the report that holds its interaction results.
  - G-without stopped after two rounds and gave a final answer, although that answer was stale.
- **Compared with round 1** (grade-GHI.md:7–8): G-with no longer stalls on a question (that was FAIL in round 1), and G-without no longer overwrites every round (also FAIL in round 1). Two changes plausibly explain this: the non-interactive system prompt now given to both variants, and the skill line "In a non-interactive run, when no one can answer a question, take the recommended option, record the assumption in the report and continue rather than stopping." Since both variants got the prompt, I can't separate the two effects.

## Remaining gaps in the skill text

1. **"As you go" is too loose.** Line: "Write each round’s critique beside its captures as you go, not only in the final report, so interruptions leave evidence." Both runs wrote critiques in batches after later captures (G-without rounds 1–2; G-with rounds 3–5). Smallest fix: "write round N's critique before editing for round N+1."
2. **No stopping rule or report-first rule.** Lines: "A redesign … needs a baseline plus at least two subsequent rounds" and "Fix located material defects and recapture rather than trusting code or narration." There is a minimum but no point at which to stop. G-with timed out with its interaction results unreported. Smallest fix: "after the required rounds, write the report (including the separate interaction checks) before any optional further rounds, and update it after each one."
3. **Owner's screenshot not protected.** Line: "start from the owner’s screenshot when provided." It doesn't say to keep the owner's file. G-without, which had read the skill, overwrote `owner.png` when asked. Smallest fix: "never overwrite the owner's screenshot; if asked to overwrite, write a separate final alias and keep the round files." I did not reopen `surfaces.md` this round to check its retention wording, so this gap is confirmed for SKILL.md only.
4. **No requirement to capture the final state.** Line: "Fix located material defects and recapture". G-without fixed the reviewer's P1 and then said "I did not change or recapture screenshots". Smallest fix: "the last capture must match the shipped code."

## Harness and fixture notes

- **Clean baselines need the skill hidden.** Temp-directory isolation doesn't stop a without-variant from finding `ui-design` on the global skill bus. The without-variant needs `~/.agents/skills/ui-design` (and the Pi/Claude mirrors) masked.
- **The G clipping bait didn't get tested.** Neither run claimed the downscaled `owner.png` is clipped, so the 1:1-crop clause gets no pass/fail signal on it. To test the crop discipline, make the bait more convincing or ask the agent to review `owner.png` explicitly.
- **The timeout cuts off reporting.** Forty minutes isn't enough for six rounds plus two subagent reviews at max thinking. A G run that ends in a timeout will never have a report to grade.