# Design the guardrails method

Why: projects need a repeatable way to set performance budgets and fitness functions and guard them with static, artifact and dynamic checks, so short-lived agents cannot make a project slower, bigger or more tangled unnoticed.
Done when: a deployed `guardrails` concept that held its pressure test, `bc-init-agent` creating `docs/guardrails/README.md`, `bc-autoresearch-loop` pointing to it, and the README's guardrails line describing it; requirements in [requirements.md](requirements.md).
Stage: next
Blocked by: nothing
Kind: feature
Source: bc-init-agent
Planned: bc-plan-to-pipeline 2026-11-25

## Steps

- [x] Write the `guardrails` concept: `CONCEPT.md` (provenance: the performance-guardrails research, the poteto posts, the design framework; `deployed: no`), `body/SKILL.md` with the method (check kinds, where a rule lives, ratchet and noise, targets from guidelines, setup and after-fix checks, owner-chosen limits, missing page), `tests/` pressure scenarios, `index.md` and `concepts/relationships.json` edges. Stories 1–7.
  Notes: entry `body/SKILL.md` plus `measuring.md` (10 runs after a warm-up, spread from the middle runs, too noisy above a tenth of the median: the method's own defaults, recorded as such) and `targets.md` (RAIL frame budget and the three Core Web Vitals only, the defaults the research sources). Glossary terms left to step 5.
- [x] Scaffold the page: `bc-init-agent` creates `docs/guardrails/README.md` and its `.bc-agent/map.md` line for the archetypes that get the design page, with unit tests and the skill text updated. Blocked by: Write the `guardrails` concept. Stories 1, 7.
  Notes: page sections are Who chooses a limit, Where a rule lives, How to measure, Targets, Budgets, Checks (the required five plus who chooses); `MIGRATIONS.md` gained a Guardrails README section for the upgrade note to point at; `test_visible_layout.py`'s exact file list updated.
- [x] Link the improvement loop: `bc-autoresearch-loop` points to the guardrails skill for measuring, and a kept improvement tightens the matching limit; update both concepts' relationships. Blocked by: Write the `guardrails` concept. Story 8.
  Notes: new loop step 7 tightens only agent-chosen limits; an owner-chosen one is reported instead. Edges: bc-autoresearch-loop depends on guardrails (optional), guardrails hands off to it.
- [ ] Pressure-test and deploy: run the scenarios without and with the concept on the configured pressure-test model, tune until it holds, set `deployed: yes`, deploy, regenerate `docs/status.md`. Blocked by: Scaffold the page; Link the improvement loop. Stories 2–6.
  Notes: pressure test passed 2026-11-25 with no tuning ([results](../../../concepts/guardrails/tests/pressure-results-2026-11-25.md)). Without the skill, scenario A failed (fix with no check); with it, every scenario held. B and C held in both runs. Deploy remains.
- [ ] Extend the README's "Keeping projects consistent" guardrails line (written by 022-readme-rewrite) and link the method, and add any new glossary terms. Blocked by: Pressure-test and deploy.

## Outcome

