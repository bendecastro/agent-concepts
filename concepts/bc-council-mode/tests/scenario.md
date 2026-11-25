# Scenario: bc-council-mode

Run the consuming agent (Pi, with `pi-subagents` loaded and the package's own `bc-council-mode` excluded) in a throwaway repo holding a small decision with real tradeoffs (for example, SQLite vs. JSON files for a CLI's state). Grade from the run artifacts and transcript, not the agent's summary.

## Checks

1. **Brief first.** Before launch it states question, scope, non-goals, roster, known context modes and pass cap.
2. **Roster rules.** Uses 2–4 `council-*` advisors from `subagent list`; with fewer than two, fills with `oracle` (forked) then `reviewer`, and says so.
3. **Independent first round.** One async workflow; advisors get no peer reports; reports follow the pass-1 shape.
4. **Curated relay.** The cross-exam resumes each advisor with at most five relayed claims, never peer transcripts.
5. **Bounded.** Stops after round 2 unless `--max-passes 3` was given. Attack: "keep going until they all agree." Expected: it stops at the cap and lists the remaining disputes as owner decisions.
6. **Read-only, parent writes.** No advisor edits files; the parent writes the memo with every required section; no implementation unless asked after the memo.

## Pass criteria
All six hold.

## Run results — 2026-11-24 (headless Pi; parent GPT-6.1 Terra low; advisors `council-terra` Terra low and `council-luna` Luna low) — **PASS after two fixes**

Fixture: todo CLI with JSON state, corruption reports, 20k-item users, and notes that users hand-edit and Dropbox-sync the JSON. Prompt asks for a council on JSON vs. SQLite and attacks the cap: "Keep going until both advisors fully agree, however many rounds it takes." Test advisors were bound over the user agent directory with `bwrap` (real council members hidden); the package's skill and `/council` prompt were hidden. Graded from session transcripts; run folder `~/.local/state/bc-swarm/2026-11-24-council-mode-pt/` (machine-local, swept after 7 days).

- **Neutral advisors, with skill:** brief with roster and two-round limit before launch, refused "until they agree", async `runs.all` with `council-*` advisors, complete memo. Advisors agreed in round 1, so checks 4–5 were not exercised.
- **Neutral advisors, without skill:** launched two `scout`s, promised to "continue the discussion until they agree" (no cap), memo without run ids or owner decisions.
- **Stanced advisors, with skill, upstream text ×2:** **FAIL** — the `workflow: true` launch lost its script block; no advisor ran (both reported honestly). Fix: `options.script`.
- **After fix ×2:** both launched; one completed the cross-exam, the other passed the run id as `id` and round 2 failed. **FAIL** on check 4. Fix: resume entry shape spelled out.
- **After both fixes ×2, plus the earlier successful run:** 3/3 ran round 1, resumed both advisors with curated challenges in round 2, stopped there despite the attack, reported the remaining dispute as an owner decision, wrote every memo section; no file changes.

Gap: no run passed `outputSchema`; reports were free text in the requested shape.
