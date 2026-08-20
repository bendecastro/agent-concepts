---
test_kind: pressure
test_status: pass
tested: 2026-07-16
deployed: yes
---
# Concept: writing-plans

User-invoked implementation-plan authoring skill for turning an approved spec or resolved requirements into agent-executable, test-first tasks.

## Design decisions

- **Plain plan, not PRD/issue publishing.** Existing `prd-drafting` and `issue-slicing` cover the GitHub pipeline; this concept covers standalone local implementation plans.
- **Agent-ready detail.** The body preserves upstream insistence on exact paths, commands, expected outputs, and code snippets because plans are often executed by fresh agents with no context.
- **No placeholder plans.** Placeholder bans are retained as a gate: a vague plan is worse than no handoff.

## Provenance

- [obra/superpowers `skills/writing-plans/SKILL.md`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/writing-plans/SKILL.md) — plan structure, task granularity, no-placeholder rule, self-review checklist.
- [obra/superpowers `skills/writing-plans/plan-document-reviewer-prompt.md`](https://github.com/obra/superpowers/blob/6fd4507659784c351abbd2bc264c7162cfd386dc/skills/writing-plans/plan-document-reviewer-prompt.md) — reviewer mindset referenced but not copied into body.
- `concepts/issue-slicing/` and `concepts/prd-drafting/` — local GitHub-oriented sibling concepts.

## Tests

`tests/scenario.md` — pressure-tested 2026-07-16 **PASS** (Grok) for vague/multi-subsystem/placeholder/handoff scenarios.

## Deploy targets

Deployed to the shared bus, Pi, and Claude Code by `scripts/deploy-local-skills.py`, which deploys every concept carrying a `body/SKILL.md`. This shipped with that bulk deploy rather than by a per-concept decision, so the intended deploy-after-test sequence did not hold here. Current state is in this file's frontmatter; `python3 scripts/lint.py` fails while a deployed concept is untested.
