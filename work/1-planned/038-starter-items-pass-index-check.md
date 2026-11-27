# Setup's starter items pass the work-index check

Why: Right after setup in the stranger test, `work_index.py` warned that the seeded `002-architecture-review` item "has no Planned: line", and the next session reported it as a pre-existing problem (stall 3 in `docs/research/2026-11-27-stranger-end-to-end/README.md`).
Done when: A freshly set-up project's `python3 .bc-agent/scripts/work_index.py --check` prints no warning for the starter items setup seeds, covered by a scaffold test.
Stage: next
Blocked by: nothing
Kind: bug
Source: 033-stranger-end-to-end-test

## Steps

- [ ] Starter items: either the seeded items carry what the index check expects or the check accepts unplanned starter items in `1-planned/` by design; decide which, change one side, add a scaffold test. Done when the test fails on the current scaffold and passes after.

## Outcome

