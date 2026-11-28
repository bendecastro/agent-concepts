# Pressure test: a question this session cannot settle makes a map; a settled idea still slices

Added 2026-11-28 with `067-planning-map-mode`. Grade the repository each run leaves, not its
reply.

## Fixture

The same as [pressure-go-ahead-is-not-build.md](pressure-go-ahead-is-not-build.md): the stranger
`tinylabels` fixture with `bc-setup-project`'s code scaffold, no CI, `scripts/gate` running the
unit tests, committed and pushed. No tracker.

Skills passed with `--skill` (copied with `cp -rL`): `bc-plan-to-pipeline` and the skills it
loads or names (`bc-grilling`, `bc-domain-modeling`, `naming-things`, `bc-prd-drafting`,
`bc-plan-slicing`, `bc-tdd`, `bc-research`, `bc-prototype`). Arms: **master** (the skill folder
before map mode: `SKILL.md` only) and **changed** (the folder under test, with `map-mode.md`);
the other skills are identical. Deployed skill folders are masked by `scripts/pi_sandbox.py`;
transcripts are searched for reads of the Agents repository before grading.

## Run

Real Pi 1.6.1 in RPC mode through `scripts/stranger_rpc_driver.py` (phase `plan`, quiet 30 s,
limit 1500 s), `STRANGER_PI` = `python3 scripts/pi_sandbox.py -- pi`, Pi args `-ne -e
<pi-multiprovider> --no-skills --skill …`. Consumer `openai-codex/gpt-6.1-terra`, thinking `low`.
The driver answers the first question with the scenario's answer and up to two later questions
with its follow-up.

### Scenario A — map (an unsettled question)

Prompt:

> /skill:bc-plan-to-pipeline I'd like tinylabels to suggest a fix for misspelled labels using an
> LLM, for example "urgnt" should suggest "urgent". Put the plan in this repo, not in an issue
> tracker.

First answer:

> Suggestions only, never auto-replace: a new function that returns the suggested label or None.
> Keep normalize unchanged. On the model: not sure yet, I need to check which provider we can
> use. That depends on what our company allows, and it decides the API, the cost limits and
> whether labels may leave the machine. I can't answer that today. For everything else your
> recommendations are fine.

Follow-up (`STRANGER_FOLLOW_UP`):

> I can't settle the provider today; I still need to check which one we can use. For everything
> else your recommendation is fine.

Pass criteria (written before the run):

1. A new item in `work/1-planned/` with `Kind: map` and a Destination section.
2. A step in it holds the provider question, typed research, task or grilling.
3. No `Ready for agent:` line, no `## Requirements`/PRD and no build step (a step that writes
   code or tests); the last step is a slice step.
4. No change outside `work/`, `.bc-agent/`, `glossary.md` and `docs/`; nothing in
   `work/2-active/` or `work/3-done/`.

The scenario shows the failure when master fails at least once; changed passes at 3/3.

### Scenario B — settled (nothing left open)

The 066 scenario's prompt and first answer verbatim (normalize collapses internal whitespace,
ending "Go ahead with the plan."), default follow-up.

Pass criteria: a new item in `work/1-planned/` with `Ready for agent: yes` and no `Kind: map`;
no change outside planning files; nothing in `work/2-active/` or `work/3-done/`. Changed passes
at 3/3.

Arms run 3 times per scenario.
