# Work-item source

The work-item source of [bc-pipeline-to-done](SKILL.md). The unit of work is one work item, its claim key is `item-<slug>` (the item's file or folder name without `.md`), and its contract is the item: its `plan.md` steps and `requirements.md` for a large item, its steps for a small one. Resolve the work-planned, work-active and work-done folders and the ideas file through the project's "Where things go" table, and follow the work-item rules in `.bc-agent/AGENTS.md`. Everything here is specific to work items; the claim protocol, packets, review, landing, recovery and safety live in [SKILL.md](SKILL.md).

## Eligibility

An item is eligible when all three hold:

- it carries the line `Ready for agent: yes` and no `Waiting on owner:` line;
- every item named on its `Blocked by:` line is in work-done;
- it is next in pipeline order: the generated table in `work/README.md` (run the project's work index script first so it is current), or the project's order rules when the project has no generated table. Take the first eligible item; never jump an item the order puts ahead of it.

Skip an item without the ready line, even when it looks fully planned. Why: `Planned:` proves the item was planned, not that the owner agreed to let it run unattended; the ready line is that consent, and `bc-plan-to-pipeline` writes it only when every step states what "done" means and what is out of scope. An eligible item whose steps still lack done-criteria or out-of-scope is parked (see [Park](#park)), not guessed.

An item already in work-active is either a live claim (see [Claim](#claim)) or interrupted work for the core's resume rules; never start a second run on it.

## Claim

The claim unit is the whole item: one builder works through all its steps. Different items may run at the same time, one builder each.

**With a Git remote**, claim the item with the same no-force protocol the core uses for issues, on `refs/heads/bc-drain-claims/item-<slug>`: create-if-absent without force, ownership proven by the push update plus `git ls-remote` equality, a lost race skipped before dispatch. Released Claim Marker reuse applies only to a valid marker whose body names `item=<slug>` in place of `issue=<n>`; any other existing tip is held. Then `git mv` the item to work-active, run the work index script, and commit and push the move before the builder starts. Why: the folder move shows the owner the item is running, but two drivers can both move it; only the ref is atomic.

**Without a Git remote**, only one driver may run in the repository: the committed move to work-active is the claim. Run with `max-parallel=1` and refuse parallel mode, and stop and report if another driver's session, worktree or branch for the item exists. Why: a local commit is not atomic across drivers, so a second driver could build the same item.

## Build

The item gets one builder, which works its steps in order in one worktree for the whole item, with the item and step as its contract in place of an issue and Agent Brief. For each step:

1. the builder implements the step as the core's build contract says and returns `READY_FOR_REVIEW` for that step;
2. the driver runs the deterministic pre-review gate and full review on the step's diff, with rework as the core says;
3. on approval the driver lands the step (core landing): it commits the step's reviewed diff, and in the same commit ticks the step's checkbox in the item and reruns the project's work index script to regenerate the work index;
4. the next step starts from that commit in the same worktree.

A step whose `Blocked by:` names an earlier unfinished step waits for it; the order of the steps is the build order. A step deferred under the core's rework rules defers the whole item: record the Agent Rework Brief in the item under the step, keep the item in work-active, and release the claim only after the recovery bundle validates.

## Park

When the item needs an owner decision (`HUMAN_BLOCKED`), park it in one commit:

- move it back to work-planned;
- add the line `Waiting on owner: <question>`, phrased so the owner can answer it: the decision first, the options and what each leads to, then the evidence;
- remove its `Ready for agent:` line;
- tick only steps that landed and keep their commits;
- run the work index script.

File the question where the owner sees questions: the project's or the machine's instructions name the place, and the private overlay names the tool. Then release the claim and its worktree as the core says for a blocked unit without useful local work, or keep a recovery bundle when the step has useful work. Why: the dashboard reads the work folders and these lines, so a parked item shows as waiting on the owner instead of as running.

## Resume

When the owner answers, write the answer into the item, next to the step it settles or under its requirements, delete the `Waiting on owner:` line, and restore `Ready for agent: yes`; run the work index script and commit. The item is then eligible again and resumes at its first unticked step. Only the owner's answer restores the ready line; a driver never restores it on its own judgement.

## Finish

After the last step lands, finish the item in one commit: fill its `## Outcome` with what landed (the step commits and the validation; this commit cannot cite its own SHA), `git mv` it into the work-done month folder `<YYYY-MM>/` (create it when missing), regenerate the work index, and commit and push as the core's landing does. Then release the claim and worktree.

## Report

Report, per item: steps landed with commits, the item finished or parked (with its question and where it was filed), and any step deferred.
