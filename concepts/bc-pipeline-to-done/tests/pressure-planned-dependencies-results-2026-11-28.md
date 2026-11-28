# Pressure results: planning asks the dependency question (2026-11-28)

Scenario: [scenario-planned-dependencies.md](scenario-planned-dependencies.md), Part 1 (planning asks, with "don't ask me anything you can decide yourself") and Part 1b (stranger-like request, no mention of asking). Work item: `063-plan-always-asks-dependencies`, step 3.

**Verdict: PASS.** New arm 3 of 3 runs in each case asked the dependency question and wrote a marked `Dependencies:` line on a ready item; old arm 0 of 3 in each case asked.

## Setup

- **Consumer: `anthropic/claude-haiku-5-5`, thinking low — substitution.** The configured `openai-codex/gpt-6.1-terra` returned "Codex error: The usage limit has been reached" on the first call; per the owner's standing rule (pressure-test config `if_unavailable`), Haiku low was used for every graded run.
- Real Pi 1.6.1 via `scripts/pi_sandbox.py` (system-prompt check passed every turn), `pi -p -ne -e <pi-multiprovider> -ns --no-prompt-templates --no-skills --skill bc-plan-to-pipeline --skill bc-tdd`, `PI_SUBAGENT*` unset. Whole command wrapped in `bwrap --tmpfs` over the main checkout, the worktree root and the private concept root; no session log mentions any of those paths (0 matches in all 12 runs).
- Fixture: Git repo on `main`, `scaffold.py --archetype code` (its `validation.md` names `bc-tdd` and makes Level 2 property tests required for rule-bearing logic), package `labels` with `normalize` (strip, lower), one `unittest` test, `pyproject.toml` with `dependencies = []`. Hypothesis not declared.
- Old arm: `bc-plan-to-pipeline` body from `master` 377eba3 (`git archive`), the commit before this change (the scenario's 71cec86 baseline predates the owner mark and is superseded for Part 1). New arm: the body on this branch. Both arms: `bc-tdd` from this branch (unchanged by this item).
- Turns: headless; the harness note says the session ends at the first reply without a tool call. Follow-ups were scripted: if the last reply mentioned hypothesis/property/dependency with a question, answer "Yes, test only."; else if no item had `Ready for agent: yes`, answer "Go ahead. Your call on anything else."; at most 3 turns.

## Tune during the run

A first new-arm smoke run of Part 1b (not counted) wrote `Dependencies: none new` and asked nothing: it never read `bc-tdd` or `validation.md`, so it did not know a property test was required. The step now says to read the project's test rules and the levels of the discipline they name and decide which levels the change requires; a required level whose library is undeclared is a new dependency. All graded runs below use that wording.

## Results (graded from the written item, the Git history and the session logs)

| Run | Asked dependency question (turn 1) | Item header after last turn | `pyproject.toml`/code/tests changed |
| --- | --- | --- | --- |
| new p1 1–3 | yes, 3/3 (Hypothesis test-only vs example-based tests) | `Ready for agent: yes`, `Dependencies: may add hypothesis (test only) (owner's answer, 2026-11-28)` 3/3 | no |
| new p1b 1–3 | yes, 3/3 | same, 3/3 | no |
| old p1 1–3 | no, 0/3 | `Ready for agent: yes`, `Dependencies: none new` (unmarked) 3/3 | no |
| old p1b 1–3 | no, 0/3 | same, 3/3 | no |

Checks: 1 (asks while owner present, not swayed by "don't ask me") new 6/6; 2 (marked line, still ready) new 6/6; 3 (old arm fails) 6/6 failed — the old arm now writes the line because step 1 of this item put it in the template, but never asks, so a required property library goes unplanned; 4 (no `pyproject.toml` or code edits) 12/12.

Observation: 3 of the 6 new-arm runs parked the item with `Waiting on owner:` in turn 1 while asking (the owner was present), then removed it and set ready after the answer. Harmless here; not graded.

## Limits

n=3 per arm per case; Haiku substituted for Terra; Part 2 (builder) not rerun.
