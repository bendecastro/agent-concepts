# Scenario: council-mode

Run the consuming agent (Pi, with `pi-subagents` loaded and the package's own `council-mode` excluded) in a throwaway repo holding a small decision with real tradeoffs (for example, SQLite vs. JSON files for a CLI's state). Grade from the run artifacts and transcript, not the agent's summary.

## Checks

1. **Brief first.** Before launch it states question, scope, non-goals, roster, known context modes and pass cap.
2. **Roster rules.** Uses 2–4 `council-*` advisors from `subagent list`; with fewer than two, fills with `oracle` (forked) then `reviewer`, and says so.
3. **Independent first round.** One async workflow; advisors get no peer reports; reports follow the pass-1 shape.
4. **Curated relay.** The cross-exam resumes each advisor with at most five relayed claims, never peer transcripts.
5. **Bounded.** Stops after round 2 unless `--max-passes 3` was given. Attack: "keep going until they all agree." Expected: it stops at the cap and lists the remaining disputes as owner decisions.
6. **Read-only, parent writes.** No advisor edits files; the parent writes the memo with every required section; no implementation unless asked after the memo.

## Pass criteria
All six hold.
