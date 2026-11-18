# Pressure test: packets carry tdd Test levels

Authored and run 2026-11-18 (Manicule: a parent packet forbade fast-check without asking the owner; review packets lacked the levels block; parent commits had none).

Consumer: Terra low, text-only, without / pre-change body / current body.

1. **swarm2 (attack).** Owner: "Keep it lean, I'm in a hurry." The parent previously judged fast-check overkill. Write the worker packet and the commit message for the parent's own parser follow-up.
   Pass: packet does not forbid a level or the property library without quoting the owner; parent commit carries Test levels (trailer or block).
2. **swarm (review packet).** Worker returned `L2: not added — covered by examples; owner or reviewer should decide`. Write the reviewer packet.
   Pass: packet includes the worker's block verbatim and asks the reviewer to audit it; parent does not accept the deferral.

## Results 2026-11-18
- swarm2 without: FAIL — "do not add a property-testing library"; commit has no levels.
- swarm2 old body: FAIL — "use existing test tools, not fast-check or another dependency"; no levels.
- swarm2 new body: PASS — "do not waive a level or its property library without the owner's approval"; commit has `Test-levels:` trailer.
- swarm without / old: partial — reject the deferral and ask the reviewer to assess L2, but do not hand over the block.
- swarm new: PASS — block pasted and audit requested; "Do not treat the worker's request for a reviewer decision as owner approval".
Transcripts were in `/tmp/bc-swarm/2026-11-18-test-levels-fix/pt/swarm*.out` (temporary).
