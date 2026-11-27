# New projects also get the guardrails and design starter items

Why: Setup offers the guardrails item (the project's fitness functions) and the design-inventory item (design consistency) only when it finds existing source code, so a new or empty project never gets either, and it is cheapest to set both up before the first code lands.
Done when: Setting up a new or empty project offers both items (design only when the planned project has a user-facing UI or CLI), worded for a project with no code yet: each waits until there is code to measure or inventory, and neither blocks the first feature.
Stage: now
Blocked by: 042-one-command-pi-install, 043-plain-pipeline-messages
Kind: feature
Source: owner choice on the 039 stranger walkthrough, 2026-11-27
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- `concepts/bc-setup-project/body/starter-items.md` gains new-project variants (or conditional wording) of `guardrails-setup-checks` and `design-inventory`: guardrails choose sourced checks for the planned stack and set limits once the first code exists; design records the intended themes, tokens and controls (via `bc-ui-design`'s new-project path) and adds the text-search checks once there is UI code.
- `concepts/bc-setup-project/body/SKILL.md` stops skipping starter items for new or empty projects and offers these two as unticked-able boxes with the reason; for a new project with no UI or CLI planned, only guardrails. The architecture-review and issue-triage items stay existing-code only.
- Filed items still pass `work_index.py --check` (they carry `Planned:` like the existing ones); `test_starter_items.py` covers the new-project case.
- CONCEPT.md, index.md and log updated; lint 0 ERROR.

## Steps

- [ ] New-project starter items for guardrails and design. Done when a targeted test files them for an empty-project survey and they pass the index check, and the existing-code tests still pass. Out of scope: changing what the existing-code items do.

## Outcome

_To be filled when finished or dropped._
