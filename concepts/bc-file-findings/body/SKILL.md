---
name: bc-file-findings
description: File a review's or hunt's findings as project work after the owner picks which to file. Use when a skill that produced findings (bug hunt, architecture review, security audit, reflection, prototype, plan challenge) reaches its filing step; the caller names the Kind, the Source and what each item must carry.
---

# File findings

How a finished review's findings become project work. The calling skill produced the findings and states three things this file leaves open: the item's `Kind:`, its `Source:`, and what each item must contain (evidence, branch, test, report path). Everything else is here.

## Wait for the pick

Wait for the owner's answer before filing anything. Why: a review proposes; only the owner decides what becomes work, and an item filed on the agent's own judgment reads as a decision nobody made.

When the message that invokes you already carries that answer (for example `all`), it is the answer: file and plan in that same reply, and do not end the reply on a summary of what you will file. Do not ask again which findings to file.

## With a project work pipeline

A project has one when `.bc-agent/AGENTS.md` has a "Where things go" table with work-planned, work-dropped and ideas roles. Resolve each role's path from that table. Do all four steps in one reply, without stopping between them; the filing is finished only when every work-planned item you filed has a `Planned:` line.

1. **Give every finding exactly one home.**
   - **Chosen** (`all` means every finding the caller pre-selected) → a numbered work item in work-planned, made from the project's work-item template, with the caller's `Kind:` and `Source:` lines and the contents the caller names.
   - **Rejected** → a numbered work item in work-dropped whose `## Outcome` states the owner's reason. Why: a recorded "no, because" stops the next review re-proposing it.
   - **Everything else** (findings the owner neither chose nor rejected) → one line each in the ideas file, pointing at the report.

   Number items as the project's work-item rules say: only the main checkout numbers items. From a git worktree, number nothing: each item becomes one ideas line stating the owner's choice and its reason, and you tell the owner it is still to be numbered in the main checkout.
2. **Place and check.** Place each new item in `work/order.md` where the project's work-item rules say, and run `.bc-agent/scripts/work_index.py --check` until it passes.
3. **Commit the filing.**
4. **Plan each filed item.** Load `bc-plan-to-pipeline` and run it from a settled source on each work-planned item you filed, one after another. Pass it the owner's answer and the report: the answer settles which findings are filed, and the caller's evidence (a reproduction test, a grilling answer) settles what it settles, so none of it is asked again. Each item gets its requirements, sliced `## Steps` and `Planned:` line in place; commit them. Planning is not starting: leave the items in work-planned, even when told "it's one line, just start it" or "file them and we're done". Why: every planned item gets requirements and sliced steps before anyone starts it; this is a handoff after the filing ends, not a nested call.

## Without a project work pipeline

Do not invent one. List the owner's picks in the reply, say where the report is, and say the findings are not filed.
