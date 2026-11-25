# Apply the settled vocabulary renames

Why: "gate" names both a discipline and the check command, and some swarm jargon does not say what it does.
Done when: discipline gates are called hard rules, the swarm terms are renamed, ticket/issue wording follows the rule, and lint is green.
Stage: next
Blocked by: 003-journal-to-bc-agent
Kind: docs
Source: bc-init-agent
Planned: grilled with the owner 2026-11-25 (decisions in the bc-init-agent grill; summary below)

## Steps

- [x] Rename discipline gates to hard rules: canon, provenance, test, immutability, capture and recovery rule (AGENTS.md, skills, lint messages, status page). "Gate" then means only `scripts/gate`.
  Note: ui-design "Capture gate" became "Capture rule" (no capture gate exists in bc-swarm/bc-drain-issues; supervisor approved). bc-drain-issues "cloud-lane provenance gate", Gate A/B, "the full gate" and similar other uses stay for a later decision. Pressure-test result logs keep old words as historical evidence.
- [x] Rename "the tooth" to routing decision and "thin-parent guard" to evidence anchors in `bc-swarm` (body, CONCEPT.md, tests).
  Note: also updated quotes in index.md, docs/guides/harnesses.md and agent-kernel CONCEPT.md; the dated tune log in tests/pressure-bc-swarm.md keeps "Rewrote the tooth" as history.
- [x] Ticket/issue wording: tracker-neutral text says ticket, GitHub-dependent text says issue (`to-tickets`, `plan-slicing`, others found by search); no skill renames.
  Note: to-tickets is GitHub-only, so it now says GitHub issues; plan-slicing is tracker-neutral, so tickets (template tag now `<ticket-template>`). bc-plan-to-pipeline tracker mode, diagnosing-bugs "bug issues"/Agent Brief and code-review "issue, PRD, ticket" left as borderline.
- [x] Record outside-repo text that still uses the old words (Pi's swarm-mode prompt) as a line in `work/0-ideas.md`.
- [x] Lint and gate green.

## Outcome


