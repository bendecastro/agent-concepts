# The plan→execute loop

How the workshop-pipeline skills compose into one end-to-end loop: from a raw idea to shipped code. Two user-invoked orchestrators (skills that run a sequence of other skills) bracket the loop (building can also be done attended, without the second); model-invoked disciplines (reusable instructions the agent applies to one kind of work) hold the reusable behavior underneath. Terms such as PRD, ADR, driver and preflight are defined in the [glossary](../../glossary.md).

```
  idea / issue / bug report
   │
   ├──► /triage (for existing tracker items: verify, brief, needs-info, out-of-scope)
   │
   ├──► /prototype (optional evidence for state/UI uncertainty)
   │
   ├──► /improve-codebase-architecture (optional architectural runway)
   │
   ▼   /bc-plan-to-pipeline   ── interactive planning (human in the loop) ──┐
   │     grilling ─► bc-domain-modeling ─► bc-prd-drafting ─► [publish PRD issue] │
   │                                     └► bc-plan-slicing ─► [publish slices]
   │                                    (slices finalized by the agent)     │
   │     (no tracker: slices become the work item's steps; no issues)       │
   ▼                                                                        │
  ready queue: work items with `Ready for agent: yes` ◄────────────────────┘
               or ready-for-agent issues
   │
   ├──► attended (standard): "continue the work" in a session
   │
   ▼   /bc-pipeline-to-done ── unattended execution (AFK) ──┐
   │     loop: claim next ready item or issue                         │
   │       └► fresh worker: tdd OR bc-diagnosing-bugs ─► validate        │
   │            └► deterministic gate ─► tiered review                │
   │                 (tier 1: combined; tier 2: Spec + Standards axes)
   │                 └► same-worktree rework/re-review (up to 3 cycles)
   │                      └► driver-owned commit ─► push to target branch ─► close
   │       └► terminal outcomes: HUMAN_BLOCKED / REWORK_DEFERRED / SYSTEMIC_FAILURE
   ▼                                                                       │
  shipped (trunk) ◄────────────────────────────────────────────────────────┘
```

## Optional architecture feedback edge (bounded, not an autonomous phase)

```text
bc-plan-to-pipeline → bc-pipeline-to-done → optional observation inbox
                                      → human-approved bc-improve-codebase-architecture → bc-plan-to-pipeline
```

After a landed issue, `bc-pipeline-to-done` may prepend at most one bounded structural observation to the project's declared context inbox. New entries are written in the consumer's current newest-first order, so bounded reads cannot hide new observations below older history. This is a separate context-only, non-authoritative update. `bc-improve-codebase-architecture` verifies the open evidence before exploration and keeps its existing human decision points: choosing a candidate, and the grilling. This is feedback, not another autonomous drain phase or a direct issue-creation path: only the human-approved route back through `bc-plan-to-pipeline` can turn a verified runway candidate into planned issues.

## Setup (once per repo) — `/bc-setup-project`

Run `/bc-setup-project` once. For a fresh code project it creates a root `AGENTS.md` and keeps project knowledge in ordinary folders:

- `work/0-ideas.md` holds undecided ideas. Work items move from `work/1-planned/` to `work/2-active/` to `work/3-done/` (filed by month); `work/4-dropped/` holds dropped work. `work/README.md` shows the work index. The owner can add `work/order.md` to rank open items; setup does not create that file.
- Decisions and research go in `docs/decisions/` and `docs/research/`; the domain glossary is `glossary.md` at the root.
- `.bc-agent/` holds agent mechanics: `AGENTS.md` (including the **Where things go** table), `map.md`, `log.md`, `conventions/`, `references/`, `templates/`, and `scripts/`. The planning and execution skills use the table to find project paths.

Setup can also offer a `publish.yaml` push-authorization rule if the project will use unattended pushes.

### What the pipeline needs

