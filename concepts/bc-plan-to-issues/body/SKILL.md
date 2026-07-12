---
name: bc-plan-to-issues
description: One-command interactive planning pipeline — grill the idea, capture the domain model, draft a PRD, and slice it into ready-for-agent GitHub issues. Run to go from a raw idea to an agent-ready issue queue without remembering the sequence. Model-invocable when the user asks to route work into the bc planning loop; the grill and slicing quiz remain interactive human gates either way.
argument-hint: "What are we planning?"
---

# Plan to Issues

Take a raw idea all the way to an agent-ready GitHub issue queue **in one pass**, so you never have to remember the order of the planning skills. This is the interactive planning front of the loop; when it finishes, the autonomous executor `/bc-drain-issues` drains the queue it produced.

This orchestrator composes **model-invoked disciplines only** (`grilling`, `domain-modeling`, `prd-drafting`, `issue-slicing`) — never another user-invoked orchestrator. It owns the publication steps itself. User-invoked exploration tools (`prototype`, `improve-codebase-architecture`, `triage`) can feed this command, but this command does not invoke them as nested orchestrators.

## Pipeline

1. **Grill.** Run `/grilling`: interview one question at a time, recommended-answer-first, down every branch of the decision tree. Answer from the codebase anything you can answer yourself rather than asking. If the grill exposes a question that cannot be resolved by conversation or code reading (state model feel, UI direction, architectural runway), pause and recommend the matching pre-planning tool: `/prototype` for throwaway evidence, `/improve-codebase-architecture` for deep-module runway, or `/triage` if the input is an existing issue backlog item that needs a drain-ready Agent Brief.

2. **Capture inline — don't batch.** As terms and decisions crystallize *during* the grill, run `/domain-modeling`: canonical names → `CONTEXT.md` (a pure glossary, no implementation detail); a decision that is costly to reverse AND would surprise a future reader AND reflects a real trade-off → an ADR under `docs/adr/`. Capture the moment it crystallizes, not at the end.
   - **Guard:** if the current directory isn't a project where `CONTEXT.md`/ADRs belong (empty/scratch dir, unrelated files), confirm with the user before creating docs, or grill without persisting.

3. **Draft the PRD.** Run `/prd-drafting`: synthesize from the grill + codebase (no re-interview), sketch and confirm the test seams, write the PRD to the standard template.

4. **Publish the PRD parent issue.** The parent is a planning/coordination artifact, not a drainable implementation task, so do **not** label it `ready-for-agent`.
   ```
   gh issue create --title "PRD: <feature name>" --body-file <path>
   ```
   Keep the returned issue number as the parent. Only implementation slices get the `ready-for-agent` label.

5. **Fold requirements into the living specs.** Update `docs/specs/<area>.md` (create the file/dir if missing; dash-case area names, one file per capability). This is the durable, normative record of *what the system is required to do* — PRDs and issues go stale by design once their work drains, so the specs are what future grills and agents read instead of re-deriving requirements from code. Merge the PRD's resolved requirements into the relevant spec file(s):
   - Write requirements as current truth ("The system SHALL …") with their key scenarios; rewrite superseded requirements rather than appending contradictions.
   - Tag each new or changed requirement `(pending #<parent>)` so unimplemented spec text is detectable; whoever touches the spec after the queue drains drops the tag.
   - Stay at requirements level: design rationale belongs in ADRs, implementation approach in the PRD, vocabulary in `CONTEXT.md`.
   - **Guard:** same as step 2 — if this isn't a project where such docs belong, confirm before creating them.

6. **Slice.** Run `/issue-slicing`: break the PRD into vertical tracer-bullet slices (prefactor first), and **quiz the user on granularity and dependencies until they approve**. This quiz is the **last human gate before autonomous execution** — do not skip it.

7. **Publish the slices.** In dependency order (blockers first) so real `#NN` fill each "Blocked by", each with `--label ready-for-agent` and `## Parent #<parent>`. These are the only newly-created issues that enter the drain queue. Each slice body must include an `## Agent Brief`-equivalent contract (desired behavior, key interfaces/domain concepts, acceptance criteria, out-of-scope, blockers) so `/bc-drain-issues` can run AFK without prior conversation:
   ```
   gh issue create --title "<slice title>" --label ready-for-agent --body-file <path>
   ```

8. **Close out.** Restate the resolved scope; point at the `CONTEXT.md`/ADRs/`docs/specs/` files written, the parent issue, and the slice issue numbers. Then recommend the handoff: **"Run `/bc-drain-issues` to execute this queue autonomously."**

## Guard rails
- This is **planning, not building** — do not write implementation code here. Code is the executor's job, one slice at a time.
- The grill (step 1) and the slicing quiz (step 6) are the human checkpoints. Everything after step 7 runs AFK, so resolve open branches now — a vague issue becomes a parked issue at execution time.
- If the source is an existing GitHub issue, run `/triage` first when it lacks an Agent Brief, has conflicting labels, or may be already implemented / out of scope.
- If planning depends on uncertain state logic, UI direction, or architecture shape, use `/prototype` or `/improve-codebase-architecture` before final PRD/slice publication; capture the verdict in the PRD rather than sending throwaway work to the drain.
- Keep research/evidence distinct from actual PRDs: exploratory notes and reports can feed the PRD, but only the drafted/published PRD parent is the PRD artifact.
