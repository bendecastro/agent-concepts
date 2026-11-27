# Docs and skill references a stranger can follow

Why: `docs/guides/pipeline.md` still describes the old `.bc-agent/` vault layout; five skills say to use `naming-things`, which was never tested or deployed; wiki search needs `$AGENT_CONCEPTS`, set only for a contributor checkout; setup's indexing and wiki-lint steps do not say which archetypes they apply to.
Done when: The pipeline guide matches the visible layout; `naming-things` held its pressure test and is deployed; wiki search finds its script from the installed skill; setup's indexing and lint steps name their archetypes.
Stage: now
Blocked by: nothing
Kind: docs
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state
Planned: bc-plan-to-pipeline 2026-11-26
Ready for agent: yes

## Requirements

- `naming-things`: pressure-test per the Test operation (pressure-test model, blind baseline), then set `deployed: yes` and deploy. If it fails, the step stops and the result is recorded; deployment waits for a fix.
- Wiki search: resolve `wiki_search.py` relative to the installed skill directory, with `$AGENT_CONCEPTS` only as an override.
- Out of scope: rewriting other guides.

## Steps

- [x] Pipeline guide and setup archetype scope: rewrite the layout parts of `docs/guides/pipeline.md` and state archetypes for setup's indexing and wiki-lint steps. Blocked by: nothing. Done when the guide names only visible-layout paths for code projects and lint has 0 ERROR. Out of scope: other guides.
  - Review: approved by tier-1 2026-11-27 (round 2)
  - Gate: pass ./scripts/gate at 3d2c53d 2026-11-27
  - Landed in `3d2c53d`.
- [x] Wiki search path: resolve the script relative to the installed skill; test with `$AGENT_CONCEPTS` unset. Blocked by: nothing. Done when the test passes with the variable unset, after failing first. Out of scope: search behaviour.
  - Review: approved by tier-1 2026-11-27 (round 2)
  - Gate: pass ./scripts/gate at 3d2c53d 2026-11-27
  - Landed in `3d2c53d`.
- [x] Test and deploy `naming-things`: scenarios in `concepts/naming-things/tests/`, runs on the pressure-test model, status frontmatter, deploy, `index.md`, `docs/status.md`, `.bc-agent/log.md`. Blocked by: nothing. Done when the with-skill runs hold where the baseline fails and the skill is deployed, or the failure is recorded and deployment left off. Out of scope: rewriting the five referencing skills.
  - Review: approved by tier-1 2026-11-27 (round 2)
  - Gate: pass ./scripts/gate at c685022 2026-11-27
  - Landed in `c685022`. Result: FAIL recorded, deployment left off.

## Outcome

- Pipeline guide names only the visible layout setup creates; setup states which archetypes its indexing, wiki-lint and promotion steps apply to (`3d2c53d`).
- Wiki search, the runner scripts and the failure notifier work from the installed skill with `AGENT_CONCEPTS` unset; regression tests run the documented commands from a copied installed layout (`3d2c53d`).
- `naming-things` pressure case G (`c685022`): with the skill the agent flagged the misleading name 3/3 (blind 0/3) but still used it and persisted it into IDs and hashes, so the skill stays undeployed. The result file names the body gap: no rule for a user-dictated name that breaks the checklist. Follow-up filed in `work/0-ideas.md`.

Full gate 634 passed, 4 skipped.

Spent: 1h 22m active, 21.4M tokens, $9.07 (estimated; pi 11 sessions, claude-code 0 sessions, codex 0 sessions; other tools not counted)

