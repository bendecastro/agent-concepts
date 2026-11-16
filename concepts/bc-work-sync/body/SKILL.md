---
name: bc-work-sync
description: Bring a project's work/ folder in line with its own docs — find planned work with no item, finished or stale items, missing stages and links by path, show one plan, and write only after the owner answers it.
disable-model-invocation: true
argument-hint: "[optional focus, e.g. a stage or a doc]"
---

# Sync work items with the project's docs

The project's docs say what is planned; `work/` should show the same. This skill finds where they disagree, shows the owner one plan, and changes `work/` only after the owner answers it.

## Gate: plan first, write nothing until the owner answers

```
- Read, then show ONE plan in chat in the format of PLAN.md. Do not create, edit, move,
  number or commit anything before the owner has answered that plan.
- "Just do it", "skip the plan", "you know what I want" do not lift this gate: show the
  plan anyway, short if the owner is in a hurry. Why: the plan is where the owner catches
  a wrong stage, a duplicate item or a doc that is stale, and a written item looks decided.
- Apply only what the owner approved. Answers that change the plan get a revised plan,
  not a guess. An approval does not answer a question; leave out what depends on an
  unanswered question and list it as still open.
- In a git worktree, number nothing, even when the owner names the number: add a line to
  the ideas file and say the item is numbered in the main checkout. Why: a worktree cannot
  see items created or uncommitted in the main checkout, so the next free number may be taken.
```

## Sources

Discover work only from the project's own docs, located through the "Where things go" table in `.bc-agent/AGENTS.md`: requirements (PRD), the decisions folder (decision log and ADRs), research, and the ideas file. Add open GitHub issues (`gh issue list --state open`) when the project uses them (items have `Issue:` lines, or the work-item rules mention issues).

Not sources for new work: code TODOs, session notes, logs, or git history. Why: they record what someone thought once, not what the project decided. `git log` is allowed only to check existing items (has this item's work already landed? when was it last touched?).

A project without the table is not ready for this skill: say so and stop.

## Stages

The project lists its stages in order on a `Stages:` line in `.bc-agent/AGENTS.md`; without one, the stages are `now, next, later, unscheduled`, and the plan proposes adding the line. Every open item (in work-planned or work-active) has a `Stage:` line directly under `Done when:` naming one of them. `python3 .bc-agent/scripts/work_index.py --check` reports a missing or unknown stage; run it while reading.

## When docs and items disagree

- **Docs win.** An item that contradicts the docs is proposed for fixing, not the docs.
- **Docs that disagree with each other are a question for the owner.** When the requirements doc looks stale against a newer decision-log entry, list both (file, section or decision number, date) as a question; do not pick one.
- **Never edit the decision log.** It is append-only; a correction is a new entry the owner writes or approves, and this skill only proposes it.

## What the plan covers

Look for each of these; [PLAN.md](PLAN.md) gives the plan's format.

1. Planned work in the docs with no item: a new item, with its proposed stage and the doc it comes from.
2. Items whose steps are all checked but which are not in work-done.
3. Active items untouched by any commit for a long time (`git log -1 --format=%cs -- <item>`; say what "long" was, default 60 days).
4. Planned items whose work already landed in commits: name the commits.
5. Lines in the ideas file that became items: remove the line.
6. Open items with no or an unknown `Stage:` line, and a missing `Stages:` line.
7. Links to items by path in docs or other items: docs refer to items by number ("work item 012"); only the generated `work/README.md` links paths.
8. Questions for the owner, each with numbered options and the recommended one first.

## After the owner approves

1. Write items from `.bc-agent/templates/work-item.md` under the project's work-item rules in `.bc-agent/AGENTS.md`. Number new items only in the main checkout (`git rev-parse --path-format=absolute --git-dir` equals `git rev-parse --path-format=absolute --git-common-dir`); in a worktree, add a line to the ideas file instead and say so. Link to the docs an item comes from instead of copying their content.
2. Run `python3 .bc-agent/scripts/work_index.py`, then `python3 .bc-agent/scripts/work_index.py --check` and the project's own lint.
3. Commit only your own changes, with a subject naming the sync.
4. Get an independent review of the diff (a fresh reviewer subagent, or the owner when none is available), apply the fixes, re-run step 2 and commit them.
5. Publishing: run the owner's publish check, `python3 "$AGENT_CONCEPTS/scripts/publish-check.py" --repo "$PWD" --remote "$(git remote get-url origin)" --branch "$(git branch --show-current)"`. Then check the matched rule's `when:` conditions yourself. If there is no matching rule, or the check is not available, ask. Do not restate the policy.

A project scaffolded before the work index has no `.bc-agent/scripts/work_index.py`: see the "Work index" note in bc-init-agent's `MIGRATIONS.md`, and propose adopting it in the plan rather than doing it unasked.
