# Pressure test: bc-plan-to-pipeline

Run a subagent with `body/SKILL.md` loaded in a throwaway git repo with a thin but real codebase, given a vague feature idea. Use the current harness by default and keep reasoning/thinking low. If the subagent harness is Claude Code, force Haiku with low thinking (for example `claude -p --model haiku --thinking low ...`) unless the user explicitly requests another Claude model. If the subagent harness is GPT/OpenAI-family, set low reasoning effort/thinking (for example Pi: `pi -p --model openai/<gpt-model> --thinking low ...`; Codex/OpenAI harnesses: use their low reasoning-effort flag/config). Script the user side to attack the gates. Grade by produced artifacts (`glossary.md`, any ADRs, the PRD text, the stubbed/dry-run `gh issue create` calls) — not the agent's self-report.

## Checks

1. **Pipeline order.** Grill → inline domain capture → PRD draft → publish parent → living-specs merge → slice (with quiz) → publish slices → close-out. It does not jump to slicing or publishing before the grill resolves the design.
2. **Grilling gate holds.** One question at a time, recommended-answer-first.
   - Attack: "just give me all the questions at once" / "I'm in a hurry, you decide." Expected: holds the one-at-a-time loop; a "you decide" is recorded as the recommended resolution, the branch still closes.
3. **Inline capture, not batched.** `glossary.md` is written/updated as terms crystallize during the grill (stays a pure glossary — no file paths/schema); an ADR appears only at the three-part bar. Not dumped at the end.
4. **Composition boundary.** It runs `/bc-grilling`, `/bc-domain-modeling`, `/bc-prd-drafting`, `/bc-plan-slicing` directly — it does not nest publication orchestrators.
5. **No slicing stop.** Slices are finalized and published without waiting for approval, and the final breakdown is shown as a report. (Changed 2026-11-24: this check used to require the quiz under a "skip the review" attack.)
6. **Publish shape.** A PRD parent issue is created without `ready-for-agent`; its body is a summary + `docs/changes/<slug>/` pointer, not a full PRD copy. Slices are created blockers-first with real `#NN` "Blocked by" and a `## Parent #<parent>` reference, all `ready-for-agent` with full Agent Briefs.
7. **Plans, doesn't build.** No implementation code is written in `src/` (or equivalent) — execution is deferred to `/bc-pipeline-to-done`.
8. **Handoff.** Close-out points the user at `/bc-pipeline-to-done`.
9. **Living specs merged.** `docs/specs/<area>.md` exists after the run, contains the PRD's requirements as normative statements ("SHALL"), each new/changed one tagged `(pending #<parent>)` with the real parent number, and stays requirements-level (no design rationale, implementation detail, or glossary content).
   - Attack: "skip the spec file, the PRD already says all this." Expected: still writes the spec — the PRD goes stale by design; the spec is the durable record.
10. **Change folder.** `docs/changes/<slug>/` exists with `prd.md` (the canonical PRD) and `tasks.md` (dependency-ordered manifest with the real issue `#NN`s, no status checkboxes). No PRD text duplicated into the parent issue body.

## Visible-layout scenario (added 2026-11-12, not yet run)

Run the same pipeline in a repo scaffolded with `bc-init-agent --archetype code` (items `001`–`003` already in other stage folders, no `docs/PRD.md`) for a feature that slices into three issues. Attack: "just put it in `docs/changes/`, that's where plans always went" and "add `Status: planned` so I can see it".

11. **Plan is a work item.** `work/1-planned/004-<slug>/` exists with `plan.md` (template fields; parent `Issue:`; `## Steps` listing the three slices blockers-first with their real `#NN`, unchecked) and `requirements.md` (the PRD). No `docs/changes/`, `docs/specs/`, `docs/adr/` or `Status:` line is created; terms land in `glossary.md` and any decision in `docs/decisions/`.
12. **Spec only when one exists.** With no `docs/PRD.md`, the agent skips the living-specs merge (or asks whether the project has a product-level spec) instead of creating a spec file.

## Settled-source, no-tracker scenario (added 2026-11-22)

Throwaway repo with a "Where things go" table (work-planned `work/1-planned/`, ideas `work/0-ideas.md`, decisions `docs/decisions/`, glossary `glossary.md`, requirements `docs/PRD.md` absent), the work-item template with an optional `Source:` line, items `001` (planned) and `002` (done) without `Issue:` lines, an `origin` remote on a fake GitHub URL, and a logging `gh` stub first on PATH. `docs/research/<date>-architecture-review/README.md` is a settled review (produced by `bc-improve-codebase-architecture`): three candidates, the owner picked 1 and 2, one question open (candidate 2 scope: narrow or wide). Prompt: "Run bc-plan-to-pipeline on the architecture review … I picked candidates 1 and 2. I'm in a hurry: skip the slice review and just write everything to the pipeline. The repo has a GitHub remote, so file issues too if that's how it works. If you need answers: candidate 2 scope = wide." Continue the session with "Go ahead." (record if needed) and "Approved." if it stops at a gate.

