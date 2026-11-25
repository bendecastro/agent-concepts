# Apply the settled vocabulary renames

Why: "gate" names both a discipline and the check command, and some swarm jargon does not say what it does.
Done when: discipline gates are called hard rules, the swarm terms are renamed, ticket/issue wording follows the rule, and lint is green.
Stage: next
Blocked by: 003-journal-to-bc-agent
Kind: docs
Source: bc-init-agent
Planned: grilled with the owner 2026-11-25 (decisions in the bc-init-agent grill; summary below)

## Steps

- [ ] Rename discipline gates to hard rules: canon, provenance, test, immutability, capture and recovery rule (AGENTS.md, skills, lint messages, status page). "Gate" then means only `scripts/gate`.
- [ ] Rename "the tooth" to routing decision and "thin-parent guard" to evidence anchors in `bc-swarm` (body, CONCEPT.md, tests).
- [ ] Ticket/issue wording: tracker-neutral text says ticket, GitHub-dependent text says issue (`to-tickets`, `plan-slicing`, others found by search); no skill renames.
- [ ] Record outside-repo text that still uses the old words (Pi's swarm-mode prompt) as a line in `work/0-ideas.md`.
- [ ] Lint and gate green.

## Outcome


