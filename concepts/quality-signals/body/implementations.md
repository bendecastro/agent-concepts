# Implementations

Load this only when you need to actually run a signal in a specific project.
The discipline in `SKILL.md` is language-neutral; tooling is not, and the
reference implementations cover three languages.

## Verified 2026-08-20

Read from the repositories directly. All carry
`Copyright (c) Robert C. Martin. All rights reserved.` — **no open licence**.
Usable as tools; do not vendor or copy their code.

| Signal | Clojure | Go | Java |
|---|---|---|---|
| CRAP | `unclebob/crap4clj` † | `unclebob/crap4go` † | `unclebob/crap4java` |
| Source mutation | `unclebob/clj-mutate` † | `unclebob/mutate4go` † | `unclebob/mutate4java` |
| Duplication | `unclebob/dry4clj` | `unclebob/dry4go` | `unclebob/dry4java` |

† ships an agent `SKILL.md` in the repository.

All three mutation tools implement the differential manifest, coverage
pre-filtering, isolated parallel workers, and a `--scan` mode that reports
mutation-site counts without running tests. Use `--scan` to size a run before
committing to it.

Acceptance mutation: `unclebob/Acceptance-Pipeline-Specification` — the spec is
language- and project-neutral and is the part worth reading. It supplies a
Gherkin parser, an IR-DRY checker, and the mutator as Babashka tasks with Go
fallbacks; the entrypoint generator, runtime, step handlers, and runner adapter
are project-specific and must be written per project.

Test-code quality: `unclebob/scrap` (Clojure/Speclj) scores *test* structural
complexity, weak-spec smells, and fuzzy duplication. Its output is explicitly
advisory — same authority as CRAP, for the same reason.

## Other ecosystems

Mature mutation testing exists outside these three languages — Stryker
(JavaScript/TypeScript, C#, Scala), PIT (JVM), mutmut and cosmic-ray (Python)
are the usual names. **Not verified here**; check the current state before
recommending one. What to check against, in priority order:

1. Does it support **incremental/differential** runs? Without this it is a
   nightly job, not a loop signal.
2. Does it **filter by coverage** before executing mutants?
3. Does it **isolate** parallel workers, and is a repeat run byte-identical?
4. Can it run **one file at a time** with a machine-readable report?

If nothing in the ecosystem clears (1), the honest move is to say so and use
mutation as an occasional audit rather than a gate.

Acceptance mutation has no off-the-shelf implementation in most ecosystems. It
is cheap to build against an existing Gherkin runner **only if** the generated
tests already read the spec at runtime. If the project transcribes scenarios
into hand-written test code, that indirection has to come first, and that is a
real refactor — say so before promising the signal.
