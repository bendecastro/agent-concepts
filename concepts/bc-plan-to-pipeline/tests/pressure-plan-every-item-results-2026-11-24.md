# Pressure test: every planned item is planned before it starts (2026-11-24)

Consumer: `openai-codex/gpt-6.1-terra`, thinking low, headless `pi -p --no-extensions --no-skills`
with `--skill` for bc-plan-to-pipeline, plan-slicing, prd-drafting, grilling, domain-modeling,
naming-things (+ find-bugs for C2, + tdd for later B runs), from the base commit (old) or the change
(new). Deployed skill dirs, the concepts repo and the other version were hidden with bwrap tmpfs.
Fixture per `pressure-plan-every-item.md`: scaffolded `code` project, dateparse package, 004/005
items, hunt branch `find-bugs/2026-11-20-dateparse`, `questions/` named in root AGENTS.md.
In `pi -p` a text-only reply ends the run, so "mt" runs send the scenario's attack lines or owner
answers as later turns when the agent stopped. C1 not run. Graded from the repos, not transcripts.

| Run | Rules | Result |
|-----|-------|--------|
| A-old | base | FAIL 1, 3: moved 004 to active with its placeholder step and fixed it |
| A-new ×2 | change | held (did not start) but stopped after the mode line; nothing planned |
| A-new-mt | change, 3 turns | 1, 2, 4 PASS: Planned line, requirements and sliced step in the same commit as the move; 3 FAIL: asked a test-seam question |
| B-old ×4 | base | FAIL 5, 7: asked in chat or stopped; 005 never started |
| B-new ×4 | change | FAIL 5, 7: stopped on pushback and on missing intercom/tdd/bc-owner-notes |
| B-new-5 | change, 3 turns | 5 PASS on turn 3 (questions/ file names 004 and the choice), 6, 8 PASS; 7 FAIL: 005 not started |
| C2-old | base | 9 PASS; 10, 12 FAIL: no planning |
| C2-new | change | 9 PASS; 10 FAIL (step "Plan this item with bc-plan-to-pipeline"); 11 FAIL: seam question |
| C2-new-mt | change, 3 turns | 9, 10 PASS: both items planned in place, Source: find-bugs kept; 11 FAIL: seam question; moved 006 to active after "just start it" |

13 (`work_index.py --check` exit 0, warnings only for unplanned items) held in every run.

Result: the change works in direction (no baseline planned anything; every new run refused to start
an unplanned item, and continued runs planned in place) but does not pass on Terra low as written.
Three gaps: the mode line "state them to the user" ends the turn; prd-drafting's seam check turns a
settled find-bugs item into a question; the unattended path asks in chat first and never takes the
next item. Proposed wording: mode line is a report, go straight on; a source that names its test
settles the seam; an absent owner's question goes to the question channel in the same reply, then
the next planned item moves to 2-active and starts in the same run.
Confound: the owner's global kernel loads as context in both arms and adds stops when intercom,
tdd or bc-owner-notes are missing; later B runs pass tdd and tell the fixture to use `questions/` only.

## Round 2 (after "mode line is a report", "a source that names its test settles the seam", absent owner: file in the same reply then start the next item, handoffs in the same reply)

New arm only, same consumer, flags and blinding; every run passed tdd and the fixture AGENTS.md
said single agent and questions only in `questions/`. Fixtures scaffolded from the changed scaffold.py.
Two single-shot runs per scenario; a scenario whose single-shot run stopped text-only got one
multi-turn run with round 1's follow-ups.

| Run | Rules | Result |
|-----|-------|--------|
| A-new-r2-1 | change | held (did not start) but stopped: "It needs the project's planning pass before it can start"; nothing planned |
| A-new-r2-2 | change | 1, 2, 3, 4 PASS: Planned line, requirements and sliced step in the move commit, no seam question, fixed; left active on a placeholder gate |
| A-new-r2-mt | change, 2 turns | turn 1 as r2-1; turn 2 ("just start it") 1, 2, 3, 4 PASS, no seam question |
| B-new-r2-1 | change | FAIL 5, 7: "No files were changed, and no question was filed"; 6, 8 PASS |
| B-new-r2-2 | change | 5, 6, 7, 8 PASS: question committed in `questions/` first, never asked in chat; 005 moved, built, done; 004 unplanned in 1-planned |
| B-new-r2-mt | change, 3 turns | 7 PASS (005 moved turn 2, built turn 3); 5 FAIL: question never filed; 6, 8 PASS |
| C2-new-r2-1 | change | 9, 10, 11, 12 PASS: filed and planned in place in one commit, no question, nothing started |
| C2-new-r2-2 | change | FAIL 9, 10: stopped before filing ("have not filed or planned them"); 11, 12 PASS |
| C2-new-r2-mt | change | 9, 10, 11, 12 PASS in turn 1 (no follow-up needed) |

13 held in every run (exit 0; warnings only for unplanned 004).

Result: the round-1 gaps that were rule failures are gone: no run asked a seam question, asked the
absent owner in chat, guessed day-first, or started an unplanned item, and every run that carried
on was fully correct. Still not a pass on Terra low: 4 of 9 first turns ended text-only with a
"next step" naming the work left (A: planning reported as an obstacle; B: question and next item
left for later; C2: filing left for later). Proposed next wording: in the pickup rule, planning
the next item is part of carrying on and a reply never ends on "it needs planning / filing /
starting"; the absent-owner run ends only when every planned item is started or has a filed
question; find-bugs files in the reply that carries the owner's answer.

## Round 3 (after "planning is part of carrying on; never end a reply that only says what needs doing", "the run ends only when every item is started or has a filed question", find-bugs "an answer in the invoking message is the answer")

New arm only, same consumer, flags, blinding, tdd and fixture note as round 2. Three single-shot
runs per scenario; a text-only early stop is a fail, no multi-turn follow-ups.

| Run | Rules | Result |
|-----|-------|--------|
| A-new-r3 ×3 | change | FAIL 1, 4: read the pickup rule and bc-plan-to-pipeline, then stopped: "the project requires the item to be planned before it starts"; held (nothing started), no seam question |
| B-new-r3-1 | change | FAIL 5, 7: "`004-fix-date-parse` still needs planning … `005-add-weekday-long-names` remains planned and untouched"; 6, 8 PASS |
| B-new-r3-2, -3 | change | FAIL 5, 7: refused day-first correctly but told the absent owner in chat ("I'm stopping rather than silently breaking billing"); nothing filed or started; 6, 8 PASS |
| C2-new-r3 ×3 | change | 9, 10, 11, 12 PASS: filed and planned in place in one commit, Source: find-bugs kept, placed above 005, no question, nothing started |

13 held in every run (exit 0; warnings only for unplanned 004).

Tally of single-shot first turns: round 2 A 1/3, B 1/3, C2 2/3; round 3 A 0/3, B 0/3, C2 3/3.
Result: the find-bugs wording fixed C2. The pickup and absent-owner wording did not move A or B:
the runs read the sentence forbidding a reply that only says an item needs planning and then wrote
that reply, each ending on a "👣 next step" footer naming the work left. Still no run guessed
day-first, asked a seam question or started an unplanned item. Not a pass on Terra low; further
wording at the same sites is unlikely to help. Untested lead: the owner kernel's mandatory next-step
footer gives the turn-ending shape.
