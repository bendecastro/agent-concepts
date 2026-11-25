---
name: bc-guardrails
description: >-
  Use when setting or changing a speed, size, memory or structure limit (a performance budget, a bundle-size cap, a frame or load-time target, a dependency or layering rule); adding or changing a check that protects such a property; fixing a regression in one (something got slower, bigger, hungrier or more tangled); or setting up a project's guardrails. Skip design-consistency checks: those live on the project's design page (bc-ui-design).
---
# Guardrails

A guardrail is a limit on how fast, small, lean or well-structured a project must stay, plus the automated check that fails when a change breaks it. Performance budgets (limits on time, bytes or memory) and fitness functions (checks for a structural property, such as "the UI layer never imports the database") follow the same method. The goal is that short-lived agents cannot make the project slower, bigger or more tangled one change at a time without a check failing.

## Start from the project's guardrails page

Read the project's `docs/guardrails/README.md` first; it lists the project's targets, budgets and checks. If it is missing, copy the `GUARDRAILS_README` text from `bc-init-agent`'s `body/scaffold.py` into `docs/guardrails/README.md` in its own commit; do not run the scaffold just for this. Without `bc-init-agent`, write the sections Who chooses a limit, Where a rule lives, How to measure, Targets, Budgets and Checks. Then add the setup checks in [Setup checks](#setup-checks).

Every check runs inside the project's existing full gate (`scripts/gate` or its equivalent); add no separate runner. Design-consistency checks stay on the project's design page (`docs/design/README.md`); the guardrails page links to it rather than copying them.

## Where a rule lives

Classify each check by what it needs to run, and pick the cheapest kind that reliably catches the problem:

| Kind | What it does | Example |
|---|---|---|
| static | inspects source or settings without running anything | a lint rule banning blocking file reads in an Electron main process; a forbidden import between layers |
| artifact | measures a built output without running the program | download size of the built bundle; number of dependencies in the lockfile |
| dynamic | runs the program and measures | startup time; time per frame; memory after a fixed workload |

Why: a static check is fast and never flaps, so it can run on every change; a dynamic check costs time and has noise, so use it only when nothing cheaper sees the problem. A text-search rule catches a known bad pattern; it does not prove the program is fast, so a user-facing target still needs a dynamic check.

## Set a limit without asking

Do not ask the owner for a number. Choose it yourself, record it as the agent's choice the owner may change, and list it as one FYI line in your report. Why: the goal is that guardrails exist, not sign-off; one recorded number is one edit for the owner to change.

- **No limit yet (ratchet).** Measure today's value, with enough repeated runs to see the noise, and set the limit at today's value plus a noise allowance. Anything worse fails. Never invent a number you did not measure. Method: [measuring.md](measuring.md).
- **User-facing target** (time per frame, page load, delay after a tap or keypress). Take it from a published guideline and cite the source on the page; defaults are in [targets.md](targets.md). Split a target into smaller allowances per step when one step owns part of it (budget decomposition).
- **After a verified improvement**, tighten the limit to the new value plus the noise allowance in the same commit. A limit only ever moves toward better unless the owner says otherwise.
- **Owner-chosen limits are fixed.** Never loosen, remove or re-measure a limit the page marks as the owner's choice to make a check pass. Fix the code, or stop and ask the owner. Why: loosening the limit hides exactly the regression the owner asked to be stopped.

## Write path

Record every limit and check on `docs/guardrails/README.md`: the measure, the limit, its source (a measurement with its date and run count, a guideline link, or a past bug) and who chose it (agent or owner). The page line lands in the same commit as the check that enforces it. Why: a line without a check is a wish, and a check without a line is a number nobody can find or change.

Pages state current values only: one fact per line, no history. Link the decision log for why an owner limit is what it is.

## After fixing a regression

When you fix something that got slower, bigger, hungrier or more tangled, and a check could have caught it, add that check in the same change, record it on the page, and mention it in one line of your report. Do this even when told there is no time: the check is part of the fix, not a separate task. Why: without the check the same mistake comes back with the next agent, who never saw this one.

## Setup checks

At project setup, and when you first add the guardrails page, add checks for well-known problems of the project's stack: for example blocking file or network I/O in an Electron main process, or download size for a web app. Ratchet each one at today's value so existing shortfalls do not fail the gate. Add a check only when you can name a source (official guidance, a published guideline) or a past bug in this project for it; record that source on the page. Why: unsourced checks add noise and cost without catching anything real.

## Report

List each limit you set or tightened and each check you added: measure, limit, source, and "agent's choice" where it applies, one line each.
