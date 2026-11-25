# Write the bc-agent glossary

Why: the bc-agent infrastructure has no shared vocabulary page, and several words clashed.
Done when: `glossary.md` defines the settled terms in the domain-modeling format, grouped by area.
Stage: next
Blocked by: 004-vocabulary-renames
Kind: docs
Source: bc-init-agent
Planned: grilled with the owner 2026-11-25 (decisions in the bc-init-agent grill; summary below)

## Steps

- [x] Concepts and deployment: concept, skill, kernel, body, raw source, inbox, ingest, provenance, deploy, harness, private concept, overlay. (harness defined once here, not repeated under Agents and runs.)
- [x] Gates and checks: gate, check, hard rule, static check, artifact check, dynamic check, guardrail (fitness function), performance budget, budget chain, hot path, baseline, ratchet, regression allowance, noise, measurement harness, pressure test, lint. (guardrail terms placed under a separate Performance guardrails heading; dropped budget chain and regression allowance, used nowhere in the repo but this item; guardrail and fitness function merged, fitness function listed as the word to avoid.)
- [x] Tickets and work: ticket, work item (ticket in the local tracker `work/`), issue (ticket on GitHub), slice, drain, claim, rework, landing.
- [x] Agents and runs: harness, agent, parent, subagent (child), role, worker, scout, swarm, track, routing decision, evidence anchors, run folder, manifest, artifact, packet, council, worktree. (run directory, the common wording in bc-swarm, recorded as the word to avoid for run folder.)
- [x] Link the glossary from AGENTS.md; lint green. (docs/README.md lists no root files, so not linked there.)

## Outcome


