# Fallbacks when a machine-only tool is missing

Why: Deployed skills name tools only the owner's machine has (publish check via the private overlay, guarded pytest runner, storage health check, Pi worker roles); on a stranger's machine the pipeline aborts at preflight or the wording leaves no defined action.
Done when: Each such reference states what to do when the tool is absent: the bundled `scripts/publish-check.py` with a policy created from `policies/publish.example.yaml`, plain pytest under the temp-file rules, skip the storage check with a note, or a clear "configure X" stop; the README install section lists what the pipeline needs.
Stage: next
Blocked by: nothing
Kind: bug
Source: stranger gap hunt (scouts), 2026-11-26; run notes in the owner's local swarm state

## Steps

- [ ] Inventory every "the machine's ..." / "if one exists" reference in deployed bodies and classify: has fallback, needs fallback, needs a stop.
- [ ] Point the publish check at the bundled script when no overlay names one; keep deny-by-default.
- [ ] Add the pipeline's Pi worker roles and pi-subagents to the README install prerequisites.
- [ ] Lint and gate green.

## Outcome

