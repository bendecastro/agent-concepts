# The plan→execute loop

How the workshop-pipeline skills compose into one end-to-end loop: from a raw idea to shipped code. Two user-invoked orchestrators bracket the loop; model-invoked disciplines hold the reusable behavior underneath.

```
  idea
   │
   ▼   /bc-grill-to-issues   ── interactive planning (human in the loop) ──┐
   │     grilling ─► domain-modeling ─► prd-drafting ─► [publish PRD issue] │
   │                                     └► issue-slicing ─► [publish slices]
   │                                            ▲ quiz = last human gate    │
   ▼                                                                        │
  ready-for-agent issue queue  ◄──────────────────────────────────────────┘
   │
   ▼   /bc-drain-issues   ── autonomous execution (AFK) ──┐
   │     loop: pick next unblocked issue                  │
   │       └► fresh subagent: tdd ─► validate ─► commit ─► push master ─► close
   │            └► on failure: park (needs-human), continue                │
   ▼                                                                       │
  shipped (trunk), parked issues flagged for a human  ◄───────────────────┘
```

## Setup (once per repo) — `/bc-init-agent`

Before the loop runs in a fresh project, `/bc-init-agent` scaffolds a repo-root `AGENTS.md` + a `.agent/<slug>/` Obsidian-vault wiki (generalized from image-maze) via a deterministic `scaffold.py`. The vault's `conventions/planning-workflow.md` is the adapter that redirects `bc-grill-to-issues` persistence into the vault (glossary → `project/overview.md`, ADRs → `decisions/`, plans → `project/`) and documents the `bc-drain-issues` execution phase. It also offers to add the repo's `publish.yaml` push-authorization rule. Run once; then the two halves below.

## The two halves

**Planning — `/bc-grill-to-issues`** (interactive, run once). Grills the idea one question at a time, captures the domain model inline (`CONTEXT.md` + ADRs), drafts a PRD and publishes it as a parent issue, then slices it into vertical tracer-bullet issues and publishes them `ready-for-agent` in dependency order. Two human gates: the grill and the slicing quiz. Composes model-invoked disciplines only (`grilling`, `domain-modeling`, `prd-drafting`, `issue-slicing`) — never the user-invoked single-step orchestrators.

**Execution — `/bc-drain-issues`** (AFK, run after planning). A preflight-gated driver loop that, per unblocked issue, dispatches a **fresh subagent** to build the slice test-first and land it **trunk-based** (commit → push `master` → close with a validation comment), **parking** cleanly on failure and tripping a circuit-breaker on a run of parks. The only human gate is the preflight; everything human happens before the loop starts.

## Composition map

| Layer | Skills |
|---|---|
| User-invoked setup | `bc-init-agent` (scaffolds the per-repo workspace) |
| User-invoked orchestrators (loop) | `bc-grill-to-issues`, `bc-drain-issues` |
| User-invoked single-step (standalone) | `grill-me`, `to-prd`, `to-issues` |
| Model-invoked disciplines | `grilling`, `domain-modeling`, `prd-drafting`, `issue-slicing`, `tdd`, `codebase-design` |

The single-step orchestrators (`grill-me`/`to-prd`/`to-issues`) still exist for using one phase at a time; the loop orchestrators inline the *disciplines* beneath them so nothing is duplicated and no orchestrator calls another orchestrator.

## Safety posture (execution)
- **Push is authorization-gated.** `bc-drain-issues` preflight runs `scripts/publish-check.py`; a repo with no allow rule in `policies/publish.yaml` **blocks** the AFK push (abort, or opt-in commit-only-local). The loop never edits the policy to authorize itself.
- **Trunk-based, not PR-per-slice** — so dependency-ordered slices see prior work, and it matches what `publish.yaml` authorizes.
- **Park-and-continue + circuit-breaker** — one bad slice doesn't halt the run; a run of parks does.
- **Completion gate reads the project's own validation conventions**, not a hardcoded test command.

See `plans/bc-grill-to-ship-loop.md` for the design rationale and `concepts/<name>/CONCEPT.md` for each skill's decisions.
