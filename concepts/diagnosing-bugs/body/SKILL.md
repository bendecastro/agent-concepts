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

**Pressure refusal (speculation).** User: "it's probably the cache, just fix that" (or any guessed root cause) **before** a red-capable loop exists → refuse to edit production code for that guess. Name/build the loop first; only then rank hypotheses. A plausible story is not evidence.

## Phase 2 — Reproduce and minimise

Run the loop and watch it go red. Confirm it matches the user's symptom, then shrink the repro one element at a time. Every remaining element should be load-bearing.

## Phase 3 — Hypothesise

Generate 3–5 ranked falsifiable hypotheses before testing any. Format each as:

> If `<cause>` is true, then `<probe/change>` will make `<prediction>` happen.

Show the ranked list to the user when they are available; proceed with your ranking if AFK **and** Phase 1's gate already holds.

## Phase 4 — Instrument

Probe one hypothesis at a time. Prefer debugger/REPL, then targeted logs at boundaries. Tag temporary logs with a unique `[DEBUG-xxxx]` prefix so cleanup is mechanical. For performance, measure/profile/bisect before fixing; don't log everything.

## Phase 5 — Fix + regression test

If a correct test seam exists, turn the minimised repro into a failing regression test **before** the fix, then fix and watch it pass. If no correct seam exists, document that finding — it is architecture debt, and after the bug is fixed you should recommend `/improve-codebase-architecture` with the specific missing seam.

## Phase 6 — Cleanup + post-mortem

Before calling it done (hard gate — "done" claims without this are false):

- Original repro no longer reproduces.
- Regression test passes, or no-seam finding is documented.
- **All `[DEBUG-...]` instrumentation is removed**, verified by running `rg '\[DEBUG-'` (or equivalent) on the tree and getting **zero** hits in production/source files you touched. Leaving DEBUG markers committed is a fail even if the bug is fixed.
- Throwaway harnesses are deleted or clearly parked.
- Commit/issue comment states the winning hypothesis and validation.

**Pressure refusal (skip cleanup).** User: "add whatever logging you need" / "just ship the fix" / time pressure → still strip every `[DEBUG-...]` marker and prove it with `rg` before finishing. Temporary instrumentation is not optional cleanup.

## AFK adaptation inside `/bc-drain-issues`

For bug issues, the issue's Agent Brief/acceptance criteria replaces the interactive user checkpoint.

**PARK gate (underspecified AFK bug).** If the issue is essentially a one-liner or lacks a repro (e.g. title/body is only "login broken" with no steps, expected/actual, environment, or failing command), **PARK / needs-info**. List the missing artifact(s): repro steps, expected vs actual, fixture/input, failing test command, logs, version. Do **not**:

- invent a plausible bug and "fix" it,
- expand a vague ticket into a speculative code change,
- treat "Resolve it" / "just fix login" as sufficient acceptance criteria.

No red-capable loop can be honest without a symptom to catch. Speculative green is a lie.

If a red-capable loop *can* be built from the issue + repo (clear AC, failing test path, or reliable repro), proceed through the phases as usual; still finish Phase 6 cleanup.
