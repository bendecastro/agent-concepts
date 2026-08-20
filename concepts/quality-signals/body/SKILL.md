---
name: quality-signals
description: Decide whether a test suite and a specification are actually worth anything, using three signals with deliberately unequal authority — CRAP ranks where to look, source mutation gates the unit suite, acceptance mutation gates the spec. Use when tests are green but confidence is low, when choosing or defending a quality gate, when asked whether coverage or complexity numbers are good enough, or when adding mutation testing to a project.
---

# Quality signals

A green suite is not evidence. In an eight-run controlled grid, four testing
disciplines — including one that wrote **no unit tests at all** — every one
passed the same 25 acceptance cases. Three of the four sat at 97–99% line
coverage with wildly different suites underneath. Coverage and a passing build
tell you the code runs. They do not tell you the tests would notice if it were
wrong, or that the specification describes the thing being built.

Three signals answer those questions. They do **not** have equal authority, and
collapsing them is the main way teams get this wrong.

| Signal | Question | Authority |
|---|---|---|
| **CRAP** `CC² × (1−cov)³ + CC` | Which function is riskiest to change? | **Advisory.** Ranks targets. Never pass/fail. |
| **Source mutation** | Would the unit suite notice if behavior changed? | **Gate.** A survivor is a real hole. |
| **Acceptance mutation** | Does the spec describe anything the app is checked against? | **Gate.** A survivor means decorative spec. |

## Never

These fail by in-the-moment rationalization, which is why they are absolute.

- **Never turn CRAP into a pass/fail threshold**, and never accept one from a
  user or a CI config without saying this first. Forcing every function under a
  CRAP cap raised coverage on every row of the grid, raised design quality on
  **none**, and dropped readability to 1–2 of 5 on **every** row. It does not
  simplify; it multiplies names — one `WHERE TO?` prompt loop became three
  mutually-recursive one-branch functions. If the user insists, comply, but say
  plainly that the number will improve and the code will get worse, and record
  that you said so. The published thresholds do not even agree with each other
  (one tool fails above 8.0, the experiment gated at 4), which is what an
  arbitrary constant looks like.
- **Never hand-edit a mutation manifest** to make a run pass or go faster. The
  manifest is a claim that a function was mutated and nothing survived. Editing
  it forges the evidence the next agent will trust instead of re-deriving.
- **Never write a test whose only purpose is to kill a mutant.** That produces
  operator-assertion suites — tests that pin `if` against `if-not` and specify
  nothing a reader would recognize as the product. A survivor is a *question*
  about behavior. Answer it with a test that names the behavior, or suppress it
  as equivalent with a stated reason.

## Order

1. **Green baseline first.** Mutation or CRAP computed against a red suite is
   noise. If the baseline fails, stop and fix it.
2. **CRAP to choose a target.** Mutation cost scales with mutation sites, so
   run it where the risk is. Read a high score as "read this function", not
   "split this function".
3. **Source mutation on that target.** One file at a time. Survivors are the
   work list.
4. **Acceptance mutation whenever a feature file or step handler changes.**
   That is exactly when a step quietly stops depending on its own example
   value.

The two mutation signals find different things and neither substitutes for the
other. Source mutation cannot see a scenario that passes for the wrong reason;
acceptance mutation cannot see an untested branch.

## Acceptance mutation

Mutate the **example values in the specification**, not the source. Change a
number, flip a boolean, replace a string with a sentinel, then re-run the
acceptance suite.

- **Killed** (suite fails) — the scenario genuinely depends on that value.
- **Survived** (suite still passes) — the spec names a value the application is
  never actually checked against. The scenario is decorative.

This requires the generated tests to **consume the specification** rather than
having its values copy-pasted into hand-written test code. That indirection is
the entire point: if the spec is a source the tests read, mutating the spec
mutates the tests. If the spec is a document someone transcribed, it can drift
arbitrarily far from the suite and nothing will report it.

Survivors are usually one of three things: setup values nothing observes, a
value the application silently corrects or ignores, or a scenario whose
assertions are too weak to distinguish the case it claims to cover. All three
are spec defects, not test defects.

## Cost discipline

A quality signal that is affordable once and never again gets switched off, and
a switched-off gate protects nothing.

- **Make mutation differential by default.** Keep a per-declaration hash
  manifest and mutate only what changed since the last clean run. The proven
  design writes that manifest as a footer *inside the source file*, so it
  travels with the code and survives a clean checkout.
- **Filter mutation sites by coverage before running them.** An uncovered site
  is a coverage gap; running the mutant to discover that wastes a whole test
  cycle.
- **Run one file at a time** and finish it — no uncovered sites and no
  survivors — before starting the next.

## Your harness can lie to you

A mutation harness must defeat the target language's compilation cache, and
must isolate parallel workers so they cannot overwrite each other's mutants.

The failure mode is nasty because it does not look like a broken tool — it
looks like a weak test. A mutant that reuses stale compiled output runs the
*original* code, passes, and is reported as a survivor. Python invalidates
cached bytecode on `(source_mtime_seconds, source_size)`, so a size-preserving
mutation such as `==` → `!=` written within the same second silently reuses the
old bytecode. Results vary run to run from identical inputs.

Before trusting any mutation run, confirm it is deterministic: **run it twice
on unchanged inputs and require identical results.** If the two runs disagree,
the harness is broken, not the suite. Mature implementations avoid the whole
class by copying the module into an isolated per-worker directory.

## What this does not do

- It does not judge design. Nothing here distinguished the four architectures
  in the grid; a human read the trees to do that. Do not report a mutation
  score as evidence of good design.
- It does not replace review or types.
- It is not free. On a codebase with no signals at all, adding acceptance
  mutation first buys the most, because a disconnected spec invalidates every
  downstream claim.

Available implementations per language: [implementations.md](implementations.md).
