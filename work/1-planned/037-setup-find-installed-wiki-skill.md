# Setup finds bc-wiki-maintain where the harness installed it

Why: In the stranger test setup skipped the wiki check because it looked only in `$HOME/.agents/skills/bc-wiki-maintain`, the directory `bc-setup-project` calls normal; `pi install` keeps skills in the package directory, where the script was present (stall 2 in `docs/research/2026-11-27-stranger-end-to-end/README.md`).
Done when: Setup runs `wiki_lint.py` from the installed `bc-wiki-maintain` skill after both the script install and `pi install`, shown by a pressure run per install method.
Stage: next
Blocked by: nothing
Kind: bug
Source: 033-stranger-end-to-end-test

## Steps

- [ ] Locate the skill: `concepts/bc-setup-project/body/SKILL.md` (the `wiki_skill_dir` paragraph) tells the agent to use the directory its harness lists for `bc-wiki-maintain`, naming the `pi install` location next to `~/.agents/skills`. Done when a Pi run after `pi install <checkout>` runs the wiki check instead of reporting it unavailable.

## Outcome

