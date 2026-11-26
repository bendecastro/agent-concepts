# Property-based tests (Level 2)

Load this when a change touches logic with a statable rule. The RED/GREEN rules in [SKILL.md](SKILL.md) still apply; this page adds what is specific to properties.

## When a property is required

**Required** when the change touches logic whose correct behaviour can be stated as a rule over many inputs:

- parsers and formatters (round-trip: `parse(format(x)) == x`);
- data transforms (invariants preserved: count, set of keys, total);
- calculations (bounds, monotonicity, agreement with a simple reference implementation);
- sorting and filtering (output ordered, a permutation or subset of the input, every kept item matches the predicate);
- state transitions (no sequence of valid operations reaches an invalid state).

**Optional** for glue, UI, I/O wiring and configuration. Example-based tests (Level 1) cover those.

If you skip a property on rule-bearing logic, name the rule you could not state. "The examples already pass" is not a reason. Why: examples cover the inputs you thought of; a property searches for the ones you did not.

## Libraries

| Language | Library | Run by |
|---|---|---|
| Python | Hypothesis | the project's pytest command through its guarded runner when configured; otherwise plain `pytest` with `tmp_path` for fixtures, cleanup even on failure, and no custom `--basetemp` |
| JS/TS | fast-check | the project's test command (for example `pnpm test`) |
| Rust | proptest | `cargo test` |

Properties live in the project's normal suite and run under its existing command; there is no separate gate. Add the library as a dev dependency the first time a project needs it, and add a property-test line to that project's `validation.md` in the same change.

**Shell is out of scope.** If shell code carries a statable rule, move that logic into Python and test it there.

Use the library's default example count. Do not raise it to look thorough or lower it to save time.

## Writing a good property

- State the rule from the spec, not from the implementation. A property that recomputes the expected value with the code under test is tautological, like any other [test that lies](SKILL.md#tests-that-lie).
- Generate the realistic input domain, including edge cases the spec allows (empty, unicode, duplicates, boundary numbers). Filter (`assume`) sparingly; a property that rejects most inputs tests little.
- One rule per property, named for the rule (`test_parse_inverts_format`).

## Fail-first for properties

A property must be seen failing for the rule it states.

- **New logic:** write the property first and watch it fail, as with any RED.
- **Code that already works:** plant a bug that breaks the stated rule (a mutation, for example dropping the last element or flipping a comparison), watch the property catch it, then revert. Use a disposable copy, as for other tests written after the code.
- **Record the evidence** where you already report validation: the mutation, the failing property and its shrunk counterexample, and the green run after revert. Under `bc-pipeline-to-done` that is `validation.json`; otherwise your report. Do not create a new evidence file.

## Pin every failure you find

When a property finds a real failure, pin its shrunk input as an explicit example so it runs every time, independent of any local cache:

- Hypothesis: `@example(...)` on the property;
- fast-check: the `examples` option of `fc.assert`;
- proptest: commit the regression file it writes (`proptest-regressions/`).

Local failure caches (`.hypothesis/` and similar) are machine-local state: never commit them, and list them as Syncthing-ignored. Hypothesis gitignores `.hypothesis/` itself; add other libraries' caches to `.gitignore`.

## Changing an existing property

Never weaken or delete an existing property to make a change pass: narrowing its generator, adding an `assume` that excludes the failing case, loosening the asserted rule, or removing it. A failing property means the code or the spec changed. If the spec really changed, stop and ask the owner; the reviewer treats an unapproved weakening as Critical.
