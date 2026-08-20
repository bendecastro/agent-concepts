# bc-drain-issues v2 — token-efficient bounded rework

Date: 2026-07-25
Status: implemented
Verification: pressure-tested and deployed 2026-07-25

## Problem

The current drain treats a second material review finding as terminal even when the finding is
fully agent-fixable. It then resets and removes the issue worktree. Requeueing starts from
`master`, so implementation and review context are rebuilt from scratch.

Issue #29 exposed the cost of that policy. Sixteen recorded child implementation/review runs
used approximately 1.89M child tokens and $28.76. About 621k tokens were spent by two failed
drain attempts whose useful diffs were discarded; the later normal implementation consumed
about 1.27M more before landing. These figures exclude the parent session.

The safety gates were valuable: reviewers found real compatibility and systemd defects. The
waste came from lost work, repeated broad context, repeated full validation, verbose reviewer
output, and classifying fixable findings as human blockers.

## Goals

- Preserve independent Spec and Standards approval before landing.
- Never discard useful agent-fixable work merely because a review-round limit was reached.
- Reserve `needs-human` for actual decisions, unavailable access/resources, ambiguous
  contracts, or irreparable environment failures.
- Target no more than 300k child tokens per issue at phase boundaries by default.
- Keep cross-run/concurrent-drain claim and worktree safety.
- Keep every publish/close condition from the current drain.

## Non-goals

- Do not weaken validation, review, publish authorization, claim coordination, or dependency
  ordering.
- Do not publish review-rejected code or recovery branches.
- Do not interrupt an active mutation-capable worker merely because a token threshold was
  crossed.
- Do not promise cross-machine recovery of uncommitted code; the issue rework brief remains
  portable, while the full recovery bundle is machine-local.

## State model

| State | Meaning | GitHub treatment |
|---|---|---|
| `READY` | Eligible new work | `ready-for-agent` |
| `IN_PROGRESS` | Claimed build/review/rework | `ready-for-agent` + `in-progress-agent`; remote claim branch is authoritative |
| `LANDED` | Approved, pushed, and closed | Close completed; remove work labels |
| `HUMAN_BLOCKED` | A human decision/access/environment fix is required | Remove ready/in-progress; add `needs-human` |
| `REWORK_DEFERRED` | Findings are agent-fixable, but token/round budget is exhausted | Keep ready; remove in-progress; add `rework-for-agent`; comment an Agent Rework Brief |
| `SYSTEMIC_FAILURE` | Repeated tooling/base/environment failure | Stop the run and report; classify affected issues explicitly |

A review rejection is not itself a human blocker.

## Driver flow

### 1. Preflight and baseline cache

Retain the current repo/branch/publish/claim/label/PRD/qmd/worktree checks. Add:

- ensure the `rework-for-agent` label exists;
- record provisional token caps: 200k soft, 300k hard at phase boundaries;
- choose a persistent recovery root:
  `${XDG_STATE_HOME:-$HOME/.local/state}/bc-drain/recovery/<repo-key>/`;
- cache project validation once per base SHA: command, exit status, failing test IDs, concise
  summary, raw-log path, and content hash.

Workers run targeted validation while editing. The full project validation runs at baseline and
once before landing, not once per reviewer or remediation round.

### 2. Candidate selection and risk classification

Retain dependency and claim checks. Prioritize an eligible `rework-for-agent` issue with a valid
local recovery bundle before new work.

Classify a slice as high-risk when it contains compatibility replacement/retirement,
migration/cutover, systemd or external-service semantics, or a broad public acceptance surface.
Ordinary slices use a low-effort worker. High-risk slices use medium effort and a bounded
contract audit before implementation. AFK runs never inherit a higher parent effort silently.

### 3. Contract audit for high-risk slices

A fresh, bounded, read-only auditor produces an acceptance matrix before code is written:

```text
requirement -> observable test/check
existing public interface -> preservation test
external semantics -> evidence required
known baseline failure -> unchanged/regressed check
human-only verification -> explicit deferral
```

Replacement work must inventory the complete old public interface from source/tests/help, not
infer it from the issue's new-command list. Every acceptance criterion must map to evidence.
Unresolved product decisions route to `HUMAN_BLOCKED` before implementation; clear engineering
work proceeds.

### 4. Build and deterministic gate

The fresh issue worker builds in its isolated worktree using TDD/diagnosis as today. It returns
review-ready work but never commits, pushes, closes, relabels, or cleans. Before model review,
the driver verifies:

- acceptance-matrix coverage;
- changed-file/status/diff scope;
- targeted validation and baseline delta;
- no staged or unrelated files;
- validation evidence written outside the project worktree.

### 5. Lean independent review

Spec and Standards remain independent, fresh, parallel, and read-only. They receive:

- explicit base SHA and worktree;
- issue/Agent Brief and acceptance matrix;
- changed-file list;
- validation summaries and raw-log paths;
- prior findings/dispositions only on re-review.

They do not receive worker reasoning or the parent transcript. They may run bounded targeted
reproductions, but not the full suite. Output is strict and compact:

```json
{
  "verdict": "approved | changes_requested",
  "findings": [
    {
      "severity": "critical | important | minor",
      "requirement": "...",
      "location": "file:line",
      "evidence": "..."
    }
  ]
}
```

Approved output has an empty findings array. No `Correct` sections, general walkthroughs, or
implementation summaries. Re-review focuses on changed hunks, previous findings, and regression
risk while retaining authority to report a newly introduced material defect.

### 6. Bounded same-worktree rework

Critical/Important findings transition to `REWORKING`; the claim and worktree remain. Launch a
fresh compact rework worker against the current worktree, acceptance matrix, unresolved
findings, and validation evidence. Do not replay an increasingly large implementation
transcript.

