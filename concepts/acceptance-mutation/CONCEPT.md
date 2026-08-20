# Concept: acceptance-mutation

Model-invoked discipline for one question: does an acceptance suite actually
depend on its specification? Mutate the example values in the spec, re-run, and
read the survivors. Carries the design-time precondition that makes the check
possible at all — generated tests must consume the specification rather than
transcribe it. Adapted from Robert C. Martin's Acceptance Pipeline
Specification, with the motivating evidence from his `negative-test-experiment`
grid.

## Design decisions

- **Narrowed from a three-signal concept on the day it was written.** The first
  version (`quality-signals`, commit `25c62a1`) covered CRAP, source mutation,
  and acceptance mutation under an authority table. Two of the three did not
  earn their place here: CRAP tooling exists only for Clojure/Go/Java, and
  source mutation's first instruction to any reader was "build or evaluate a
  mutation harness" — a skill whose opening move is a project has a low chance
  of ever being acted on. The authority table existed mainly to hold three
  things together and evaporated with them. Narrowing cost one rewrite because
  nothing had been deployed or pressure-tested yet.
- **The precondition outranks the check.** The mutation is mechanical; the
  decision that generated tests read the spec is architectural, free at design
  time and a refactor afterwards. So the body leads with it and gives a
  tooling-free version — *if I changed one number in this scenario, what would
  fail?* Most readers will never run a mutator, and that question alone
  separates executable specification from documentation filed next to code.
- **Survivors are classified before they are fixed, in three named kinds.**
  Without the taxonomy the reflex is to tighten an assertion until the report
  goes green, which is fastest and destroys the finding. Kind 2 — a value the
  application silently corrects or ignores — is the reason to run the check and
  is the one most easily mistaken for the other two.
- **The kind 2 example is the local prototype finding**, kept because it is
  concrete and because it demonstrates the boundary against source mutation: a
  scenario asserting a specific room passed for every room, with a green unit
  suite and every source mutant killed. One observation, not validation.
- **Two `## Never` rules, both about clearing the report rather than fixing the
  defect.** Written as a gate block from the start; `unslop` and `codebase-docs`
  both failed their first pressure runs because rules stated inside topic
  sections lost to a direct user instruction. The deletion rule deliberately
  admits the legitimate case (the step really was noise) and requires saying so,
  because a flat prohibition would be wrong and therefore ignored.
- **The experiment is used for one claim only.** That all eight runs passed the
  same 25 acceptance cases, including the one with zero unit tests, and that
  acceptance results were identical across four different architectures. That is
  what justifies distrusting a green acceptance suite. The grid's design and
  cleanliness ratings are subjective and single-author, and nothing here rests
  on them.
- **The complexity-threshold rule moved to `code-review`.** It was the most
  broadly applicable thing in the first version — generalized past CRAP it
  covers `ruff C901`, ESLint `complexity`, and Sonar gates — but it fires when
  someone proposes or reviews a gate, which is `code-review`'s moment, not this
  one. One rule, one home.
- **The source-mutation harness lessons were demoted, not deleted.** Differential
  manifests, coverage pre-filtering, defeating the compilation cache, and the
  run-twice integrity check now sit in `body/implementations.md` under an
  explicit "if you later add source mutation" heading. They cost nothing to
  carry, are expensive to rediscover, and load only when someone goes looking.
- **The gap is stated rather than covered.** Source mutation genuinely finds
  things this cannot — untested branches above all. The body says so plainly.
  A known uncovered gap beats a skill instructing the reader to build tooling.
- **Named for the check, not the property.** `spec-connectedness` describes the
  thesis better, but the description does the work of firing and it carries both
  moments (writing/reviewing Gherkin, and designing the acceptance layer);
  a concrete searchable name beats an abstract accurate one.

## Provenance

Full citation record, licence position, and what was deliberately not filed:
[`raw/ingested/unclebob-quality-tools/`](../../raw/ingested/unclebob-quality-tools/SOURCE.md).

- [unclebob/Acceptance-Pipeline-Specification](https://github.com/unclebob/Acceptance-Pipeline-Specification)
  — the primary source. The pipeline shape (feature → parser → IR → generated
  entrypoints → runner adapter → step handlers), acceptance mutation as
  example-value mutation of the IR rather than source mutation, the runner
  adapter's supplied-IR contract, the test/infrastructure exit-code split, and
  the IR-DRY checker. Read 2026-08-20.
- [unclebob/negative-test-experiment](https://github.com/unclebob/negative-test-experiment)
  — the evidence that a green acceptance suite distinguishes almost nothing.
  Read in full 2026-08-20.
- [unclebob/mutate4go](https://github.com/unclebob/mutate4go),
  [clj-mutate](https://github.com/unclebob/clj-mutate),
  [mutate4java](https://github.com/unclebob/mutate4java)
  — the differential-manifest and isolated-worker designs behind the demoted
  source-mutation section.
- CPython `importlib._bootstrap_external._validate_timestamp_pyc` — read from
  the local stdlib 2026-08-20; the authority for the stale-bytecode warning in
  `implementations.md`.
- Local throwaway prototype (Python implementation of the pipeline and the
  mutator, 2026-08-20, **not retained**) — source of the kind 2 example and of
  the compilation-cache failure. One observation each.
- `concepts/prompting-agents/body/SKILL.md` — altitude, explain-the-why, gates
  reserved for rationalization failure modes.

**Considered and not adopted:** CRAP and any complexity threshold (the rule
against it lives in `code-review`); source mutation as a first-class signal;
SwarmForge's role packs and handoff daemon (overlap `dispatching-parallel-agents`
and `bc-swarm`); `scrap`, `dry4*`, and `speclj-structure-check`.

## Tests

`tests/pressure-acceptance-mutation.md` — six checks, two load-bearing (the
`## Never` rules). **Not yet run; deploy is blocked on it.**

## Deploy targets

**Not deployed.** The test gate applies: two gates and a design-time
precondition, none held under pressure yet. When it passes, deploy via
`scripts/deploy-local-skills.py` to the shared bus, Pi, and Claude Code.
