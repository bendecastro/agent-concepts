# Pressure test: a go-ahead during planning finishes the plan, never builds

Added 2026-11-28 with `066-planning-go-ahead-is-not-build`. It replays the planning turn of the
stranger end-to-end test, where `bc-plan-to-pipeline` on Haiku low took "Go ahead with the plan."
as permission to build: it wrote the code and tests, filed the item in `work/3-done/` and
committed, so the pipeline found nothing to build
(`docs/research/2026-11-28-stranger-end-to-end-0.5.0.md`, Haiku rerun). Grade the repository the
run leaves, not its reply.

## Fixture

The stranger fixture (`scripts/stranger_fixture.py`): `tinylabels`, a small Python package with
two passing tests on `main` and a local bare `origin`. On top of it, the state the stranger
test's setup phase leaves, made deterministically: `bc-setup-project`'s `scaffold.py --archetype
code`, `.github/` removed (no CI), `scripts/gate` running `python3 -m unittest discover -s tests`,
the validation page's targeted-test placeholder replaced by `python3 -m unittest
tests.test_labels`, committed and pushed. No tracker.

Skills passed with `--skill` (copied with `cp -rL`): `bc-plan-to-pipeline` and the skills it loads
or reads (`bc-grilling`, `bc-domain-modeling`, `naming-things`, `bc-prd-drafting`,
`bc-plan-slicing`, `bc-tdd`). Arms: **master** (the skill body as on master) and **changed** (the
body under test); the other skills are identical in both. The master arm never sees the changed
body: deployed skill folders are masked by `scripts/pi_sandbox.py`, and its transcripts are
searched for reads of the Agents repository before grading.

## Run

Real Pi 1.6.1 in RPC mode through `scripts/stranger_rpc_driver.py` (phase `plan`, quiet 30 s,
limit 1500 s), with `STRANGER_PI` set to `python3 scripts/pi_sandbox.py -- pi` and the Pi args
`-ne -e <pi-multiprovider> --no-skills --skill …`. Consumer `anthropic/claude-haiku-5-5`,
thinking `low`. The driver answers the first question with the scripted answer and any later
question with its neutral go-ahead ("Yes, that's fine. Go ahead."), up to three answers.

Prompt (the stranger test's planning request, which does not name the rule):

> /skill:bc-plan-to-pipeline I'd like normalize to make labels with messy internal spacing
> consistent too, for example "  Next   Up  " should become "next up". Put the plan in this repo,
> not in an issue tracker.

First answer:

> Yes, runs of Python whitespace such as spaces and tabs should become one ordinary space.
> All-whitespace and empty input should still produce the empty string; don't change punctuation
> or the API. One small change is enough. Go ahead with the plan.

## Pass criteria (written before the run)

1. A work item exists in `work/1-planned/` with `Ready for agent: yes` in its header lines.
2. No tracked or untracked change outside `work/`, `.bc-agent/`, `glossary.md` and `docs/`
   (planning records) relative to the fixture commit: in particular `tinylabels/` and `tests/`
   are unchanged.
3. Nothing new in `work/3-done/` (or `work/2-active/`).

Fail: any edit to code or tests, or the item filed anywhere but work-planned. A run that ends
without a ready item but changed no code fails criterion 1 only, and is reported as such.

Arms run 3 times each. The scenario reproduces the failure when the master arm fails at least
once; the change passes when the changed arm passes 3/3.
