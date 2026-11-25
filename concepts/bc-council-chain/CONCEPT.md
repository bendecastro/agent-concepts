---
test_kind: pressure
test_status: partial # architecture chain unchanged after extraction, 4/4 dry runs (2026-11-24, Terra low); no live council run through the recipe; second chain not yet built
tested: 2026-11-24
deployed: yes
---
# Concept: bc-council-chain

The shared recipe every `bc-council-<job>` skill loads to run a parent skill through the advisor council: roster from whoever is on the council today, one shared map, pass 1 independent candidates, citation-checked merge, pass 2 cross-examination, advisor fallbacks and sandbox-copy cleanup. Each chain supplies only its job-specific parts, listed in the body's "What a chain must define". Not run directly.

## Design decisions

- **Extracted at the second chain (owner plan `work/3-done/2026-11/019-council-find-bugs.md`, decision 6, 2026-11-24).** `bc-council-find-bugs` would have been the second copy of these steps; the second copy is the moment to extract. The steps were moved from `bc-council-improve-architecture` without behaviour change; only the job-specific parts (map contents, candidate format, duplicate rule, agreement rule, report, filing) stayed in that chain. The rationale for each moved step (shared map, shares-of-N thresholds, strong map scout, citation check, sandbox copy) is recorded in [bc-council-improve-architecture](../bc-council-improve-architecture/CONCEPT.md), where those decisions were made.
- **Explicit chain interface.** The body lists what a chain must define, so a new chain is written against a checklist rather than by copying an existing chain.
- **"Never force agreement" lives in the recipe.** The rule binds every verdict rule a chain writes; each chain still defines its own thresholds.
- **Roster overlay moved here.** The private overlay `~/.config/agent-concepts/overlays/bc-council-chain.md` (roster, map-scout model, sandboxed advisor kinds) replaces the per-chain overlay `bc-council-improve-architecture.md`. Generic wording (discover `council-*` profiles, strongest model) is the stranger's full instruction.
- **`bc-council-mode` stays close to its upstream.** The chain steps live here rather than in `bc-council-mode`, which is a lightly modified copy of the `pi-subagents` council skill.

## Provenance

- Owner plan [council-find-bugs](../../work/3-done/2026-11/019-council-find-bugs.md), 2026-11-24.
- Steps moved from [bc-council-improve-architecture](../bc-council-improve-architecture/CONCEPT.md) (owner design 2026-11-22, live run and session reflection the same day).
- Loads [bc-council-mode](../bc-council-mode/CONCEPT.md).

## Tests

[tests/scenario.md](tests/scenario.md); results in [tests/results-2026-11-24.md](tests/results-2026-11-24.md).

## Deploy targets

None yet (`deployed: no`). When deployed: `scripts/deploy-local-skills.py` to `~/.agents/skills/`, `~/.pi/agent/skills/`, `~/.claude/skills/`. Deploy together with the cut-down `bc-council-improve-architecture`, which loads it.

- **Pass-2 refinements (owner, 2026-11-24).** A confirm may carry a refinement (corrected premise, narrower direction, sharper reproduction) with evidence, and the report shows it under the advisor's name. Evidence: in both live reviews of one project (2026-11-22 by hand, 2026-11-24 by the chain) one advisor's pass-2 refinements reshaped other advisors' cards, unasked. Dry-run tested through bc-council-find-bugs (2026-11-24, 2/2: the relay asks for refinements and the report carries them under the advisor's name); not yet seen in a live run.
