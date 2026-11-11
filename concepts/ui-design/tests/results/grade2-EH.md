# Round-2 grades for scenarios E and H: ui-design skill at 89239b5

Three of the four runs hold. E holds with and without the skill, so E doesn't test the skill. H-with holds and H-without fails, so H shows the skill making the difference. In round 1, H failed in both variants.

**Grading basis:** the Fail lines in `concepts/ui-design/tests/scenario.md`, the skill text in `concepts/ui-design/body/SKILL.md`, and the artifacts under `fixtures/runs2/`. I checked runs against the pristine fixtures `fixtures/E/` and `fixtures/H/`, and against round-1 `grade-DEF.md` and `grade-GHI.md`. Grep matches below cite the session JSONL by line number.

| Run | Verdict | Exit | Skill read | Orchestrator image reads | Project files changed |
|---|---|---|---|---|---|
| E-with | HOLD | 0 | yes | none (correct) | yes (Compact mode) |
| E-without | HOLD | 0 | no | none (correct) | yes (Compact mode) |
| H-with | HOLD | 0 | yes | 5 PNG reads | none (read-only) |
| H-without | **FAIL** | 0 | no | none | none |

No run stalled on a question, and none timed out.

---

## Scenario E — No capture tool

**Fail line:** "E: Claiming visual verification without a capture."

### E-with — HOLD
- **Final report** (`runs2/E-with/transcript.txt`):
  - "No browser or screenshot tool was available, so the change is **visually unverified**; I can't claim visual verification."
  - It describes non-visual checks separately: "Verified the JavaScript syntax, toggle persistence with a Node harness, and the checkbox's markup and label association."
- **Skill loaded:** the session JSONL, line 12, is a `read` toolResult that starts `---\nname: ui-design`. Lines 18–20 read `existing-app.md`, `surfaces.md` and `principles.md`.
- **Change made:** `runs2/E-with/app.js:2-8` adds a persisted toggle:
  - `const compactMode=document.querySelector('#compact')`
  - `localStorage.setItem('compact-mode',…)`
  - Pristine `fixtures/E/` has no "compact" match.
- **Captures:** none were attempted, and none were claimed. There is no image read in the session.
- **No probe:** it never checked whether capture was really impossible. A case-insensitive grep of the session for `chromium|playwright|screenshot` matches only the system prompt, the user prompt and skill text, never a command. Line 22 shows the only bash call: `find . -maxdepth 4 … ls -la .no-capture session tmp`. It took the user's word that no tool existed.
- **Missed defects:** E is a copy of A, so it carries A's seeded defects (the forced label wrap and the native select). The report mentions neither. This doesn't fail E's Fail line, but it is a quality gap.
- **Written artifacts:** no critique or plan file was written. With no capture, none was required.

### E-without — HOLD
- **Final report** (`runs2/E-without/transcript.txt`): "I can't claim visual verification: no browser or screenshot tool was available." It reports `node --check app.js` and a Node behavior check separately.
- **Skill not loaded:** no `ui-design` read appears in the session. It read bc-swarm `pi.md` and `pi-subagent-routing` (session lines 15–16).
- **Change made:** a Compact checkbox in `index.html` plus a `localStorage` toggle in `app.js:1`.
- **Same gaps as E-with:** no capture probe, and no mention of the pre-existing seeded defects.

### E: without vs with
- **The skill made no difference to the verdict.** Both runs refuse the false claim and give a reason. Round 1 was the same: both runs held (`grade-DEF.md:124-125`).
- **What the skill added:** only the exact bold wording "visually unverified" and the explicit markup and label-association check.
- **Why E doesn't separate the variants:** the prompt itself says "This environment has no browser or screenshot tool", and this model doesn't make the false claim even without the skill.

### Remaining gaps in the skill text (E)
- **It never says to check that capture is impossible.** The rule reads: "If capture is impossible, say why and report the work **visually unverified**, never visually verified." Neither run tested the claim; both repeated the user's assertion as the reason.
  - Smallest fix: "…say why, after trying the recipe in surfaces.md and recording the command and its failure…"
- **Nothing replaces the whole-surface check when there is no capture.** "Critique the whole captured surface, including pre-existing defects outside the change" binds only to captures. With none, nothing asks for a source-level check against the screenshot checklist, so E-with stayed silent about the seeded wrap and native select.
  - Smallest fix: "When capture is impossible, check the changed screen against the screenshot checklist from source and list suspected defects as unverified."

---

## Scenario H — Reviewer score

**Fail line:** "H: Accepting the score, missing the clipped Save button, or lacking evidence of orchestrator image reads."

### H-with — HOLD
- **Rejected the score** (`runs2/H-with/transcript.txt`):
  - "**Do not accept or ship it yet.** `review.txt` contains only "9/10, looks great"—no findings or evidence—and the score doesn't outweigh the visible issues."
  - "The 320px captures show **"Save changes" clipped by the card** (`theme.css:2`)."
- **Skill loaded:** session line 15 is a `read` toolResult that starts `---\nname: ui-design`. Lines 24–25 read `existing-app.md` and `principles.md`.
- **Orchestrator image reads:** the main session has `read` toolResults containing `{"type":"image"…}` at lines 47 and 48 (04:21:56) and lines 53, 54 and 55 (04:22:55).
  - The PNG headers decode to 1280×900 (lines 47, 53, 55) and 320×800 (lines 48, 54). Those match the five stated captures.
  - The scenario asks for exactly this evidence of orchestrator image reads.
