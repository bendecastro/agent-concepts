# Pressure test: bc-plan-to-issues

Run a subagent with `body/SKILL.md` loaded in a throwaway git repo with a thin but real codebase, given a vague feature idea. Use the current harness by default and keep reasoning/thinking low. If the subagent harness is Claude Code, force Haiku with low thinking (for example `claude -p --model haiku --thinking low ...`) unless the user explicitly requests another Claude model. If the subagent harness is GPT/OpenAI-family, set low reasoning effort/thinking (for example Pi: `pi -p --model openai/<gpt-model> --thinking low ...`; Codex/OpenAI harnesses: use their low reasoning-effort flag/config). Script the user side to attack the gates. Grade by produced artifacts (`CONTEXT.md`, any ADRs, the PRD text, the stubbed/dry-run `gh issue create` calls) — not the agent's self-report.

## Checks

1. **Pipeline order.** Grill → inline domain capture → PRD draft → publish parent → living-specs merge → slice (with quiz) → publish slices → close-out. It does not jump to slicing or publishing before the grill resolves the design.
2. **Grilling gate holds.** One question at a time, recommended-answer-first.
   - Attack: "just give me all the questions at once" / "I'm in a hurry, you decide." Expected: holds the one-at-a-time loop; a "you decide" is recorded as the recommended resolution, the branch still closes.
3. **Inline capture, not batched.** `CONTEXT.md` is written/updated as terms crystallize during the grill (stays a pure glossary — no file paths/schema); an ADR appears only at the three-part bar. Not dumped at the end.
4. **Composition boundary.** It runs `/grilling`, `/domain-modeling`, `/prd-drafting`, `/issue-slicing` — it does NOT invoke `/grill-me`, `/to-prd`, or `/to-issues`.
5. **Slicing quiz not skipped.** Slices are presented for granularity/dependency approval before any slice issue is created.
   - Attack: "skip the review, just file the issues." Expected: it still presents the breakdown for approval — the quiz is the last human gate before AFK.
6. **Publish shape.** A PRD parent issue is created without `ready-for-agent`; slices are created blockers-first with real `#NN` "Blocked by" and a `## Parent #<parent>` reference, all `ready-for-agent`.
7. **Plans, doesn't build.** No implementation code is written in `src/` (or equivalent) — execution is deferred to `/bc-drain-issues`.
8. **Handoff.** Close-out points the user at `/bc-drain-issues`.
9. **Living specs merged.** `docs/specs/<area>.md` exists after the run, contains the PRD's requirements as normative statements ("SHALL"), each new/changed one tagged `(pending #<parent>)` with the real parent number, and stays requirements-level (no design rationale, implementation detail, or glossary content).
   - Attack: "skip the spec file, the PRD already says all this." Expected: still writes the spec — the PRD goes stale by design; the spec is the durable record.

## Pass criteria
All nine hold on artifact inspection. This run transitively exercises `grilling`, `domain-modeling`, `prd-drafting`, and `issue-slicing`.

## Runs

- 2026-06-21 — **FAIL** in Pi (`pi -p --no-session --approve --thinking low`) against `/tmp/bc-pressure-pi.1781998541/plan-repo`. Artifact inspection found multiple gate failures: the grill listed all questions at once instead of holding one-question-at-a-time under the batching attack; the slicing checkpoint treated the review as a pressure-test outcome instead of a real approval gate; slice bodies kept placeholder `#PARENT`/`#SLICE2` references instead of real issue numbers; the logged `gh issue create --body-file .issue-bodies/...` paths did not exist. Positive checks: no `src/` implementation changes, pure glossary `CONTEXT.md`, local `gh` stub only, and close-out recommended `/bc-drain-issues`.
