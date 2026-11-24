---
name: bc-plan-to-pipeline
description: One-command interactive planning pipeline — grill the idea (or only the questions a settled design leaves open), capture the domain model, draft a PRD, and slice it into the project's work pipeline as a work item, into ready-for-agent GitHub issues, or both. Run to go from an idea or an approved design to agent-ready work without remembering the sequence. Model-invocable when the user asks to route work into the bc planning loop; the grill remains the interactive human gate either way.
argument-hint: "What are we planning?"
---

# Plan to Pipeline

Take an idea all the way to agent-ready work **in one pass**, so you never have to remember the order of the planning skills. This is the interactive planning front of the loop. Work lands in the project's work pipeline (a work item), in an issue tracker, or both; when tracker issues exist, the autonomous executor `/bc-drain-issues` drains them.

## Choose the mode first

Decide both modes before step 1 and state them to the user in one line (for example "Mode: work item only, from a settled source").

- **Tracker or no tracker.** Use the tracker when the project already plans in it (it has `ready-for-agent` issues, or its work items carry `Issue:` lines) or the user plainly asks for issues. A GitHub remote alone is not enough: many projects keep their plans only in work items, and issues created there are a second copy nobody drains. A conditional request ("file issues too if that's how it works", "if the project uses them") is not a plain ask: it defers to the project's practice, so check that practice. The mode line names the evidence for the tracker choice (for example "no tracker: no `Issue:` lines or `ready-for-agent` issues"). **No tracker** otherwise, or when the user asks for work items only: skip every issue step (the parent issue, slice issues, `ready-for-agent` labels, `Issue:` lines, `#NN` references and `pending #NN` tags) and file the plan as a work item only (see [Where project files go](#where-project-files-go)). Without a tracker and without a "Where things go" table, use the fallback change folder and its `tasks.md` as the slice list.
- **Raw idea or settled source.** A **settled source** is a design the owner already settled: an architecture review whose candidates the owner picked, an approved spec, a finished grilling. Do not re-run the full grill on it. In step 1 ask only the questions the source leaves open, in one batch, then continue. A **raw idea** gets the full grill.

Slicing (step 6) never stops for approval, in any mode.

This orchestrator composes **model-invoked disciplines only** (`grilling`, `domain-modeling`, `naming-things`, `prd-drafting`, `issue-slicing`) — never another user-invoked orchestrator. It owns the publication steps itself. User-invoked exploration tools (`prototype`, `improve-codebase-architecture`, `triage`) can feed this command, but this command does not invoke them as nested orchestrators.

## Where project files go

This skill names project files by role: the **glossary**, the **decisions** folder, the **work-planned** folder, the **ideas** file, the **research** folder and **requirements** (the product-level spec). Resolve each role in the "Where things go" table in the project's `.bc-agent/AGENTS.md`, and follow the work-item rules in the same file (naming, numbering, template). Why: each project has one table, so a project that keeps something elsewhere changes one place and every skill follows.

When the project has no such table, use the paths this skill used before:

- If `.bc-agent/conventions/planning-workflow.md` exists, it is the project's mapping (an older `.bc-agent/` vault): glossary in the Glossary section of `.bc-agent/project/overview.md`, ADRs in `.bc-agent/decisions/`, plans and PRDs in `.bc-agent/project/`. Follow it.
- Otherwise: glossary `glossary.md`, ADRs `docs/adr/`, the change folder `docs/changes/<change-slug>/` with `prd.md` and `tasks.md`, and living specs `docs/specs/<area>.md`.

**The plan is a work item** when the table exists. The fallback change folder is used only without a table; creating `docs/changes/`, `docs/specs/` or `docs/adr/` in a project with a table would scatter the plan outside the folders that show its status.

Write a `Source: <name>` line under the item's header lines, naming what produced the plan: the upstream skill (for example `improve-codebase-architecture`) for a settled source, or `bc-plan-to-pipeline` for a raw idea. In a large plan it goes in `plan.md`.

