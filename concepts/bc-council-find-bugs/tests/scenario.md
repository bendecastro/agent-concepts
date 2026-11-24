# Pressure scenario: bc-council-find-bugs on the practice project

Plan decision 10: the pressure-test model stands in for every advisor. Consumer model: the
pressure-test model from the private config (2026-11-24: `openai-codex/gpt-6.1-terra`, thinking
low), headless `pi -p`. Never use real council advisors.

## Setup

1. `scratch=$(mktemp -d)`. Per run, copy `../../find-bugs/tests/practice-project/` (never
   `answer-key.md`) to `$scratch/<run>`, `git init -b main`, scaffold a work pipeline with
   `python3 concepts/bc-init-agent/body/scaffold.py --root . --slug shopkit --archetype code`,
   add a `work/order.md` holding only a heading, commit.
2. Stand-in advisors: copy the user agent profiles except `council-*` into `$scratch/agents`, add
   three read-only profiles `council-standin-1..3` (tools read/grep/find/ls, model the
   pressure-test model, thinking low, `inheritSkills: false`), and bind that folder over the user
   agent folder so only the stand-ins are on the council.
3. Run from `$scratch/<run>`:
   `bwrap --dev-bind / / --tmpfs <overlays folder> --bind $scratch/agents <user agents folder>
   pi -p --model <model> --thinking low --no-swarm -nc -ns --no-prompt-templates
   --skill <bc-council-find-bugs/body> --skill <council-chain/body> --skill <find-bugs/body>
   --skill <council-mode/body> --session-dir $scratch/sess-<run> "<prompt>"`.
   The skill has `disable-model-invocation`, so the prompt must start with the slash command.

Prompt: `/skill:bc-council-find-bugs whole repository`, then harness notes: every subagent runs on
the pressure-test model at low thinking; headless, so run subagents in the foreground or wait for
them; the owner is away and answers the filing question with `all`, so file in the same session,
then clean up.

## Pass (each run), graded from artifacts against `../../find-bugs/tests/answer-key.md`

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
