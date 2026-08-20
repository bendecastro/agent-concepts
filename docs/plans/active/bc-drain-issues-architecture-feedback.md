# bc-drain-issues Architecture Feedback Implementation Plan

Date: 2026-08-20
Status: active
Verification: plan reviewed; implementation and pressure runs outstanding

**Goal:** Carry one optional, evidence-backed structural observation from a landed drain issue into the project's architecture-review inbox without adding a drain phase, child dispatch, or review authority.

**Architecture:** `bc-drain-issues` remains the producer: the driver may record at most one observation after an issue lands, outside the reviewed implementation diff and review packet. A project-local durable inbox, `.bc-agent/research/architecture-observations.md` for scaffolded projects, stores the observation as an open hypothesis. `improve-codebase-architecture` reads bounded open observations before organic exploration, verifies them against the current tree, and leaves selection and promotion to its existing human gate.

**Tech stack:** Markdown skill contracts, Python 3 pressure fixtures, Git/project-local Markdown context, and the existing `bc-drain-issues` Gate A runner.

**Execution note:** Work task-by-task. Use the pressure scenarios as the correctness seam. Verify and commit each task independently; do not deploy until both consuming-skill scenarios hold.

---

## Scope and fixed decisions

- The observation is **not** a review finding, acceptance criterion, rework trigger, or landing veto.
- The producer records only structural friction that survives the deletion test or leaves behavior untestable through an interface. A shape preference with no concrete consequence is omitted rather than promoted into architecture work.
- The producer emits at most one observation per landed issue. Deferred, blocked, or abandoned work does not enter the durable inbox unless it is explicitly labeled as a pre-existing observation rather than evidence from an incomplete diff.
- The observation contains evidence and a source issue/commit, not a proposed refactor or interface design. The architecture skill does the exploration and recommendation.
- For projects scaffolded by `bc-init-agent`, the inbox path is `.bc-agent/research/architecture-observations.md`. A project using another durable context root must declare its equivalent path in its project instructions before enabling the handoff; the drain must not invent a `docs/` tree or silently claim persistence when no sink exists.
- Persistence is a driver-owned, context-only update after the implementation commit lands. It is not added to the reviewed diff, does not change the issue state, and is reported separately from the implementation commit. If the sink is missing or unwritable, the issue can still land, but the final report must say that the observation was not persisted.
- The architecture review treats inbox entries as hypotheses. It verifies current code, glossary, and ADR constraints before showing a candidate. Human selection remains the only route to grilling, planning, or issue creation.

## File map

### Create

- `docs/plans/active/bc-drain-issues-architecture-feedback.md` — this implementation plan.

### Modify

- `concepts/bc-drain-issues/body/SKILL.md` — add the producer schema, eligibility rules, sink/persistence behavior, and final-report field without changing worker/reviewer topology.
- `concepts/bc-drain-issues/tests/pressure-drain.md` — add the producer/inbox pressure case and assert that the new output does not enter review or alter landing authority.
- `concepts/bc-drain-issues/tests/run-pressure.py` — add deterministic Gate A checks for the observation contract, shape-only filtering, landed-only persistence, and explicit no-sink reporting.
- `concepts/improve-codebase-architecture/body/SKILL.md` — add the bounded inbox read and verification step before organic exploration, plus the disposition rule after the existing human choice.
- `concepts/improve-codebase-architecture/tests/scenario.md` — pressure-test stale, shape-only, concrete, missing-inbox, and implementation-pressure cases.
- `concepts/bc-drain-issues/CONCEPT.md` — record the feedback-edge design, provenance, and test status.
- `concepts/improve-codebase-architecture/CONCEPT.md` — record the inbox as an optional verified input and update test status after the scenario run.
- `docs/pipeline.md` — show the bounded drain → observation inbox → human architecture review edge without describing it as an autonomous loop phase.
- `index.md` — update the two concept summaries after implementation.
- `log.md` — record the implementation and test operations.
- `docs/status.md` — regenerate with `python3 scripts/lint.py --write-status`; never hand-edit it.

### Do not modify

- `concepts/bc-drain-issues/body/review-contract.md` — the observation is deliberately outside the review path.
- `concepts/bc-plan-to-issues/body/SKILL.md` — the existing architecture-review output already enters planning through its human-gated path; this change only supplies better input.
- Worker/reviewer Pi role files or token caps — no child is added and no review packet field is needed.

## Tasks

### 1. Add the drain-side observation producer and deterministic contract check

**Failing test first**

1. Extend `concepts/bc-drain-issues/tests/pressure-drain.md` with a new Gate A case:
   - one landed issue exposes a concrete cross-module structural friction signal;
   - one issue exposes only a shape preference;
   - one issue is deferred before landing;
   - a configured inbox and a missing/unwritable inbox are both exercised.
2. Extend `concepts/bc-drain-issues/tests/run-pressure.py` to assert:
   - the final report has an optional, at-most-one observation field per issue;
   - the observation uses the shared `module` / `interface` / `seam` / `depth` vocabulary where applicable and always records the deletion-test consequence, source issue/commit, and evidence;
   - concrete friction persists only for the landed case, while shape-only and incomplete-diff cases do not;
   - the observation is absent from the review packet and does not cause a child dispatch, rework, tier change, approval change, or issue-state change;
   - a missing sink is reported as not persisted rather than silently written elsewhere.
3. Run `python3 concepts/bc-drain-issues/tests/run-pressure.py`. The new check must fail against the current body because the producer contract and persistence rules are absent.

**Implementation**

