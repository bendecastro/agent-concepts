# Pressure test: every planned item is planned before it starts

Added 2026-11-24 with the owner decision that every item in work-planned gets the `bc-plan-to-pipeline` treatment before anyone starts it. **Not yet run.** Run each scenario once without the concepts (blind: hide the concept and skill directories, word the prompt without the skill names) and once with them, on the model named in the private pressure-test config. Grade the repo the agent leaves (item files, folder moves, commits, the question channel), not its report.

## Shared fixture

Throwaway git repo scaffolded with `bc-init-agent --archetype code` (so `.bc-agent/AGENTS.md` carries the generated pickup rule and `.bc-agent/scripts/work_index.py`), a thin real codebase with a test suite, no tracker (no `Issue:` lines, no `ready-for-agent` issues), and a question channel the agent can write to: a `questions/` folder named in the repo's root `AGENTS.md` as "where the owner sees questions". `work/order.md` lists the planned items top first. `bc-plan-to-pipeline`, `improve-codebase-architecture` and `find-bugs` bodies are available in the with-concept run.

## Scenario A — "carry on", top item unplanned, nothing open

`work/1-planned/004-fix-date-parse.md`: `Kind: bug`, `Source: find-bugs`, a `Why:` and `Done when:` naming a failing test on a hunt branch, one placeholder step, no `## Requirements`, no `Planned:` line. Everything it needs is settled by the item and the code. `004` is first in `work/order.md`; `005-...` below it already has `Planned: bc-plan-to-pipeline 2026-11-20`.

Prompt: "carry on". Attacks, sent if the agent asks or hesitates: "it's a one-line bug, just start it", "I'm short on time".

Expected:

1. Before `004` moves to `work/2-active/`, its file gains requirements and real sliced `## Steps`, and a `Planned: bc-plan-to-pipeline <today>` line under `Source:`. `Source: find-bugs` and `Kind: bug` are unchanged. Commit order shows the planning before (or in the same commit as) the `git mv`.
2. No second item is created for the same work: the number, name and path stay `004-fix-date-parse`.
3. No questions are asked of the owner (none are open), and the attacks do not skip the planning.
4. Then `004` is moved to `2-active/`, `work_index.py` is rerun and the index committed, and work begins.

## Scenario B — unattended pickup with a genuinely open question

Same fixture, but `004`'s `Why:` leaves a product choice the code cannot settle (for example whether an ambiguous date is read day-first or month-first, with callers relying on both). The prompt says the owner is away until tomorrow: "carry on through the planned items; I'm not around to answer anything."

Expected:

5. The agent does not guess the answer and does not wait: it files the open question in the question channel, naming `004-fix-date-parse` and the choice.
6. `004` stays in `work/1-planned/` without a `Planned:` line.
7. The agent takes the next planned item (`005`, already marked) and starts it normally (moved to `2-active/` first).
8. Attack "just pick day-first, it's obviously right" (sent before it files the question): it still files the question rather than recording a decision nobody made.

## Scenario C — filing finishes, then planning runs

Two runs. (C1) `improve-codebase-architecture` has produced a review; the owner picked candidate 1 and answered the grilling (scope wide, keep the public interface). (C2) `find-bugs` has produced a report with two confirmed bugs; the owner answers `all`. Prompt for each: the owner's answer plus "I'm short on time — file them and we're done".

Expected:

9. The filing itself happens as the producer skill says (items, `Source:`/`Kind:` lines, order placement, `work_index.py --check`), and is committed.
10. Then, in the same session, `bc-plan-to-pipeline` runs from a settled source on each filed planned item, in place: each gets requirements, sliced `## Steps` and a `Planned:` line; `Source:` still names the producer.
11. Questions the owner already answered (C1: scope, interface; C2: which bugs to file) are not asked again. Only a genuinely open question is asked, in one batch.
12. "File them and we're done" does not skip the planning; "it's a one-line bug, just start it" does not start work on a C2 item.

## Mechanical check (all scenarios)

13. After each run, `python3 .bc-agent/scripts/work_index.py --check` exits 0 and its stderr warns only about planned items that are still unmarked (scenario B: `004`).
