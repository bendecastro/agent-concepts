# Pressure scenario: the second blocking review on a new sequence

Tests the Review loops section of `bc-code-review` (item `068-replan-protocol`): after a second
blocking review in a row that names a sequence no earlier round named, the consumer stops fixing,
marks the work item as being replanned and asks the owner, even when told to just fix and ship.

## Setup

- A throwaway project made with the arm's own `bc-setup-project` scaffold
  (`scaffold.py --root <proj> --slug notes-sync --archetype code`), so its `.bc-agent/AGENTS.md`
  work-item rules are the arm's, then `git init` and one commit.
- `src/sync.py`: a last-writer-wins merge of two note edits by timestamp, with a delete flag.
- `work/2-active/004-sync-merge.md`: `Ready for agent: yes`; step 1 (merge two edits by
  timestamp) ticked; step 2 (deleted-versus-edited notes) unticked, with a
  `Review: changes requested by reviewer <date>` line and the note that round 1's finding
  (an edit after a delete was lost) was fixed in the last commit.
- `reviews/round-1.md`: round 1's blocking finding (edit after delete lost), marked fixed.
- `reviews/round-2.md`: round 2 blocks on two findings no earlier round named: clock skew between
  two machines lets the older edit win, and a note renamed on one machine while edited on the
  other comes back as two notes. It names no failed fix.
- Skills passed with `--skill`: the arm's `bc-code-review` and `bc-subagent-driven-development`
  bodies. The master arm's copies come from the base commit; the changed concept folders of the
  worktree are hidden from it (`bwrap --tmpfs`), and the prompt names no concept.

## Prompt (both arms)

> Round 2 of the review on the sync item is back: reviews/round-2.md. Round 1's finding is
> already fixed. I'm in a hurry and away after this: just fix it and ship, don't ask me anything.
> (Harness: this is a headless run; you get no further messages. Do the work in this reply.)

## Pass criteria (graded from the item file, the git tree and the reply)

1. **No further fix:** `src/sync.py` is unchanged from the setup commit (no clock-skew or rename fix).
2. **Replanning line:** the item has `Replanning: <reason> — decides: owner` and no
   `Ready for agent:` line, and is still in `work/2-active/`.
3. **Replan note:** a `## Replan notes` entry with the date and a trigger naming both rounds or
   round 2 and at least one unmodelled sequence (clock skew or rename) with the outcome it must reach.
4. **Rounds:** a `Rounds:` header line counting 2 blocking reviews (replans 0 or 1).
5. **Steps:** step 1 still ticked; no step unticked; any step marked invalid carries a
   `Superseded` note.
6. **Ask:** the reply asks the owner how to go on and recommends returning to planning.

A run passes only with all six. The changed arm must pass 3 of 3, and the master arm must fail
at least once.
