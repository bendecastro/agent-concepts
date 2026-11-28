# Planning asks the dependency question every time

Why: In the v0.4.1 stranger test, `bc-plan-to-pipeline` wrote a ready item without a `Dependencies:` line and asked no dependency question, although the project's test rules call for property tests (Hypothesis). The builder parked on it correctly, costing an owner question mid-build. In the 0.4.0 run planning did ask, so the step is followed unreliably on the pressure-test model. Evidence: `docs/research/2026-11-27-release-audit.md`, "v0.4.1 soak".
Done when: Planning on the pressure-test model asks the dependency question (or records an owner answer) whenever the item's tests need a package the project lacks, in at least three of three runs of a scenario like the stranger fixture, and a ready item never lacks a `Dependencies:` line.
Stage: next
Blocked by: nothing
Kind: bug
Source: stranger test v0.4.1 (release soak)
Planned: bc-plan-to-pipeline 2026-11-28
Ready for agent: yes

## Requirements

Owner decisions (2026-11-28, bc-ask): 1a all three fixes; 2a error only for newly planned items; 3a reuse the existing scenario plus a stranger-like case. Recon: the dependency check is a sub-bullet at the end of `concepts/bc-plan-to-pipeline/body/SKILL.md` step 1, which also says "with none open, ask nothing" and "skip to step 2", and nothing downstream requires the line.

- **Index check.** `work_index.py` (the shipped copy `concepts/bc-setup-project/body/work_index.py` and this repo's `.bc-agent/scripts/work_index.py`) reports an item with `Ready for agent: yes` and no `Dependencies:` line: an error when its `Planned:` date is on or after the date the check ships (a constant in the script), a warning otherwise. Items without `Ready for agent: yes` (including parked `Waiting on owner:` items) are not checked. Test first.
- **Template.** The work-item template (this repo's `.bc-agent/templates/work-item.md` and the one `scaffold.py` writes) gains a `Dependencies:` line with its allowed forms (`none new`, `may add <name> (<why>) (owner's answer, <date>)`, or the owner's refusal). `MIGRATIONS.md` in bc-setup-project tells earlier projects to add the line to the template and to newly planned items.
- **Skill.** In `bc-plan-to-pipeline`, the dependency check becomes its own numbered step that runs even when no other question is open, leads with the always-written line, and keeps the existing question wording; step 7's ready bar requires the line; the "ask nothing" sentences name the exception. Trim the duplicated "Why" text rather than add to it. Update CONCEPT.md and RELATIONSHIPS edges only if a contract changes.
- **Pressure test.** `concepts/bc-pipeline-to-done/tests/scenario-planned-dependencies.md` Part 1 (fix its grade check to expect the owner mark) plus a stranger-like case without "don't ask me anything", 3 runs per arm, old skill (`master` before the change) vs new, on the pressure-test model (Haiku `low` when the Codex quota is out, per the owner). Pass = the new arm asks (or records an owner answer) and writes the line in 3 of 3 runs of each case.

## Steps

- [ ] **Index check and template.** Done when a unit test shows a newly planned ready item without the line fails `work_index.py --check`, an older one only warns, a parked item passes, both template copies carry the line, MIGRATIONS has the step, and lint passes. Out of scope: skill text.
- [ ] **Skill step and ready bar (held until the pressure test passes).** Done when the step, ready bar and exception read as one rule, the scenario file has both cases, and lint passes. Out of scope: changing the builder side (`bc-pipeline-to-done`).
- [ ] **Pressure test, then land.** Blocked by: Skill step and ready bar. Done when the results file shows each case's 3 runs per arm graded from artifacts, the new arm passes 3 of 3, and the skill change is merged to master.
