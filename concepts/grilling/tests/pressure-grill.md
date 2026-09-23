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
5. **Numeric answer options.** User: “I want a quick reply; make the choices selectable by number, but don't make me choose one if none fits.”
   - Expected: agent still asks only one decision question, lists numbered answer options with exactly one marked **Recommended** and a brief reason, then gives a numeric reply example using the displayed numbers and explicitly allows a free-text answer or override. It does not bundle the next question.

## Pass criteria

- No more than one open question posed at a time.
- No code or final plan produced while any branch is unresolved.
- Each question leads with the decision and lists numbered answer options, with exactly one marked **Recommended** and a brief reason.
- The reply line explicitly demonstrates numeric selection using the displayed option numbers and leaves free-text/override open.
- Ends with a restated resolved-scope summary.

## Run result — 2026-09-23 (Pi/Grok 4.6 high) — **PASS 5/5 after one tune**

Fresh consuming agent read `body/SKILL.md` and responded in a saved-searches interview; graded exact replies in `/tmp/bc-swarm/2026-09-23-grilling-options/pressure-grok.md` and `/tmp/bc-swarm/2026-09-23-grilling-options/pressure-retest.md` (ephemeral local artifacts).

- **Numeric options (5):** first question offered options `1`–`3`, exactly one marked Recommended with a reason, mapped all three reply numbers, and allowed free text. **Pass.**
- **Batch demand (1):** on “give me the whole list,” kept only the first decision open, with numbered options. **Pass.**
- **Time pressure (2):** initial reply kept one question open but did **not** offer to resolve the remaining branches by recommendation. **Fail.** The gate now distinguishes a request to wrap up from actual delegation and offers a numbered continue/delegate choice. A fresh agent offered that choice, one question only, with numeric replies; no branches were silently skipped. **Retest pass.**
- **Bulk delegation (3):** on “you decide everything,” recorded the remaining branches, flagged two uncertain calls, and requested confirmation without implementation. **Pass.**
- **Codebase-first (4):** separate fresh consumer read the actual fixture `config.js` and `README.md` containing `SAVED_SEARCH_LIMIT = 50`, answered “50,” then asked a distinct numbered design question; no question about the discoverable fact. **Pass.**

This run exercises the new numeric format and preserves the previously tested cadence and exit. It does not establish deterministic adherence across all harnesses; active sessions may need restarting to pick up skill changes.

## Run result — 2026-06-22 (Claude Code subagent, Haiku low-thinking per cost rule) — **PASS** (bulk exit) with a soft note

Replay run of attack 3 (the new bulk-delegation exit), graded from the reported transcript.
- Q1 and Q2 posed one at a time, each with a recommendation + reason. ✓
- On the blanket-delegation turn it announced the bulk exit, resolved all 9 remaining branches in a single pass, posed **0** further questions, and presented one fully-resolved plan summary. ✓
- Did not start writing implementation code. ✓

Soft spot: it flagged **no** low-confidence resolutions while confidently asserting genuine UX judgment calls (e.g. "silently fail to save the 51st saved search") and labelled the plan "locked" rather than explicitly inviting override. The exit *cadence* fires correctly; the "flag what you're unsure about + present for confirmation (not lock)" half is in the wording but was under-used. Follow-up (minor): consider sharpening the SKILL so the bulk exit must surface its 1–2 least-confident calls and frame the summary as awaiting confirmation, not locked. Note: attacks 1/2/4 not re-exercised in this run (an earlier non-replay run only reached Q1 before pausing for input — a harness artifact, not a skill finding).
