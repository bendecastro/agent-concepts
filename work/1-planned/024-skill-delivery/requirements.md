# Requirements: skill delivery

## Problem Statement

People outside this repository cannot reliably install its skills. The only installer, `scripts/deploy-local-skills.py`, assumes a clone of the whole repository, replaces any existing skill of the same name without asking, and has no uninstall. Thirteen concepts link into other concepts' folders by relative path (`../../tdd/body/SKILL.md`), and most of those links point at the always-on kernel, which is not a skill. Copying a skill alone, as `npx skills` does, breaks every one of those links. Six concepts name tools only the owner has (`bc-pytest`, `bc-ask`, `publish-check` and others). Generic names such as `tdd`, `code-review` and `research` clash with other collections: `npx skills` overwrites the earlier skill, and Pi keeps whichever it finds first. CI runs only on Ubuntu, and the gate uses Bash features that the Bash shipped with macOS lacks. Every agent commit is pushed to `master`, so anything that installs from `master` gets half-finished work.

Evidence: [install-methods research](evidence/2026-11-25-install-methods-research.md), [repository scout](evidence/2026-11-25-repo-scout.md).

## Solution

Strangers install the public skills with the method native to their agent: a Claude Code plugin, a Codex plugin, a Pi package, or `npx skills` for any other agent. Each method installs a tagged release, never `master`. Every public skill works alone apart from the skills it says it needs, refers to those skills by name, works without the owner's tools, and has a `bc-` name. A fresh-install test in CI proves each method on Linux and macOS.

Decisions (grill, 2026-11-25):

1. Claude Code, Codex and Pi are tested. Other agents use `npx skills` and are listed as untested.
2. Skills that use the owner's tools stay public. Every public skill works without the owner's tools: the public text describes each step generically, and the owner's [private overlay](../../../glossary.md) names the tool.
3. Skills refer to each other by name. Each skill lists the skills it needs, and every install method installs them too. Links into the kernel's storage-safety section become a short self-contained rule in the skill.
4. Install methods: one Claude Code plugin and one Codex plugin, each with every public skill; a Pi package (`pi install git:…`); `npx skills` for other agents. The clone-and-link script stays for contributors. The docs tell users to pick one method per agent, because two methods install every skill twice.
5. Every public skill gets the `bc-` prefix ([decision 0001](../../../docs/decisions/0001-bc-prefix-for-public-skill-names.md)). The old names stay as aliases on the owner's machines only.
6. The fresh-install test runs in CI with no login and no model calls. Behaviour stays with the pressure tests, which run before a release.
7. Linux and macOS are tested in CI; Windows is listed as untested.
8. Strangers get tagged releases ([decision 0002](../../../docs/decisions/0002-tagged-releases-for-strangers.md)). A release goes out only after the fresh-install test and the pressure tests of changed discipline skills pass. A changelog lists each release's changes.

## User Stories

1. As someone using Claude Code, I want to install the skills as one plugin, so I get them and their updates through Claude's own commands.
2. As someone using Codex, I want the same through a Codex plugin.
3. As someone using Pi, I want to install the skills with `pi install`, so the subagent skills work with Pi's subagents.
4. As someone using another agent, I want an `npx skills` command, so I can install all the skills or a ready-made pack with the skills each one needs.
5. As an installer of one skill, I want the skills it needs installed with it, so no instruction points at something missing.
6. As someone with other skill collections, I want no name clashes, so installing these skills never replaces or hides a skill I already have.
7. As a stranger, I want every public skill to work without the owner's private tools, so no step tells me to run something I cannot get.
8. As a stranger, I want to install a tested release and pin a version, so a half-finished push never reaches me.
9. As a stranger, I want to update and uninstall with my agent's usual commands, so I can try the skills without leaving debris.
10. As a macOS user, I want installs tested on macOS, so they work on my machine.
11. As the owner, I want my old skill names to keep working on my machines, so my habits and other projects do not break.
12. As a contributor, I want the clone-and-link script to skip skills it did not create and to remove what it installed, so it never overwrites someone's own skill.

## Implementation Decisions

- **One list of public skills and what each needs.** Each public skill's needed skills come from the `loads` edges in `concepts/relationships.json`, so there is one source. A public skill is any concept not marked `deployed: no`, except kernels, which are injected rather than installed. The plugin and package descriptions, the `npx skills` pack commands and the fresh-install test read that list; none keeps its own copy.
- **Name references.** A body names another skill by its `bc-` name and, where useful, the section ("load `bc-tdd`, section Test levels"). Lint rejects relative links from one concept's `body/` into another concept's folder.
- **Kernel rules inline.** Where a skill links to the kernel's storage-safety section, it states the needed rule in two or three sentences (make scratch folders with `mktemp -d`, delete what tests create, and so on) and names the kernel as optional extra context.
- **Owner tools.** Each of the six concepts describes the step in generic terms and keeps the overlay line from the repository convention; the owner's tool names move to the owner's private overlays. Lint's personal-terms check covers the public text.
- **Aliases.** The old names go into the deploy-alias list used by `deploy-local-skills.py` on the owner's machines; no plugin or package ships them.
- **Pi-only skills.** Skills that launch Pi subagents say so in their description, so non-Pi users know before they rely on them.
- **Releases.** Version tags `vMAJOR.MINOR.PATCH`; plugin and package descriptions carry the same version; `CHANGELOG.md` at the repository root. Tagging and pushing a release follows the publish policy.

## Testing Decisions

- A good test checks what a stranger meets after installing, not how the build scripts work inside.
- **Lint** (existing): fails on a relative link from one concept's body into another concept, on a needed skill missing from a skill's list, on a public skill without the `bc-` prefix, and on the owner's terms in public text. Prior art: the current lint checks for broken links and personal terms.
- **Fresh-install test** (new, in CI on Linux and macOS, no login): for each method, start from an empty home folder (`HOME=$(mktemp -d)`); install; check that the agent lists the skills, that every needed skill is present, and that one bundled helper script runs; update to the release under test; uninstall and check nothing remains. Prior art: the fresh-HOME install in marcfargas/skills `validate.yml`. First check whether each agent can list its skills without being logged in; where it cannot, check the installed files instead and say so in the test.
- Behaviour (whether a model follows a skill) stays with the pressure tests, run before a release.

## Out of Scope

- Windows support beyond listing it as untested.
- Live model calls or API keys in CI.
- Several themed plugins; a Cursor package or Gemini extension.
- Changing what any skill teaches, beyond wording needed to drop owner tools and path links.
- Publishing to any skill directory or marketplace other than the plugin files in this repository.

## Further Notes

- The kernel (`agent-kernel`) is not installed as a skill; strangers keep using the bootstrap guide for it.
- After the rename, the owner's other projects that name skills keep working through the aliases; renaming those mentions is optional later work.