`/bc-pipeline-to-done` needs separate agents to build and review changes. If the harness cannot launch them, the pipeline stops before claiming work. Other agents need equivalent roles and isolation. To work from GitHub issues, also install and sign in to the [GitHub CLI](https://cli.github.com/) (`gh`); `/bc-setup-project` checks it when the project has a GitHub remote, and local work items do not need it.

In Pi, the [Pi install](../../README.md#pi) brings `pi-subagents` and the pipeline's auditor, builder and reviewer [roles](../../concepts/bc-pipeline-to-done/body/roles.md), with nothing to copy. If `pi-subagents` is missing, the pipeline offers to install it, then asks you to restart Pi.

### Optional machine tools

The skills name a few machine tools a project may have configured. None is required; without one, the agent does this:

| Tool | If you have not configured one |
|---|---|
| Guarded pytest runner | Run plain `pytest` in the project environment. Use `tmp_path` for test fixtures, clean up temporary files even on failure and do not set a custom `--basetemp`. |
| Storage health check | Skip the check and say so in one line of the run report. If a configured check fails to run or reports critical or unknown health, stop and report it. |
| Wrapper for heavy checks | Run the project's full validation command directly. The session combining the changes runs it, not each worker. |
| Publish-policy checker | The pipeline uses its bundled checker. With no policy file, it asks once before pushing if you can answer; otherwise it commits locally and pushes nothing. |

## The two halves

**Intake — `/bc-triage`** (interactive, as needed). Turns existing issues/PRs into the bc state machine: verify, grill if needed, write an Agent Brief, mark `ready-for-agent`, route broad work into `/bc-plan-to-pipeline`, or record rejections as dropped work items in `work/4-dropped/`.

**Evidence / runway — `/bc-prototype` and `/bc-improve-codebase-architecture`** (interactive, optional). Use prototypes when a state/UI decision needs a throwaway artifact before the PRD. Use architecture review when a feature or bug exposes poor seams and needs a deep-module plan before slicing.

**Planning — `/bc-plan-to-pipeline`** (interactive, run once per feature). Grills the idea one question at a time, captures the domain model inline (`glossary.md` + ADRs), drafts a PRD and publishes it as a parent issue, then slices it into vertical tracer-bullet issues (small pieces that each run the whole path from user action to result) and publishes them `ready-for-agent` in dependency order. One human decision point: the grill; the agent finalizes the slices without an approval stop. Composes model-invoked disciplines only (`bc-grilling`, `bc-domain-modeling`, `bc-prd-drafting`, `bc-plan-slicing`) — never the user-invoked single-step orchestrators.

**Building — attended (the standard way).** Open a session and tell the agent to continue the work. It follows the project's work rules in `.bc-agent/AGENTS.md`: it reads the active items and checks for a live holder before resuming unfinished work. Then it takes the next item in pipeline order and ticks the steps as they land, using your own agent, skills and checks. It asks you when something is unclear.

**Building — unattended, `/bc-pipeline-to-done`** (AFK, the option for when you are away; the old name `/bc-drain-issues` still works as an alias). It builds the same queue from one of two sources: work items carrying `Ready for agent: yes` (which `/bc-plan-to-pipeline` writes only when every step states its done-criteria and what is out of scope), or GitHub issues labelled `ready-for-agent`. Because nobody is there to answer questions, it replaces the owner with checking, so it costs more tokens and takes longer than the same work done attended.

- **Claim.** The driver claims each unit before any work starts so two drivers cannot build the same thing: a no-force `bc-drain-claims/issue-<n>` or `bc-drain-claims/item-<slug>` branch on the remote. A work item is claimed whole; one builder works through its steps in order and ticks each as it lands. With no Git remote, only one driver may run, the committed move of the item to `work/2-active/` is the claim, and the run commits locally without pushing.
- **Audit and build.** High-risk units get a read-only audit first. A **fresh builder** then builds the unit test-first (or runs `bc-diagnosing-bugs` for bugs) in its own worktree; it cannot commit, push, or change the issue or work item. Performance, size, memory and structure fixes follow the [builder's guardrails rule](../../concepts/bc-pipeline-to-done/body/execute-issue.md#build-loop).
- **Review and land.** A deterministic pre-review gate (an automated check with fixed rules, not an agent's judgment) runs, then tiered review: tier 1 uses one combined reviewer, while tier 2 uses two independent axes (Spec and Standards). The driver lands (commit, push to the preflight-recorded target branch, close the issue with a validation comment, or tick the step) only when every review approves the exact final diff. Material findings receive bounded same-worktree rework/re-review for up to three cycles. A finished work item gets its Outcome filled and moves to `work/3-done/`.
- **Outcomes.** `HUMAN_BLOCKED` for a human decision, unavailable access, contract clarification, or irreparable environment repair; `REWORK_DEFERRED` when fixable findings outlast the round or token bound; `SYSTEMIC_FAILURE` for repeated tooling, base, or environment failure. A work item that needs a decision is parked: the driver adds `Waiting on owner: <question>`, removes its `Ready for agent:` line, releases the claim and moves on; when you answer, write the answer into the item, delete the waiting line and restore `Ready for agent: yes`. Preflight (the checks and decisions made before a run starts) is the only planned human decision point.


## Composition map

| Layer | Skills |
|---|---|
| User-invoked setup | `bc-setup-project` (scaffolds the per-repo workspace) |
| User-invoked orchestrators (loop) | `bc-plan-to-pipeline`, `bc-pipeline-to-done` |
| User-invoked intake / exploration | `bc-triage`, `bc-prototype`, `bc-improve-codebase-architecture` |
| User-invoked single-step (standalone) | `bc-to-spec`, `bc-to-tickets` |
| Model-invoked disciplines | `bc-grilling`, `bc-domain-modeling`, `bc-prd-drafting`, `bc-plan-slicing`, `bc-research`, `bc-tdd`, `bc-diagnosing-bugs`, `bc-codebase-design`, `bc-optimize-code`, `bc-code-review` |

`bc-to-spec` and `bc-to-tickets` remain for one-phase-at-a-time publication. For a standalone interview and domain capture, use `bc-grilling` + `bc-domain-modeling` directly. The loop orchestrators inline the *disciplines* beneath them so nothing is duplicated and no orchestrator calls another orchestrator.

## Safety posture (execution)
- **Push is authorization-gated.** [Pipeline preflight](../../concepts/bc-pipeline-to-done/body/SKILL.md#preflight--before-the-loop) uses the overlay's checker or the bundled one. If there is no policy file, the driver asks once for this run's target-branch push when the owner can answer, or commits locally and pushes nothing when they cannot. A yes sets single-driver mode and does not authorize claim-ref writes, issue changes, or a policy change.
- **Trunk-based, not PR-per-slice** — so dependency-ordered slices see prior work, and it matches what `publish.yaml` authorizes.
- **Parallel-safe claiming** — when authorized, drain runners claim through a remote `bc-drain-claims/issue-<n>` or `bc-drain-claims/item-<slug>` branch before working a unit; concurrent runners skip units they fail to claim. Local-only runs use one driver and no remote writes.
- **Bounded outcome handling** — fixable material findings use same-worktree rework/re-review for up to three cycles and then `REWORK_DEFERRED`; `HUMAN_BLOCKED` and `SYSTEMIC_FAILURE` remain distinct classifications.
- **Completion gate reads the project's own validation conventions**, not a hardcoded test command.
- **Tiered review gates landings** — the deterministic gate runs first; tier 1 uses one combined reviewer, while tier 2 uses two independent axes (Spec + Standards), with one-way escalation on gate rejection or a Critical finding.
- **Optional bounded improvement** — after a slice is GREEN, the per-issue agent runs `bc-optimize-code` *only when* the issue targets a measurable metric; a change is kept only if correctness still holds and the metric provably improves, else reverted. No metric ⇒ skipped (never optimize blind).

See [`work/3-done/2026-08/011-bc-grill-to-ship-loop.md`](../../work/3-done/2026-08/011-bc-grill-to-ship-loop.md) for the design rationale and `concepts/<name>/CONCEPT.md` for each skill's decisions.