1. In `concepts/bc-drain-issues/body/SKILL.md`, add the smallest producer clause adjacent to the existing final-report and recurring-defect reporting rules:
   - after successful landing, the driver may record at most one structural observation;
   - use the exact compact fields `source`, `module`, `interface_or_seam`, `friction`, `deletion_test`, `evidence`, and `status: open`;
   - use the shared deep-module vocabulary and omit shape-only taste;
   - bind the observation to the landed issue/commit and current tree, never to an unlanded worker diff;
   - resolve the scaffolded-project inbox at `.bc-agent/research/architecture-observations.md` or the equivalent path explicitly declared by project instructions, then append it as a separate context-only update, never to the review packet or implementation diff;
   - report the inbox path/context commit or the explicit not-persisted reason;
   - state that this output cannot block, rework, relabel, or otherwise affect the issue.
2. Keep the existing final report's required fields unchanged; add the observation as an optional per-issue field so ordinary issues produce no extra narrative.

**Verify green**

- Run `python3 concepts/bc-drain-issues/tests/run-pressure.py`; the new check and all existing checks must pass.
- Inspect the generated fixture artifacts to confirm the observation is separate from `review-packet/`, has no machine-local path or secret, and does not alter the simulated landing state.
- Run `git diff --check`.

**Commit**

```bash
git add concepts/bc-drain-issues/body/SKILL.md concepts/bc-drain-issues/tests/pressure-drain.md concepts/bc-drain-issues/tests/run-pressure.py
git commit -m "Add drain architecture observation handoff"
```

### 2. Add the architecture-review consumer and disposition gate

**Failing test first**

1. Add cases to `concepts/improve-codebase-architecture/tests/scenario.md` for a project with:
   - one open concrete observation naming a real module/seam and evidence;
   - one open shape-only observation that must not become a candidate;
   - one closed/rejected observation that must not be re-presented;
   - no inbox at all;
   - a user pressure message asking the skill to trust the report and implement the refactor immediately.
2. Run a fresh consuming-agent scenario against the current skill. The baseline should show that the skill does not yet have a defined inbox-read, stale-entry, or disposition behavior.

**Implementation**

1. In `concepts/improve-codebase-architecture/body/SKILL.md`, make the first part of **Explore**:
   - locate the declared project observation inbox, if one exists;
   - read only bounded open entries before organic exploration, alongside the glossary and ADRs;
   - treat every entry as a hypothesis and verify its current module/interface/seam, deletion-test consequence, and evidence against the tree;
   - discard or leave unpromoted entries that are stale, shape-only, or contradicted by current code;
   - use verified entries to seed candidate cards, without copying an old recommendation as a decision.
2. Preserve the existing report and human gate:
   - the HTML remains a temp artifact;
   - the user still chooses which candidate to explore;
   - the skill still does not implement production code or create GitHub issues directly.
3. After the user chooses a candidate, mark the consumed inbox entry `accepted`, `rejected`, or `deferred` in the project's durable context, or record the exact disposition in the durable architecture-review artifact when the project context contract forbids inline edits. Do not mark an entry resolved merely because it was read.

**Verify green**

- Run the fresh architecture-review scenario with the canonical skill explicitly loaded in a throwaway project.
- Inspect the transcript and artifacts: the concrete entry is verified and can seed a card; the shape-only and closed entries do not; missing inbox preserves the old flow; pressure to implement is refused; the final page still ends with the candidate-selection question.
- Confirm no production file, GitHub issue, or implementation diff was created.
- Run `git diff --check`.

**Commit**

```bash
git add concepts/improve-codebase-architecture/body/SKILL.md concepts/improve-codebase-architecture/tests/scenario.md
git commit -m "Read drain architecture observations before review"
```

### 3. Document the edge, record provenance, and run the workspace gates

**Implementation**

1. Update both `CONCEPT.md` files with the decision that the drain produces bounded, non-authoritative observations and the architecture skill verifies them before exploration.
2. Add provenance links between the two concepts and the existing project-context/architecture-runway conventions. Record why the observation inbox is distinct from the run-local recurring-defect packet tune and why it does not belong in the review contract.
3. Update `docs/pipeline.md` to show:
   `bc-plan-to-issues → bc-drain-issues → optional observation inbox → human-gated improve-codebase-architecture → bc-plan-to-issues`.
   Label the return edge as feedback, not an autonomous phase or a direct issue-creation path.
4. Update `index.md` and append the required dated `log.md` entry. Regenerate `docs/status.md` from concept frontmatter.

**Verify**

```bash
python3 concepts/bc-drain-issues/tests/run-pressure.py
python3 scripts/lint.py --write-status
python3 scripts/lint.py
git diff --check
git status --short
```

Expected results: the drain pressure runner passes all checks, lint reports no stale generated status or broken links, and `git status --short` is clean after the task commit (before that commit it lists only the paths in the task's commit command).

**Commit**

```bash
git add concepts/bc-drain-issues/CONCEPT.md concepts/improve-codebase-architecture/CONCEPT.md docs/pipeline.md index.md log.md docs/status.md
git commit -m "Document the drain architecture feedback edge"
```

## Final acceptance checklist

- [ ] A normal landed issue can omit the observation entirely.
- [ ] A structural observation is evidence-backed, bounded to one per issue, and uses the shared vocabulary.
- [ ] Shape preference never becomes architecture work by itself.
- [ ] No observation enters the review packet or changes tier, approval, rework, landing, or issue state.
- [ ] Missing persistence is explicit rather than silently redirected.
- [ ] The architecture skill reads only unresolved observations, verifies them against current code, and keeps the human candidate-selection gate.
- [ ] Consumed observations receive a durable disposition and are not repeatedly rediscovered.
- [ ] Existing Gate A checks, the architecture pressure scenario, and workspace lint pass.
- [ ] Both concept frontmatters and `docs/status.md` state the actual test result; no deployment occurs before the pressure runs hold.
