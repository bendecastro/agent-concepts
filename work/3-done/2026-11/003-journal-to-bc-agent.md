# Move the journal to .bc-agent/log.md

Why: the bc-agent layout keeps the project journal at `.bc-agent/log.md`; two journals would split history.
Done when: root `log.md` is gone, its entries open `.bc-agent/log.md`, and no file names the old path.
Stage: next
Blocked by: 002-docs-reshape
Kind: docs
Source: bc-init-agent
Planned: grilled with the owner 2026-11-25 (decisions in the bc-init-agent grill; summary below)

## Steps

- [x] `git mv log.md .bc-agent/log.md`, keeping the scaffold's durable-facts intro. Intro rewritten to cover both journal entries and durable facts; the scaffold's one entry re-headed in the `## [date] op | subject` form at the bottom.
- [x] Rewrite every reference to root `log.md` (AGENTS.md, lint, skills that say append to `log.md`). Skill bodies that say `log.md` mean a scaffolded project's, vault's or teach host's log and stay unchanged; lint/portability exemptions keyed on the name or new path.
- [x] Lint and gate green.

## Outcome

Done. The journal is `.bc-agent/log.md` with history following (`git log --follow`); lint and portability check point at it; mentions of other projects' `log.md` were left alone. Gate green locally (468 passed, tree d6014365) and in GitHub CI.


