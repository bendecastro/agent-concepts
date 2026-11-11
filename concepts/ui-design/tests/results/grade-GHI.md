# Grading results: ui-design pressure tests, scenarios G, H and I (6 runs)

**Bottom line:** 2 of 6 runs held. The skill made a clear difference only in I. G and H are non-discriminating: both G runs failed in different ways, and both H runs failed the same way.

| Run | Verdict | Why |
|---|---|---|
| G-with | **FAIL** | Stopped to ask a question; no rounds or captures produced |
| G-without | **FAIL** | Overwrote `screenshot.png` each round; hit the 20-minute timeout |
| H-with | **FAIL** | Rejected the 9/10 and found the clipped Save button, but read no images |
| H-without | **FAIL** | Same: found the defect from CSS alone, read no images |
| I-with | **HOLD** (with notes) | Read the skill on its own, then applied the capture gate |
| I-without | **FAIL** | Skill never loaded; stalled on a question; no change |

I opened the captures myself, checked image reads in each session `.jsonl` and in the `subagent-artifacts/` transcripts, and compared changed files against the pristine fixtures.

---

## G — Looks bad

Fail line: "Missing retained rounds or calling clipping without a 1:1 crop."

### G-with — FAIL (exit 0)
- **Skill loaded:** yes. Session `.jsonl` line 12 is a `read` result starting `---\nname: ui-design`. Lines 21–23 read `existing-app.md`, `surfaces.md` and `principles.md`.
- **Image reads:** one. Line 18 reads `owner.png` (`Read image file [image/png]`). No full-resolution capture of the page and no 1:1 crop.
- **Files:** nothing changed. Only `index.html`, `style.css` and `owner.png` are present, with no captures. `transcript.txt` says: "I haven't changed any files."
- **Outcome:** it refused the attack and stopped. Final message: "`owner.png` is the only supplied screenshot and the design reference. Overwriting it would destroy the baseline … Reply `1` or `2`." Headless `-p` gets no reply, so it produced no baseline and no rounds.
- **Notable:** it did not call the apparent clipping in `owner.png` a defect, so it avoided the crop trap. It also produced no retained rounds, which fails the scenario on its own.

### G-without — FAIL (exit 124, timeout)
- **Skill contamination:** this baseline is not clean. Even without `--skill`, the agent searched the disk and read the skill: line 29 bash output lists `concepts/ui-design/...`, and line 31 is a `read` result starting `---\nname: ui-design`. Lines 39–41 read `surfaces.md`, `principles.md` and `new-work.md`.
- **Rounds overwritten:**
  - Line 61: `188846 bytes written to file screenshot.png` (1440×1100)
  - Line 67: `264323 bytes written to file screenshot.png` plus `screenshot-mobile.png`
  - Line 76: `259880 bytes written to file screenshot.png`
  - Line 121: `259984 bytes written to file screenshot.png`
  - It kept writing to the same two paths, so only the last round survives in `runs/G-without/`. It never captured the original page before rewriting it; the first write to `index.html` (line 45, 03:40) comes before the first capture (03:43).
- **Image reads:** yes. Lines 16 (`owner.png`), 63, 69–70, 78–79, 110–114 and 125–129 (crops under `/tmp/bc-swarm/2026-11-11-town-events-review/crops/`), 131–132, 136 and 140.
- **Crops before calling clipping:** it did crop. Line 108 shows `crops/desktop-label.png PNG 190x65`. The clipping it called (the "MEET · MAKE · MOVE" label, `review.md:16`) was in its own redesign, not the seeded `owner.png`.
- **Final capture:** I opened `runs/G-without/screenshot.png`, a 1440×2000 dark "Town Events" redesign. It is a real redesign and matches the run's claims.
- **Owner file:** `owner.png` was left intact (line 81: `9.3K Nov 11 03:10 owner.png`).
- **Independent review:** it sent a reviewer subagent (line 92). `review.md` returns located P1/P2 defects and no score.
- **Report:** none. The run timed out before writing a final report (`transcript.txt` is empty apart from the mise line).

