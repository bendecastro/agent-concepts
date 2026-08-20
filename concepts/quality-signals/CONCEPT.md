# Concept: quality-signals

Model-invoked discipline for deciding whether a test suite and a specification
are worth anything. Three signals with deliberately unequal authority: CRAP
ranks where to look and never gates, source mutation gates the unit suite, and
acceptance mutation — mutating the *example values in the spec* — gates the
specification. Adapted from Robert C. Martin's 2026 tool cluster, and inverted
against his own experimental evidence on the one point where the tools invite
the wrong reading.

## Design decisions

- **The concept refuses to gate on CRAP, which is the opposite of what the
  tools imply.** `crap4java` exits non-zero above 8.0; the reference workflow
  is "start with the worst function." But the eight-run grid in
  `negative-test-experiment` forced CRAP below 4 across four testing
  disciplines and found it raised coverage on every row, raised design quality
  on **none**, and scored 1–2 of 5 on readability on **every** row. The author's
  own summary: "It does not simplify. It multiplies names." A concept that
  shipped the threshold would be canonizing the failure its source measured.
  CRAP stays as a targeting signal, which is what it is good at.
- **The three signals get different authority, stated as a table.** The single
  most common failure is treating them as interchangeable "code quality"
  numbers and gating on whichever is cheapest to compute. Naming the authority
  per signal, in one table, is cheaper than three separate arguments.
- **Acceptance mutation is ranked first for adoption**, above the better-known
  source mutation. Two reasons. The grid: all eight runs passed the same 25
  acceptance cases, including the run with zero unit tests, so acceptance
  passing is worth nothing until you know the spec is connected. And a local
  check: a prototype of all three signals found a defect that source mutation
  could not see — a `shoot` function silently redirected any non-adjacent
  arrow to the first neighbour, so a scenario naming a specific room passed for
  every room. The unit suite was green and every source mutant was killed.
- **The spec-as-source requirement is stated explicitly.** Acceptance mutation
  only works if generated tests *read* the specification at runtime. If
  scenarios are transcribed into hand-written test code, mutating the spec
  mutates nothing. The body says this and says the indirection is a real
  refactor, because promising the signal without it is the obvious way to waste
  a day.
- **Cost discipline is treated as correctness, not optimization.** A gate too
  slow to run gets switched off, and a switched-off gate protects nothing. The
  differential manifest (per-declaration hashes written as a footer inside the
  source file) is the mechanism that makes mutation a loop signal rather than a
  nightly job. Measured on the local prototype: after editing one function, a
  rerun selected 2 mutants instead of 19.
- **"Your harness can lie to you" is a section, not a footnote.** A mutation
  harness that reuses stale compiled output reports the *original* code passing
  as a survivor — it presents as a weak test, not a broken tool, and the
  investigation goes to the wrong place. Found the hard way while prototyping:
  identical inputs produced 6 then 10 survivors across two runs. Mechanism
  confirmed in the CPython source rather than inferred —
  `importlib._bootstrap_external._validate_timestamp_pyc` invalidates on
  `(source_mtime & 0xFFFFFFFF, source_size & 0xFFFFFFFF)`, so a size-preserving
  mutant written in the same second reuses the old bytecode. The body ships the
  general rule (defeat the compilation cache, isolate workers) plus a cheap
  falsifiable check: run twice, require identical results.
- **Evidence strength is labelled, not smoothed.** The grid is n=1 product,
  single author, with design and cleanliness scored subjectively by that same
  author. It is strong enough to refuse a threshold, and not strong enough to
  claim CRAP-driven refactoring harms design in general. The body says
  "has never been shown to improve design", not "harms design".
- **Language-neutral body, tooling in a loaded reference.** The reference
  implementations cover Clojure, Go, and Java only. Putting them in `SKILL.md`
  would make the concept read as unusable to a TypeScript or Python project,
  when the discipline transfers and only the tools do not.
  `body/implementations.md` carries the tool table plus four criteria for
  judging an unverified tool in another ecosystem.
