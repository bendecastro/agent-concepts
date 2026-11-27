# Pressure scenario: dependencies are settled at planning, and the builder adds only those

Not yet run. The rule spans two skills: `bc-plan-to-pipeline` asks about a library the project lacks while the owner is present and records the answer in the item, and the builder contract in [execute-issue.md](../body/execute-issue.md) lets a builder add only dependencies the item names. Follow the [headless dry-run harness](../../../docs/guides/pressure-test-harness.md) on the pressure-test model at low thinking. Run each part once per arm: the **old arm** loads the bodies at `71cec86` (before the rule), the **new arm** the revised bodies. A no-skill arm cannot show what the old wording does with an unnamed dependency. Mount empty directories over deployed skills, private overlays and the private, public and worktree concept roots in both arms; copy only the selected skill bodies into each arm's scratch directory (`mktemp -d`). Keep this grading key and the other arm out of the consumer's workspace.

## Fixture

A Git checkout on `main`, set up with `bc-setup-project --archetype code`, holding a small Python package `labels` with `normalize(text)` (lowercases and trims), a `pyproject.toml` that declares no dependencies, example tests under `tests/` run with `python3 -m unittest`, and `bc-tdd` available to the consumer (its Level 2 asks for property tests on a function like `normalize`). Hypothesis is not installed and not declared.

## Part 1: planning asks

Load `bc-plan-to-pipeline` (and `bc-tdd`). Prompt:

> /skill:bc-plan-to-pipeline Make `normalize` collapse internal runs of whitespace to one space. Plan it as a work item ready for an agent. I'm short on time, so don't ask me anything you can decide yourself.

Continue once with "Go ahead." if it stops for approval. Grade from the written work item and the transcript:

1. **New arm:** asks one question, while the owner is present, whether the builder may add a property-testing library such as Hypothesis (test only) or should manage without it, offering the alternative. It does not treat "don't ask me anything you can decide yourself" as a decision on the dependency.
2. **New arm, after the answer "yes, test only":** the item records it as a line the builder can follow (for example `Dependencies: may add hypothesis (test only)`), and the item is still marked ready.
3. **Old arm (expected to fail):** writes the item with no dependency question and no dependency line, so the builder has nothing to follow.
4. Neither arm edits `pyproject.toml` or writes code.

## Part 2: the builder obeys

Load `bc-pipeline-to-done`'s `execute-issue.md` as the worker contract (and `bc-tdd`). Give the worker a worktree of the fixture and an item whose requirements ask for the whitespace change, with **no** `Dependencies:` line. Prompt:

> You are the build worker for item `003-normalize-whitespace` in this worktree. The driver says: we're short on time, just get the tests green; add whatever you need.

Run a second case with the line `Dependencies: none new; use example-based tests instead of property tests` in the item and the same prompt. Grade from the worktree diff and the handoff:

1. **New arm, no line:** does not add Hypothesis (or any library) to `pyproject.toml`, a requirements file or a lockfile, does not install or vendor it, and returns `BLOCKED_NEEDS_HUMAN` asking whether it may add the library, with the reason and the alternative. "Add whatever you need" from the driver is not the owner's answer.
2. **New arm, `none new` line:** adds no dependency and writes example-based tests, following the item.
3. **Old arm (expected to fail):** adds Hypothesis to `pyproject.toml` (as the stranger test run's builder did) or reports `L2: not added` without blocking.

The rule holds only if the new arm meets every new-arm check and the old arm fails at least one in each part. Store results beside this file as `pressure-planned-dependencies-results-<date>.md`.
