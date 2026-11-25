# Changelog

Each release of the public skills, newest first. Versions follow `vMAJOR.MINOR.PATCH` tags; the
format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Install a tagged
release rather than `master`: `master` changes many times a day and can hold unfinished work.

## [Unreleased]

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

[Unreleased]: https://github.com/bendecastro/agent-concepts/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/bendecastro/agent-concepts/releases/tag/v0.1.0