- **The `## Never` block was used from the start**, rather than stating the
  three rules inside their topic sections. Both `unslop` and `codebase-docs`
  failed their first pressure runs the same way: rules written as prose
  sentences inside topic sections lost to a direct user instruction. All three
  rules here are exactly the "user pushes back in the moment" shape.
- **CRAP's gate carries a comply-with-warning path, not a refusal.** The user
  may legitimately want the threshold. A flat refusal is not useful and would
  be ignored; the requirement is that the warning survives into something
  durable. Same pattern as `unslop`'s agent-facing override.
- **SwarmForge's role packs were read and not adopted.** The orchestration
  layer (specifier → coder → cleaner → architect → hardener → QA, tmux panes,
  worktrees, a handoff daemon) overlaps `dispatching-parallel-agents`,
  `bc-swarm`, and `bc-drain-issues`. What was taken is the article structure
  and the tool-invocation rules; every rule was rewritten to carry its why,
  because SwarmForge's originals are bare imperatives that work when one author
  owns every role prompt.
- **`scrap`, `dry4*`, and `speclj-structure-check` are noted, not built in.**
  Test-code scoring and duplication detection are real signals but they are
  advisory in the same way CRAP is, and adding two more advisory numbers to a
  concept whose thesis is *authority differs per signal* would dilute it. They
  appear in `implementations.md` only.

## Provenance

Full citation record, licence position, and what was deliberately not filed:
[`raw/ingested/unclebob-quality-tools/`](../../raw/ingested/unclebob-quality-tools/SOURCE.md).

- [unclebob/negative-test-experiment](https://github.com/unclebob/negative-test-experiment)
  — the evidence for every claim about what CRAP, coverage, and acceptance
  testing do and do not buy. Read in full 2026-08-20.
- [unclebob/Acceptance-Pipeline-Specification](https://github.com/unclebob/Acceptance-Pipeline-Specification)
  — the acceptance-mutation design and the spec-as-consumed-source requirement.
- [unclebob/mutate4go](https://github.com/unclebob/mutate4go),
  [unclebob/clj-mutate](https://github.com/unclebob/clj-mutate),
  [unclebob/mutate4java](https://github.com/unclebob/mutate4java)
  — embedded differential manifests, coverage pre-filtering, isolated workers,
  `--scan`, one-file-at-a-time workflow.
- [unclebob/crap4clj](https://github.com/unclebob/crap4clj),
  [crap4go](https://github.com/unclebob/crap4go),
  [crap4java](https://github.com/unclebob/crap4java) — the CRAP formula and the
  mutually inconsistent thresholds.
- [unclebob/swarm-forge](https://github.com/unclebob/swarm-forge)
  `swarmforge/constitution/articles/` — article structure and tool-invocation
  rules.
- CPython `importlib._bootstrap_external._validate_timestamp_pyc` — read from
  the local stdlib 2026-08-20; the authority for the stale-bytecode rule.
- Local throwaway prototype (Python port of all three signals, 2026-08-20,
  **not retained**) — source of the differential 19→2 measurement, the
  false-survivor discovery, and the disconnected-scenario finding. Treat these
  as one observation each, not as validation.
- `concepts/prompting-agents/body/SKILL.md` — altitude, explain-the-why, and
  gates reserved for rationalization failure modes.
- `concepts/bc-autoresearch-loop/body/SKILL.md` — the neighbouring metric
  discipline; its "pair every scalar with a correctness check" rule is the same
  instinct applied to performance work.

**Considered and not adopted:** the SwarmForge role packs and handoff daemon
(overlaps existing orchestration concepts); the CRAP threshold in any form;
`scrap`/`dry4*`/`speclj-structure-check` as first-class signals; the Clean Code
teaching repositories.

## Tests

`tests/pressure-quality-signals.md` — eight checks, three of them load-bearing
(the `## Never` rules). **Not yet run; deploy is blocked on it.**

## Deploy targets

**Not deployed.** The test gate applies: this concept enforces three gates and
a determinism requirement, and none of them has held under pressure yet. When
it passes, deploy via `scripts/deploy-local-skills.py` to the shared bus, Pi,
and Claude Code, as with the other model-invoked disciplines.
