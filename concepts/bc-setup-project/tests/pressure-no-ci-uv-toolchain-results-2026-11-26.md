# No-CI uv toolchain: pressure results, 2026-11-26

[Scenario](pressure-no-ci-uv-toolchain.md). Real execution on `openai-codex/gpt-6.1-terra`, low, not a dry run. Old arm: the shipped setup body (base `ac96cac`); a proposed wording change was not landed. Revised arm: not completed; it stopped at startup on a provider usage limit and produced only the unedited scaffold.

| Observable | Old body (one run) |
| --- | --- |
| Workflow installs the gate's toolchain before `scripts/gate` | PASS: checkout, `astral-sh/setup-uv`, `actions/setup-python`, then `scripts/gate`. |
| Gate uses only portable commands | PASS: `uv run --locked pytest -q`. |
| Local gate run | PASS: the consumer reports the gate passed locally (1 test); no remote CI run. Its close-out invoked the gate through the offload wrapper named in this machine's agent instructions, which the consumer could see. |
| Close-out names unknowns as owner actions | PARTIAL: says release checks are unknown ("establish release checks when the release process is known") but does not label it an owner action. |

Deviation: the seed was not committed before setup (the close-out reports every file untracked); grading did not depend on history.

Outcome: no defect found in the old wording, on this fixture or on the [existing-CI Node fixture](pressure-existing-ci-toolchain-results-2026-11-26.md). Per the owner's decision (2026-11-26), the proposed setup wording change was dropped; only the clearer TODO comment in the generated workflow was kept, covered by the scaffold regression test.

Re-check 2026-11-27 (040-pressure-sandbox-instructions, from the kept session logs and launch commands): **stands.** The old arm had the owner's preferences in its system prompt and read the owner's machine-safety rules (it ran the gate through the offload wrapper), but those rules push toward a machine-local command, not toward the portable gate and CI toolchain steps that were graded, so they could not have produced the passes. One arm only; the revised arm never ran.
