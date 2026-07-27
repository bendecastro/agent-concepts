# Contested Gate B deterministic trace

This fixture is the deployment Gate B for the `bc-drain-issues` v3 review-economy change. It compares the pinned v2 skill with v3 under a locked S0 → S1 → S2 trace that always contains exactly two Standards-only rework rounds.

It measures review/rework token cost under controlled topology. It does **not** replace the natural contested fixture's autonomous discovery pressure.

## Locked trace

| Round | State | Authoritative outcome | Golden advancement |
|---|---|---|---|
| R1 | S0 | Standards finds F1; Spec approves | S0 → S1 fixes F1 |
| R2 | S1 | Standards finds F2; v2 Spec approves | S1 → S2 fixes F2 |
| R3 | S2 | Standards approves; v2 Spec approves | none |
| final sync | S2 | v3 focused Spec approval | none |

Dispatch is fixed:

- **v2:** Spec + Standards at R1, R2, and R3.
- **v3:** Spec + Standards at R1; Standards at R2 and R3; focused Spec hash-sync at S2.

Both arms therefore perform exactly two reworks. Golden transitions control state advancement; a model mismatch fails fidelity instead of changing the dispatch topology.

## Pass contract

A real result passes only when all of the following hold:

1. v2 and v3 use `openai-codex/gpt-5.6-sol` with explicit `medium` effort.
2. Every expected reviewer/reworker slot maps one-to-one to a unique completed Pi child lifecycle artifact.
3. Reviewer JSON matches the strict review schema and the locked verdict; F1/F2 findings must identify the authoritative file with Important/Critical evidence.
4. Each reworker patch changes only the existing acceptance-unmapped helper and produces the target defect behavior.
5. Baseline and S2 each run the full suite once and fail only unchanged `tests/test_known_baseline.sh`.
6. Command receipts show the read-only Git probe succeeds and all mutation/network/publication probes are rejected.
7. Both final approvals bind to the exact S2 review-diff hash; stale Spec approval cannot land.
8. Provider-derived v2 tokens remain at or below 500,000 and provider-derived v3 tokens are lower than v2.

The result envelope may reference evidence, but it may not supply token totals, usage labels, a replacement trace, or a self-asserted fidelity flag. `run-trace.py` regenerates and validates the canonical contract independently.

## Generate and self-test

```bash
python3 make-fixture.py /tmp/gate-b-trace-v2
python3 make-fixture.py /tmp/gate-b-trace-v3
python3 run-trace.py --self-test --assert-dispatch-matrix
```

Independent roots must have identical base, state tree, review-diff, transition, and fixture-identity hashes.

## Isolation boundary

Generated roots have:

- no Git remote;
- a fixture-owned HOME/XDG configuration with no credentials;
- fail-closed PATH stubs for Git, GitHub, and publication commands;
- future oracle patches outside the measured child worktree;
- run/arm/slot/fixture/state-bound command and validation receipts.

The fixture does **not** claim physical network isolation (`physical_network_isolation: false`). An absolute executable or another network client can bypass PATH stubs. Run only in the generated sanitized environment, expose no credentials, and treat this as a documented residual—not proof of a network-denied sandbox. No real GitHub, network, push, PR, or publication mutation is permitted.

## Files

- `make-fixture.py` — creates deterministic repositories, states, transitions, metadata, stubs, and sanitized environment.
- `run-trace.py` — validates fixture identity, dispatch, behavior, evidence, lifecycle usage, fidelity, and landing eligibility.
- `AGENT-PROMPT.md` — trusted-parent procedure for the real v2/v3 run.
- generated `TRACE.json` — canonical machine-readable contract for that root.

Preserve real result artifacts and the verifier output under `tests/results/`. Never replace failed or invalid runs; add a new dated result so provenance remains intact.
