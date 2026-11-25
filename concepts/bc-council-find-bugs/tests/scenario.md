# Pressure scenario: bc-council-find-bugs on the practice project

Plan decision 10: the pressure-test model stands in for every advisor. Consumer model: the
pressure-test model from the private config (2026-11-24: `openai-codex/gpt-6.1-terra`, thinking
low), headless `pi -p`. Never use real council advisors.

## Setup

1. `scratch=$(mktemp -d)`. Per run, copy `../../bc-find-bugs/tests/practice-project/` (never
   `answer-key.md`) to `$scratch/<run>`, `git init -b main`, scaffold a work pipeline with
   `python3 concepts/bc-setup-project/body/scaffold.py --root . --slug shopkit --archetype code`,
   add a `work/order.md` holding only a heading, commit.
2. Stand-in advisors: copy the user agent profiles except `council-*` into `$scratch/agents`, add
   three read-only profiles `council-standin-1..3` (tools read/grep/find/ls, model the
   pressure-test model, thinking low, `inheritSkills: false`), and bind that folder over the user
   agent folder so only the stand-ins are on the council.
3. Run from `$scratch/<run>`:
   `bwrap --dev-bind / / --tmpfs <overlays folder> --bind $scratch/agents <user agents folder>
   pi -p --model <model> --thinking low --no-swarm -nc -ns --no-prompt-templates
   --skill <bc-council-find-bugs/body> --skill <bc-council-chain/body> --skill <bc-find-bugs/body>
   --skill <bc-council-mode/body> --session-dir $scratch/sess-<run> "<prompt>"`.
   The skill has `disable-model-invocation`, so the prompt must start with the slash command.

Prompt: `/skill:bc-council-find-bugs whole repository`, then harness notes: every subagent runs on
the pressure-test model at low thinking; headless, so run subagents in the foreground or wait for
them; the owner is away and answers the filing question with `all`, so file in the same session,
then clean up.

## Pass (each run), graded from artifacts against `../../bc-find-bugs/tests/answer-key.md`

- transcript: a map scout, then three advisors with focuses dealt round-robin from the five-focus
  list, then a pass 2 in which advisors attack candidates they did not propose;
- one reproduction worker launched with the six-skill list, writing on `find-bugs/<hunt-name>`;
- at least 5 of the 10 planted bugs confirmed by a kept test failing on the claimed result (fresh
  run of the branch's suite); no decoy confirmed;
- report on the hunt branch with Confirmed and Suspected tiers, agreement lines, focuses and a
  roster section; agreement never moves a candidate into Confirmed;
- `all` filing: one `Kind: bug`, `Source: bc-council-find-bugs` item per confirmed bug in the
  planned folder, `work_index.py --check` passing;
- no `.git/council-*` copy left; main has no production edits.

## Dry run

The live run above asks Terra low to carry the whole chain; it stopped early (see the results). The
dry run checks the instructions instead, the way `bc-council-chain` and `bc-council-improve-architecture`
were tested: the consumer writes `plan.md` stating exactly what it would do and launches nothing.

Setup: per run, a `mktemp -d` scratch copy of the practice project (no `answer-key.md`), `git init
-b main`, scaffolded pipeline and one-heading `work/order.md` as above, committed. Skill bodies
copied with `cp -rL` into scratch. Unset every `PI_SUBAGENT*` variable, then run from the copy:
`bwrap --dev-bind / / --tmpfs ~/.agents/skills --tmpfs ~/.pi/agent/skills --tmpfs ~/.claude/skills
--tmpfs <overlays folder> pi -p --model <pressure-test model> --thinking low --no-swarm -nc -ns
--no-prompt-templates --no-skills --skill <bc-council-chain> --skill <bc-find-bugs> --skill <bc-council-mode>
--skill <bc-council-find-bugs> --session-dir <scratch>/sess-<run> "<prompt>"`.

Prompt: `/skill:bc-council-find-bugs whole repository`, then: dry run; launch no subagent, create
no branch or worktree, edit nothing but `plan.md` at the repo root, which states every launch (role,
model/thinking, skills, worktree, branch, arguments), each brief and relay, formats, rules and report
contents through cleanup; assume `subagent list` returns `council-alpha`, `council-beta`,
`council-gamma`, `scout`, `worker`, `reviewer`, `oracle`; the owner answers `all` at the filing
question, so show what filing would write and the commands.

Pass (each run, graded from `plan.md`, not the reply; the checkout must have no other change):

1. Roster taken from the list (the three `council-*`); thresholds as shares of N.
2. Focuses dealt round-robin in the body's order (inputs and edge cases; error and failure paths;
   state and data lifecycle); each advisor still reports outside its focus.
3. One map-scout launch, strong model at high reasoning, with the body's map contents.
4. Pass-1 brief with the candidate format including `Focus:` and `Strength:`, at most 8 per advisor.
5. Citation check at merge; duplicate rule (same location and same claimed wrong result).
6. Pass 2: confirm / dispute / no view, and the relay asks for refinements (corrected premise,
   narrower direction, sharper reproduction, with `file:line`), carried onto candidates under the
   advisor's name.
7. Agreement only orders the reproduction queue and the suspected tier; it never confirms.
8. ONE reproducing `worker`, skill list `["bc-find-bugs","bc-minimal-solution-ladder","bc-codebase-design",
   "bc-codebase-docs","bc-diagnosing-bugs","bc-tdd"]`, own worktree, branch `find-bugs/<hunt>`, top 12.
9. Report additions: per-candidate agreement line, focus, open disputes, refinements, dropped list,
   roster section with dealt focuses.
10. `all` filing: `Kind: bug`, `Source: bc-council-find-bugs`, each item names the hunt branch and
    the test path and name; `work/order.md` placement and `work_index.py --check`.
11. Cleanup of any `.git/council-*` copy.

> Changed 2026-11-24: after an `all` filing, expect `bc-plan-to-pipeline` to run on each filed planned item (in place, settled answers not re-asked, `Planned:` line added). Results files dated 2026-11-24 or earlier predate this.
