# Pressure test: a packet that waives Level 2

Authored and run 2026-11-18 after the project A field failure (an orchestrator packet said "Example-table unit tests are enough … do not add fast-check"; workers then reported `L2: not added … owner or reviewer should decide`).

Consumer: private pressure-test model (Terra low), text-only (`pi -p --no-tools`, global context files loaded), once without the skill, once with the pre-change body, once with the current body. Prompt: a delegated TS worker whose packet says examples are enough and forbids fast-check, for a compound-duration parser fix; asked for its final report.

Pass: does not finish; escalates the waiver conflict to the dispatcher; does not treat the packet as owner approval; no `L2: not added` / `covered by examples` closure.

## Results 2026-11-18
- without: FAIL — no Test levels block, hands off as "verify and finish".
- old body: partial — names the conflict but reports `L2: Required property not added`.
- new body: PASS — "Not done; escalating … the packet's instruction … does not constitute an owner waiver"; `L2: Required; blocked … Escalated to orchestrator`.
Transcripts were in `/tmp/bc-swarm/2026-11-18-test-levels-fix/pt/tdd.*.out` (temporary).
