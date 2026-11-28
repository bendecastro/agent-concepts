# Work-item source

The work-item source of [bc-pipeline-to-done](SKILL.md). The unit of work is one work item, its claim key is `item-<slug>` (the item's file or folder name without `.md`), and its contract is the item: its `plan.md` steps and `requirements.md` for a large item, its steps for a small one. Resolve the work-planned, work-active and work-done folders and the ideas file through the project's "Where things go" table, and follow the work-item rules in `.bc-agent/AGENTS.md`. Everything here is specific to work items; the claim protocol, packets, review, landing, recovery and safety live in [SKILL.md](SKILL.md).

## Eligibility

An item is eligible when all three hold:

- it carries the line `Ready for agent: yes` and no `Waiting on owner:` line;
- every item named on its `Blocked by:` line is in work-done;
- it is next in pipeline order: the generated table in `work/README.md` (run the project's work index script first so it is current), or the project's order rules when the project has no generated table. Take the first eligible item; never jump an item the order puts ahead of it. Why: an unattended drain has no one to say which item matters more, so the owner's order is the only priority it has.

When the user's request names an item ("build 003-whitespace", "build the item I just planned"), that naming is the order decision for this run: build that item without asking about the order, provided the other two conditions hold. Record the change the project's way in the claim commit — for example move the item to the top of `work/order.md` — and rerun the work index script. Why: the user has already chosen; asking again whether to skip the items ahead stalls a run the user started on purpose.

Skip an item without the ready line, even when it looks fully planned. Why: `Planned:` proves the item was planned, not that the owner agreed to let it run unattended; the ready line is that consent, and `bc-plan-to-pipeline` writes it only when every step states what "done" means and what is out of scope. An eligible item whose steps still lack done-criteria or out-of-scope is parked (see [Park](#park)), not guessed.

An item already in work-active is either a live claim (see [Claim](#claim)) or interrupted work for the core's resume rules; never start a second run on it.

## Claim

The claim unit is the whole item: one builder works through all its steps. Different items may run at the same time, one builder each.

**When preflight permits remote claims**, claim the item with the same no-force protocol the core uses for issues, on `refs/heads/bc-drain-claims/item-<slug>`: create-if-absent without force, ownership proven by the push update plus `git ls-remote` equality, a lost race skipped before dispatch. Released Claim Marker reuse applies only to a valid marker whose body names `item=<slug>` in place of `issue=<n>`; any other existing tip is held. Then `git mv` the item to work-active, add the driver's `Held by:` line (below), run the work index script, and commit the move on the recorded target branch and push it there before the builder starts. Why: the folder move shows the owner the item is running, but two drivers can both move it; only the ref is atomic.

**Without a Git remote, or when the core preflight records single-driver or local-only mode**, the committed move to work-active is the claim. Start the builder's worktree from that local claim commit, not a fetched tip, and do not push the move before the builder starts. Only with no Git remote, skip the core preflight's publish check and claim-ref authorization (steps 2 and 3) and run every other preflight step. In local-only mode all commits stay local. Since only one driver may run in the repository, use `max-parallel=1`: if parallel building was requested, build one item at a time and report why. Stop and report if another driver's session, worktree or branch for the item exists. Why: a local commit is not atomic across drivers, so a second driver could build the same item.

## Held by line

The driver holds the item, not its builder: in the commit that moves the item to work-active, or the first commit when it resumes an item already there, it writes `Held by: <tool> <session> since <YYYY-MM-DD HH:MM> <UTC or +HH:MM>` under the item's header lines (its agent tool, its session name or id without spaces, the time it started), replacing any line a stopped driver left. It removes the line in the commit that parks, defers or finishes the item, and before ending a run that leaves the item in work-active. The builder in its worktree never writes it. Why: the owner's dashboard shows who holds each active item and since when, and a line left behind looks like a live run.

## Build

The item gets one builder, which works its steps in order in one worktree for the whole item, with the item and step as its contract in place of an issue and Agent Brief. For each step:

1. the builder implements the step as the core's build contract says and returns `READY_FOR_REVIEW` for that step;
2. the driver runs the deterministic pre-review gate and full review on the step's diff, with rework as the core says;
3. on approval the driver lands the step (core landing): it commits the step's reviewed diff, and in the same commit ticks the step's checkbox in the item, records the step's `Review:` and `Gate:` lines (below) and reruns the project's work index script to regenerate the work index;
4. the next step starts from that commit in the same worktree.

A step whose `Blocked by:` names an earlier unfinished step waits for it; the order of the steps is the build order. A step deferred under the core's rework rules defers the whole item: record the Agent Rework Brief in the item under the step and remove its `Held by:` line, keep the item in work-active, and release the claim only after the recovery bundle validates. A replan stop (two blocking reviews in a row on new sequences, `bc-code-review`'s Review loops) is recorded the same way, plus the `Replanning:`, Replan notes and `Rounds:` lines that rule names, and the question is filed as for a park; the item stays in work-active.

## Review and Gate lines

Every review verdict and gate run on a step is one line in that step's Notes, each on its own indented line under the step, oldest first, kept when a later round passes:

- `Review: <approved | changes requested> by <reviewer> <YYYY-MM-DD>`, one per reviewer verdict, where `<reviewer>` names who reviewed (the reviewer role or agent, `tier-1`, or `owner`);
- `Gate: <pass | fail> <command> at <commit> <YYYY-MM-DD>`, one per run of the deterministic pre-review gate or the project's check command, where `<commit>` is the short SHA the checked tree was built on (`HEAD` when the gate ran).

The driver writes them, and raises the item's `Rounds:` line for each blocking review, in the landing commit for a passed step and in the deferring commit for a deferred one; reviewers and the builder never edit the item. Why: the owner's dashboard reads these lines to show whether each step passed review and the gate, and a result kept only in the run's artifacts is gone once the run is cleaned up.

## Park

When the item needs an owner decision (`HUMAN_BLOCKED`), park it in one commit. A decision that blocks only a later step does not stop the steps before it: claim the item, build and land those steps, and park when the build reaches the blocked step. Why: landed steps are useful work the owner's answer does not change. To park:

- move it back to work-planned;
- add the line `Waiting on owner: <question>`, phrased so the owner can answer it: the decision first, the options and what each leads to, then the evidence;
- remove its `Ready for agent:` line;
- tick only steps that landed and keep their commits;
- remove its `Held by:` line;
- run the work index script.

File the question where the owner sees questions: the project's or machine's instructions name the place, and the private overlay may name the tool. If no place is named or the named place cannot be used, the parked item's `Waiting on owner: <question>` line is the fallback; include the exact question and item in the run report. Then release the claim and its worktree as the core says for a blocked unit without useful local work, or keep a recovery bundle when the step has useful work. Why: the work item shows it is waiting even without a separate question destination.

## Resume

When the owner answers, write the answer into the item, next to the step it settles or under its requirements, delete the `Waiting on owner:` line, and restore `Ready for agent: yes`; run the work index script and commit. The item is then eligible again and resumes at its first unticked step. Only the owner's answer restores the ready line; a driver never restores it on its own judgement.

## Finish

After the last step lands, finish the item in one commit: fill its `## Outcome` with what landed (the step commits and the validation; this commit cannot cite its own SHA) and end it with the `Spent:` line, remove its `Held by:` line, `git mv` it into the work-done month folder `<YYYY-MM>/` (create it when missing), regenerate the work index, and commit and push as the core's landing does. Then release the claim and worktree.

The `Spent:` line comes from the spent script beside the work index script: run `python3 .bc-agent/scripts/work_spent.py <item-name>` in the main checkout and paste the line it prints, unchanged, as the last line of `## Outcome`, for example `Spent: 2h 10m active, 3.4M tokens, $5.20 (estimated; pi 3 sessions, claude-code no files, codex 0 sessions; other tools not counted)`. It estimates the item's active time, tokens and cost from the agent tools' session files; never write or adjust the figures yourself. A project without the script gets no `Spent:` line. Why: the owner's dashboard shows what each item cost, and a guessed figure is worse than none.

## Report

Report, per item: steps landed with commits, the item finished or parked (with its question and where it was filed), and any step deferred.
