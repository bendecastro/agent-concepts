# CI catches new agent versions breaking installs, and loads the kernel in real Pi

Why: CI runs only on push against pinned Pi, Claude Code and Codex (Pi 1.6.0 while the README says the kernel needs 1.6.1+), and the install test runs Pi with extensions off, so a new agent release or a broken kernel extension reaches strangers first.
Done when: A weekly scheduled workflow installs on the latest agent versions and opens an issue on failure; the pinned CI Pi matches the README's minimum; the fresh-install test loads the packed package with extensions on and proves the kernel section reaches the system prompt.
Stage: now
Blocked by: nothing
Kind: tests
Source: blind-spot council, owner decisions 2026-11-27 (4a: findings A and B)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- `.github/workflows/`: a `schedule:` (weekly) plus `workflow_dispatch` job running `scripts/fresh_install_test.py` with unpinned agent CLIs; on failure it opens or updates one GitHub issue (`issues: write`), so 048's session-start check files it.
- `gate.yml` and `release.yml` pin Pi to the README's minimum (1.6.1) or the README is corrected to the version CI proves; one home for the number if feasible.
- `fresh_install_test.py`: one method loads the packed package with extensions enabled and checks the kernel text appears in the system prompt (for example via `pi_sandbox.py`'s system-prompt check), without a model call if possible.

## Steps

- [x] Add the scheduled latest-agents run, align the Pi pin, and load the kernel extension in the install test. Done when the new method fails with the kernel extension removed and passes with it, and the scheduled workflow validates (`workflow_dispatch` run green or `actionlint` clean). Out of scope: Windows.

## Outcome

Weekly and manual latest-CLI installs report failures to one issue; pinned Pi is 1.6.1. The packed Pi test checks the assembled kernel prompt without a model request, and fails when the extension is removed. Actionlint validates the workflows.
