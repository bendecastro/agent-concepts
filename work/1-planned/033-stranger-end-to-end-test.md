# Stranger test: the whole loop with no private config

Why: Every gap found on 2026-11-26 came from skills only ever run on the owner's machine; nothing checks the loop as a stranger meets it.
Done when: A repeatable sandboxed run with no `~/.config/agent-concepts/` and no owner tools installs from the README, sets up a sample repository on `main` without CI, plans and builds one item, and records every stall; its results are filed and each stall becomes an item or a fix.
Stage: later
Blocked by: 027-pipeline-default-branch, 028-missing-private-tool-fallbacks, 029-setup-green-gate-and-ci
Kind: tests
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state

## Steps

- [ ] Sandbox recipe (hidden private config and owner tools) in the pressure-test harness guide.
- [ ] Sample repository fixture on `main`, tests but no CI.
- [ ] Run on the pressure-test model, including a check that a worker does not run the full suite without the kernel.
- [ ] File results and the resulting items.

## Outcome

