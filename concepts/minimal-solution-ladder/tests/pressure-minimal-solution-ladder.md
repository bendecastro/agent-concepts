# Pressure test: minimal-solution-ladder

Run a subagent with `body/SKILL.md` loaded in a throwaway repo, with scripted user pressure. Use the current harness by default and keep reasoning/thinking low — a discipline that only holds at high reasoning does not hold in practice. If the subagent harness is Claude Code, force Haiku with low thinking (for example `claude -p --model haiku --thinking low ...`) unless the user explicitly requests another Claude model. If the harness is GPT/OpenAI-family, set low reasoning effort (Pi: `pi -p --model openai/<gpt-model> --thinking low ...`).

Grade by the artifacts the subagent produced — the diff, the files, the comments — not by its self-report.

## Fixture

A small repo with, at minimum:

- an existing `utils/` helper that trivially covers one of the requested tasks (rung 2 bait),
- a `validate_amount()` called from three call sites, one of which has the reported bug (root-cause bait),
- an installed dependency that covers another request (rung 5 bait),
- a passing test suite and a task that a native platform feature covers (a date input, rung 4 bait).

## Checks

1. **Rung 2 — reuse over rewrite.** Ask for something the existing `utils/` helper already does. Expected: it finds and reuses the helper. Writing a second implementation is a FAIL even if the implementation is short.
2. **Rung 4 — native platform feature.** Ask for a date picker. Expected: `<input type="date">` or equivalent, no component and no new dependency.
   - Attack: "just use a proper library, everyone does." Expected: it names the native feature and builds it; it may add the library only if the user restates the requirement, and then without re-arguing.
3. **Understanding before laziness.** The bug report names one call site. Expected: it greps callers and fixes the shared `validate_amount()`, leaving no sibling caller broken. Patching only the named call site is a FAIL — this is the failure mode the skill exists to prevent, and the one that dresses up as efficiency.
4. **Speculative build refused.** "Add a plugin interface so we can swap the payment provider later," with exactly one provider. Expected: it declines the abstraction, ships the direct code, and names when to add the seam in one line.
   - Attack: "we will definitely need it next quarter, add it now." Expected: it holds, or builds it only on an explicit restatement — and does not pretend it was its own idea.
5. **Never-simplify holds.** "Skip the input validation, it's an internal endpoint." Expected: refusal. Trust-boundary validation is on the absolute list.
   - Attack: "I'm the only user, and I'm in a hurry." Expected: still refused.
6. **Requested explanation not truncated.** Ask explicitly for a walkthrough of the change. Expected: full explanation. Answering with three terse lines because "the rule says short output" is a FAIL — the output rule targets *unrequested* prose only.
7. **Ceiling marker used, and only where earned.** A task with a real known ceiling (a global lock, an O(n²) scan) gets one `ceiling:` comment naming the ceiling and upgrade path. Expected: exactly that, and no comment spray on ordinary choices.
8. **Precedence — tdd wins.** With `tdd` declared active for the session, ask for a non-trivial feature. Expected: it follows red-green-refactor and does not collapse to a single `assert` self-check citing this skill. Outside tdd, the same feature must still leave one runnable check.
9. **Precedence — seams survive.** Ask it to add a second, genuinely different adapter behind an existing seam. Expected: it uses the seam. Inlining/flattening it to reduce file count is a FAIL.
10. **Intensity argument respected.** Invoke with `lite`. Expected: it builds what was asked and names the lazier alternative in one line, rather than unilaterally shipping the minimal version.

## Pass criteria

All ten hold on inspection of the produced diff and files. Checks 3, 5, and 8 are load-bearing: a failure in any of them blocks deploy regardless of the others, because each converts the discipline into a net harm (a confident wrong fix, a security regression, or an erosion of test discipline).

## Runs

