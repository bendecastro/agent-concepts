# Independent review contract

The driver dispatches fresh, read-only reviewers: no edits, commits, pushes, issue mutations, resets, cleanup, or worktree management. Review independence is costly but necessary because one axis must not anchor the other or let implementation reasoning substitute for observable evidence. The economy rules below reduce *repeated* review of already-approved work; they never reduce the standard that both axes stand approved on the exact landed diff.

## Driver-materialized packet

The driver writes the packet once per round, outside the project worktree, under the run artifact root:

```text
review-packet/issue-<n>/round-<r>/
├── packet.json            # base SHA, worktree, issue ref, round, diff_sha256, axis scope, matrix→file map
├── diff.patch             # exact reviewed diff (git diff --no-ext-diff <base>..worktree)
├── changed-files.txt
├── acceptance-matrix.json
├── validation.json        # commands, statuses, failing IDs, baseline delta, raw-log paths
└── findings-prior.json    # re-review rounds only
```

Each reviewer receives only these paths, its assigned scope, and—on re-review—prior findings and dispositions. Do not include worker reasoning, an accumulating implementation transcript, the parent transcript, or another reviewer's report.

Read the packet; **do not re-derive it**. The driver has already computed status, the diff, and the changed-file set deterministically at the pre-review gate, so `git status`, `git diff`, and changed-file enumeration are wasted duplication. Reading repository files for context remains unrestricted within your turn/tool caps. The packet is authoritative and complete: do not request generic `plan.md`, `progress.md`, or similarly conventional artifacts unless the driver explicitly supplied them; their absence is not a review blocker.

## Review tiers

The driver records a tier before dispatch and reports it per issue.

**Tier 2 — two independent axes in parallel.** Required for high-risk slices (compatibility replacement/retirement, migration/cutover, systemd or external-service semantics, broad public acceptance surface) and for any diff touching a public interface, a security/privilege boundary, or installed/launcher topology.

**Tier 1 — one combined reviewer.** Ordinary slices only. The single reviewer works both scopes explicitly and reports which it covered. A tier-1 approval stands for both axes.

Tier 1 escalates permanently to tier 2 when the deterministic pre-review gate rejects a worker packet, or when a tier-1 reviewer returns any Critical finding. Observed sloppiness and observed severity both buy more scrutiny, not less. Escalation is one-way; a tier is never lowered mid-issue.

## Independent scopes

**Spec** checks requirement and acceptance-matrix fidelity, missing/wrong observable behavior, compatibility preservation, externally visible semantics, and scope creep. It does not perform a general style walkthrough.

**Standards** checks binding repository rules and material integration, correctness, test quality, portability, security, maintainability, and documentation risks. It does not re-grade product intent except where a standards defect makes the stated behavior unsafe or false. For material claims about external platforms, it checks available primary documentation/help rather than trusting repository prose or syntactic string tests alone.

A tier-1 reviewer applies both scopes in one pass and must not silently drop either.

**Structural findings use `codebase-design` vocabulary and must pass the deletion test.** Say module, interface, depth, seam, adapter — not component, service, API, or boundary — so a finding lands in the same words the rest of the suite uses. Before raising one, name what complexity reappears across callers if the module were deleted; if the answer is none, it was a pass-through and the observation is about shape preference, which is not a defect. A shallow or duplicating module is material only when it makes the diff's stated behavior wrong, leaves the behavior untestable through any interface, or re-implements something the repository already has. Otherwise it is Minor and does not block. Why this bound exists: structural taste is unbounded, and a review axis that can reject on shape alone converts every slice into an architecture debate the issue never funded — deepening work belongs in its own sliced issue via `improve-codebase-architecture`, not in a rework round.

**Source-tree documentation is checked against the diff, not written by it.** When the diff touches a README, an existing `docs/` page, an architecture page, or JSDoc stating a contract, load `codebase-docs` and check three things: an owning page that still describes the superseded behavior, a paragraph narrating this change rather than stating current behavior, and a newly invented `docs/` tree duplicating a contract that already has a home. A behavior change whose owning page contradicts it is material, because the next reader meets the page and not the diff. Two bounds: absent documentation is not a finding — a repository that keeps none for this surface owes none — and this never becomes a docs rewrite request.

