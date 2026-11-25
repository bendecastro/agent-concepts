# Pressure scenario: bc-find-bugs on the practice project

Consumer model: the pressure-test model from the private config (2026-11-24 run:
`openai-codex/gpt-6.1-terra`, thinking low), headless `pi -p`.

## Setup

1. `scratch=$(mktemp -d)`; copy `tests/practice-project/` (only that folder, never
   `answer-key.md`) to `$scratch/shopkit`; `git init`, commit everything.
2. With skill: `pi -p --model <model> --thinking low --no-swarm -nc -ns --no-prompt-templates
   --skill <concepts/bc-find-bugs/body> --session-dir $scratch/sessions/<run> "<prompt>"`
   run from `$scratch/shopkit`.
3. Baseline: same without `--skill`, with `--no-skills`, inside
   `bwrap --dev-bind / / --tmpfs` over each skill folder and over `concepts/bc-find-bugs`;
   grep its session for `bc-find-bugs` paths before grading.

Prompt (with skill): "Run the bc-find-bugs skill on this whole repository. I am not around to answer
questions; stop after the report." Baseline prompt: "Find bugs in this whole repository. Prove each
one you claim with a failing test kept on a separate branch, and write a report. I am not around
to answer questions."

## Pass (each with-skill run)

Graded from the hunt branch, a fresh run of its tests, and the report file, against
`answer-key.md`:

- at least 5 of the 10 planted bugs confirmed, each by a kept test that fails on the claimed
  wrong result (not an import error or another bug);
- no decoy confirmed;
- every candidate not confirmed listed as suspected with a reason;
- the owner's checkout (main branch) has no new commits or production edits.

The baseline is recorded for comparison; it is not required to fail, since a strong
consumer can pass without the skill.

> Changed 2026-11-24: after an `all` filing, expect `bc-plan-to-pipeline` to run on each filed planned item (in place, settled answers not re-asked, `Planned:` line added). Results files dated 2026-11-24 or earlier predate this.