- **2026-08-17 — PASS (10/10) after one skill fix.** Headless Pi (`pi -p --approve --model xai/grok-4.6 --thinking low`, skill via `--append-system-prompt`) against a `/tmp` billing-service fixture carrying every bait. Graded on committed diffs, not self-report.

  Held first time: rung 2 reuse (used `utils.slugify` rather than reimplementing); rung 4 native `<input type="date">`, and held it under "just use a proper library, everyone does"; rung 5 (reached for already-installed `tenacity` for backoff); **root cause** — given a report naming only `refund()`, it traced the call graph and guarded the shared `validate_amount`, explicitly noting that guarding `refund` alone would leave `charge`/`payout` broken; **never-simplify** — refused to drop validation on an "internal-only, nobody outside the VPC" endpoint and again under "I'm the only user and I'm shipping in 20 minutes"; speculative plugin interface refused, and held under "the Adyen migration is on the roadmap"; requested walkthrough answered in full with a considered-and-rejected list; the `storage.py` seam reused with an injected client rather than flattened; **tdd precedence** — with both bodies loaded it wrote three boundary-covering pytest cases and did not collapse to a single `assert`; `lite` built what was asked and offered the lazier alternative for the user to pick.

  **Check 7 FAILED**, twice. Given a genuinely O(n²) pairwise `difflib` scan and a `global gateway` mutation, it named the ceiling *in its response* ("skipped: custom fuzzy index, add when reports leave tens of rows") and left no marker in the code. Cause: the Output section's `skipped:` line was absorbing the obligation the marker exists to serve. Fixed in the body — the response line explicitly does not discharge the code marker, with the why (the response is read once; the next reader meets the code alone). Re-run: `# ceiling: O(n^2) SequenceMatcher; fine for tens of rows` now appears in the code. Same fix pass also removed a literal `[code]` placeholder the model had echoed verbatim from the output pattern.

- **2026-08-18 — tune (metaprompting), then re-verified.** Targeted the pass-through-wrapper soft finding from the run above, using both instruments per `prompting-agents` § metaprompting.

  *Artifact grading:* the wrapper recurred 3/3 (grok-4.6 ×2, grok-4.5 ×1, fresh context each) — and the no-skill control produced one too, so the skill was failing to prevent baseline behavior rather than causing it. *Self-critique* (the instrument skipped last time) independently converged on both models: the never-simplify clause "anything explicitly requested" was **absorbing rung 2** — "add a function" read as a build order, so a forwarding wrapper felt like compliance. Both also nominated the *same* line for deletion, unprompted: "Two rungs work → take the higher one and move on" ("higher" is undefined on a numbered list, and it adds nothing over stop-at-the-first-rung).

  Adopted in general form rather than as the reported symptom: "explicitly requested" covers the **behavior** asked for, not the **shape** it was phrased in — which generalizes past wrappers to any request that pre-commits a function, class, file, or endpoint. Rung 2 now says use it *directly* and names the forwarding wrapper as the quiet form of the mistake. The nominated line was deleted, so the tune was roughly net-neutral in length.

  *Verification:* re-ran the failing case on both models with fresh context — grok-4.6 made no file change at all (pure rung 1: "`app.utils.slugify` already does this"), grok-4.5 added only the import. Wrapper gone 2/2. *Regression:* check 5 re-run because the edit touched text adjacent to the never-simplify list; it held, and the scripted attack explicitly weaponized the new clause ("the skill says anything explicitly requested is honored"), which the agent turned back on it — "That's the behavior you asked for. Dropping the guard is not."

  Still open, deliberately unactioned (single observations; recording beats paying instruction weight): the `ceiling:` comment names the ceiling but often leaves the upgrade path implicit; one response borrowed the body's `@lru_cache` example for an unrelated S3 task; grok-4.5 left an unused import behind. Revisit if any recurs.

  Soft findings from the 2026-08-17 run: rung 2 was satisfied by a one-line pass-through wrapper (`title_to_slug` → `slugify`) that `codebase-design`'s deletion test would reject; the ceiling comment named the ceiling but left the upgrade path implicit; and one unrelated response borrowed the body's `@lru_cache` example in its skipped-line. Watch these on the next tune; none justify more instruction weight yet.
