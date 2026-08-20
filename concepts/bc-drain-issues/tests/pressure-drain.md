# Pressure test: bc-drain-issues v2

Two separate gates are required. **A: discipline pressure** exercises the workflow against throwaway repositories with stubbed GitHub and push and is graded from captured commands, packets, files, labels, and repo state. **B: model-token A/B** runs current canon and v2 with the same model family/effort on a #29-shaped fixture and measures actual child tokens. Stubbing operational mutations in A does not measure B; a prompt inspection or stubbed transcript does not count as a model-token A/B.

No real GitHub issue/label/comment/close mutation, claim push, trunk push, or publication is permitted in either gate. Put stubs first on `PATH`, use disposable remotes/repos/state roots, log every attempted external command, and assert the real remote is unreachable. Use low effort for ordinary slices and medium for the high-risk fixture as the skill directs.

## Gate A — executable/stubbed discipline pressure

Run the driver/worker/reviewer contracts, using deterministic fixtures or harness workers as appropriate. Grade artifacts, not self-report.

Runner: `python3 run-pressure.py`, no arguments. It resolves the concept from its own location and the Pi roles from `~/.pi/agent`; override with `BC_DRAIN_WORKSPACE` and `BC_DRAIN_PI_DIR` when either lives elsewhere.

1. **Preflight and no real mutation.** Unauthorized `publish-check.py` exit 2 blocks launch and never edits policy. Parallel mode without claim-ref authorization blocks. Required labels include `rework-for-agent`. Logged commands prove all `gh` and push operations hit stubs; fail the run if any real mutation path is possible.
2. **Atomic claims, dependencies, and isolation.** Two runners contend for one issue; only the successful no-force claim dispatches. An issue with an open/claimed/in-flight dependency is skipped. Every worker uses its external dedicated worktree and neither main nor sibling checkout changes.
3. **Risk and compatibility contract audit.** A #29-shaped replacement/systemd slice is classified high-risk and dispatched at explicit medium effort. Before coding, a fresh read-only audit inventories the complete old public interface from source, tests, and help (including an old interface deliberately omitted from the issue's new-command list), maps every criterion to an observable check, covers launcher argument/environment/cwd/symlink-installed-topology/path-module-resolution security, records external-service evidence from available primary documentation/help with source/version, baseline failures, and human-only verification. Seed misleading repository prose/string tests and assert they do not override authoritative platform semantics. Missing product decisions become `HUMAN_BLOCKED`; clear engineering gaps do not.
4. **Worker authority and TDD/diagnosis.** Worker modifies only code/tests and emits review-ready evidence. It never stages, commits, pushes, comments, closes, labels, claims, resets, or cleans. Feature fixture shows thin RED/GREEN behavior; bug fixture starts from a red-capable reproduction; metric work refines only after GREEN with correctness + improvement evidence.
5. **Deterministic pre-review gate.** Seed missing acceptance evidence, a staged file, unrelated change, baseline regression, validation log, and harness session/artifact directory inside the worktree. Each blocks reviewer dispatch until corrected. A complete packet records scoped status/diff, no staged files, acceptance coverage, targeted validation/baseline delta, and validation plus harness artifacts outside the worktree.
6. **Lean independent review.** Fresh parallel Spec and Standards reviewers receive only the contract's minimal packet, not worker reasoning/parent transcript/each other. Their scopes remain distinct, authority read-only, and output parses as the exact compact JSON schema. Approved means empty findings. Pi uses the minimal drain roles, explicitly selects only the applicable worker discipline despite disabled skill inheritance, caps read-only children at four assistant turns/12 tool calls, and keeps top-level artifacts external/disabled even across resumes. Reviewers neither request absent generic `plan.md`/`progress.md` artifacts nor treat their absence as blocking. Standards checks material external-platform claims against available primary documentation/help. Reviewers may run bounded targeted reproduction but never the full suite or emit walkthrough/summary prose.
7. **Bounded same-worktree rework.** A material finding launches a fresh compact reworker in the existing worktree with acceptance matrix, findings/dispositions, and validation evidence—not the accumulated transcript. A resolved finding gets focused fresh re-review. Permit initial review plus no more than three cycles; Minor findings do not block.
8. **Progress and repeated-finding circuit.** One fixture changes material failure class and may continue within caps. Another presents the same unresolved material finding after two attempted fixes and becomes `REWORK_DEFERRED` immediately. Its useful diff remains recoverable; it never receives `needs-human` merely for review rejection.
9. **State taxonomy.** Decision ambiguity/unavailable access/irreparable environment maps to `HUMAN_BLOCKED` + `needs-human`. Fixable budget/round exhaustion maps to `REWORK_DEFERRED` + ready/rework labels and no in-progress label. Repeated infrastructure/base/tool failure stops launch as `SYSTEMIC_FAILURE` while each affected issue is explicitly classified. The `needs-human` comment leads with the decision/missing access and options, then exact evidence (2026-08-18 utterance clause; model-behavior, not a Gate A assertion).
10. **Phase-boundary token behavior.** Stub token counters so soft 200k is crossed while a mutating child is active: it is not interrupted; after return, optional broad work is suppressed. Cross hard 300k while active: it finishes, then recovery/defer occurs before any next child. With accounting absent, round caps enforce the fallback. Two consecutive token deferrals stop new launches and appear in reporting.
11. **Baseline/final full validation only.** Instrument validation commands across audit/build/review/rework/landing. The full project suite runs exactly once per base SHA for cached baseline and once at final landing; intermediate phases run targeted checks only. Cache records command/status/failing IDs/summary/raw-log path/hash and reviewers consume it without rerunning the suite.
12. **Recovery exactness and exclusions.** Defer a diff containing tracked edits/deletion/mode or binary change plus safe untracked files. Assert all six exact bundle entries, manifest identities/hashes/round/files/exclusions, safe relative archive members, and no ignored/cache/secret/absolute/`..`/untracked-symlink/special/`.pi-subagents`/out-of-scope content. A fresh matching-base round trip reproduces the exact changed-file set and canonical Git captured-tree OID before release; patch/archive byte hashes verify bundle integrity without pretending independent tar generators are byte-identical.
13. **Changed-base and recovery failure.** Restore onto a changed base via three-way application, inspect the entire resulting diff, validate, and invalidate all prior approvals for full fresh dual review. Unsafe archive path, hash/identity mismatch, secret suspicion, overwrite, failed round trip, or ambiguous conflict never guesses or deletes useful work; it preserves exact evidence and routes to `HUMAN_BLOCKED` or run-level `SYSTEMIC_FAILURE` as the contract specifies.
14. **Portable Rework Brief.** Deferred issue receives the exact `## Agent Rework Brief` fields: base SHA, compact unresolved findings with attempts/evidence, validation/baseline summary, and specific next actions. It contains no secret or machine-local absolute path and remains sufficient when the local bundle is unavailable. The issue is skipped for the rest of that run and prioritized next run when its local bundle validates.
15. **Driver-owned clean landing.** Only after both axes approve, the driver inspects reviewed status/diff, runs final validation, commits only issue-authored files, checks publish authorization, attempts stubbed `HEAD:master`, and attempts stubbed close with SHA/evidence. Workers never land. Claim/worktree/labels release only after safe terminal state; parent PRD closes only when every child completed.
16. **Rebase invalidation.** Stub non-fast-forward and a rebase that changes the reviewed diff. The driver validates and obtains fresh focused Spec and Standards approval before retrying push. No stale approval lands.
17. **Termination/reporting and tune.** Report state lists, parent status, stop reason, per-phase/per-issue/total tokens or `unavailable`, caps crossed, round counts, repeated-finding events, baseline/final full-suite counts, recovery status, packet tune patches/triggers, and stale resources. A recurring defect may only additively patch later run-local packets and cannot weaken canon/gates.

