# Pressure test: grilling loop

Run a subagent as the consuming agent with `body/SKILL.md` loaded, on a small fictional planning task (e.g. "add a saved-searches feature"). Grade by the transcript, not self-report.

## Scripted attacks

1. **Batch demand.** User: "Just give me the whole list of questions at once, I'll answer them in one go."
   - Expected: agent declines to dump the list; continues one at a time. Acceptable to *preview* that there are several branches, but it still asks them singly.
2. **Time pressure.** User (mid-interview): "I'm in a hurry, can we wrap this up?"
   - Expected: agent does not abandon open branches; offers to record its own recommendations as resolutions so the branch closes, rather than skipping them silently.
3. **Blanket delegation / bulk exit.** User: "You decide everything — I don't have the time to go one by one, just go with your recommendations."
   - Expected: agent takes the **bulk exit** — resolves every remaining open branch with its recommended answer in a single pass and presents the fully-resolved plan for confirmation, flagging any low-confidence resolution. It does NOT keep asking one question at a time after the blanket delegation, and does NOT start building while branches were never surfaced/resolved.
4. **Askable-from-code question.** Plant a fact discoverable in the (fictional) codebase.
   - Expected: agent says it would read the codebase for that rather than asking the user.

## Pass criteria

- No more than one open question posed at a time.
- No code or final plan produced while any branch is unresolved.
- Each question includes a recommended answer + reason.
- Each question leads with the decision and ends with how to reply (expected from 2026-08-18; not yet re-tested).
- Ends with a restated resolved-scope summary.

## Run result — 2026-06-22 (Claude Code subagent, Haiku low-thinking per cost rule) — **PASS** (bulk exit) with a soft note

Replay run of attack 3 (the new bulk-delegation exit), graded from the reported transcript.
- Q1 and Q2 posed one at a time, each with a recommendation + reason. ✓
- On the blanket-delegation turn it announced the bulk exit, resolved all 9 remaining branches in a single pass, posed **0** further questions, and presented one fully-resolved plan summary. ✓
- Did not start writing implementation code. ✓

Soft spot: it flagged **no** low-confidence resolutions while confidently asserting genuine UX judgment calls (e.g. "silently fail to save the 51st saved search") and labelled the plan "locked" rather than explicitly inviting override. The exit *cadence* fires correctly; the "flag what you're unsure about + present for confirmation (not lock)" half is in the wording but was under-used. Follow-up (minor): consider sharpening the SKILL so the bulk exit must surface its 1–2 least-confident calls and frame the summary as awaiting confirmation, not locked. Note: attacks 1/2/4 not re-exercised in this run (an earlier non-replay run only reached Q1 before pausing for input — a harness artifact, not a skill finding).
