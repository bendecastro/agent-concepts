# bc-drain-issues v3 — review-phase economy

Date: 2026-07-26
Status: implemented; Gate A 22/22, deterministic Gate B harness ready, real model A/B outstanding

## Problem

v2 cut per-issue child tokens 12.2% and fixed the lost-work failure, but it left the review
phases structurally unchanged: every review round dispatches two independent axes, and every
rework round dispatches both again. Gate B measured a *clean* issue — one worker, one rework, no
re-review — where review was 61,012 of 277,012 child tokens (22%).

The exposure is the multiplier, not the single pass. v2 permits an initial review plus three
rework/re-review cycles, so a contested issue can dispatch **eight reviewer children**. At the
Gate B per-axis rates (Spec 24,104; Standards 36,908) that is roughly 244k tokens of review on
one issue — more than the entire measured clean run — and most of it re-reads a diff that an
axis already approved.

Three specific wastes:

1. **Blind re-review.** If Spec approved with empty findings and the reworker only touched the
   hunks Standards flagged, re-running Spec re-reads the whole diff to reach the same verdict.
2. **Duplicated derivation.** Both reviewers independently run `git status`, `git diff <base>`,
   enumerate changed files, and locate raw logs — all of which the driver already computed
   deterministically at the pre-review gate. Independence is about reasoning, not about
   re-running Git.
3. **Uniform axis count.** A two-file bug fix and a systemd compatibility replacement both pay
   for two independent reviewers, even though the driver has already classified their risk.

## Goals

- Reduce review-phase child tokens, especially on contested issues, without weakening the
  invariant that **both review axes must stand approved on the exact landed diff**.
- Keep independence where it demonstrably caught defects (high-risk compatibility/service work).
- Make every economy decision deterministic and driver-owned, so it is auditable rather than a
  model's discretionary shortcut.

## Non-goals

- Do not reduce the number of *rework* rounds or relax the deterministic pre-review gate.
- Do not let a reviewer decide its own scope, tier, or budget.
- Do not weaken recovery, claim, publish, or landing rules.
- Do not trade a review round for a rework round; the rework worker is the more expensive unit
  (Gate B: 50,425 vs ~30,000 per reviewer).

## A. Standing approval and selective re-review

Replace "re-dispatch both axes every round" with **standing approval plus deterministic
invalidation**. This generalizes a rule v2 already has: a rebase that changes the reviewed diff
invalidates approval.

An axis approval is a record, not an event:

```json
{"axis":"spec","round":1,"diff_sha256":"<hash of the reviewed diff>","verdict":"approved"}
```

After each rework round the driver computes the new reviewed diff and evaluates, per axis, an
**invalidation trigger** from the diff delta — never from model judgment:

| Axis | Standing approval is invalidated when the rework delta… |
|---|---|
| Spec | touches a file/hunk mapped to any acceptance-matrix row; changes a public interface, CLI surface, or externally observable behavior; or changes external-platform interaction |
| Standards | adds or removes a file; changes dependencies, privilege/security-relevant code, or installed/launcher topology; or changes or deletes a test |
| Both | the axis raised the findings being reworked; the base SHA changed; or the delta cannot be mapped deterministically |

The raising axis always re-reviews. The approving axis re-reviews only on a trigger. Before
landing, the driver verifies each axis holds a standing approval whose `diff_sha256` equals the
final reviewed diff; any mismatch forces a focused re-review of that axis. In the deterministic
Gate B trace, Spec legitimately skips both intermediate Standards-only rounds but its S0 approval
is stale after each golden transition, so v3 must run one focused Spec hash-sync on S2 before
landing. Thus "both axes approved the landed diff" remains literally true — the change is that
an untouched axis is not asked the same question at every intermediate state.

The "cannot be mapped deterministically" row is the fail-safe: ambiguity costs a review, never
an assumption.

## B. Driver-materialized review packet

The driver writes the packet once per round, outside the worktree, under the run artifact root:

```text
review-packet/issue-<n>/round-<r>/
├── packet.json            # base SHA, worktree, issue ref, round, diff_sha256, axis scope, matrix→file map
├── diff.patch             # exact reviewed diff (git diff --no-ext-diff <base>..worktree)
├── changed-files.txt
├── acceptance-matrix.json
├── validation.json        # commands, statuses, failing IDs, baseline delta, raw-log paths
└── findings-prior.json    # re-review rounds only
```

Reviewers read these paths and **must not re-derive the packet** with `git status`, `git diff`,
or changed-file enumeration. They may still read repository files for context and run the
bounded reproduction of section D. The packet is authoritative and complete; a missing generic
`plan.md`/`progress.md` remains non-blocking.

