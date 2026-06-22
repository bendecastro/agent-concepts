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
- Ends with a restated resolved-scope summary.
