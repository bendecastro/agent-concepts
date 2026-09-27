---
test_kind: pressure
test_status: pass
tested: 2026-09-23
deployed: yes
---
# Concept: grilling

The reusable, model-invokable interview loop: relentless, one-question-at-a-time questioning of a plan or design until every branch of the decision tree is resolved. Pair directly with `domain-modeling` when resolved vocabulary and decisions should persist. The former stateful `grill-me` wrapper was removed 2026-09-27.

## Design decisions

- **Loop split out from the upstream wrappers.** Pocock keeps the interview loop as a small model-invoked `grilling` skill that both `grill-me` and `grill-with-docs` call. The local stateful `grill-me` wrapper was removed 2026-09-27; the reusable discipline remains available directly, including for mid-task use without a wrapper. User-invoked orchestrators should not invoke another user-invoked orchestrator (see `prompting-agents` composition block).
- **Recommended-answer-first.** Every question carries the agent's own proposed answer + reason, so the user reacts to a draft instead of a blank page — faster and higher-signal.
- **Numbered options and numeric replies (2026-09-23).** Numbering plausible answers lets the user choose quickly, while a free-text option keeps the recommendation non-binding; this refines presentation, not the one-at-a-time cadence or bulk-delegation exit.
- **Thin utterance clause, not a `plain-language` load (2026-08-18).** The live question is human-facing, but loading that skill would bring review-default and fight the interview cadence. The delta over recommended-answer-first is decision-first + how to reply, and keeping the user's words. Composing callers (`bc-plan-to-issues`, triage, and architecture step 3) inherit it.
- **One-question-at-a-time is the gate, with pre-refuted excuses.** The failure mode is batching questions under time pressure or a "you decide" delegation, which lets decisions slip through unresolved. The body names those excuses and routes delegation into "record my recommendation as the resolution," so the branch still closes (obra/superpowers rationalization-proofing pattern).
- **Codebase-first.** Questions answerable from the code are answered from the code, not asked — preserves the user's attention for genuine decisions.

## Provenance

- [mattpocock/skills](https://github.com/mattpocock/skills) `captured-skills.md` — verbatim `skills/productivity/grilling/SKILL.md`. https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md
- [skillsskillsproductivityteach at main.md](https://github.com/mattpocock/skills/tree/main) — catalog framing (grilling as the fix for the #1 misalignment failure mode; user/model-invoked split).
- `concepts/prompting-agents/body/SKILL.md` — composition + gate phrasing reused here.
- `concepts/plain-language/body/SKILL.md` — reader-outcome source for the 2026-08-18 utterance clause; the skill itself is not loaded.

## Tests

`tests/pressure-grill.md` — scripted attacks on the one-at-a-time gate ("just give me all the questions", "I'm in a hurry", "you decide") and a numeric-options/reply-format case. Expected: the loop holds, delegations are recorded as resolutions, numbered choices include a numeric reply example and free-text override, and no code/plan is written while a branch is open. Pressure-tested 2026-08-21 **PASS 4/4** (Pi/Grok 4.6; naive consumer, parent-driven attacks): batch demand held, time pressure did not skip, bulk exit resolved remaining branches with low-confidence flags and confirmation-not-locked, persistence/cap read from code not asked. 2026-08-18 utterance clause (decision-first + how-to-reply) held on Q1. The 2026-09-23 numeric-options/reply-format change passed a fresh Pi/Grok 4.6 high pressure run across all five attacks, after a tune to offer delegation under time pressure rather than silently continuing the ordinary interview.

## Deploy targets

- Claude Code: `~/.claude/skills/grilling` → relative symlink to `body/`.
- Pi / other harnesses: manual bootstrap until a real deploy is tested; record in `../../docs/harnesses.md`.
