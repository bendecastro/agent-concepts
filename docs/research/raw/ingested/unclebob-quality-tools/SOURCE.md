# Source: Robert C. Martin's 2026 quality-tool cluster

- **What:** Citation record for the sources behind two rules — "complexity
  scores are not a quality bar" in `code-review`, and "acceptance evidence must
  discriminate" in `bc-drain-issues`. Read 2026-08-20 from the GitHub API and
  `raw.githubusercontent.com`; nothing was cloned or vendored.
- **License:** the tool repositories carry
  `Copyright (c) Robert C. Martin. All rights reserved.` — **no open licence**.
  Bodies are therefore cited, never redistributed. The concept reimplements
  ideas, not code.

## Primary sources

- [unclebob/negative-test-experiment](https://github.com/unclebob/negative-test-experiment)
  — **the load-bearing evidence.** Eight independent Hunt the Wumpus runs:
  four testing disciplines (three-laws TDD, test-last, bundling, none) crossed
  with a forced CRAP < 4 pass, then mutation against each frozen tree. Read
  `experiment-abstract.txt`, `experiment-conclusion.md`, `experiment-summary.md`
  in full. Findings used: all eight passed the same 25 acceptance cases
  including the zero-unit-test run; CRAP-on raised coverage on every row,
  raised design on none, and scored 1–2 of 5 on cleanliness on every row;
  mutation produced operator tests and "never a different Wumpus"; coverage sat
  at 97–99% across three very different disciplines.
- [unclebob/Acceptance-Pipeline-Specification](https://github.com/unclebob/Acceptance-Pipeline-Specification)
  — the acceptance-mutation design. Gherkin → JSON IR → generated entrypoints →
  runner adapter, plus a mutator that changes **example values in the IR** to
  check whether the acceptance tests actually depend on them. Deliberately
  language- and project-neutral. Also carries an IR-DRY checker for repeated,
  near-duplicate, and synonym step text.
- [unclebob/mutate4go](https://github.com/unclebob/mutate4go),
  [unclebob/clj-mutate](https://github.com/unclebob/clj-mutate),
  [unclebob/mutate4java](https://github.com/unclebob/mutate4java)
  — mutation testing with **embedded differential manifests**: a footer written
  into the source file holding a per-declaration hash, so a rerun mutates only
  changed scopes. Also the source of the isolated-worker-directory design and
  the coverage pre-filter. `mutate4go` and `clj-mutate` ship `SKILL.md` files.
- [unclebob/crap4clj](https://github.com/unclebob/crap4clj),
  [unclebob/crap4go](https://github.com/unclebob/crap4go),
  [unclebob/crap4java](https://github.com/unclebob/crap4java)
  — `CRAP = CC² × (1 − coverage)³ + CC`. `crap4clj` and `crap4go` ship
  `SKILL.md`. Note the thresholds disagree with each other and with the
  experiment: `crap4java` exits non-zero above 8.0, the experiment gated at 4.
- [unclebob/swarm-forge](https://github.com/unclebob/swarm-forge)
  — tmux + git-worktree agent orchestration. Read
  `swarmforge/constitution/articles/{engineering,workflow,handoffs}.prompt`.
  Used for the article structure and the tool-invocation rules; the role packs
  (two/four/six-pack) were read and not adopted.

## Supporting sources

- [unclebob/scrap](https://github.com/unclebob/scrap) — CRAP's counterpart for
  *test* code: structural complexity, weak-spec smells, fuzzy duplication.
  Its README states the output is "recommendations, not directives" aimed at an
  AI assistant.
- [unclebob/speclj-structure-check](https://github.com/unclebob/speclj-structure-check)
  — catches spec nesting the test framework silently ignores.
- [unclebob/dry4java](https://github.com/unclebob/dry4java),
  `dry4clj`, `dry4go` — structural duplicate detection by normalized-AST
  fingerprints compared with Jaccard similarity.
- CPython `importlib._bootstrap_external._validate_timestamp_pyc` — read from
  the local stdlib 2026-08-20. Confirms bytecode invalidation keys on
  `(source_mtime & 0xFFFFFFFF, source_size & 0xFFFFFFFF)`, which is the
  mechanism behind the false-survivor rule in the concept body.

## Why filed

The `code-review` rule inverts the obvious reading of these tools — it refuses
to gate on a complexity score — and that refusal rests entirely on the
experiment's grid. A rule that contradicts its own source needs the source on
file.

Two standalone concepts were built from this material and both were removed the
same day: `quality-signals` (2026-08-20, commit `25c62a1`), narrowed to
`acceptance-mutation` (commit `63e51de`), then removed entirely. The reason is
recorded in `log.md`: the user's repositories contain zero feature files and
zero BDD runners, and the bc pipeline's specs are prose acceptance criteria that
no generated test consumes, so the check had no artifact to run against. What
survived is the transposition of the idea onto acceptance-matrix evidence.

## Deliberately not filed

- Tool source code and `SKILL.md` bodies: all rights reserved upstream.
- The SwarmForge role packs (`two-pack`/`four-pack`/`six-pack` branches) and the
  handoff daemon: they encode a tmux/worktree topology this workspace already
  solves with `dispatching-parallel-agents` and `bc-swarm`.
- The Clean Code teaching repositories (`fitnesse`, `videostore`, `spacewar`,
  and the rest of the 94): teaching material, not agent scaffolding.
- Local throwaway prototypes (a Python port of all three signals, written
  2026-08-20 to test the mechanisms) were **not retained**. Findings that
  survived into the concept are recorded in `CONCEPT.md`; the durable authority
  for the bytecode-cache rule is the CPython source above, not that run.