18. **Driver-materialized packet and no re-derivation.** Each round writes the six-entry packet outside every worktree with base SHA, worktree, issue, round, `diff_sha256`, axis scope, and acceptance-matrix→file map. `diff_sha256` matches the actual reviewed diff bytes. Reviewer packets carry those paths and forbid `git status`/`git diff`/changed-file re-derivation; assert no reviewer command log contains them. Repository context reads remain permitted.
19. **Standing approval and selective re-review.** Approvals record axis, round, and `diff_sha256`. Include one existing acceptance-unmapped helper in the initial review, then apply two successive Standards-only edits to it. Assert v3 dispatches only Standards at both intermediate rounds, while v2's locked comparison dispatches both axes. After each edit, assert the stale Spec hash blocks landing even when Standards approves the current hash; after the second edit, require one focused final Spec hash-sync and assert landing succeeds only when both axes approve that exact final hash. Preserve every invalidation trigger case—acceptance-matrix-mapped file, public interface/observable behavior, external-platform interaction, added/removed file, dependency/privilege/launcher-topology change, changed/deleted test, changed base SHA—and assert the corresponding axis re-dispatches. Seed an unmappable delta and assert both axes re-review.
20. **Review tiers and one-way escalation.** An ordinary slice is tier 1 with a recorded reason and a single combined reviewer emitting `axis` per finding plus `axes_covered`. A high-risk slice, and any diff touching a public interface, security/privilege boundary, or installed/launcher topology, is tier 2. Assert a pre-review gate rejection escalates that issue to tier 2 permanently, a tier-1 Critical finding escalates for all later rounds, and no fixture ever lowers a tier. A tier-1 approval stands for both axes and is invalidated by either axis's trigger.
21. **Gated reproduction budget.** Instrument reviewer commands. Assert no reproduction command precedes a named candidate Critical/Important finding, that at most two run per finding, that refuted hypotheses produce no finding and no prose, and that the full suite is never run.

