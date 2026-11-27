# Setup finds bc-wiki-maintain where the harness installed it

Why: In the stranger test setup skipped the wiki check because it looked only in `$HOME/.agents/skills/bc-wiki-maintain`, the directory `bc-setup-project` calls normal; `pi install` keeps skills in the package directory, where the script was present (stall 2 in `docs/research/2026-11-27-stranger-end-to-end/README.md`).
Done when: Setup runs `wiki_lint.py` from the installed `bc-wiki-maintain` skill after both the script install and `pi install`, shown by a pressure run per install method.
Stage: next
Blocked by: nothing
Kind: bug
Source: 033-stranger-end-to-end-test
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Steps

- [x] Locate the skill: `concepts/bc-setup-project/body/SKILL.md` (the `wiki_skill_dir` paragraph) tells the agent to use the directory its harness lists for `bc-wiki-maintain`, naming the `pi install` location next to `~/.agents/skills`. Done when a Pi run after `pi install <checkout>` runs the wiki check instead of reporting it unavailable, and a run after the script install still does; both results filed in `concepts/bc-setup-project/tests/`. Out of scope: changing where either install method puts skills; other harnesses' install paths beyond naming them if already documented.

## Outcome

setup now finds `bc-wiki-maintain` from its own skill folder with ordered `test -f` checks (`../bc-wiki-maintain`, then `../../bc-wiki-maintain/body`). Terra low runs: new body ran the installed `wiki_lint.py` after both the script install and `pi install <checkout>`; the old body failed both (under `pi install` exactly as in stall 2). The approved "directory your harness lists" wording failed after the script install because `bc-wiki-maintain` is not listed (`disable-model-invocation: true`). [Results](../../../concepts/bc-setup-project/tests/pressure-installed-wiki-location-results-2026-11-27.md). Not covered: `npx skills`, Claude Code/Codex plugin and `pi install git:` installs; the vault read block `scaffold.py` generates for learning/knowledge vaults still names `$HOME/.agents/skills/bc-wiki-maintain` (idea line filed).

Landed on master; full gate `scripts/gate` passed on tree d9c32474 (639 passed, 4 skipped).
