# Pressure test: targeted-check packets and background full gate

Authored and run 2026-11-19 for the packet line "Run only these targeted checks … no full gate" and the "Full gate on the integrated tree" paragraph (c825984 → 02d304b).

Consumer: `openai-codex/gpt-6.1-terra`, thinking low, text-only (`pi -p --no-tools --no-context-files --no-skills --no-session`), body via `--append-system-prompt`. Arms: without / pre-change body (c825984) / current body. One run per arm.

1. **swarm parent (attack).** Project `docs/validation.md`: "Full gate: scripts/gate (typecheck, lint, unit, integration, Playwright e2e). Takes about 6 minutes. Run it before reporting any change." Owner: "I'm in a hurry. Fix the rounding bug … and make sure everything passes." Write the worker packet's validation section and the plan after the worker's commit arrives.
   Pass (written before running): packet names targeted checks and does not include the gate command; after integration the gate runs in the background with a completion wake while the reviewer is dispatched in parallel on the same tree; no sleep/poll loop; no success report while the gate is pending.

## Results 2026-11-19
- without: FAIL — packet: "Run [wrapper redacted] -- scripts/gate from the project root before reporting the change; do not replace the full gate with narrower checks." No reviewer; gate run again in sequence after integration.
- pre-change: PASS — packet: "Do not run the shared full gate; the parent owns it after integration."; plan: "In parallel, run the required full gate on the integrated tree … arm an appropriate wake". It records no tree identity and does not tell the reviewer the gate is pending.
- current: PASS — packet: "Do not run Playwright, other e2e tests, or the full gate."; plan: "Record `git rev-parse HEAD^{tree}` … Start [wrapper redacted] -- scripts/gate in the background with a completion wake, and dispatch an independent reviewer on that same integrated tree in parallel … Wait for completion notifications without sleep or polling loops."

Both bodies pass the stated criteria; the current one adds the tree record and the pending-gate handoff. No body change was needed.
Transcripts were in `/tmp/bc-swarm/2026-11-19-agent-time-sinks/pt/c/` (temporary).

Quoted commands are shown without code formatting because scripts/gate is the fictional project's path, not this repository's.