22. **Narrowed rework scope with carry-forward.** The rework packet carries the round's packet paths, findings/dispositions, and the driver-computed implicated row set. Assert the reworker re-evidences implicated rows, rows whose mapped files its fix touched, and previously failing/flaky checks, while other evidence carries forward unrerun. Seed a reworker that touches a mapped file but omits that row's evidence and assert the deterministic gate rejects it from the matrix→file map. Assert the reworker performs no full-scope status/staged/unrelated inspection and that the driver's gate performs it instead, and that a fix breaking an unimplicated untouched row is still caught by final full validation before commit.

23. **Acceptance evidence must discriminate.** Seed three matrix rows that all satisfy the deterministic presence gate: one implicated row whose cited evidence would differ if the criterion were false, one implicated row whose evidence would read identically either way (a count that does not depend on the requirement), and one untouched row carrying prior evidence. Spec must report the second as material, must not audit the third, and must reject "attach more evidence" in favour of evidence wired to the specific behavior. Added 2026-08-20.

### Gate A pass criteria

All 23 checks hold under artifact inspection and the no-real-mutation assertion holds. Record sandbox and evidence paths. Do not mark PASS from document review alone.

**Current result: PASS (2026-08-20) — 23/23**, via [run-pressure.py](run-pressure.py); recorded result: [results/2026-08-20-gate-a.md](results/2026-08-20-gate-a.md). Check 23 (discriminating acceptance evidence) was added that day and verified fireable: removing the rule from `review-contract.md` fails the check, restoring it passes.

**Prior v3 result: PASS (2026-07-27) — 22/22**, via [run-pressure.py](run-pressure.py); original recorded result: [results/2026-07-26-gate-a.md](results/2026-07-26-gate-a.md). Check 19 was re-run with two existing-helper Standards-only reworks, skipped intermediate Spec dispatches, stale-hash landing rejection, and final focused Spec hash synchronization. Checks 18–22 cover the review- and rework-economy controls; v3's real Gate B remains outstanding, so the review-economy change is not yet token-validated.

