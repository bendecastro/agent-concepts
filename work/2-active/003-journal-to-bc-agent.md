# Move the journal to .bc-agent/log.md

Why: the bc-agent layout keeps the project journal at `.bc-agent/log.md`; two journals would split history.
Done when: root `log.md` is gone, its entries open `.bc-agent/log.md`, and no file names the old path.
Stage: next
Blocked by: 002-docs-reshape
Kind: docs
Source: bc-init-agent
Planned: grilled with the owner 2026-11-25 (decisions in the bc-init-agent grill; summary below)

## Steps

- [ ] `git mv log.md .bc-agent/log.md`, keeping the scaffold's durable-facts intro.
- [ ] Rewrite every reference to root `log.md` (AGENTS.md, lint, skills that say append to `log.md`).
- [ ] Lint and gate green.

## Outcome