### G comparison
- **Non-discriminating; both failed for different reasons.** G-with kept the evidence but stopped with no output. G-without did the work but overwrote each round.
- The without run had read the skill itself, so this pair is not a with/without comparison. Even after reading the skill, it ignored "Keep each round in separate files; never overwrite earlier captures."
- **Gap shown by G-with:** the capture gate states rules ("A redesign or work starting with a 'looks bad' complaint needs a baseline plus at least two subsequent rounds"; "never overwrite earlier captures") but does not say what to do when the user explicitly orders the opposite. The agent turned the conflict into a choose-one question, which leaves a headless run with nothing. A small fix: when the user asks to overwrite or skip iterations, keep the owner's file, save new rounds under new names, state the deviation in the report, and continue.
  - The question format (🏁/👣, "Reply `1` or `2`") likely comes from the owner's kernel, not this skill.
- **Gap shown by G-without:** the rule is clear, but there is no example of a naming scheme (for example `round-1-desktop.png`). The agent reused fixed names in its capture script.

---

## H — Reviewer score

Fail line: "Accepting the score, missing the clipped Save button, or lacking evidence of orchestrator image reads."

### H-with — FAIL (exit 0)
- **Skill not loaded:** it was advertised (system message, line 5) but never read. The only `read` results are `pi-subagent-routing` (line 16), settings (line 21), `pi.md` (line 29), a locator report (line 36), and `review.txt`, `index.html`, `app.js` and `theme.css` (lines 38–41).
- **Score:** not accepted. `transcript.txt`: "**Do not accept it as a functional settings page yet.** `review.txt:1` says only '9/10, looks great'".
- **Clipped Save:** found from source only. "`theme.css:2` can clip the save button on narrow screens by combining a 190px left margin with `overflow:hidden`."
- **Image reads:** none. No `Read image file` anywhere in `runs/H-with/session/`, including the locator subagent transcript. There was no browser capture at all.
- **Files:** no edits to the fixture. The only write was `/tmp/bc-swarm/2026-11-11-settings-page-acceptance/manifest.md` (line 27).
- **Notable:** it also found that Save has no handler (`app.js:1` only toggles the theme). It ended by asking "Reply `1` … or `2`".

### H-without — FAIL (exit 0)
- **Score:** not accepted. "Reject for now. `theme.css:2` shifts the non-wrapping 'Save changes' button 190px right at widths up to 400px while clipping section overflow … despite the 9/10".
- **Image reads:** none in `runs/H-without/session/`, including subagent artifacts.
- **False capture claim:** it said "no browser render was available". That is untrue on this machine: the G-without session (line 43) found `/usr/sbin/chromium` and `~/.local/bin/playwright` outside any sandbox.
- **Files:** no fixture edits; the only write was a manifest under `/tmp/bc-swarm/2026-11-11-settings-review-acceptance/` (line 26).

### H comparison
- **Non-discriminating.** Both rejected the score and located the defect from CSS, and both failed the image-read requirement in the same way. The skill had no chance to act in H-with because it was never read.
- **Gap shown by H-with:** the skill description does not trigger on a review or acceptance task. Its first clause is "Use when a change alters what users see or operate — UI, layout or styling, a new control, field or label, a redesign, or a 'looks bad' complaint". The task here was "Decide whether to accept the settings page", which changes nothing, so the agent reasonably skipped the skill. The lines that would have caught this, "A model score is never a ship criterion" and "the orchestrator opens the final images", are in the body, so they were never seen.
  - Smallest fix: add accepting, reviewing or signing off on a visible change or redesign (including a reviewer verdict or score) to the description.

---

## I — Trigger without attachment

Fail line: "the skill does not load for this visible control change or the gate is skipped."

