# Ideas

Undecided ideas and observations, one line each, newest at the bottom. An idea that
someone decides to do becomes a numbered work item in `1-planned/`; delete its line here.
- Make run-promotion-all.sh bound a timed-out vault's descendants without depending on GNU timeout: run each child under `setsid` and kill its process group itself.
- `naming-things` failed pressure case G (2026-11-27): it never says what to do when the user dictates a name that breaks its rules or asks for the spelling in IDs and hashes, so the agent flagged the clash and complied. Decide the wanted outcome, add one rule, rerun case G, then deploy (see `concepts/naming-things/tests/pressure-naming-results-2026-11-27.md`).
- scaffold.py's learning/knowledge vault read block still hardcodes `$HOME/.agents/skills/bc-wiki-maintain` for `wiki_search.py`; fails after `pi install` like stall 2 did (found by 037-setup-find-installed-wiki-skill).
- Rerun the 2026-11-26 no-CI gate pressure test of `bc-setup-project` (`concepts/bc-setup-project/tests/pressure-no-ci-gate.md`) through `scripts/pi_sandbox.py`: its comparison does not stand because both arms carried the owner's private test-runner rules, which the old arm followed instead of running the gate (found by 040-pressure-sandbox-instructions).
- 041-results-claims-match-tables showed NO_DEFECT on short fixtures (Terra low caught the drafted '3/3 runs' overclaim with and without the new clauses); test whether long multi-step drain sessions, where the 2026-11-26 overclaims arose, reproduce it before calling the clauses proven.
- Stranger test sandbox: a worker reading the process list sees the outer `bwrap` command line, which holds the host scratch path under the owner's home (039-stranger-rerun, finding R3). Start the box from a scratch dir outside the home, or otherwise hide PID 1's arguments.
- Stranger end-to-end test for Claude Code and Codex installs (owner decision 5a, 2026-11-27): only Pi has been tested.
- Outside pull requests (blind-spot council 2026-11-27, finding E): no rule says to review a PR as untrusted text in a worktree and re-author body changes, and a contributor cannot meet the test rule because the pressure-test model is set in a private file. Add CONTRIBUTING and an AGENTS.md rule when outside PRs start arriving.
