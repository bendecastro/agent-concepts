# Requirements: pipeline to done

## Problem

The README's loop is three skills: plan the idea, put it in the pipeline, then let agents build it. The third skill, `bc-drain-issues`, only reads GitHub issues: it picks issues labelled `ready-for-agent`, claims them, builds them with independent review, and closes them. A project that plans in work items (the `work/` pipeline `bc-init-agent` scaffolds) has no unattended builder, so the loop stops at step two. Work items also lack three things an unattended builder needs: a marker that an item may run without the owner watching, steps that state what "done" means and what is out of scope, and a state for an item waiting on the owner.

The skill also launches three Pi roles by fixed name (`bc-drain-auditor`, `bc-drain-worker`, `bc-drain-reviewer`), and the owner's live role files are links into this public repository, so the owner's setup and the public examples cannot differ.

## Solution

Rename `bc-drain-issues` to `bc-pipeline-to-done` (the old name stays as a deploy alias) and give it two sources behind one shared core. The core keeps the claim, worker packets, independent review, landing, recovery and safety rules once. An issue source and a work-item source each handle choosing, claiming, reading the contract, parking and finishing.

Decisions (grill, 2026-11-25):

1. One skill, two sources; the shared rules exist once.
2. The skill names jobs, not roles: an auditor (read-only, fresh, no extra skills), a builder (writes in its own worktree, never commits) and a reviewer (read-only, fresh). A private overlay (`~/.config/agent-concepts/overlays/bc-pipeline-to-done.md`, per the repo's overlay convention) names the roles a machine uses. `examples/agents/` stays as optional examples; the "keep the names" rule goes. The owner's live role files become their own copies, not links.
3. A work item is eligible when it has the line `Ready for agent: yes`, its `Blocked by:` items are done, and it comes next in the pipeline order. `bc-plan-to-pipeline` writes that line only when every step states its done-criteria and what is out of scope.
4. The claim unit is the whole item: one builder works through its steps in order; different items may run at the same time.
5. With a Git remote, the item is claimed by the same no-force remote ref the issue source uses, keyed by the item's slug. Without a remote, only one driver may run and moving the item to `work/2-active/` (committed) is the claim.
6. An item needing an owner decision is parked: moved back to `work/1-planned/` with a `Waiting on owner: <question>` line and its `Ready for agent` line removed; the question goes where the owner sees questions (the overlay names the tool). When the owner answers, the answer is written into the item and the ready line restored.
7. Item `008-bc-drain-issues-v3-review-economy` stays separate and runs after this item.

## User stories

1. As the owner, I want agents to build planned work items without me watching, so the loop works in projects that do not use GitHub issues.
2. As the owner, I want to mark which items may run unattended, so a loosely planned item does not start building by itself.
3. As the owner, I want a parked item and its question to show on my dashboard, so I know what is waiting on me.
4. As the owner, I want my own subagent roles separate from the public examples, so I can tune them without publishing the change.
5. As someone installing the skill, I want it to work with my own subagent setup, so I am not forced to copy fixed role names.
6. As a driver, I want one claim rule per source, so two drivers never build the same item or issue.
7. As a driver, I want the review, landing and recovery rules to be identical for both sources, so a fix to them reaches both.
8. As an existing user, I want `bc-drain-issues` to keep working as a name, so my habits and links do not break.

## Out of scope

- Measuring the review-economy token win (item `008-bc-drain-issues-v3-review-economy`).
- Changing the review, landing or safety rules themselves beyond what the split needs.
- Filing GitHub issues for work-item projects.
