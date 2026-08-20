---
name: acceptance-mutation
description: Check whether an acceptance suite actually depends on its specification, by mutating the example values in the spec and seeing whether anything fails. Use when writing or reviewing Gherkin/BDD/acceptance/feature tests, when deciding how a spec becomes executable tests, when acceptance tests are green but confidence is low, or when asked whether a feature suite means anything.
---

# Acceptance mutation

In an eight-run controlled experiment, the same product was built four
different ways — including once with **no unit tests at all** — and every run
passed the same 25 acceptance cases. The programs were not the same: they
differed in module structure, in hazard-check order, in whether IO was
injected, even in random-number generator. Acceptance testing distinguished
none of it.

So a green acceptance suite is compatible with almost anything. The question
worth answering is narrower and checkable: **does the suite actually depend on
what the specification says?**

## The precondition, decided before any tests exist

Acceptance mutation only works if the executable tests **read** the
specification at run time. The usual shape:

```
feature file → parser → IR → generated entrypoints → runner adapter → step handlers
```

The IR is the seam. Because the tests consume it, changing a value in the spec
changes what the tests assert.

If instead someone transcribed the scenario into hand-written test code, the
spec and the tests can drift arbitrarily far apart and nothing will ever report
it. The document becomes commentary sitting next to unrelated code.

You do not need any tooling to check which situation you are in. Ask: **if I
changed one number in this scenario, what would fail?** If you cannot name a
mechanism, you do not have executable specification.

This is cheap to decide while designing the acceptance layer and a real
refactor afterwards. Raise it at design time, and say plainly that adding the
indirection later is a project, not a chore.

## The check

Mutate one example value in the spec, re-run the acceptance suite, restore.
Numbers `+1`, booleans flipped, strings replaced with a sentinel.

- **Killed** — the suite fails. The scenario genuinely depends on that value.
- **Survived** — the suite still passes. The spec names a value the application
  is never actually checked against.

Cost is one acceptance run per example value, so size the run before starting
it and scope it to changed feature files rather than the whole suite.

## Reading survivors

A survivor is a **specification** defect. Name which of three kinds it is
before touching anything:

1. **Setup value nothing observes.** The scenario establishes a fact no
   assertion depends on. Usually the step is noise and the scenario is weaker
   than it looks.
2. **A value the application silently corrects or ignores.** Often a real
   defect in the application, not the spec. Observed case: a scenario asserting
   "the player shoots into room 2" passed for *every* room, because the code
   quietly redirected any invalid target to the first neighbour. The unit suite
   was green and every source mutant was killed; only this check saw it.
3. **Assertions too weak to distinguish the case the scenario claims to
   cover.** The scenario names a situation and then checks something that would
   hold in the opposite situation too.

Kind 2 is the reason to run this at all, and it is the one most easily
mistaken for kinds 1 or 3.

## Never

- **Never clear a survivor by tightening an assertion until the mutant fails.**
  It is the fastest way to a green report and it destroys the finding —
  a kind 2 survivor is an application defect, and strengthening the test
  converts a bug report into a test detail. Classify first, then fix the thing
  that is actually wrong.
- **Never delete the value, the step, or the scenario to make a survivor go
  away.** A scenario that no longer says anything cannot have anything survive.
  If a step really is noise, removing it is a legitimate fix — but say that it
  was noise and that the scenario is now narrower than it appeared.

## What this does not do

It cannot see an untested branch, a boundary condition, or a behavior no
scenario mentions. It tells you whether the scenarios you have are connected to
anything, not whether you have the right scenarios. Source mutation covers the
other question, at meaningfully higher cost — see
[implementations.md](implementations.md).

It says nothing about design. In the experiment above, acceptance results were
identical across four genuinely different architectures.