Call the feature's requirements document by the project's term: the requirements role in the table (a work item's `requirements.md` or `## Requirements` section), not "PRD", when the project names it differently. This skill says "PRD" only for brevity.

- **Small plan** (exactly one slice, with or without a tracker): one file `NNN-slug.md` in work-planned, from `.bc-agent/templates/work-item.md`. Put the feature's requirements in a `## Requirements` section above `## Steps`.
- **Large plan** (more than one slice, with or without a tracker): a folder `NNN-slug/` in work-planned holding two files, plus any evidence worth keeping:
  - `plan.md` — the work-item template; its `Issue:` line holds the parent issue (none without a tracker), and its `## Steps` list the slices in dependency order, one checkbox each with title, issue `#NN` (with a tracker), blocked-by and user stories covered;
  - `requirements.md` — the PRD.
  Why two files: the steps already are the slice map, so a separate slices file would be a second copy that drifts.

Number items only from the main checkout: the next number is the highest across all stage folders plus one. In a git worktree, stop after step 2, add one line for the plan to the ideas file, and resume from step 3 in the main checkout; tell the user so. Why: two worktrees cannot see each other's numbers and would pick the same one. Never write a `Status:` line; the item stays in work-planned, and the agent that starts the work moves it.

In a hybrid project the glossary is shared with `teach`: follow the shared-glossary rule in `domain-modeling` (ask before removing or redefining a term you did not add this session).

## Pipeline

1. **Grill.** From a settled source, read it, answer what the source and the code already settle, and ask the owner only the questions left open, in one batch; skip to step 2 when none remain. From a raw idea, run `/grilling`: interview one question at a time, recommended-answer-first, down every branch of the decision tree. Answer from the codebase anything you can answer yourself rather than asking. If the grill exposes a question that cannot be resolved by conversation or code reading (state model feel, UI direction, architectural runway), pause and recommend the matching pre-planning tool: `/prototype` for throwaway evidence, `/improve-codebase-architecture` for deep-module runway, or `/triage` if the input is an existing issue backlog item that needs a drain-ready Agent Brief.

2. **Capture inline — don't batch.** As terms and decisions crystallize *during* the grill, run `/domain-modeling`: canonical names → the glossary (a pure glossary, no implementation detail); a decision that is costly to reverse AND would surprise a future reader AND reflects a real trade-off → a record in the decisions folder. Capture the moment it crystallizes, not at the end.
   - **Guard:** if the current directory isn't a project where a glossary and decision records belong (empty/scratch dir, unrelated files), confirm with the user before creating docs, or grill without persisting.
   Apply `naming-things` when choosing domain or public code names during the grill.

3. **Open the plan's home and draft the PRD.** With a table, create the work item (see [Where project files go](#where-project-files-go)); without one, create the change folder `docs/changes/<change-slug>/` (dash-case, named for the feature). Either is the single physical home for this change's planning artifacts; without it they scatter across tracker bodies, comments, and temp files. Run `/prd-drafting`: synthesize from the grill + codebase (no re-interview), sketch and confirm the test seams, and write the PRD to the standard template as the item's requirements (`## Requirements` in a small item, `requirements.md` in a large one) or as `docs/changes/<change-slug>/prd.md`. If pre-planning evidence exists that's worth keeping (a `/prototype` verdict, an architecture-review excerpt), file it in the large item's folder or the change folder, or as a dated folder in the research role for a small item — these otherwise die as temp files. (Step 2's guard applies here as well: confirm before creating docs in a directory that isn't a real project.)

4. **Publish the PRD parent issue (tracker mode only; skip without a tracker).** The parent is a planning/coordination artifact, not a drainable implementation task, so do **not** label it `ready-for-agent`. Its body is a coordination pointer, not a second copy of the PRD (a duplicated PRD drifts from the canonical one): the problem/solution summary plus `Planning artifacts: <path of the work item or change folder>`.
   ```
   gh issue create --title "PRD: <feature name>" --body-file <summary-with-pointer>
   ```
   Keep the returned issue number as the parent and record it on the work item's `Issue:` line (in `plan.md` for a large item). Only implementation slices get the `ready-for-agent` label. A small item with a single slice skips the parent: its one slice issue goes on the `Issue:` line in step 7.

5. **Fold requirements into the living specs.** With a table, do this only when the project has a product-level spec (the requirements role's file exists, or the user confirms the project needs one); merge into the requirements role's file; otherwise skip this step, because the feature's requirements already live in its work item. Without a table, update `docs/specs/<area>.md` (create the file/dir if missing; dash-case area names, one file per capability). This is the durable, normative record of *what the system is required to do* — PRDs and issues go stale by design once their work drains, so the specs are what future grills and agents read instead of re-deriving requirements from code. Merge the PRD's resolved requirements into the relevant spec file(s):
   - Write requirements as current truth ("The system SHALL …") with their key scenarios; rewrite superseded requirements rather than appending contradictions.
   - Tag each new or changed requirement `(pending #<parent>)` (the single slice's issue for a small item; `(pending <work-item path>)` without a tracker) so unimplemented spec text is detectable; whoever touches the spec after the queue drains drops the tag.
   - Stay at requirements level: design rationale belongs in decision records, implementation approach in the PRD, vocabulary in the glossary.
   - **Guard:** same as step 2 — if this isn't a project where such docs belong, confirm before creating them.

6. **Slice.** Run `/issue-slicing`: break the PRD into vertical tracer-bullet slices (prefactor first), check granularity and dependencies yourself, and continue to step 7 without waiting for approval. Show the final slices in your reply as a report, not a question. Only when the user asked in this request to review the slices first, present them as a draft and wait.

7. **Publish the slices.** Without a tracker, publish nothing: write the final breakdown into the item's `## Steps` (a large item's `plan.md`), each unchecked step with slice title, blocked-by references (by step title) and user stories covered, or into `tasks.md` in the fallback change folder; then go to step 8. With a tracker: in dependency order (blockers first) so real `#NN` fill each "Blocked by", each with `--label ready-for-agent` and `## Parent #<parent>`. These are the only newly-created issues that enter the drain queue. Each slice body must include an `## Agent Brief`-equivalent contract (desired behavior, key interfaces/domain concepts, acceptance criteria, out-of-scope, blockers) so `/bc-drain-issues` can run AFK without prior conversation:
   ```
   gh issue create --title "<slice title>" --label ready-for-agent --body-file <path>
   ```
   Then record the real numbers. With a table: write the final breakdown into the item's `## Steps` (a large item's `plan.md`), each unchecked step with slice title, its issue `#NN`, blocked-by references and user stories covered; a small item's single slice goes on its `Issue:` line. The folder the item sits in and its checked steps are its status, so add no status text. Without a table: write `docs/changes/<change-slug>/tasks.md` with the same entries. It's the map of the change, written once the real numbers exist — **not** a status board: completion state lives only in the tracker (duplicated state drifts; whoever wants status runs `gh issue list`).

8. **Close out.** Restate the resolved scope; point at the work item or change folder, the glossary, decision records and spec files written, and, with a tracker, the parent issue and the slice issue numbers. Then recommend the handoff: with a tracker, **"Run `/bc-drain-issues` to execute this queue autonomously."**; without one, name the work item as the next work to start.

## Guard rails
- This is **planning, not building** — do not write implementation code here. Code is the executor's job, one slice at a time.
- The grill (step 1, or the open-questions batch from a settled source) is the human checkpoint; slicing does not wait for approval. Everything after the grill runs without the user, and the drain runs AFK, so resolve open branches now — a vague issue becomes a parked issue at execution time.
- If the source is an existing GitHub issue, run `/triage` first when it lacks an Agent Brief, has conflicting labels, or may be already implemented / out of scope.
- If planning depends on uncertain state logic, UI direction, or architecture shape, use `/prototype` or `/improve-codebase-architecture` before final PRD/slice publication; capture the verdict in the PRD rather than sending throwaway work to the drain.
- Keep research/evidence distinct from actual PRDs: exploratory notes and reports can feed the PRD (and may be filed in the change folder as evidence), but only the work item's requirements (or `docs/changes/<change-slug>/prd.md` without a table) are the PRD artifact — the parent issue just points at it.

For glossary discovery in legacy projects, follow `domain-modeling`’s legacy glossary rule.
