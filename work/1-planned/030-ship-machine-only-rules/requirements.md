# Requirements: ship the rules that only live in the owner's setup

## Solution

Kernel delivery and the setup check moved to `035-kernel-package` (owner decision 2026-11-26: separate package, setup only checks).

2. **Carry-on order in the generated work rules.** When told to carry on without a named item: read every active item first; unfinished active work comes before new items from `work/order.md`; before taking an active item, check for a live holder (`Held by:` line and recent commits) and ask rather than take it.
3. **Questions while away.** Where skills say "file the questions where the owner sees questions (the project's or machine's instructions name the place)", add the fallback: with no named place, park the item with a `Waiting on owner: <question>` line. Dashboards stay optional adapters.
4. **Regression fixes load guardrails.** `bc-pipeline-to-done`'s worker packet for a performance, size, memory or structure regression loads `bc-performance-guardrails` and requires the new check or a stated reason it cannot catch the regression; the reviewer checks for it.

## User Stories

2. As a stranger, "carry on" resumes unfinished active work before starting new items.
3. As a stranger away from the keyboard, my unattended run parks questions where I will see them.
4. As a stranger, an unattended regression fix leaves a check behind.

## Testing Decisions

Pressure scenarios on the pressure-test model, blind baseline, one per reworded rule: carry-on with one active and one planned item (active resumed); away-mode open question without a named place (`Waiting on owner:` written); drain regression fix (guardrails loaded, check added).

## Out of Scope

- Kernel content and delivery (`035-kernel-package`); any dashboard.
