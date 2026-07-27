# bc-drain-issues Deterministic Gate B Trace Implementation Plan

**Goal:** Replace the probabilistic deployment Gate B workload with a deterministic two-rework Standards trace while preserving the existing natural fixture as ecological pressure evidence.

**Architecture:** A new fixture generator creates a byte-stable base plus three locked candidate states: S0 contains Standards defect F1, S1 fixes F1 while introducing F2, and S2 fixes F2. A deterministic controller validates state/delta hashes, locked v2/v3 dispatch topology, final exact-hash approvals, isolation metadata, and real-run result envelopes; model invocation remains a thin manual Pi adapter in `AGENT-PROMPT.md`.

**Tech stack:** Python 3 standard library, Git CLI, POSIX shell fixture files, Markdown contracts.

**Execution note:** Work task-by-task. Use the controller self-test as the RED/GREEN seam. Verify the existing 22-check Gate A and commit the complete canonical update after inspection.

---

## File map

### Create

- `agents/concepts/bc-drain-issues/tests/fixtures/contested-gate-b-trace/make-fixture.py` — generate isolated deterministic base/S0/S1/S2 artifacts, local stubs, hashes, findings, and dispatch manifest.
- `agents/concepts/bc-drain-issues/tests/fixtures/contested-gate-b-trace/run-trace.py` — deterministic fixture/controller self-test and real-result verifier; never fabricates model usage.
- `agents/concepts/bc-drain-issues/tests/fixtures/contested-gate-b-trace/README.md` — deployment benchmark contract and pass criteria.
- `agents/concepts/bc-drain-issues/tests/fixtures/contested-gate-b-trace/AGENT-PROMPT.md` — thin real-model runner handoff.
- `agents/plans/bc-drain-issues-gate-b-deterministic-trace.md` — this implementation record.

### Modify

- `agents/concepts/bc-drain-issues/tests/run-pressure.py` — exercise an existing-file Standards-only delta, skipped intermediate Spec review, stale-hash landing rejection, and final Spec hash synchronization.
- `agents/concepts/bc-drain-issues/tests/pressure-drain.md` — designate the trace as deployment Gate B and the existing fixture as ecological pressure.
- `agents/concepts/bc-drain-issues/tests/fixtures/contested-gate-b/README.md` — relabel the natural fixture without changing historical criteria.
- `agents/concepts/bc-drain-issues/tests/fixtures/contested-gate-b/AGENT-PROMPT.md` — stop treating natural pressure as canonical deployment Gate B.
- `agents/plans/bc-drain-issues-v3-review-economy.md` — record deterministic trace and final hash-sync interpretation.
- `agents/concepts/bc-drain-issues/CONCEPT.md` — record benchmark/ecological split and outstanding real A/B.
- `agents/index.md` and `agents/log.md` — update canonical status/bookkeeping.

## Task 1 — Build the deterministic trace generator

- [x] Create the new fixture directory and a failing controller self-test entry point that expects `TRACE.json` with S0/S1/S2 state hashes, two transition hashes, findings F1/F2, and locked dispatch sequences.
- [x] Run `python3 .../run-trace.py --self-test`; expected RED: missing generator/trace contract.
- [x] Implement `make-fixture.py` with fixed Git identity/dates and commit-signing disabled.
- [x] Generate base B, candidate states S0/S1/S2, exact review diffs, golden transition patches, acceptance map, validation metadata, authoritative Standards findings, local stubs, and `TRACE.json`.
- [x] Ensure F1 and F2 are genuine sequential internal-helper defects and both transitions modify only the same existing acceptance-unmapped helper without adding/removing files, changing tests, or firing Spec triggers.
- [x] Run two independent generations and assert identical base SHA, state tree IDs, review diff hashes, and transition hashes.

## Task 2 — Implement deterministic control and result verification

- [x] Implement `run-trace.py --self-test` to verify state reconstruction, patch application, hashes, two Standards findings, and no Spec invalidation flags.
- [x] Lock dispatch topology: v2 `R1 spec+standards, R2 spec+standards, R3 spec+standards`; v3 `R1 spec+standards, R2 standards, R3 standards, final-sync spec`.
- [x] Assert stale Spec approval blocks S1/S2 landing and final focused Spec approval plus final Standards approval both bind S2's exact review diff hash.
- [x] Implement `--verify-result <json>` for unique Pi lifecycle sessions and artifact-derived usage, exact dispatches, model/effort equality, outcome-backed two-rework fidelity, fail-closed receipt isolation, full-suite counts, final approval hashes, and v3 token win.
- [x] Run `python3 .../run-trace.py --self-test --assert-dispatch-matrix`; expected GREEN.

## Task 3 — Extend Gate A exact-hash/selective-review coverage

- [x] Modify check 19 to seed an existing unmapped helper before initial review.
- [x] Apply two Standards-only edits to that existing helper and assert intermediate Spec dispatch is skipped.
- [x] Assert the stale Spec hash cannot land after either edit.
- [x] Add final focused Spec approval on the final hash and assert landing then succeeds with both exact hashes.
- [x] Preserve all existing trigger cases and the 22-check count.
- [x] Run `python3 agents/concepts/bc-drain-issues/tests/run-pressure.py`; expected 22/22 PASS.

## Task 4 — Split deployment benchmark from ecological pressure

- [x] Write the trace README and real-model `AGENT-PROMPT.md` using the existing minimal drain roles and explicit same-model/medium controls.
- [x] Require fixture-controlled state advancement; model mismatch is a fidelity failure and never changes the trace.
- [x] Relabel the existing contested fixture/prompt as ecological pressure and preserve the 2026-07-27 invalid result unchanged.
- [x] Update `pressure-drain.md`, v3 plan, `CONCEPT.md`, index, and log without weakening correctness or the two-round criterion.

## Task 5 — Final verification and publication

- [x] Run fixture self-test and independent-generation identity check.
- [x] Run Gate A and `python3 agents/scripts/lint.py`.
- [x] Validate Python syntax, JSON outputs, `git diff --check`, and final status/diff.
- [x] Commit only agent-authored files with a concise test/design message.
- [x] Run `agents/scripts/publish-check.py`; push only when authorized.