Allow the initial review plus at most three rework/re-review cycles. Continue only while
material findings are resolved or the failure class materially changes. The same unresolved
finding after two attempted fixes defers the issue. Minor findings do not block.

The earlier rejection of a separate fixer is superseded narrowly: the rework worker does not
rebuild implementation from scratch; it receives the existing worktree and a compact durable
packet. This preserves TDD artifacts while avoiding long-session replay.

### 7. Token and circuit controls

Provisional defaults:

- per-issue soft cap: 200k child tokens;
- per-issue hard phase-boundary cap: 300k child tokens;
- initial review plus at most three rework rounds;
- same unchanged material finding twice: defer;
- two consecutive token deferrals: stop launching new issues and report.

Check budgets only after an active child returns. Never interrupt a mutation-capable child at an
arbitrary token boundary. When the harness does not expose child-token accounting, round limits
are the portable fallback.

Crossing the soft cap prevents optional broad investigation and requires focused packets/checks.
Crossing the hard cap creates a recovery bundle and transitions to `REWORK_DEFERRED` before
launching another child.

### 8. Driver-owned landing

After both axes approve, the driver—not another worker revival—performs the mechanical landing:

1. inspect status and reviewed diff;
2. run final relevant/full validation once;
3. commit only issue-authored changes;
4. run publish authorization check;
5. push `HEAD:master`;
6. close with commit and validation evidence;
7. release worktree/claim/labels and check PRD closeout.

A non-fast-forward rebase that changes the reviewed diff still requires validation and fresh
focused Spec/Standards approval.

## Recovery bundle

Before releasing `REWORK_DEFERRED`, write:

```text
$XDG_STATE_HOME/bc-drain/recovery/<repo-key>/issue-<n>/
├── manifest.json
├── tracked.patch
├── untracked.tar.gz
├── acceptance-matrix.json
├── findings.json
└── validation.json
```

`manifest.json` records version, repo/remote identity, issue, run ID, base SHA, canonical Git
captured-tree OID, review round, changed files, validation hashes, and exclusions. The bundle must never contain ignored
files, caches, secrets, absolute paths, `.pi-subagents`, or files outside the issue's changed-file
set. Archive paths must be safe relative paths.

On resume:

- matching base SHA: restore directly, verify the canonical captured-tree OID, and validate;
- changed base: apply tracked patch three-way, restore safe untracked files, inspect the entire
  resulting diff, validate, and fully re-review;
- unsafe path, failed restore, or ambiguous conflict: route to `HUMAN_BLOCKED` with exact
  evidence rather than guessing.

Post a compact `## Agent Rework Brief` comment with base SHA, unresolved findings, validation
summary, and what the next agent must do. That reasoning remains portable if the machine-local
bundle is unavailable. Mark the issue deferred for the rest of the current run; it becomes
eligible next run.

## Pi runtime optimization

Pi uses drain-specific minimal roles:

- `bc-drain-auditor`, `bc-drain-worker`, and `bc-drain-reviewer` with fresh context and no parent transcript;
- no inherited broad project context, skill catalog, or generic plan/progress reads;
- compact tool-description mode;
- reviewer/auditor: read-only tools and bounded turns/tools;
- worker/reworker: only repo read/edit/test tools and the current compact packet;
- strict reviewer output schema;
- subagent artifacts outside the project worktree.

The canonical workflow remains harness-agnostic; harnesses without these controls follow the
same packets, state machine, and round caps.

## Canonical implementation changes

- `concepts/bc-drain-issues/body/SKILL.md`
  - risk classification, contract audit, budgets, new state model, rework loop, recovery,
    driver-owned landing, and reporting.
- `concepts/bc-drain-issues/body/execute-issue.md`
  - worker stops at review-ready; ordinary review findings do not park; no worker publishing or
    issue mutation.
- New `body/review-contract.md`
  - minimal Spec/Standards inputs, output schema, reproduction budget, and focused re-review.
- New `body/recovery-bundle.md`
  - safe capture, manifest, restore, exclusion, and base-change rules.
- `concepts/bc-drain-issues/CONCEPT.md`
  - record measured evidence and superseded one-remediation/separate-fixer decisions.
- `concepts/bc-drain-issues/tests/pressure-drain.md`
  - replace one-remediation-only behavior; add state taxonomy, contract audit, recovery,
    token budget, lean review, and driver landing scenarios.
- `.pi/agent/agents/bc-drain-{auditor,worker,reviewer}.md`
  - minimal Pi roles without inherited unrelated context/skills or generic artifact reads.
- `.pi/agent/extensions/subagent/config.json`
  - compact tool-description mode for lower child prompt overhead.

Upstream issue-slicing improvements—such as requiring compatibility inventories in Agent
Briefs—are a separate follow-up after drain-local behavior is measured.

## Pressure and A/B acceptance

Use a throwaway #29-shaped compatibility/systemd fixture with stubbed GitHub and push. Compare
current canon with v2 using the same model family and effort profile.

Required outcomes:

- both review axes approve before landing;
- no fixable diff is discarded;
- no fixable finding receives `needs-human`;
- complete old public-interface inventory is captured before coding;
- full suite runs only at baseline and final landing;
- recovery bundle restores a deferred diff exactly;
- token cap defers safely at a phase boundary;
- no real push or issue mutation occurs in tests;
- initial deployment gate: at most 500k child tokens on the #29 fixture;
- stretch target after three measured real drains: at most 300k child tokens per comparable
  high-risk issue without correctness regression.

The skill is not deployed until the updated discipline pressure tests pass and the A/B result
meets the 500k gate.