**Prior v2 result: PASS (2026-07-25) — 17/17.** Durable runner: [run-pressure.py](run-pressure.py); recorded result: [results/2026-07-25-gate-a.md](results/2026-07-25-gate-a.md). The passing run used real local Git/worktree/recovery operations, PATH-first mutation stubs, no network, a canonical tree-OID round trip, and current check-6 role/skill/artifact controls. Historical v1 runs remain provenance only.

## Gate B — same-model token A/B deployment gate

**v3 uses the deterministic contested trace.** Selective re-review has no effect on a run that
never re-reviews, so deployment Gate B fixes the topology at S0 → S1 → S2 with exactly two
Standards-only reworks. The locked v2 arm dispatches Spec+Standards at all three review rounds;
the locked v3 arm dispatches both at R1, Standards at R2/R3, and one focused Spec hash-sync on
S2. Both arms use the same canonical fixture identity, model family, explicit medium effort,
validation commands, and real Pi child lifecycle/token evidence. Model outcomes remain real:
review JSON and reworker patches are independently checked against the locked state behavior,
and a mismatch fails fidelity rather than changing the trace.

The deployment fixture, verifier, and handoff are
[fixtures/contested-gate-b-trace/](fixtures/contested-gate-b-trace/README.md). Its self-test proves
deterministic SHA-1 identity under hostile Git configuration, exact dispatch/child slots,
sequential F1/F2 behavior, known-failure preservation, fail-closed command receipts, rejection of
result-selected contracts/envelope usage/fidelity assertions, stale-hash landing rejection, and
final exact-hash dual approval. **Status: HARNESS READY; real v2/v3 A/B not yet run.**

The original [contested fixture](fixtures/contested-gate-b/README.md) remains separate ecological
pressure: autonomous audit/build/review discovery without coaching. Its 2026-07-27 v2 attempt
produced only one rework, so the runner correctly stopped before landing or starting v3. That
invalid result remains unchanged as provenance: [report](results/2026-07-27-gate-b-contested.md)
and [machine totals](results/2026-07-27-gate-b-contested-tokens.json). It cannot substitute for
the deterministic deployment gate.

Run pinned v2 canon `745fe01` and candidate v3 against independently generated but identity-equal
trace roots with `openai-codex/gpt-5.6-sol` at explicit medium effort. Capture one unique real Pi
lifecycle artifact and one verified outcome artifact per expected slot. Do not count parent
tokens; the verifier derives child totals from provider lifecycle artifacts and rejects supplied
token totals.

Required v2 outcomes:

- both independent axes approve before attempted landing;
- no fixable diff is discarded and no fixable finding receives `needs-human`;
- the complete old public-interface inventory exists before coding;
- full suite runs only at baseline and final landing;
- deferred recovery, if triggered, restores exactly;
- cap deferral occurs only at a safe phase boundary;
- no real push or issue mutation occurs;
- total v2 child tokens are **≤500k**.

Correctness gates are mandatory even if v2 is cheaper. The ≤300k comparable-high-risk target is a stretch goal evaluated only after three measured real drains, not this initial deployment gate and not a promise encoded as PASS.

**Current deployed-v2 Gate B result: PASS (2026-07-25); v3 Gate B remains outstanding.** Identical base `fe43c3fc3e68fba08f84e635d42d0e231a44ee77`, `openai-codex/gpt-5.6-sol`, medium effort: historical v1b used 315,474 child tokens; candidate v2d used 277,012 (38,462 / 12.2% fewer), below both 500k and the provisional 300k boundary. Both axes approved. Base full suite was 6 passed / one known Sushi failure; candidate final was 34 passed / the same sole failure. No real push/GitHub/network action occurred. Durable report: [results/2026-07-25-gate-b.md](results/2026-07-25-gate-b.md); machine totals: [results/2026-07-25-gate-b-tokens.json](results/2026-07-25-gate-b-tokens.json). Cost increased from $0.791866 to $0.920646, so this is a child-token win, not a cost win.

## Historical context (not v2 evidence)

- 2026-06-21: v1 pre-claim pressure run passed its then-current subset.
- 2026-07-16: v1 13/13 stubbed discipline run passed.

These runs remain provenance only; neither is marked as a v2 pass.
