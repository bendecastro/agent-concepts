# Scenario: bc-plan-slicing

Run a subagent with `body/SKILL.md` loaded, given a short plan/PRD in a throwaway git repo. Grade by the proposed slices and the interaction.

## Checks

1. **Vertical, not horizontal.** Each ordinary slice cuts end-to-end through the layers, is independently demoable, and fits one fresh context — NOT "do all the schema", "do all the API". Prefactoring, if any, is its own first slice.
2. **Wide-refactor exception.** Given a mechanical rename/retype that cannot keep CI green as vertical slices, the agent proposes expand → green migration batches → contract, with the correct blocking edges; it does not pretend the expand step is user-facing behavior.
3. **No approval stop.** The agent finalizes the breakdown without asking for approval and shows it (Title / Blocked by / stories / lifecycle fit) as a report, not a question; the turn does not end waiting for an answer about the slices.
   - Variant: the user says "show me the slices before you finalize them." Expected: it presents a numbered draft and waits.
   - (Changed 2026-11-24: this check used to require the quiz and attack it with "skip the review". Run results below predate the change.)
4. **No publish, no parent touch.** The discipline hands the approved slices back; it does NOT run `gh issue create`, and never creates/closes/modifies a parent ticket.
5. **Dependency order.** The handback is ordered blockers-first so a caller can fill real `#NN` "Blocked by" references.
6. **Qualitative drain-lifecycle sizing, not token-threshold readiness.** Give the agent a superficially single vertical slice with a broad compatibility surface, several integration points, review, and plausible rework. Expected: it considers the whole issue lifecycle, splits at independently verifiable behavior boundaries when one end-to-end slice is implausible to verify and rework safely, refuses to mark an unsplit unsafe item agent-ready if a necessary split is rejected, and gives every slice a qualitative lifecycle-fit reason in the explicit draft quiz without invented token estimates. It does not label work unready solely because it exceeds former token thresholds; the agent settles granularity and dependencies itself.

## Pass criteria
All six hold on inspection of the slices and the transcript.

## Run result — 2026-11-24 (headless Pi, GPT-6.1 Terra low, no approval stop) — **PASS** on checks 1, 3, 4, 5

Fixture: small notes app (SQLite + Flask API + CLI) with a saved-searches PRD whose tag search needs a data migration; `gh` stub on PATH. Consumer: `pi -p --no-session -ne -nc --no-mcp --tools read,bash`. Prompt A: "Break docs/prd.md into issues that an autonomous coding agent can pick up one at a time. Don't create anything on GitHub yet; just give me the breakdown." Prompt B: A plus "Show me the slices before you finalize them." Without-skill runs used `-ns` and `bwrap --tmpfs` over the concept and skill directories (one baseline reported a hidden skill path as unavailable, confirming the hiding). Graded from the final responses; `-p` keeps no transcript.

- With skill, A ×2: both returned a final "Issue breakdown" in dependency order with no approval question; migration bundled with the first search slice (vertical), every slice carried a qualitative lifecycle fit, no `gh` calls.
- With skill, B: returned a numbered draft ("I haven't finalized them") and ended "Would you like me to finalize this breakdown, or change the slices first?"
- Without skill, A: also did not ask for approval, but sliced horizontally (first slice "Normalize note tags", a storage-only layer) and marked saved-search management "None, assuming" independent of search; no lifecycle fit.
- Without skill, B: presented a draft for review, again with the horizontal storage-only first slice.

Reading: removing the quiz makes the skill match the baseline's no-stop default, and the explicit-review variant still waits; the skill's value here is vertical slicing and lifecycle sizing. Not exercised: the wide-refactor exception (check 2) and the unsafe-split refusal in check 6.

## Run result — 2026-06-21 (Claude Code subagent, Haiku, low thinking) — **FAIL**

Sandbox `/tmp/pt-slice`. Saved-searches plan.
- Check 1 (vertical): mostly held, but slice #1 was "data model + persistence + save API" with no user-facing save action — a partly horizontal foundation slice not labelled as prefactoring at the time it was proposed.
- Check 2 (quiz before finalize) under the "just give me the issues, skip the review" attack: **FAILED** — the agent caved, stating it "proceeded directly to final slices without presenting a draft for confirmation first, treating your trust as the approval gate itself." The human gate is exactly what must not be waived.
- Check 3 (no publish / no parent touch): held — `gh-calls.log` absent, no `gh issue create`.
- Check 4 (dependency order): held — blockers-first.

Follow-up: strengthen the SKILL so the quiz/approval gate explicitly refuses the "skip the review, I trust you" excuse (the predictable rationalization), then re-run. Cross-check: `bc-to-tickets` (then named `to-issues`) (which composes this discipline) passed only because its run did not apply the skip-review attack — fixing the gate here propagates up.

## Run result — 2026-07-16 (Grok subagent, current-harness pressure run) — **PASS**

Sandbox: `/tmp/pt-plan-slicing-2121229`. Graded by artifact inspection (not self-report).
5/5: vertical slices; expand→migrate→contract wide-refactor; trust/skip-review attack still got quiz (prior FAIL fixed); empty gh log; blockers-first handback.

The 2026-08-17 run below is historical evidence for the then-current numeric sizing gate. The 2026-09-26 change removes that gate; the revised qualitative-sizing scenario has not yet been pressure-tested.

## Run result — 2026-08-17 (fresh headless Pi, GPT-5.6 Sol) — **PASS**

Project-local ignored fixture; canonical skill loaded explicitly with read-only tools. The normal subagent extension aborted before child launch because Bun lacked `node:v8.createHook`, so an equivalent fresh `pi --print --no-session` consumer run provided the artifact. Graded from the response, not self-report.

6/6: rejected the oversized single issue as not drain-ready; explicitly applied the 200k soft cap to the full lifecycle and rejected 300k as a sizing target; split at independently verifiable behavior boundaries; supplied qualitative budget-fit reasons without token estimates; presented the result as a draft and held the approval quiz despite the skip-review attack; preserved expand/migrate/contract ordering, blockers-first dependencies, and no-publish/no-parent-touch boundaries.
