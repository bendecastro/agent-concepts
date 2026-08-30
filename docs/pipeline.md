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
   │     loop: claim next unblocked issue (remote claim branch)       │
   │       └► fresh worker: tdd OR diagnosing-bugs ─► validate        │
   │            └► deterministic gate ─► tiered review                │
   │                 (tier 1: combined; tier 2: Spec + Standards axes)
   │                 └► same-worktree rework/re-review (up to 3 cycles)
   │                      └► driver-owned commit ─► push master ─► close
   │       └► terminal outcomes: HUMAN_BLOCKED / REWORK_DEFERRED / SYSTEMIC_FAILURE
   ▼                                                                       │
  shipped (trunk) ◄────────────────────────────────────────────────────────┘
```

## Optional architecture feedback edge (bounded, not an autonomous phase)

```text
bc-plan-to-issues → bc-drain-issues → optional observation inbox
                                      → human-gated improve-codebase-architecture → bc-plan-to-issues
```

After a landed issue, `bc-drain-issues` may prepend at most one bounded structural observation to the project's declared context inbox. New entries are written in the consumer's current newest-first order, so bounded reads cannot hide new observations below older history. This is a separate context-only, non-authoritative update. `improve-codebase-architecture` verifies the open evidence before exploration and keeps its existing human candidate-selection and grilling gates. This is feedback, not another autonomous drain phase or a direct issue-creation path: only the human-gated route back through `bc-plan-to-issues` can turn a verified runway candidate into planned issues.

## Setup (once per repo) — `/bc-init-agent`

Before the loop runs in a fresh project, `/bc-init-agent` scaffolds a repo-root `AGENTS.md` + a `.bc-agent/` Obsidian-vault wiki (generalized from image-maze) via a deterministic `scaffold.py`. The vault's `conventions/planning-workflow.md` is the adapter that redirects `bc-plan-to-issues` persistence into the vault (glossary → `project/overview.md`, ADRs → `decisions/`, plans → `project/`) and documents the `bc-drain-issues` execution phase. It also offers to add the repo's `publish.yaml` push-authorization rule. It also offers to install a per-vault `bc-wiki-maintain` systemd user timer so log promotion can run overnight; install happens only after confirm. Run once; then the two halves below.

## The two halves

**Intake — `/triage`** (interactive, as needed). Turns existing issues/PRs into the bc state machine: verify, grill if needed, write an Agent Brief, mark `ready-for-agent`, route broad work into `/bc-plan-to-issues`, or record durable `.bc-agent/out-of-scope/` rejections.

**Evidence / runway — `/prototype` and `/improve-codebase-architecture`** (interactive, optional). Use prototypes when a state/UI decision needs a throwaway artifact before the PRD. Use architecture review when a feature or bug exposes poor seams and needs a deep-module plan before slicing.

**Planning — `/bc-plan-to-issues`** (interactive, run once per feature). Grills the idea one question at a time, captures the domain model inline (`CONTEXT.md` + ADRs), drafts a PRD and publishes it as a parent issue, then slices it into vertical tracer-bullet issues and publishes them `ready-for-agent` in dependency order. Two human gates: the grill and the slicing quiz. Composes model-invoked disciplines only (`grilling`, `domain-modeling`, `prd-drafting`, `issue-slicing`) — never the user-invoked single-step orchestrators.

**Execution — `/bc-drain-issues` / `/implement`** (AFK, run after planning/triage). A preflight-gated driver loop atomically claims each unblocked issue, dispatches a **fresh worker** to build it test-first (or run `diagnosing-bugs` for bugs), runs a deterministic pre-review gate, then applies tiered review: tier 1 uses one combined reviewer, while tier 2 uses two independent axes (Spec and Standards) before trunk-based landing (commit → push `master` → close with a validation comment). Material findings receive bounded same-worktree rework/re-review for up to three cycles. Terminal outcomes stay distinct: `HUMAN_BLOCKED` for a human decision, unavailable access, contract clarification, or irreparable issue-local environment repair; `REWORK_DEFERRED` when fixable findings outlast the round or token bound; and `SYSTEMIC_FAILURE` for repeated tooling, base, or environment failure. Preflight is the only planned human gate; these outcomes are reported rather than collapsed into one parking state.

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
- **Bounded outcome handling** — fixable material findings use same-worktree rework/re-review for up to three cycles and then `REWORK_DEFERRED`; `HUMAN_BLOCKED` and `SYSTEMIC_FAILURE` remain distinct classifications.
- **Completion gate reads the project's own validation conventions**, not a hardcoded test command.
- **Tiered review gates landings** — the deterministic gate runs first; tier 1 uses one combined reviewer, while tier 2 uses two independent axes (Spec + Standards), with one-way escalation on gate rejection or a Critical finding.
- **Optional bounded improvement** — after a slice is GREEN, the per-issue agent runs `bc-autoresearch-loop` *only when* the issue targets a measurable metric; a change is kept only if correctness still holds and the metric provably improves, else reverted. No metric ⇒ skipped (never optimize blind).

See `plans/implemented/bc-grill-to-ship-loop.md` for the design rationale and `concepts/<name>/CONCEPT.md` for each skill's decisions.