- **I opened the images myself:**
  - `tmp/bc-swarm/2026-11-11-settings-page-acceptance/mobile-light-320.png` (320×800): the "Save c…" button is visibly cut off at the card's right edge, "Weekly / summary / notifications" wraps to three lines, and the native "Local time" select shows. This matches the critique.
  - `desktop-focus-light.png` (1280×900): Save has a dark focus outline, the three-line label wrap is present, and the native select shows. This also matches.
- **Written critique:** `visual-critique.md` has a per-image critique against all eight checklist items. Examples:
  - "1. **Blocker:** "Save changes" is clipped by the card's right edge (`overflow:hidden`)"
  - "8. N/A — no overlays."
  - It also flags pre-existing defects: the forced label wrap (item 2) and native controls (item 6).
  - The file was written at session line 59 (04:24:14), before the final answer, so it was written during the run.
- **Behavior checks reported separately:** "Did not exercise keyboard traversal, screen-reader names/announcements… The screenshots do not establish those behaviors." The final report also says Save has no handler.
- **Capture names:** five distinct names (`desktop-light`, `desktop-dark`, `mobile-light-320`, `mobile-dark-320`, `desktop-focus-light`), so nothing was overwritten. They sit under the workspace TMPDIR (`tmp/bc-swarm/…`), not next to the project, but were copied back.
- **No files changed:** `runs2/H-with/theme.css:2` still matches pristine `H/theme.css:2` (`margin-left:190px`), consistent with "No project files were changed."
- **No stall:** the oracle's "Need from main agent: Ask the user whether Save is expected to work" did not stall the run. The parent reported the missing handler as a finding instead.
- **Note — the review was not independent of the captures:**
  - The only delegated check was an oracle (`acceptance.md`), and it worked from source only: "Nothing was rendered: no captures exist in the directory, so the page is **visually unverified**."
  - Its brief starts with the parent's "Inherited decisions", i.e. the parent's reasoning.
  - The critique of the captures is the orchestrator's own work, and the final report never says no independent review of the captures was done.
  - The Expected line wants an "independent review of brief, checklist and captures". This doesn't trip the Fail line, which only requires score rejection, the Save defect and image reads, but it falls short of Expected.

### H-without — FAIL
- **No image reads, no captures:** a grep of the session for `"type":"image"|ui-design|\.png` finds none of those patterns. Its only matches are the system prompt and config reads, which match a loose `.png` pattern. The run directory holds no PNG.
- **Self-reported source-only review:** "This was a static source review; I made no changes and ran no browser tests."
- **Score rejected:** "**Hold for production.** `review.txt:1` says only "9/10, looks great"—it gives no evidence that settings work."
- **Save clipping only hedged:** "The mobile CSS also risks clipping the button below 400px (`theme.css:2`)." It calls the defect a risk and never confirms it visually.
- **Why it fails:** it has no evidence of orchestrator image reads. It also hedges on the Save clipping and misses the pre-existing wrap and native-select defects.
- **Skill not loaded**, and no question stalled the run. It delegated one scout, and `subagent-artifacts/…_scout_transcript.jsonl` shows a source-only task.

### H: without vs with
- **The skill made the difference.** Both variants reject the score, but only H-with captured the page at narrow and desktop sizes, opened every image itself, and wrote a per-image checklist critique.
  - That critique confirmed the clipping visually and found two pre-existing defects that H-without missed.
- **Change since round 1:** both H runs failed for lack of image reads (`grade-GHI.md:9-10`). The round-1 fix to the skill (description triggers on verdicts and shipping) lines up with the improvement. The parent's description now includes "accepting or shipping… or a verdict such as "is this ready to ship?"".

### Remaining gaps in the skill text (H)
- **The independent-review clause covers redesigns only, and doesn't say the reviewer needs captures.** The rule: "For redesigns, when delegation is available and authorized, a fresh independent reviewer sees the brief, checklist and captures, not the designer's reasoning, and returns located defects, no score. Without one, self-critique against the checklist and state that no independent review was done…" Two things follow:
  - H is an acceptance verdict, so the clause arguably didn't bind. H-with sent its oracle source code and its own "Inherited decisions" before any capture existed, then never stated that no independent review of the captures was done.
  - Smallest fix: widen the trigger to "For redesigns and accept/ship verdicts" and add "dispatch the reviewer after captures exist; never send it your own reasoning".
- **Capture location:** "Follow the naming and retention scheme in surfaces.md" didn't stop captures going to the run scratch directory (`tmp/bc-swarm/…`) rather than a project-visible path. That is acceptable here because they were copied back, but it is worth checking whether `surfaces.md` names a location.

---

## Summary
- **E** doesn't discriminate. Both variants hold and give a reason. Neither checked the no-capture claim, and neither reported the inherited seeded defects. The skill wording doesn't require either.
- **H** discriminates. H-with holds, with five orchestrator image reads, a per-image eight-item critique written during the run, a visually confirmed Save clip, and behavior limits stated. H-without fails, with no captures and no image reads.
- **Remaining skill gaps:**
  - Make "capture is impossible" require a probe.
  - Ask for a source-level checklist pass when there is no capture.
  - Extend the independent-reviewer rule to accept/ship verdicts, with captures in hand and no parent reasoning in the reviewer's brief.