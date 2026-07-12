# Concept: grilling

The reusable, model-invokable interview loop behind `/grill-me`: relentless, one-question-at-a-time questioning of a plan or design until every branch of the decision tree is resolved. Holds the discipline; `grill-me` is the user-invoked orchestrator that wraps it (and adds persistence).

## Design decisions

- **Loop split out from the orchestrator.** Pocock keeps the interview loop as a small model-invoked `grilling` skill that both `grill-me` and `grill-with-docs` call. We keep that split even though we merged the two orchestrators into one stateful `grill-me`: the loop is reusable discipline an agent can also reach for mid-task without a slash command, and a user-invoked orchestrator shouldn't invoke another user-invoked one (see `prompting-agents` composition block).
- **Recommended-answer-first.** Every question carries the agent's own proposed answer + reason, so the user reacts to a draft instead of a blank page — faster and higher-signal.
- **One-question-at-a-time is the gate, with pre-refuted excuses.** The failure mode is batching questions under time pressure or a "you decide" delegation, which lets decisions slip through unresolved. The body names those excuses and routes delegation into "record my recommendation as the resolution," so the branch still closes (obra/superpowers rationalization-proofing pattern).
- **Codebase-first.** Questions answerable from the code are answered from the code, not asked — preserves the user's attention for genuine decisions.

## Provenance

- `raw/ingested/pocock-skills-upstream/captured-skills.md` — verbatim `skills/productivity/grilling/SKILL.md`. https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md
- `raw/ingested/skillsskillsproductivityteach at main.md` — catalog framing (grilling as the fix for the #1 misalignment failure mode; user/model-invoked split).
- `concepts/prompting-agents/body/SKILL.md` — composition + gate phrasing reused here.

## Tests

`tests/pressure-grill.md` — scripted attacks on the one-at-a-time gate ("just give me all the questions", "I'm in a hurry", "you decide"). Expected: the loop holds, delegations are recorded as resolutions, no code/plan written while a branch is open. Pressure-tested as part of the `grill-me` run (which calls this loop) — see grill-me CONCEPT.

## Deploy targets

- Claude Code: `~/.claude/skills/grilling` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../harnesses.md`.
