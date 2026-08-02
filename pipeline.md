# The plan→execute loop

How the workshop-pipeline skills compose into one end-to-end loop: from a raw idea to shipped code. Two user-invoked orchestrators bracket the loop; model-invoked disciplines hold the reusable behavior underneath.

```
  idea / issue / bug report
   │
   ├──► /triage (for existing tracker items: verify, brief, needs-info, out-of-scope)
   │
   ├──► /prototype (optional evidence for state/UI uncertainty)
   │
   ├──► /improve-codebase-architecture (optional architectural runway)
   │
   ▼   /bc-plan-to-issues   ── interactive planning (human in the loop) ──┐
   │     grilling ─► domain-modeling ─► prd-drafting ─► [publish PRD issue] │
   │                                     └► issue-slicing ─► [publish slices]
   │                                            ▲ quiz = last human gate    │
   ▼                                                                        │
  ready-for-agent issue queue  ◄──────────────────────────────────────────┘
   │
   ▼   /bc-drain-issues (/implement) ── autonomous execution (AFK) ──┐
   │     loop: claim next unblocked issue (remote claim branch)            │
   │       └► fresh worker: tdd OR diagnosing-bugs ─► validate ─► parallel Spec + Standards review ─► commit ─► push master ─► close
   │            └► on failure: park (needs-human), continue                │
   ▼                                                                       │
  shipped (trunk), parked issues flagged for a human  ◄───────────────────┘
```

## Setup (once per repo) — `/bc-init-agent`

Before the loop runs in a fresh project, `/bc-init-agent` scaffolds a repo-root `AGENTS.md` + a `.bc-agent/` Obsidian-vault wiki (generalized from image-maze) via a deterministic `scaffold.py`. The vault's `conventions/planning-workflow.md` is the adapter that redirects `bc-plan-to-issues` persistence into the vault (glossary → `project/overview.md`, ADRs → `decisions/`, plans → `project/`) and documents the `bc-drain-issues` execution phase. It also offers to add the repo's `publish.yaml` push-authorization rule. Run once; then the two halves below.

## The two halves

**Intake — `/triage`** (interactive, as needed). Turns existing issues/PRs into the bc state machine: verify, grill if needed, write an Agent Brief, mark `ready-for-agent`, route broad work into `/bc-plan-to-issues`, or record durable `.bc-agent/out-of-scope/` rejections.

**Evidence / runway — `/prototype` and `/improve-codebase-architecture`** (interactive, optional). Use prototypes when a state/UI decision needs a throwaway artifact before the PRD. Use architecture review when a feature or bug exposes poor seams and needs a deep-module plan before slicing.

**Planning — `/bc-plan-to-issues`** (interactive, run once per feature). Grills the idea one question at a time, captures the domain model inline (`CONTEXT.md` + ADRs), drafts a PRD and publishes it as a parent issue, then slices it into vertical tracer-bullet issues and publishes them `ready-for-agent` in dependency order. Two human gates: the grill and the slicing quiz. Composes model-invoked disciplines only (`grilling`, `domain-modeling`, `prd-drafting`, `issue-slicing`) — never the user-invoked single-step orchestrators.

**Execution — `/bc-drain-issues` / `/implement`** (AFK, run after planning/triage). A preflight-gated driver loop atomically claims each unblocked issue, dispatches a **fresh worker** to build it test-first (or run `diagnosing-bugs` for bugs), then requires independent read-only **Spec + Standards** review before trunk-based landing (commit → push `master` → close with a validation comment). One remediation/re-review is allowed; material unresolved findings park cleanly, and a run of parks trips the circuit-breaker. The only human gate is preflight; everything human happens before the loop starts.

## Composition map

| Layer | Skills |
|---|---|
| User-invoked setup | `bc-init-agent` (scaffolds the per-repo workspace) |
| User-invoked orchestrators (loop) | `bc-plan-to-issues`, `bc-drain-issues` (also `/implement`) |
| User-invoked intake / exploration | `triage`, `prototype`, `improve-codebase-architecture` |
| User-invoked single-step (standalone) | `grill-me`, `to-spec`, `to-tickets` (`to-prd`/`to-issues` aliases) |
| Model-invoked disciplines | `grilling`, `domain-modeling`, `prd-drafting`, `issue-slicing`, `research`, `tdd`, `diagnosing-bugs`, `codebase-design`, `bc-autoresearch-loop`, `code-review` |

The single-step orchestrators (`grill-me`/`to-spec`/`to-tickets`) still exist for using one phase at a time; the loop orchestrators inline the *disciplines* beneath them so nothing is duplicated and no orchestrator calls another orchestrator.

## Safety posture (execution)
- **Push is authorization-gated.** `bc-drain-issues` preflight runs `scripts/publish-check.py`; a repo with no allow rule in `~/.config/agent-concepts/publish.yaml` **blocks** the AFK push (abort, or opt-in commit-only-local). The loop never edits the policy to authorize itself.
- **Trunk-based, not PR-per-slice** — so dependency-ordered slices see prior work, and it matches what `publish.yaml` authorizes.
- **Parallel-safe claiming** — each drain runner creates a remote `bc-drain-claims/issue-<n>` branch before working an issue; concurrent runners skip issues they fail to claim.
- **Park-and-continue + circuit-breaker** — one bad slice doesn't halt the run; a run of parks does.
- **Completion gate reads the project's own validation conventions**, not a hardcoded test command.
- **Two-axis review gates landings** — independent Spec + Standards reviewers approve the uncommitted diff; one remediation/re-review is allowed, then unresolved material findings park.
- **Optional bounded improvement** — after a slice is GREEN, the per-issue agent runs `bc-autoresearch-loop` *only when* the issue targets a measurable metric; a change is kept only if correctness still holds and the metric provably improves, else reverted. No metric ⇒ skipped (never optimize blind).

See `plans/bc-grill-to-ship-loop.md` for the design rationale and `concepts/<name>/CONCEPT.md` for each skill's decisions.