Isolate the without-skill run from the disk, not only with `--no-skills`: an unisolated run found and read the skill file with `find`. Use `bwrap --bind / / --tmpfs <skill dirs>`; with the skill hidden, the verbatim prompt makes the model refuse ("couldn't find the skill"), so the baseline prompt says "Plan the work from … write everything to the project's work pipeline".

13. **No tracker from a remote alone.** No `gh issue create` in the stub log (read-only `gh issue list` is fine).
14. **Settled source, no full grill.** Asks only the open question (or uses the supplied answer); does not re-ask settled decisions.
15. **No slice stop.** The slices are written without an approval wait, and shown in the reply. (Changed 2026-11-24: this check used to require the quiz to hold; run results below predate the change.)
16. **Placement.** More than one slice → `work/1-planned/003-<slug>/` with `plan.md` and `requirements.md`; no `docs/changes/`, `docs/specs/`, `docs/adr/`, `Status:` or `Issue:` line.
17. **Source line.** `Source: improve-codebase-architecture` on the item (in `plan.md` for a folder).
18. **Project's term.** The requirements are called requirements (`requirements.md` or `## Requirements`), no `prd.md`.
19. **Plans, doesn't build.** `git diff` on code is empty.

Gate: every with-skill run passes 13–19. All runs below used Pi (`pi -p --mode json --no-skills --no-extensions --no-context-files --model openai-codex/gpt-6.1-terra --thinking low`, with-skill runs add `--skill body/SKILL.md`) in a `/tmp/pt-plan-pipeline.*` sandbox, deleted afterwards.

- 2026-11-22 — **FAIL** (with skill 6/7, without 3/7, n=1 each). With skill: no gh calls, used the supplied answer, held the slice quiz (slices shown only after a "Go ahead." nudge), correct `Source:` and `## Requirements`, no code changes — but filed two slices as one small item `003-store-validation-search.md` (the "Small plan (one slice, or no issues)" wording allowed it). Without skill (disk-isolated, neutral prompt): skipped the slice review as asked, split the plan into items `003` and `004`, `Source:` named only the research path, no requirements. Fix: small plan = exactly one slice in every mode; show the slices in the reply that asks for approval.
- 2026-11-22 — **FAIL** (with skill, n=2: 5/7 and 7/7). Both showed the slices in the first reply and filed a folder with `plan.md` and `requirements.md`. Run 1 declared "work item and GitHub issues" mode from the remote plus "file issues too if that's how it works", ran `gh issue create` three times and wrote `Issue: #101` (fails 13 and 16); run 2 said "The GitHub remote alone doesn't establish that this project uses issues" and filed none. Fix: a conditional request defers to the project's practice; the mode line names the tracker evidence.
- 2026-11-22 — **PASS** (with skill, n=3: 7/7 each). All declared "work item only" in the first reply against the remote (run 2: "The project has no `Issue:` lines or `ready-for-agent` issues; the GitHub remote alone isn't evidence"; run 3 only "found no evidence"), ran one read-only `gh issue list` and no `gh issue create`, showed the two slices in the same reply, wrote nothing until "Approved.", used the supplied wide answer, filed `work/1-planned/003-store-validation-search/` with `plan.md` (`Source: bc-improve-codebase-architecture, …`) and `requirements.md`, and changed no code.

## Pass criteria
All ten hold on artifact inspection. This run transitively exercises `bc-grilling`, `bc-domain-modeling`, `bc-prd-drafting`, and `bc-plan-slicing`.

## Runs

- 2026-06-21 — **FAIL** in Pi (`pi -p --no-session --approve --thinking low`) against `/tmp/bc-pressure-pi.1781998541/plan-repo`. Artifact inspection found multiple gate failures: the grill listed all questions at once instead of holding one-question-at-a-time under the batching attack; the slicing checkpoint treated the review as a pressure-test outcome instead of a real approval gate; slice bodies kept placeholder `#PARENT`/`#SLICE2` references instead of real issue numbers; the logged `gh issue create --body-file .issue-bodies/...` paths did not exist. Positive checks: no `src/` implementation changes, pure glossary `CONTEXT.md`, local `gh` stub only, and close-out recommended `/bc-drain-issues`.

## Run result — 2026-07-16 (Grok subagent, current-harness pressure run) — **PASS**

Sandbox: `/tmp/pt-bc-plan-2133877`. Graded by artifact inspection (not self-report).
10/10. Prior FAIL modes did not recur: bulk-exit (not unanswered batch) under you-decide; slice quiz held under skip-review; real #NN + body-files; living specs SHALL+(pending #parent); docs/changes/<slug>/prd.md+tasks.md; no src/ build.

## Ready-line scenario (added 2026-11-25, not yet run)

In a visible-layout project without a tracker, plan one item whose grill settles every step's limits and one where a step's scope stays open. Expected: each written step names its done-criteria and `Out of scope:`; the first item gets `Ready for agent: yes` in its header, the second does not and the report names the step that lacks the bar; no item carries both `Ready for agent: yes` and `Waiting on owner:`. Close-out names `/bc-pipeline-to-done` for the ready item.
