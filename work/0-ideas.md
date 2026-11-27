# Ideas

Undecided ideas and observations, one line each, newest at the bottom. An idea that
someone decides to do becomes a numbered work item in `1-planned/`; delete its line here.
- Make run-promotion-all.sh bound a timed-out vault's descendants without depending on GNU timeout: run each child under `setsid` and kill its process group itself.
- Outside-repo text still using pre-004 words (update by hand; not canon): Pi swarm-mode prompt `~/.pi/agent/extensions/swarm-mode/kernel.md` ("Recovery gate", "Tooth", "the tooth") and `extensions/swarm-mode/index.ts` ("Before Tooth/dispatch"); Pi `agents/ui-designer.md` ("its capture gate"); old Pi mission records under `missions/` are historical and stay.
- `naming-things` failed pressure case G (2026-11-27): it never says what to do when the user dictates a name that breaks its rules or asks for the spelling in IDs and hashes, so the agent flagged the clash and complied. Decide the wanted outcome, add one rule, rerun case G, then deploy (see `concepts/naming-things/tests/pressure-naming-results-2026-11-27.md`).
- scaffold.py's learning/knowledge vault read block still hardcodes `$HOME/.agents/skills/bc-wiki-maintain` for `wiki_search.py`; fails after `pi install` like stall 2 did (found by 037-setup-find-installed-wiki-skill).
- Rerun the 2026-11-26 no-CI gate pressure test of `bc-setup-project` (`concepts/bc-setup-project/tests/pressure-no-ci-gate.md`) through `scripts/pi_sandbox.py`: its comparison does not stand because both arms carried the owner's private test-runner rules, which the old arm followed instead of running the gate (found by 040-pressure-sandbox-instructions).
- 041-results-claims-match-tables showed NO_DEFECT on short fixtures (Terra low caught the drafted '3/3 runs' overclaim with and without the new clauses); test whether long multi-step drain sessions, where the 2026-11-26 overclaims arose, reproduce it before calling the clauses proven.
