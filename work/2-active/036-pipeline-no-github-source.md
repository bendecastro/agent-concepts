# Pipeline: no GitHub remote means no issue source

Why: In the stranger test the pipeline stopped before building because it could not check GitHub issues in a project whose only remote is a local path, even though work items were ready (stall 1 in `docs/research/2026-11-27-stranger-end-to-end/README.md`).
Done when: In a project with no GitHub remote, `/bc-pipeline-to-done` drains ready work items without calling `gh` or asking which source to use, shown by a pressure run that stopped with the old wording and continues with the new.
Stage: next
Blocked by: nothing
Kind: bug
Source: 033-stranger-end-to-end-test
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Steps

- [ ] Reproduce: the first run started the build without project instructions (`-nc`), and `.bc-agent/AGENTS.md` says issues are optional. Run the build phase on a work-items-only fixture with project instructions loaded. Done when the stall reproduces (continue) or does not (drop this item with the evidence). Out of scope: editing the skill before the stall reproduces.
- [ ] Source choice: `concepts/bc-pipeline-to-done/body/SKILL.md` "Choose the source" says the issue source exists only when the project has a GitHub remote; pressure-test old vs new wording on a work-items-only repository with a local remote. Done when the new wording proceeds without `gh` and the old one stops, with results filed in `concepts/bc-pipeline-to-done/tests/`. Blocked by: Reproduce. Out of scope: changing how projects with a GitHub remote choose a source; the full stranger rerun (039-stranger-rerun).

## Outcome

