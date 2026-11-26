# Requirements: starter items for existing codebases

## Problem Statement

When `bc-setup-project` sets up an existing codebase, it creates `docs/design/README.md` and `docs/guardrails/README.md` with empty lists and ends by naming follow-up skills in chat. Nothing records the design the app already has, so the first agent to touch the UI can build a second version of an existing control. Nothing adds the stack checks that `bc-performance-guardrails` § Setup checks says belong "at project setup", because setup never hands off to that skill. And `work/` starts empty, so the owner's dashboard shows none of the follow-up work.

## Solution

On an existing codebase, setup proposes **starter items** in its init plan: the follow-up work its survey shows applies, each with the reason it applies. The owner unticks what they do not want. After the scaffold, the setup agent writes the accepted items into the planned folder and places them in `work/order.md` where `work_index.py --check` says. Setup itself runs no audit.

The four starter items, and when each is proposed:

| Starter item | Proposed when | Written as |
|---|---|---|
| Design inventory | The project has a UI or CLI surface | Full steps, `Ready for agent: yes` |
| Guardrails setup checks | The project has source code | Full steps, `Ready for agent: yes` |
| Architecture review | The project has source code (the owner unticks it when not needed) | `Needs owner:` (run `/bc-improve-codebase-architecture`) |
| Issue triage | The project has open GitHub issues | `Needs owner:` (run `/bc-triage`) |

## User Stories

1. As an owner setting up an existing codebase, I want the follow-up work filed as items, so that it shows on my dashboard and I can rank it.
2. As an owner, I want only the items that apply proposed, so that a project without a UI gets no design item.
3. As an owner, I want to see each proposed item with the reason it applies and untick it in the init plan, so that nothing lands that I did not accept.
4. As an owner, I want the guardrails and design-inventory items ready for an unattended drain, so that `/bc-pipeline-to-done` can build them without another planning pass.
5. As an owner, I want the architecture-review and triage items marked as needing me, so that a drain does not try to run interactive skills.
6. As an owner, I want setup to stay short, so that it files the audits rather than running them, even when told to hurry.
7. As an agent running `bc-performance-guardrails`, I want its setup checks to reach every existing codebase through the starter item, so that the instruction "at project setup" is actually carried out.

## Implementation Decisions

- Scope: existing codebases only (the survey finds source code). A new or empty project gets no starter items; it has nothing to inventory or measure.
- The setup agent writes the items, following a new reference file, `starter-items.md`, in `concepts/bc-setup-project/body/`, that holds, for each starter item, its applicability signal and its item text (header lines and steps). `scaffold.py` does not change. Why: deciding whether an item applies needs judgment, and numbering and placement already have checked rules.
- Applicability signals come from the survey `bc-setup-project` already runs (step 2): a UI or CLI surface (front-end frameworks, templates, styles, a CLI entry point with user-facing output), source code present, open issues from `gh issue list` when `gh` works.
- The design-inventory item follows `bc-ui-design`'s `existing-app.md` and `design-framework.md`: record the existing tokens, theme and control kinds on design pages and add the text-search checks with a baseline that may only fall.
- The guardrails item follows `bc-performance-guardrails` § Setup checks: sourced checks for the stack's known problems, each held at today's measured value, run inside `./scripts/gate`. Measuring comes first; any improvement becomes a follow-up item for `bc-optimize-code`, not part of this item.
- The architecture-review and triage items carry `Needs owner:` and no `Ready for agent:` line, because `/bc-improve-codebase-architecture` and `/bc-triage` are interactive and only the owner invokes them.
- Items are numbered and placed by the project's existing work-item rules (next free number, `work_index.py --check` placement in `work/order.md`); each carries `Source: bc-setup-project` and a `Kind:` line (design inventory: design; guardrails: performance; architecture review: architecture; triage: none).
- `concepts/relationships.json` gains `hands_off` edges from `bc-setup-project` to `bc-performance-guardrails`, `bc-ui-design`, `bc-improve-codebase-architecture` and `bc-triage`; generated views are regenerated.
- `bc-performance-guardrails` § Setup checks names the starter item as the way setup reaches it.

## Testing Decisions

- Deterministic: a test in `concepts/bc-setup-project/tests/` extracts each item text from `starter-items.md`, fills its placeholders into a fixture work folder and runs `work_index.py --check` on it; it also checks the ready items have a `Done when` and `Out of scope` on every step and the owner items have `Needs owner:` and no ready line. Watched failing before the reference file exists.
- Pressure test (the test rule; the setup skill body is deployed by symlink, so it runs on the branch before landing): a consuming agent on the pressure-test model sets up fixture repositories in dry-run planning mode: a library without UI and without issues (no design or triage item proposed), a web app with a UI (design item proposed), and a scripted owner who says to hurry and "just fix the performance now" (files the items, runs no audit). Once blind without the change, once with it; graded on the written plan and item files.

## Out of Scope

- Running any audit during setup.
- Starter items for new or empty projects.
- Changing `scaffold.py`.
- A size threshold for the architecture review.
- Re-offering starter items to projects set up before this change (a later `MIGRATIONS.md` note may cover it).