`packet.json` carries the acceptance-matrix→file map that makes section A's Spec trigger
deterministic, and `diff_sha256` is the identity that standing approvals bind to. One artifact
therefore serves economy, determinism, and auditability at once.

## C. Risk-tiered axis count

The driver already classifies risk before the claim. Extend that classification into a recorded
**review tier**:

- **Tier 2 — dual independent axes** (v2 behavior). Any high-risk slice: compatibility
  replacement/retirement, migration/cutover, systemd or external-service semantics, broad public
  acceptance surface. Also any slice whose diff touches a public interface, a security/privilege
  boundary, or installed/launcher topology.
- **Tier 1 — single combined reviewer.** Ordinary slices. One fresh read-only reviewer carries
  both scopes, works both checklists explicitly, and emits the same JSON schema with an `axis`
  field per finding plus an `axes_covered` acknowledgement.

Tier 1 is bounded by escalation rules, so it cannot become the silent default:

- Tier is computed and recorded **before** dispatch, with its classification reason.
- The pre-review gate rejecting a worker packet escalates that issue to tier 2 for the remainder
  of its life. Observed sloppiness buys more scrutiny, not less.
- Any Critical finding from a tier-1 reviewer escalates the issue to tier 2 for all subsequent
  rounds; a single reviewer that found something severe may be under-covering.
- A tier-1 approval counts as a standing approval for **both** axes, and is invalidated by
  either axis's trigger in section A.
- Tier is reported per issue so a human can audit whether the cheap path is being over-used.

This is the only lever that genuinely trades independence, and the only one whose value depends
on the escalation rules actually firing — Gate A must attack them directly.

## D. Reproduction budget gated on a formed finding

v2 permits "bounded targeted reproduction", which reads as licence for exploratory command runs.
v3 gates it: a reviewer may run reproduction commands **only after** it has a specific candidate
Critical or Important finding, and only to prove or refute that named finding — at most two
commands per finding. Reading the packet and repository context is unrestricted within the
existing turn/tool caps.

Refuted hypotheses are simply dropped, not reported; the output schema is unchanged.

## Rejected alternative

**Serial Spec→Standards with early exit.** It would skip the Standards run whenever Spec
rejects, but it loses batched findings, so one rework round becomes two. The rework worker cost
more than either reviewer in Gate B, so this trades a cheap unit for an expensive one. Reviews
stay parallel.

## Expected effect

On a clean issue the win is small: lever B's removed derivation plus lever C's single reviewer,
roughly 24k–37k saved out of 277k. On a contested three-round issue the win is structural —
selective re-review removes most of up to six re-review dispatches. v3 should therefore be
measured on a **deterministic contested trace**; a clean or probabilistically single-rework
fixture cannot see its main effect. The original natural contested fixture remains ecological
pressure for autonomous discovery, not the deployment gate.

## Canonical implementation changes

- `body/review-contract.md` — standing approval/invalidation table, packet paths and
  no-re-derivation rule, tier-1 combined-reviewer contract and schema addition, gated
  reproduction budget.
- `body/SKILL.md` — tier classification at claim time, packet materialization at the
  deterministic gate, selective re-review dispatch, pre-landing standing-approval verification,
  escalation rules, and reporting fields.
- `CONCEPT.md` — record the four decisions, their evidence, and what they supersede.
- `tests/pressure-drain.md` and `tests/run-pressure.py` — new checks 18–21 and extensions to
  checks 6, 7, and 16.

## Acceptance

Gate A (deterministic) must show:

- an untouched axis is not re-dispatched, **and** every landed diff carries a standing approval
  from both axes bound to its exact hash;
- each invalidation trigger fires on a seeded delta, and an unmappable delta forces review;
- reviewers receive packet paths and no reviewer re-derives status/diff;
- tier 1 is chosen only for ordinary slices, and both escalation paths (gate rejection, Critical
  finding) force tier 2;
- reproduction commands never precede a formed finding.

Gate B (model A/B) uses `tests/fixtures/contested-gate-b-trace/`: a deterministic S0 → S1 → S2
high-risk trace with exactly two Standards-only reworks, locked v2/v3 dispatch, real Pi lifecycle
token evidence, independently checked reviewer/reworker outcomes, and a mandatory focused final
Spec hash-sync. It must show fewer child tokens than v2 with no correctness regression and both
axes standing approved on the exact S2 hash. The 2026-07-27 natural contested attempt remains
invalid ecological evidence after only one rework. v3 is not token-validated until the real
trace A/B runs.
