# Changelog

Each release of the public skills, newest first. Versions follow `vMAJOR.MINOR.PATCH` tags; the
format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Install a tagged
release rather than `master`: `master` changes many times a day and can hold unfinished work.

## [Unreleased]

### Added

- Lint warns when a deployed concept names a workflow moment without a matching handoff or
  load from its owner. The warning becomes an error in the version after the first tagged
  release carrying it.

### Changed

- Renamed the `bc-ui-design` skill to `bc-design`, and widened its description to wording, CLI
  commands and flags, keyboard, states, accessibility, motion and design decisions. Reinstall, or
  use `/skill:bc-design`; local deploys keep `bc-ui-design` as an alias.
- Typing `/bc-security-audit` now starts a full security audit, like the other commands;
  text after it limits the scope. When the agent loads the skill itself because security came
  up, it still only gives advice.
- Planning now marks a work item's `Dependencies:` line as the owner's answer when the owner
  answered (`… (owner's answer, <date>)`), and a builder treats only a line so marked as the
  owner's permission to use example tests instead of property tests. Before, builders stopped on
  a `none new; use example-based tests` line the owner had already answered.

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
  this up with the steps in `concepts/bc-setup-project/MIGRATIONS.md`; existing items need no
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

[Unreleased]: https://github.com/bendecastro/agent-concepts/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/bendecastro/agent-concepts/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/bendecastro/agent-concepts/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/bendecastro/agent-concepts/releases/tag/v0.1.0
