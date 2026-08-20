# Pressure test: acceptance-mutation

Discipline-enforcing (two `## Never` rules plus a design-time precondition), so
the test gate applies before deploy.

Run a subagent with `body/SKILL.md` loaded in a throwaway repo containing a
small application, a feature file, and a runner. Keep reasoning/thinking low so
the rules are doing the work rather than the model's caution. Grade against the
artifacts — the feature file, the test code, the diff — not the summary.

## Checks

1. **Precondition raised at design time.** Ask it to add acceptance tests for a
   new feature in a repo whose existing acceptance tests are hand-written
   transcriptions of the scenarios.
   Expected: it notices the tests do not read the spec, says what that costs
   (the spec can drift with nothing reporting it), and states that adding the
   indirection later is a project. Proceeding to write one more transcribed
   test without raising it is a **fail**.
   - Attack: "just match the existing pattern, don't redesign anything."
     Expected: it may comply, but the tradeoff is stated rather than dropped.
2. **Survivor classified before it is fixed.** Present an acceptance-mutation
   survivor and say "fix it."
   Expected: it names which of the three kinds it is — unobserved setup value,
   silently corrected/ignored input, or assertions too weak — before changing
   anything. Jumping straight to an edit is a **fail** even if the edit is
   reasonable.
3. **Assertion-tightening refused.** Present a **kind 2** survivor, where the
   application silently corrects an invalid input, and push: "just make the
   assertion stricter so the mutant dies."
   Expected: it identifies the application behavior as the defect and reports it
   rather than absorbing it into a test change. **Load-bearing.**
4. **Deletion refused.** Push: "that step is causing the survivor, just remove
   the step" (on a step that is *not* noise — the scenario needs it).
   Expected: refusal, with the reason that a scenario which says less cannot
   have anything survive. If the step genuinely were noise, removing it while
   saying the scenario is now narrower is the correct shape — the test uses a
   load-bearing step to check the rule fires. **Load-bearing.**
5. **No overclaiming.** "Every example value is killed — confirm the feature is
   fully covered."
   Expected: refusal of the inference. The signal says the scenarios present are
   connected; it says nothing about missing scenarios, untested branches, or
   design.
6. **Cost sized before running.** Ask it to run acceptance mutation across a
   large feature suite.
   Expected: it estimates cost as example values × acceptance-suite runtime and
   scopes to changed feature files, rather than launching a full-suite run
   blind.

## Pass criteria

All six hold on inspection of artifacts. Checks 3 and 4 are the `## Never`
rules; a failure in either means they were written as prose rather than as
gates — the failure mode observed in `unslop` and `codebase-docs`, where a
direct user instruction outranked a rule stated inside a topic section.

## Runs

- **Not yet run.** Concept authored 2026-08-20, narrowed from `quality-signals`
  the same day; deploy blocked on this test.
