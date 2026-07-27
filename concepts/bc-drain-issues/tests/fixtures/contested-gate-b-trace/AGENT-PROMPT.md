# Real Gate B deterministic trace runner

You are the **trusted parent harness** for a real v2/v3 token comparison. Follow `TRACE.json` exactly. Do not let a child select the trace, advance state, edit evidence, or see future oracle artifacts.

## Hard controls

- Use a fresh generated root for each arm.
- Use `openai-codex/gpt-5.6-sol` with explicit `medium` thinking for **every** child.
- Create one globally unique Pi child session for every `expected_child_slots` entry; never reuse or simulate a session.
- Preserve the pinned v2 skill from Git revision `745fe01`; use the candidate v3 skill for the v3 arm.
- Do not run real GitHub, network, push, PR, publish, or external-state mutations.
- Keep model worktrees disposable and evidence outside `child-worktree`.
- Never invent token usage. Reference the completed Pi `status.json`; the verifier derives totals.
- Never change topology after a model mismatch. Record the mismatch, continue only with the golden next state, and expect verification to fail fidelity.

## Prepare

From this fixture directory:

```bash
python3 make-fixture.py /tmp/gate-b-trace-v2
python3 make-fixture.py /tmp/gate-b-trace-v3
python3 run-trace.py --self-test --assert-dispatch-matrix
```

Confirm both generated `TRACE.json` files have the same `fixture_identity`, `base_sha`, state hashes, transition hashes, controls, and expected child-slot shapes.

Create a trusted evidence directory outside both generated child worktrees. Choose one non-empty `run_id`. Combine both arms' command receipts and validation records into one JSONL file per evidence type.

## Execute one arm

1. Source that root's `env.sh`. Set `GATE_B_RUN_ID`, `GATE_B_ARM`, `GATE_B_SLOT_ID`, `GATE_B_STATE_HASH`, and `GATE_B_TRANSITION_HASH` from the current expected slot before invoking any fixture stub.
2. Run the six controlled boundary probes once, bound to the arm's first slot:
   - `git status` → 0
   - `git push` → 97
   - `git -c fixture.key=value push` → 97
   - `git upload-pack .` → 97
   - `gh pr create` → 97
   - `publish-check.py` → 97
3. Run the baseline full suite once on the generated base repository. Record a schema-2 validation JSONL entry bound to the first slot. It must report exit 1, only `tests/test_known_baseline.sh`, and its canonical hash.
4. Walk `dispatch[arm]` in order. For each review slot:
   - Materialize only that slot's state in a fresh disposable worktree.
   - Give the child the issue/review packet and the current state's review diff, never future states/transitions.
   - Ask for strict review JSON only:

     ```json
     {"verdict":"approved|changes_requested","findings":[{"severity":"Critical|Important","requirement":"...","location":"file:line","evidence":"..."}]}
     ```

   - Save the exact JSON outside the measured worktree as that slot's `outcome_artifact`.
   - Save/reference the completed Pi run's `status.json` and child index.
5. For each rework slot:
   - Materialize the slot's source state in a fresh disposable worktree.
   - Give the reworker only the current finding and current-state packet.
   - After it finishes, save a binary/full-index Git patch from the canonical source tree to the worker attempt outside the worktree as `outcome_artifact`.
   - Do not use that attempt to choose the next state. Advance the controller with the canonical golden transition.
6. Run the full suite once on S2. Record a schema-2 validation JSONL entry bound to the last S2 review slot. It must have the same sole known failure and file hash as baseline.

Additional read-only stub commands are allowed and must remain receipt-bound to their actual slot. All unsupported, mutation, network, and publication commands must be rejected. Do not delete inconvenient receipts.

## Evidence records

Each command/validation record must carry the exact binding fields for its expected slot:

```json
{
  "schema_version": 2,
  "run_id": "...",
  "arm": "v2|v3",
  "slot_id": "...",
  "fixture_identity": "...",
  "state_hash": "review hash or null",
  "transition_hash": "transition hash or null"
}
```

For validation records also include:

```json
{
  "phase": "baseline|final",
  "command": ["./run-tests.sh"],
  "exit_code": 1,
  "failures": ["tests/test_known_baseline.sh"],
  "known_failure_sha256": "..."
}
```

## Result envelope

Write one result JSON beside the trusted evidence. Do not include `trace_path`, token totals, usage labels, or `fidelity` fields.

```json
{
  "schema_version": 2,
  "fixture_base_sha": "<TRACE base_sha>",
  "fixture_identity": "<TRACE fixture_identity>",
  "run_id": "<trusted run id>",
  "controls": {"model": "openai-codex/gpt-5.6-sol", "effort": "medium"},
  "evidence": {
    "command_receipts": "commands.jsonl",
    "validation_log": "full-suites.jsonl",
    "sanitized_home_receipt": "sanitized-home.json"
  },
  "arms": {
    "v2": {
      "dispatch": "<exact TRACE dispatch.v2 array>",
      "sessions": [
        {
          "slot_id": "<exact expected slot>",
          "status_artifact": "/absolute/path/to/status.json",
          "child_index": 0,
          "outcome_artifact": "/absolute/path/to/review.json-or-rework.patch"
        }
      ],
      "reworks": ["F1", "F2"],
      "full_suite_invocations": {"baseline": 1, "final": 1, "total": 2},
      "final_approvals": "<exact Spec and Standards S2 hash records>"
    },
    "v3": "<same shape with exact v3 dispatch and slots>"
  }
}
```

Copy one generated `metadata/sanitized-home.json` to the evidence directory unchanged.

## Verify and record

```bash
python3 run-trace.py --verify-result /path/to/result.json
```

A PASS means canonical fixture identity, dispatch, real lifecycle usage, reviewer outcomes, reworker behavior/scope, validation evidence, command rejection, exact-hash landing, token ceiling, and v3 token win all verified. A FAIL is an invalid/failed run; preserve it with its evidence rather than editing history.

Physical network isolation is not enforced. The sanitized HOME/no-remote/PATH-stub boundary reduces risk but absolute executables remain a residual. Run from a credential-free parent environment and abort if that condition cannot be met.
