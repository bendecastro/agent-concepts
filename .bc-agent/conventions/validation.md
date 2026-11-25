# Validation

Run from the repository root. `bc-pipeline-to-done` reads this page to know what "validated" means.
Each stage has one owner.

## While working

Owner: the worker, job or reviewer. Run targeted checks only: typecheck, lint, and the unit
tests affected by the change (name the test files or IDs). Budget: 60 s. Workers, jobs and
reviewers run no browser or e2e tests and not the full gate.
Why: each full run costs minutes and parallel workers multiply it; the full gate runs once on
the integrated tree.

```sh
python3 scripts/lint.py
python3 -m pytest -q <the affected test files>   # or the machine's guarded pytest runner
```

## Full gate

Owner: the session that integrates changes. `scripts/gate` holds every step (install,
typecheck, lint, all tests including every browser/e2e test, build) and runs them directly,
so CI runs the same file on a clean checkout. Start it in the background with a wake, through
the machine's offload wrapper if its agent instructions name one. Budget 300 s, measured, not enforced:
pass it to the wrapper's budget option if available; otherwise time the run. Never wrap the gate in `timeout`:
an over-budget run must finish and count toward the two-in-a-row rule.

```sh
scripts/gate
```

- Run it once per integrated tree and record the tree SHA (`git rev-parse HEAD^{tree}`) and
  the result in the work item's evidence. A parallel reviewer reports the gate as pending
  instead of rerunning it; the parent combines the gate result with the review verdict before landing.
  Why: the same tree gives the same result; a second run only adds minutes.
- Run one full gate at a time on a host; queue the others (an offload wrapper may do this).
  Why: two gates on one host slow each other and the owner's machine.
- For a flaky failure, rerun only the failing tests, never the whole gate in a loop.
- Budget: 5 minutes on the host that runs it. After two over-budget runs in a row, open a work item
  to make the gate fast again before more feature work.
  Why: an unmeasured gate only grows, and every later change pays for it.

## Release

Owner: the session cutting a release. None yet: concepts deploy through symlinks, and
`scripts/portability-check.py` (inside the gate) covers the fresh-clone install path.

## Baseline checks

```sh
git status --short
```

- Do not claim build/test/runtime validation was run unless it actually ran.
- Add newly discovered canonical commands here and to `../references/commands.md`.

## Test levels

The `tdd` skill defines these levels.

- Level 1: unit (example-based) tests — on.
- Level 2: property-based tests — required for logic with a statable rule. They run inside the
  project's test command, with no separate gate. Library: Hypothesis (installed by the CI
  workflow).
  Keep the local failure cache out of version control (Hypothesis already writes its own
  `.gitignore` inside `.hypothesis/`; add any other library's cache to `.gitignore`) and list
  it as Syncthing-ignored machine-local state.
- Level 3: off

<!-- Only the owner turns Level 3 (formal verification) on, one line per component: -->
<!-- Level 3: on — <component path> — <tool> <pinned version> — spec: <spec file> — command: <proof command> -->
<!-- A refused Level 3 suggestion is recorded so agents stop re-suggesting it: -->
<!-- Level 3 declined: <component>, <YYYY-MM-DD>, <reason> -->
