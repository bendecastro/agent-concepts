# Starter items

Setup offers these follow-up items in its init plan. The first four are for a project that already has source code; the last two are for a new or empty project, where the checks and design notes are cheapest to set up before the first code lands. Each section heading is the item's filename slug; copy only the fenced text into the work item. Replace `{{stage}}` with a stage from the project's `Stages:` line and `{{date}}` with the setup date (`YYYY-MM-DD`). Every item here is already planned by this reference, so `work_index.py --check` does not ask for `bc-plan-to-pipeline`; only the two ready items carry `Ready for agent: yes`, because the owner-led items wait on the owner's own command.

## design-inventory

Applies when: the survey finds a user-facing UI or CLI, for example a front-end framework, UI templates or styles, or a CLI entry point with user-facing output.

```markdown
# Inventory the existing design

Why: The project's existing design is not recorded, so new work can duplicate controls or introduce a second theme.
Done when: The current design has a documented reuse path and text-search checks catch new departures without failing on existing ones.
Stage: {{stage}}
Blocked by: nothing
Kind: design
Source: bc-setup-project
Planned: bc-setup-project {{date}}
Ready for agent: yes

## Steps

- [ ] Inventory the current surfaces following `bc-ui-design`'s `existing-app.md` and `design-framework.md`. Record the existing themes, tokens by role, control kinds and where to reuse them on design pages linked under Pages in `docs/design/README.md`. Done when the pages point to the current implementations and distinguish shared controls from one-offs. Out of scope: redesigning surfaces, adding tokens or replacing existing controls.
- [ ] For control rules that can be checked by text search, add checks to the project's own test runner and list them under Checks in `docs/design/README.md`. Name the part to reuse and the design-page rule in each diagnostic; record current hits in a per-file baseline that may only fall. Done when the checks pass at the recorded baseline and catch a new violation. Out of scope: fixing baseline hits or encoding visual-only judgments as text rules.

## Outcome

_To be filled when finished or dropped._
```

## guardrails-setup-checks

Applies when: the survey finds project source code.

```markdown
# Add guardrails setup checks

Why: Known problems for this stack can creep in without a check, but existing shortfalls should not block unrelated work.
Done when: Each selected stack risk has a sourced check in the project gate with a limit based on the project's measured starting point.
Stage: {{stage}}
Blocked by: nothing
Kind: performance
Source: bc-setup-project
Planned: bc-setup-project {{date}}
Ready for agent: yes

## Steps

- [ ] Follow `bc-performance-guardrails`' Setup checks: choose checks for known problems of this stack that have an official source, published guideline or past project bug. Measure the current value before setting each limit and record the source, measure, command and baseline in `docs/guardrails/README.md`. Done when every proposed check has a source and a reproducible current measurement. Out of scope: unsourced checks, invented budgets and performance fixes.
- [ ] Run the checks inside `./scripts/gate` and ratchet each at today's measured value. Record how to tighten the limit as the measure improves. Done when the new checks pass at baseline and fail on a controlled regression. Out of scope: optimizing the code or raising a limit to hide a regression; file improvements separately for `bc-optimize-code`.

## Outcome

_To be filled when finished or dropped._
```

## architecture-review

Applies when: the survey finds project source code. The owner can leave this out when a review is not needed.

```markdown
# Review the codebase architecture

Why: An existing codebase may have structural friction worth reviewing before taking on larger changes.
Done when: The owner has reviewed the architecture and recorded which findings, if any, to take forward.
Stage: {{stage}}
Blocked by: nothing
Kind: architecture
Needs owner: Run `/bc-improve-codebase-architecture` when ready to lead the review.
Source: bc-setup-project
Planned: bc-setup-project {{date}}

## Steps

- [ ] Owner starts the interactive review and decides what to take forward.

## Outcome

_To be filled when finished or dropped._
```

## issue-triage

Applies when: the survey confirms open GitHub issues with `gh issue list`. If `gh` is unavailable or the listing fails, do not infer that the project has open issues.

```markdown
# Triage the open GitHub issues

Why: Existing issues need decisions about what belongs in the project's work queue.
Done when: The owner has triaged the open issues and recorded their dispositions.
Stage: {{stage}}
Blocked by: nothing
Kind: none
Needs owner: Run `/bc-triage` when ready to decide which issues to take forward.
Source: bc-setup-project
Planned: bc-setup-project {{date}}

## Steps

- [ ] Owner starts interactive triage and decides what to do with the open issues.

## Outcome

_To be filled when finished or dropped._
```

## guardrails-for-new-project

Applies when: the survey finds no project source code yet (a new or empty project).

```markdown
# Plan guardrails checks for the first code

Why: Known problems for the planned stack are cheapest to catch from the first commit, before any shortfall builds up.
Done when: Each chosen stack risk has a sourced check in the project gate, with a limit measured on the project's first code.
Stage: {{stage}}
Blocked by: nothing
Kind: performance
Source: bc-setup-project
Planned: bc-setup-project {{date}}
Ready for agent: yes

## Steps

- [ ] Follow `bc-performance-guardrails`' Setup checks for the planned stack: choose checks for its known problems that have an official source or published guideline, and list each with its source and the command that will measure it in `docs/guardrails/README.md`, marked as having no limit yet. Done when every chosen check has a source and a measuring command. Out of scope: limits, since there is no code yet to measure, and unsourced checks.
- [ ] Once the project has its first working code, add the checks to `./scripts/gate`, measure today's value and set each limit there. If there is no code yet, leave this step open; it does not block any other item. Done when the checks pass at the measured limit and fail on a controlled regression. Out of scope: optimizing code or raising a limit to hide a regression.

## Outcome

_To be filled when finished or dropped._
```

## design-for-new-project

Applies when: the survey finds no project source code yet and the owner plans a user-facing UI or CLI.

```markdown
# Record the intended design before the first UI

Why: Writing down the intended look and controls before the first screen keeps later work from inventing a second theme or a duplicate control.
Done when: The intended design is recorded on design pages and text-search checks catch departures from it once there is UI code.
Stage: {{stage}}
Blocked by: nothing
Kind: design
Source: bc-setup-project
Planned: bc-setup-project {{date}}
Ready for agent: yes

## Steps

- [ ] Follow `bc-ui-design`'s `new-work.md` and `design-framework.md` to record the intended themes, tokens by role and the kinds of control the project will use, on design pages linked under Pages in `docs/design/README.md`. Done when the pages name each theme, token role and control kind, marked as the agent's choice the owner may change. Out of scope: building screens or controls.
- [ ] Once the project has UI or CLI code, add text-search checks for the recorded control rules to the project's own test runner and list them under Checks in `docs/design/README.md`; name the part to reuse and the design-page rule in each failure message. If there is no code yet, leave this step open; it does not block any other item. Done when the checks pass and catch a new violation. Out of scope: visual-only judgments as text rules.

## Outcome

_To be filled when finished or dropped._
```