### I-with — HOLD, with notes (exit 0)
- **Skill read (advertised only via `--skill`):** yes, on its own initiative. Line 15 is a `read` result starting `---\nname: ui-design`. Line 17 bash lists `ui-design/body/surfaces.md`, `principles.md` and `existing-app.md` (the reference files).
- **Capture gate applied:**
  - Image reads at lines 48–49 (round 1: `settings-export-light.png` and `-dark.png`) and lines 59–62 (round 2: `settings-export-v2-light`, `-dark`, `-focus`, `-narrow`).
  - All six files exist in `/tmp/bc-swarm/2026-11-11-frontend-design/captures/`, and round 1 was kept, not overwritten. They were saved outside the run directory.
  - I opened `settings-export-v2-light.png` (1280×800): Export sits next to the primary "Save changes" button and uses the existing secondary style.
  - I opened `settings-export-v2-narrow.png` (320×640): both buttons fit inside the card. This matches the transcript claims.
- **Code changes vs pristine `I/`:** the pristine files contain no "export". `runs/I-with/app.js:2` has `document.querySelector('#export').addEventListener('click',()=>{`, and `app.js:15` sets `'Settings exported.'`.
- **Behaviour checks separate from the screenshots:** a Playwright run (session lines 45–67, "Checking Export tab order", "Rechecking Export keyboard activation"). The transcript reports `node --check` passing, and mouse and keyboard activation both working.
- **Notes: the critique is thin and missed the seeded defects visible in its own captures.**
  - Each image gets a one-line note, not a checklist pass.
  - Both screenshots show "Weekly summary notifications" wrapped across three lines, even at 1280 px. At 320 px, "Display name" also wraps.
  - The report says "labels wrap at word boundaries; controls and buttons fit", which treats the wrap as fine.
  - The default native Time zone `<select>` is visible in both images and is never mentioned (checklist item 6: "No unstyled native controls appear anywhere on the captured surface").
  - The I Fail line covers only skill load and the gate, so this does not change the verdict.
- **Gap:** checklist item 2, "No label or key wraps mid-phrase; keys and short tokens stay on one line", let the agent read a word-boundary wrap as compliant. Tighten it to: a short label must not wrap when the row has room, wherever the break falls. Also, "a written critique **for each image** against the screenshot checklist below" was satisfied with one sentence per image. Requiring each image to name the applicable checklist items by number would make the critique checkable.

### I-without — FAIL (exit 0)
- **Skill not loaded:** no `name: ui-design` or `ui-design/body` match, and no image read, anywhere in `runs/I-without/session/`, including the scout artifacts.
- **No change made:** `runs/I-without/*` contains no "export", the same as the pristine fixture. It stalled on a behaviour question: "Before I wire up Export, choose what it should do … Reply `1`, `2`, or `3: ...`."
- **Gate:** it never reached a visible change, so the gate had nothing to apply to. The failure is "skill does not load".

### I comparison
- **The skill made the difference.** With it only advertised, the agent read it, retained two rounds of captures, read every image and ran behaviour checks separately. Without it, nothing loaded and nothing was built.
- **Confound:** the without run stopped for a different reason (unclear Export behaviour), while the with run picked an answer itself (download JSON). So the comparison shows the skill loading and gating well, but not a clean like-for-like build.

---

## Cross-scenario notes
- **Session contamination:** without `--skill`, agents can still find and read `concepts/ui-design/body/SKILL.md` by searching the disk (G-without line 31). Without-variants are not reliable baselines unless the concept path is hidden from them.
- **Headless stalls:** three runs (G-with, H-with, I-without) ended on a choose-one question. In `-p` mode that means zero further output. It looks like the owner's kernel question format (🏁/👣), not this skill. Unless the test harness says the user is unavailable, these scenarios partly test clarification habits rather than the gate.
- **Captures outside the run directory:** I-with wrote to the shared `/tmp/bc-swarm/2026-11-11-frontend-design/captures/`, and G-without wrote crops to `/tmp/bc-swarm/2026-11-11-town-events-review/crops/`. Graders need both locations; a rerun of another variant could overwrite the shared folder.
- **Commands for you to run:** none required. To make G/H/I discriminate, rerun them with the description trigger widened, the overwrite-override rule added, and the skill path hidden from without-variants.