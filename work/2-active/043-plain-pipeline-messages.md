# Setup, planning and the pipeline speak plainly and add no surprise dependencies

Why: In the 039 stranger rerun a newcomer met jargon ("publish policy", "claim commit", "review tier", `$unavailable` cost rows), noise (an unauthenticated-`gh` note in a project with no GitHub, a "0m active, 0 tokens, cost unknown" Spent line), and a builder that added Hypothesis to `pyproject.toml` without asking.
Done when: The push question, the final report and the Spent line read plainly for someone new; setup says nothing about `gh` in a project without a GitHub remote; a dependency the project lacks is settled at planning time and the builder adds only dependencies the plan names.
Stage: now
Blocked by: nothing
Kind: feature
Source: owner decisions 4a and "remove all friction" on the 039 stranger walkthrough, 2026-11-27
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- Pipeline push question in plain words, e.g. "May I push finished work to `origin` `main`?"; the chat report leads with what landed, the checks and the reviews, keeps the per-child cost table only when costs are known, and moves recovery paths and tier detail to the run log. The contract's required report facts stay recorded somewhere (run log), not dropped.
- `work_spent.py`: when nothing was measured, the line says so plainly ("Spent: not measured") instead of zeros.
- `bc-setup-project`: no `gh` remark when the project has no GitHub remote.
- Dependencies (decision 4a): `bc-plan-to-pipeline` asks once, while the user is present, when the item will need a library the project lacks (including test libraries a discipline such as `bc-tdd`'s property tests calls for) and records the answer in the item; the builder contract in `bc-pipeline-to-done` lets the builder add only dependencies the item names, and stops the unit with a question for any other.
- Touch only these files' sections plus their CONCEPT.md, tests, index.md and log. Do NOT edit `concepts/bc-pipeline-to-done/body/SKILL.md` lines about roles, overlay or preflight (042 owns them); the report and push-question sections are yours.
- The dependency rule is a discipline gate: it needs a pressure test on the pressure-test model before release; leave `test_status` honest and write the scenario under the concepts' `tests/`.

## Steps

- [ ] Plain push question, plain report, plain Spent line, no `gh` noise. Done when targeted tests cover the Spent line and a setup survey without a GitHub remote, and lint passes. Out of scope: role and install wiring (042-one-command-pi-install).
- [ ] Planned dependencies: planning asks, builder obeys. Done when the scenario file exists with old/new arms and expected outcomes. Out of scope: running the pressure test (the parent runs it on the pressure-test model).

## Outcome

_To be filled when finished or dropped._
