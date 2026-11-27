# Setup's starter items pass the work-index check

Why: Right after setup in the stranger test, `work_index.py` warned that the seeded `002-architecture-review` item "has no Planned: line", and the next session reported it as a pre-existing problem (stall 3 in `docs/research/2026-11-27-stranger-end-to-end/README.md`).
Done when: A freshly set-up project's `python3 .bc-agent/scripts/work_index.py --check` prints no warning for the starter items setup seeds, covered by a scaffold test.
Stage: next
Blocked by: nothing
Kind: bug
Source: 033-stranger-end-to-end-test
Planned: bc-plan-to-pipeline 2026-11-27

## Steps

- [x] Starter items: either the seeded items carry what the index check expects or the check accepts unplanned starter items in `1-planned/` by design; decide which, change one side, add a scaffold test. Done when the test fails on the current scaffold and passes after.

## Outcome

Owner chose to seed the line (2026-11-27): the owner-led `architecture-review` and `issue-triage` starter items in `concepts/bc-setup-project/body/starter-items.md` now carry `Planned: bc-setup-project {{date}}`, and `test_starter_items.py` fails on any `work_index.py` warning (it failed on both items before the change). The index check is unchanged, so the warning still flags real unplanned items.
