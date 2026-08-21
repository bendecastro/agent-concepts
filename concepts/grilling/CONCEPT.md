---
test_kind: pressure
test_status: pass
tested: 2026-08-21
deployed: yes
---
# Concept: grilling

The reusable, model-invokable interview loop behind `/grill-me`: relentless, one-question-at-a-time questioning of a plan or design until every branch of the decision tree is resolved. Holds the discipline; `grill-me` is the user-invoked orchestrator that wraps it (and adds persistence).

## Design decisions

- **Loop split out from the orchestrator.** Pocock keeps the interview loop as a small model-invoked `grilling` skill that both `grill-me` and `grill-with-docs` call. We keep that split even though we merged the two orchestrators into one stateful `grill-me`: the loop is reusable discipline an agent can also reach for mid-task without a slash command, and a user-invoked orchestrator shouldn't invoke another user-invoked one (see `prompting-agents` composition block).
- **Recommended-answer-first.** Every question carries the agent's own proposed answer + reason, so the user reacts to a draft instead of a blank page — faster and higher-signal.
- **Thin utterance clause, not a `plain-language` load (2026-08-18).** The live question is human-facing, but loading that skill would bring review-default and fight the interview cadence. The delta over recommended-answer-first is decision-first + how to reply, and keeping the user's words. Orchestrators that call this loop (`grill-me`, `bc-plan-to-issues`, triage, architecture step 3) inherit it.
- **One-question-at-a-time is the gate, with pre-refuted excuses.** The failure mode is batching questions under time pressure or a "you decide" delegation, which lets decisions slip through unresolved. The body names those excuses and routes delegation into "record my recommendation as the resolution," so the branch still closes (obra/superpowers rationalization-proofing pattern).
- **Codebase-first.** Questions answerable from the code are answered from the code, not asked — preserves the user's attention for genuine decisions.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — verbatim `skills/productivity/grilling/SKILL.md`. https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md
- [skillsskillsproductivityteach at main.md](https://github.com/mattpocock/skills/tree/main) — catalog framing (grilling as the fix for the #1 misalignment failure mode; user/model-invoked split).
- `concepts/prompting-agents/body/SKILL.md` — composition + gate phrasing reused here.
- `concepts/plain-language/body/SKILL.md` — reader-outcome source for the 2026-08-18 utterance clause; the skill itself is not loaded.

## Tests

`tests/pressure-grill.md` — scripted attacks on the one-at-a-time gate ("just give me all the questions", "I'm in a hurry", "you decide"). Expected: the loop holds, delegations are recorded as resolutions, no code/plan written while a branch is open. Pressure-tested 2026-08-21 **PASS 4/4** (Pi/Grok 4.6; naive consumer, parent-driven attacks): batch demand held, time pressure did not skip, bulk exit resolved remaining branches with low-confidence flags and confirmation-not-locked, persistence/cap read from code not asked. 2026-08-18 utterance clause (decision-first + how-to-reply) held on Q1.

## Deploy targets

- Claude Code: `~/.claude/skills/grilling` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../docs/harnesses.md`.
