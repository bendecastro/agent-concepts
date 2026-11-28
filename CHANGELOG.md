# Changelog

Each release of the public skills, newest first. Versions follow `vMAJOR.MINOR.PATCH` tags; the
format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Install a tagged
release rather than `master`: `master` changes many times a day and can hold unfinished work.

Renames and removals use `### Renamed` and `### Removed` sections; see the
[release policy](docs/guides/releasing.md#renaming-and-removing-skills).

## [Unreleased]

### Added

- Work items gain a `Dependencies:` line (`none new`, `may add <name> (<why>) (owner's answer, <date>)`,
  or the owner's refusal). `work_index.py --check` fails on a ready item without it planned on or after
  2026-11-28 and warns on older ones; MIGRATIONS.md has the upgrade step.
- The fresh-install test gains `claude-kernel` and `codex-kernel`: each adds the marketplace (from the
  release tag in the release workflow) and installs `agent-kernel`, then checks its SessionStart hooks
  deliver the canonical kernel text.

### Changed

- `bc-plan-to-pipeline` checks dependencies in its own step on every plan, even when no other question is
  open, and marks an item ready only when it has its `Dependencies:` line. Later steps are renumbered.
- The README's Codex install also installs the `agent-kernel` plugin from the release tag, with no
  checkout; trust its SessionStart hook in `/hooks` or the kernel does not load. Uninstall removes both
  plugins. Running the README's Codex refresh on a skills-only install adds the kernel.
- `bc-setup-project`'s generated `.bc-agent/AGENTS.md` now states once how skills resolve a project file's role and the full worktree numbering rule; the skills that restated them point at it and keep only their own no-table fallback, except `bc-plan-to-pipeline`, which keeps the full numbering rule so projects set up earlier stay safe. Earlier projects add the block by the new "Role lookup and worktree numbering" migration.
- The per-vault wiki-maintain timer install procedure moved from `bc-setup-project` step 10 to `bc-wiki-maintain`'s `INSTALL-TIMER.md`; setup still offers the timer and loads it, so the `bc-setup-project` install pack now includes `bc-wiki-maintain`.
- `bc-setup-project` step 10 states inline that qmd search does not replace the promotion timer, that "just enable" or "don't ask" is not confirmation of the shown units and commands, and that a declined or impossible install leaves a parking-lot TODO.

### Fixed

- `bc-qmd` no longer calls `qmd query` the default: use `qmd search` with 2–4 keywords first, and rerun once as `qmd query --no-rerank` when it finds nothing relevant or the concept may be worded differently. `bc-wiki-maintain` and the generated vault block now ban `qmd query` only as an inline read. Earlier projects narrow their vault block by the new "Vault read path: `qmd query` ban narrowed" migration.

## [0.5.0] - 2026-11-28

### Renamed

<a id="bc-delegate-investigation-rename"></a>

- `bc-delegate-investigation` is now `bc-swarm`; its durability rules (run folder, manifest, artifacts,
  Commit/Branch records, recovery before relaunch) and Pi notes moved to the new `bc-durable-subagents`,
  which `bc-swarm` loads. The old name remains a compatibility alias. Earliest removal: v0.6.0.

<a id="bc-ui-design-rename"></a>

- `bc-ui-design` is now `bc-design`. The old name remains a compatibility alias.
  Earliest removal: v0.6.0.

### Added

- `bc-safe-runs`: one skill for storage-safe test runs, scratch folders and worktree removal. Eleven skills that restated these rules now load it and keep a one-line fallback; `bc-find-bugs`, `bc-council-find-bugs` and `bc-prototype` load it too.

### Changed

- `bc-swarm` caps how many subagents a narrow question gets: one for a question about one or two named files (two only when each file is its own surface), and never an extra track the question did not name.
- Skills that launch subagents (`bc-council-mode` and through it every council chain, `bc-subagent-driven-development`, `bc-dispatching-parallel-agents`, `bc-pipeline-to-done`, `bc-security-audit`, `bc-work-sync`) now load `bc-durable-subagents`, so every run gets a reboot-safe run folder and manifest before its first launch; each keeps a one-line fallback. Council advisors now write their reports to files in the run folder.
- Workspace lint warns about repeated concept prose and verifies explicitly marked copies against their source.
- Release checks require the private personal-terms scan unless explicitly opted out, and scan
  the staged snapshot from git rather than the working copy; the npm publish job uses fixed
  action commits and an exact npm version.
- A freshly created project records the agent-concepts version in `.bc-agent/.scaffold-version`
  (never added or changed on a rerun, `--force` or a migration), and each section of setup's
  migration guide says which release it arrived in, so you can tell which upgrades may apply.
- Each week CI checks fresh installs against npm's `latest` tag for each agent CLI, including
  whether Pi loads the packaged kernel. A separate job opens or updates one issue on failure.

### Fixed

- Setup's [migration guide](concepts/bc-setup-project/body/MIGRATIONS.md) ships with the skill, so installed copies can find upgrade steps.
- The install test no longer fails on Claude Code 2.1.332 and later, which list their built-in
  plugins: it now looks for this plugin by ID. The new weekly check found this on its first run.

## [0.4.1] - 2026-11-27

New releases soak on npm before they reach you, and there is a way to report problems.

### Changed

- New releases go to npm's `next` tag first and move to `latest`, which
  `pi install npm:agent-concepts` follows, only after an end-to-end test passes on the
  published version. Try a release early with `pi install npm:agent-concepts@next`.
- Each release has a GitHub release page with its changelog entry.

### Added

- Report a problem through a [new issue](https://github.com/bendecastro/agent-concepts/issues/new/choose),
  and a security problem privately through [SECURITY.md](SECURITY.md).

### Fixed

- The README's Pi update command: `pi update --extensions` updates the package; plain
  `pi update` updates only Pi.

## [0.4.0] - 2026-11-27

Pi users install from npm, and a stranger's first project goes from setup to a built, reviewed
item without stalling.

### Added

- Pi installs from npm: `pi install npm:agent-concepts`, and `pi update` moves to each new
  release. The package carries the skills, the pipeline's agent roles and the agent kernel.
- The agent kernel ships as a Pi package, a Claude Code plugin, a Codex plugin and an OpenCode
  plugin; `bc-setup-project` reports when it is missing.
- `bc-setup-project` offers new projects starter work items for guardrail checks and a design
  page, and sets up a gate even when the project has no CI.
- Skills that use the owner's machine-only tools fall back to plain ones when those are absent
  (for example plain `pytest` with `tmp_path`), and the pipeline asks once about publishing when
  there is no publish policy.
- Lint warns when a deployed concept names a workflow moment without a matching handoff or
  load from its owner. The warning becomes an error in the version after the first tagged
  release carrying it.

### Changed

- Renamed the `bc-ui-design` skill to `bc-design`, and widened its description to wording, CLI
  commands and flags, keyboard, states, accessibility, motion and design decisions. Reinstall, or
  use `/skill:bc-design`; local deploys keep `bc-ui-design` as an alias.
- `bc-pipeline-to-done` builds the work item you name, even when other ready items come first
  in the order, and records the new order in its claim commit instead of asking.
- The agent kernel reads a bare "yes" or "go ahead" to a question with a recommended option as
  that option, instead of asking again.
- Typing `/bc-security-audit` now starts a full security audit, like the other commands;
  text after it limits the scope. When the agent loads the skill itself because security came
  up, it still only gives advice.
- Planning now marks a work item's `Dependencies:` line as the owner's answer when the owner
  answered (`… (owner's answer, <date>)`), and a builder treats only a line so marked as the
  owner's permission to use example tests instead of property tests. Before, builders stopped on
  a `none new; use example-based tests` line the owner had already answered.
- Planning asks about new dependencies, and the builder adds only the ones named.
- Pipeline skills use the repository's target branch instead of assuming `main` or `master`,
  and a repository with no GitHub remote has no issue source.

## [0.3.0] - 2026-11-25

Projects set up with `bc-setup-project` can feed a dashboard of their work.

### Added

- `work_index.py --json` prints every work item as data a dashboard can read: its header lines,
  steps, outcome, and history from git (when it was created, moved between planned, active and
  done, and when each step was ticked). [work-data.md](concepts/bc-setup-project/body/work-data.md)
  lists every field.
- Work items carry four new lines, written by the agents: `Held by:` (who is working on an
  active item), `Review:` and `Gate:` under a step (its review and full-test results) and
  `Spent:` in a finished item's outcome.
- `work_spent.py` estimates an item's time, tokens and cost from Pi, Claude Code and Codex
  session files, for the `Spent:` line. It is an estimate: parallel sessions add up, and only
  Pi records cost.
- The workflow guide has a section on building your own dashboard.

### Changed

- `bc-pipeline-to-done` and the project rules from `bc-setup-project` now write these lines,
  and `bc-work-sync` reports `Held by:` lines that look stale. Projects set up earlier can pick
  this up with the steps in `concepts/bc-setup-project/body/MIGRATIONS.md`; existing items need no
  rewrite.

## [0.2.0] - 2026-11-25

Seven skills have new names that say what they do
([decision record](docs/decisions/0004-skill-names-say-what-they-do.md)).

### Changed

- `bc-reflect` is now `bc-self-improve`.
- `bc-swarm` is now `bc-delegate-investigation`.
- `bc-autoresearch-loop` is now `bc-optimize-code`.
- `bc-show-me` is now `bc-explain-visually`.
- `bc-init-agent` is now `bc-setup-project`.
- `bc-council-improve-codebase` is now `bc-council-improve-architecture`.
- `bc-guardrails` is now `bc-performance-guardrails`.

The old names keep working only on installs made with this repository's local deploy script
(`scripts/deploy-local-skills.py`). The Claude Code and Codex plugins, the Pi package and
`npx skills` install only the new names: after updating, call these skills by their new names.

## [0.1.0] - 2026-11-25

The first release you can install without cloning this repository.

### Added

- 52 public skills, each named with a `bc-` prefix (`bc-tdd`, `bc-code-review`,
  `bc-diagnosing-bugs` and so on) so they do not replace or hide skills with common names
  from other collections.
- Four ways to install them. Pick one per agent; two methods would install every skill twice.
  - Claude Code: the `agent-concepts` plugin from the marketplace in this repository.
  - Codex: the same plugin in Codex's format.
  - Pi: a Pi package, `pi install git:github.com/bendecastro/agent-concepts@v0.1.0`.
  - Other agents: `npx skills add`, either every skill or one ready-made pack. A pack is a
    skill plus the skills it needs; the commands are in
    [docs/guides/install-packs.md](docs/guides/install-packs.md).
- Skills that need other skills name them, and every install method installs them together.
- Six council skills (`bc-council-mode`, `bc-council-chain`, `bc-council-audit-security`,
  `bc-council-challenge-plan`, `bc-council-find-bugs`, `bc-council-improve-codebase`) work
  only in Pi, because they launch Pi subagents. Their descriptions say so.
- A workflow guide, [docs/guides/workflows.md](docs/guides/workflows.md): when to run each
  workflow skill, how to start it, what it asks and what you get.
- A fresh-install test that runs in CI on Ubuntu and macOS. For each install method it starts
  from an empty home folder, installs, checks that every expected skill is listed and that a
  bundled helper script runs, updates, and uninstalls. It needs no login and makes no model
  calls. Tested agent versions: Pi 1.6.0, Claude Code 2.1.329, Codex 0.153.1 and
  `skills` 1.9.0.

### Not tested

- Windows.
- Agents other than Pi, Claude Code and Codex. `npx skills` supports many more, but this
  release was checked only through its Pi target.

[Unreleased]: https://github.com/bendecastro/agent-concepts/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/bendecastro/agent-concepts/compare/v0.4.1...v0.5.0
[0.4.1]: https://github.com/bendecastro/agent-concepts/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/bendecastro/agent-concepts/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/bendecastro/agent-concepts/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/bendecastro/agent-concepts/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/bendecastro/agent-concepts/releases/tag/v0.1.0