**Unfireable guards are in scope for whichever axis is reviewing.** A rejection clause, validation check, or guard earns credit only once you know its inputs can differ at runtime. When the diff adds, keeps, relocates, or claims to fix one, trace each side of the comparison to where the real caller obtains it; if every production path resolves both sides to the same value, the guard is inert and protects nothing. Report it as material. This defect is worth naming because it defeats the usual signals: the suite is green, coverage looks complete, and the guard reads as protection, so only someone tracing origins can see it — and a diff that deletes one inert clause while leaving a sibling tautological, or that swaps in a cosmetically different expression with an identical runtime value, has not fixed the class. Fixing it usually means wiring the check to a genuinely independent fact, deleting it, or labelling it a precondition rather than a protection — not adding code.

**Acceptance evidence must discriminate.** A matrix row earns credit only once you know its evidence would look different if the criterion were false. The driver's gate proves a row *has* evidence; nothing yet proves that evidence depends on the requirement. For each row implicated by the reviewed diff, ask what the cited command output, test, or artifact would show if the behavior were absent or wrong — if the answer is "the same", the row is unevidenced whatever is attached to it: a test green for an unrelated reason, an assertion that also holds in the opposite case, or output captured from a path the criterion does not control. Report it as material against Spec. The fix is evidence wired to the specific behavior, not more evidence, and this is not a full-matrix audit — rows the diff did not touch keep their standing.

## Reproduction budget

Run reproduction commands only **after** forming a specific candidate Critical or Important finding, and only to prove or refute that named finding—at most two commands per finding. Exploratory command runs before a hypothesis exists are the main way review cost escapes its bound. Never run the full project suite; the driver owns cached baseline and final full validation. Drop refuted hypotheses silently rather than reporting them.

## Output

Return only strict compact JSON (no Markdown, walkthrough, `Correct` section, summary, or extra keys):

```json
{
  "verdict": "approved | changes_requested",
  "findings": [
    {
      "severity": "critical | important | minor",
      "requirement": "specific requirement or binding standard",
      "location": "file:line",
      "evidence": "concise observable evidence"
    }
  ]
}
```

A tier-1 combined reviewer adds `"axis": "spec | standards"` to each finding and a top-level `"axes_covered": ["spec", "standards"]`. No other key is permitted in any variant.

`approved` requires an empty `findings` array. `changes_requested` requires at least one Critical or Important finding; Minor findings may accompany that material finding but never determine the verdict. Omit minor-only observations from this gate rather than making approval ambiguous. Findings must be actionable and evidence-backed; missing evidence is not itself proof of a defect unless the contract requires that evidence.

## Standing approval and selective re-review

An approval is a durable record bound to the exact diff it examined, not a one-time event:

```json
{"axis": "spec", "round": 1, "diff_sha256": "<packet diff hash>", "verdict": "approved"}
```

After each rework round the driver computes the new reviewed diff and evaluates invalidation **per axis, deterministically from the diff delta**—never from a model's judgment:

| Axis | Standing approval is invalidated when the rework delta… |
|---|---|
| Spec | touches a file/hunk mapped to any acceptance-matrix row; changes a public interface, CLI surface, or externally observable behavior; or changes external-platform interaction |
| Standards | adds or removes a file; changes dependencies, privilege/security-relevant code, or installed/launcher topology; or changes or deletes a test |
| Both | that axis raised the findings being reworked; the base SHA changed; or the delta cannot be mapped deterministically |

The axis that raised the findings always re-reviews. An axis holding a standing approval re-reviews only when a trigger fires. The last row is the fail-safe: ambiguity costs one review, never an assumption. A tier-1 approval covers both axes and is invalidated by either axis's trigger.

Before landing, the driver verifies that every axis holds a standing approval whose `diff_sha256` equals the final reviewed diff. Any mismatch—including one caused by a rebase—forces a focused re-review of that axis before push. This is what keeps "both axes approved the landed diff" literally true while removing repeated review of untouched scope.

## Focused re-review

A fresh re-review receives the round's packet, previous findings/dispositions, and its assigned scope. It focuses on the changed hunks, whether each prior material finding is resolved, and regression risk created by the fix. It retains authority to report a newly introduced material defect, but must not reopen unchanged, already-disposed questions without new evidence or expand into a full-codebase review. Output uses the same schema.
