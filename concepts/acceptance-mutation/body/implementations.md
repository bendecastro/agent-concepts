# Implementations

Load this when actually building or running the pipeline. The discipline in
`SKILL.md` is language-neutral and the precondition check needs no tooling at
all.

## The reference specification

[unclebob/Acceptance-Pipeline-Specification](https://github.com/unclebob/Acceptance-Pipeline-Specification)
— read the spec even if you build your own. It is deliberately language- and
project-neutral, and it is the only worked design for this that I know of.

It supplies three portable tools (Babashka tasks, with Go fallbacks): a Gherkin
parser producing canonical JSON IR, an **IR-DRY checker** that reports repeated,
near-duplicate, and possible-synonym step text so feature files can be
normalized, and the mutator itself.

Four components are necessarily project-specific and must be written per
project: the entrypoint generator, the acceptance runtime, the step handlers,
and the runner adapter. The runner adapter is the piece that makes mutation
possible — it takes an IR path and reports pass, fail, or infrastructure error,
so the mutator can feed it a modified IR without regenerating anything.

Licence note: `Copyright (c) Robert C. Martin. All rights reserved.` Usable as
tools; do not vendor or copy the code.

## Building it against an existing runner

Most BDD runners (Cucumber and its ports) already parse feature files into an
internal AST, but few expose it as a stable artifact you can modify and feed
back. Before promising this signal, check whether the runner can execute from a
**supplied** parsed representation rather than from the `.feature` file on disk.

If it cannot, the cheapest honest version is to mutate the feature file itself
on a scratch copy and point the runner at that. Cruder, but it answers the same
question, and it needs no pipeline.

Exit-code discipline for whatever runner you use: distinguish *test failed*
from *infrastructure error*. A mutator that treats a crashed run as a kill
reports false confidence.

## If you later add source mutation

Not needed for anything above. Recorded because these were the non-obvious,
expensive-to-rediscover parts, and none of it is in the usual tutorials.

- **Differential runs or nothing.** Keep a per-declaration hash manifest and
  mutate only what changed since the last clean run; the proven design writes
  it as a footer inside the source file so it survives a fresh checkout. Without
  this, mutation is a nightly job rather than a loop signal, and a signal too
  slow to run gets switched off. Reference implementations:
  `unclebob/mutate4go`, `unclebob/clj-mutate`, `unclebob/mutate4java` (Go,
  Clojure, Java only).
- **Filter sites by coverage first.** An uncovered site is a coverage gap;
  running the mutant to discover that wastes a full test cycle.
- **Defeat the compilation cache, and isolate parallel workers.** A mutant that
  reuses stale compiled output runs the *original* code, passes, and is reported
  as a survivor — it presents as a weak test rather than a broken tool, so the
  investigation goes to the wrong place. Python invalidates cached bytecode on
  `(source_mtime_seconds, source_size)`, so a size-preserving mutation such as
  `==` → `!=` written within the same second silently reuses the old bytecode.
  Verified in CPython's `importlib._bootstrap_external._validate_timestamp_pyc`.
- **Require two identical runs.** Cheapest possible integrity check: run the
  mutator twice on unchanged inputs. If the results differ, the harness is
  broken, not the suite.
- **Never gate on a complexity metric.** See `code-review`, which owns this
  rule.
