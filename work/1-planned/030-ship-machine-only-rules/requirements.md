# Requirements: ship the rules that only live in the owner's setup

## Solution

1. **Kernel install offer.** During setup's survey, check whether the harness's always-on instructions file (per `docs/guides/harnesses.md`) contains the kernel (its heading `# Agent Kernel` or the harness's delta). If not, offer to add it and add it only after the user confirms; on decline, add one line to the ideas file. The kernel offered is the everyone-only kernel from `034-kernel-for-everyone`.
2. **Carry-on order in the generated work rules.** When told to carry on without a named item: read every active item first; unfinished active work comes before new items from `work/order.md`; before taking an active item, check for a live holder (`Held by:` line and recent commits) and ask rather than take it.
3. **Questions while away.** Where skills say "file the questions where the owner sees questions (the project's or machine's instructions name the place)", add the fallback: with no named place, park the item with a `Waiting on owner: <question>` line. Dashboards stay optional adapters.
4. **Regression fixes load guardrails.** `bc-pipeline-to-done`'s worker packet for a performance, size, memory or structure regression loads `bc-performance-guardrails` and requires the new check or a stated reason it cannot catch the regression; the reviewer checks for it.

## User Stories

1. As a stranger, setup tells me the kernel is missing and installs it when I agree.
2. As a stranger, "carry on" resumes unfinished active work before starting new items.
3. As a stranger away from the keyboard, my unattended run parks questions where I will see them.
4. As a stranger, an unattended regression fix leaves a check behind.

## Testing Decisions

Pressure scenarios on the pressure-test model, blind baseline, one per reworded rule: kernel missing at setup (offer made, nothing written before consent); carry-on with one active and one planned item (active resumed); away-mode open question without a named place (`Waiting on owner:` written); drain regression fix (guardrails loaded, check added).

## Out of Scope

- Writing the kernel's content (034); any dashboard.
