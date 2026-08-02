# Natural ecological-pressure runner prompt

This prompt preserves the autonomous contested A/B as ecological evidence. It is **not** the
deterministic deployment Gate B; use `../contested-gate-b-trace/AGENT-PROMPT.md` for that gate.

Hand the block below to the agent that will run this natural pressure test. It assumes that agent
has a shell, can run `bc-drain-issues`, and can report per-child token usage. Replace nothing
except the two bracketed values in step 0 if your harness differs.

---

You are running the **natural ecological-pressure A/B** for `bc-drain-issues`: an autonomous
measurement of whether the v3 review-economy revision costs fewer child tokens on a naturally
contested issue without losing correctness. This run cannot authorize deployment because its
rework topology is probabilistic. This is a measurement, not a feature task. Produce trustworthy
results, including invalid topology or numbers that make v3 look bad.

## 0. Setup

- Canon workspace: `$AGENT_CONCEPTS`
- Fixture generator: `$AGENT_CONCEPTS/concepts/bc-drain-issues/tests/fixtures/contested-gate-b/make-fixture.py`
- Read `<that dir>/README.md` first — it describes the fixture, the isolation guarantees, its
  residual risks, and the pass criteria. Read `../../pressure-drain.md` for the inherited v2
  Gate B outcomes.
- Model and effort: use **one model family and one explicit effort setting for both arms**
  (v2's Gate B used `openai-codex/gpt-5.6-sol` at medium). Never let one arm inherit a different
  effort. Record exactly what you used.

## 1. Build two identical sandboxes

```sh
python3 make-fixture.py   # once per arm; note each printed root
```

Confirm both roots have the same `base_sha` in `FIXTURE.json`. For each arm, `. <root>/env.sh`
before doing anything else, and verify `command -v gh git publish-check.py` all resolve inside
`<root>/stubs`. If they do not, stop — the isolation is void.

## 2. Pin the two arms

- **v2 arm:** `cd "$AGENT_CONCEPTS" && git worktree add --detach /tmp/gateb-v2 745fe01`, then run the
  drain against `/tmp/gateb-v2/agents/concepts/bc-drain-issues/body/`.
- **v3 arm:** run against `$AGENT_CONCEPTS/concepts/bc-drain-issues/body/`.

Before spending tokens, prove the arms differ:
`grep -c 'do not re-derive it' <arm>/review-contract.md` must be `0` for v2 and `1` for v3.

## 3. Run each arm

Run `bc-drain-issues` against the fixture repo (`<root>/repo`) with the canon for that arm. The
queue holds #102 (the contested slice) and #103 (which depends on it). Let the drain do its own
thing — do **not** coach the workers, hint at the omitted `reload`/`apply-change` commands, or
correct a reviewer. Coaching invalidates the measurement.

Never edit `agents/policies/`. Never push anything anywhere real.

## 4. Capture per arm

- Child tokens **per child**, summed once per unique child session, split by phase: audit, build,
  each review (record which axes ran in each round), each rework, re-review. Exclude parent
  tokens; report them separately if available.
- Number of rework rounds, and for each round which axes were dispatched and which held a
  standing approval without re-review (v3 arm).
- Review tier chosen per issue and any escalation (v3 arm).
- Full-suite invocation count and where each occurred.
- Final state of each issue, the landed diff, and whether both hidden commands survived.
- `<root>/commands.log`: every `push`/`gh`/`publish-check` attempt, and proof each hit a stub.
- Cost, if your harness reports it.

## 5. Judge honestly

Report a **valid ecological comparison** only if every criterion in the fixture README holds,
including:

- at least two rework rounds actually occurred (otherwise record the run as invalid ecological
  evidence, say so, stop, and do not treat it as deployment Gate B);
- both axes hold a standing approval bound to the exact landed diff hash;
- an axis whose trigger did not fire was not re-dispatched;
- `reload` and `apply-change` still work;
- restart-policy claims cite `primary-docs/`, not `docs/README.md`;
- `tests/test_known_flaky.sh` still fails and nothing else regressed;
- v3 total child tokens < v2 total child tokens.

If v3 is not cheaper, or is cheaper but broke something, **report that plainly**. A negative
result is the point of running the gate — v3's levers were reasoned from a single clean
measurement and a contested run is exactly the evidence that could overturn them. Do not adjust
the fixture, the caps, or the criteria to produce a pass.

## 6. Write the result

Create `$AGENT_CONCEPTS/concepts/bc-drain-issues/tests/results/<YYYY-MM-DD>-gate-b-contested.md`
following the shape of `2026-07-25-gate-b.md`: locked comparison table (fixture base, model,
effort, per-arm totals, delta), per-phase breakdown, correctness section, and a measurement-notes
section recording limitations. Add machine totals as a sibling `.json`. Then update
`tests/pressure-drain.md` (the Gate B status line) and `CONCEPT.md` (the Tests section) with the
measured numbers, append an `AGENTS.md`-style entry to `agents/log.md`, and commit. Push only if
`agents/scripts/publish-check.py` authorizes it.

State clearly that deployment remains governed by the deterministic trace Gate B, regardless of
this ecological result.
