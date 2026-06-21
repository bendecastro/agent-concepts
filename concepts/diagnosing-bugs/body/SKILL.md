---
name: diagnosing-bugs
description: Diagnosis loop for hard bugs and performance regressions. Use when the user says diagnose/debug, reports broken/throwing/failing/slow behavior, or an issue is a bug without a tight repro.
---

# Diagnosing Bugs

A discipline for hard bugs and performance regressions. It complements `tdd`: first build a tight red-capable feedback loop for the bug, then fix and regression-test it.

Read `.bc-agent/project/overview.md` or `CONTEXT.md` and relevant ADRs before editing so hypotheses use project vocabulary.

## Phase 1 — Build a feedback loop

This is the skill. If you have a tight pass/fail signal that catches **this exact bug**, the rest is mechanical. If you don't, staring at code only creates vibes.

Try, in roughly this order:

1. Failing test at the highest seam that reaches the bug.
2. Curl/HTTP script against a dev server.
3. CLI invocation with fixture input and expected output diff.
4. Headless browser script asserting DOM/console/network.
5. Replay a captured trace/log/payload.
6. Throwaway harness around the minimal subsystem.
7. Property/fuzz loop for intermittent wrong output.
8. `git bisect run` harness if the bug appeared between known states.
9. Differential loop: old vs new version/config.
10. HITL script only as a last resort.

Tighten the loop: faster, sharper, more deterministic. For flaky bugs, raise reproduction rate with repetition, stress, seeds, and narrowed timing windows.

**Gate:** name one command you have already run that is red-capable, deterministic/high-repro, fast enough, and agent-runnable. No command, no hypothesis phase.

## Phase 2 — Reproduce and minimise

Run the loop and watch it go red. Confirm it matches the user's symptom, then shrink the repro one element at a time. Every remaining element should be load-bearing.

## Phase 3 — Hypothesise

Generate 3–5 ranked falsifiable hypotheses before testing any. Format each as:

> If `<cause>` is true, then `<probe/change>` will make `<prediction>` happen.

Show the ranked list to the user when they are available; proceed with your ranking if AFK.

## Phase 4 — Instrument

Probe one hypothesis at a time. Prefer debugger/REPL, then targeted logs at boundaries. Tag temporary logs with a unique `[DEBUG-xxxx]` prefix so cleanup is mechanical. For performance, measure/profile/bisect before fixing; don't log everything.

## Phase 5 — Fix + regression test

If a correct test seam exists, turn the minimised repro into a failing regression test **before** the fix, then fix and watch it pass. If no correct seam exists, document that finding — it is architecture debt, and after the bug is fixed you should recommend `/improve-codebase-architecture` with the specific missing seam.

## Phase 6 — Cleanup + post-mortem

Before calling it done:

- Original repro no longer reproduces.
- Regression test passes, or no-seam finding is documented.
- All `[DEBUG-...]` instrumentation is removed (`rg '\[DEBUG-'`).
- Throwaway harnesses are deleted or clearly parked.
- Commit/issue comment states the winning hypothesis and validation.

## AFK adaptation inside `/bc-drain-issues`

For bug issues, the issue's Agent Brief/acceptance criteria replaces the interactive user checkpoint. If no red-capable loop can be built from the issue and repo, PARK with exactly what artifact/access/detail is missing.
