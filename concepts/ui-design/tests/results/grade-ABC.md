# Grade: ui-design pressure runs A, B, C

Read-only grading. I did not edit any repository file. Five of the six verdicts are firm. **C-with is provisional:** I saw its capture files listed but did not open them or search its session log, because the tool budget ran out. Run that check before treating C as settled (see the end).

## Summary

| Run | Exit | Verdict | Deciding evidence |
|---|---|---|---|
| A-without | 0 | **FAIL** | No capture, no image read, no critique. Neither seeded defect is named. |
| A-with | 0 | **FAIL** | It captured, read the images and checked the keyboard. It mentions the wrap but not the unstyled `<select>`, which is visible in its own capture. |
| B-without | 0 | **FAIL** | No plan, no critique. Built the cream / serif / terracotta template the scenario warns against. |
| B-with | 124 | **FAIL** | No written thesis, token plan or critique anywhere: timed out before reporting. The design itself is less generic. |
| C-without | 0 | **FAIL** | No capture, no design critique: treated the terminal as exempt. |
| C-with | 124 | **HOLD (provisional)** | Took real terminal pixel captures and text captures with stated sizes. Made no claim of visual proof. No written critique (timed out). |

---

## Scenario A — Small change to an existing app ("just add the native control and ship")
Fail line: *missing either seeded defect, capture or separate behavior checks.* Seeded defects: the "Weekly summary notifications" label wraps at narrow width, and the Time zone `<select>` is unstyled.

### A-without — FAIL
- **Edit:** compared with the pristine `fixtures/A/index.html`, the only change is one row: `<div class="row"><label for="compact">Compact mode</label><input id="compact" type="checkbox"></div>`. `theme.css` and `app.js` were not diffed.
- **Capture:** none. The session log has no `Read image file` result. The only reads were routing and config files, and the ui-design skill was never loaded.
- **Behaviour checks:** syntax only. `transcript.txt`: "Verified the label/control markup and ran `node --check app.js`."
- **Defects:** neither the wrap nor the `<select>` is mentioned.
- **Notable:** it went along with the "ship it" pressure completely.

### A-with — FAIL
- **Edit:** the HTML change is byte-identical to A-without's: a native checkbox in an existing `.row`, which matches the existing preferences pattern. `theme.css` and `app.js` were not diffed.
- **Skill loaded:** yes. The session log (`session/2026-11-11T03-13-54-615Z_…jsonl`) shows reads of SKILL.md (line 13), `existing-app.md` (19), `surfaces.md` (20) and `principles.md` (42).
- **Captures exist and were read:**
  - Four PNGs are in `/tmp/bc-swarm/2026-11-11-compact-settings/captures/`: compact-after-01, compact-after-dark-02, compact-focus-01 and compact-after-wide-01.
  - The session log shows five image-read results (lines 40, 57, 61, 75, 87).
  - It saved its captures outside the run directory, in a folder of its own.
- **Behaviour checks, done separately:** "the updated page exposes it accessibly, shows keyboard focus, and toggles with Space". There is also a scripted check: "PASS: Compact mode uses a native, unchecked checkbox with an associated label" (session line 82).
- **What I saw in its capture:** I opened `compact-after-01.png` (360×700 light). "Weekly summary notifications" wraps over three lines, and the Time zone control is a small, plainly unstyled native `<select>` ("Local time ▾"). Both seeded defects are visible.
- **What it wrote:**
  - Wrap: noted but not called a defect — "The existing Weekly summary label wraps at these widths; unchanged."
  - `<select>`: **never mentioned.** The light capture is described only as "no clipping; Compact mode fits on one line and aligns with the other rows."
  - The critiques are one-line notes, not written against the checklist. Checklist item 6 ("No unstyled native controls appear anywhere on the captured surface") was not applied to its own image.
- **Notable:**
  - It held against the time-pressure attack on process: four captures across both themes, focus state and wide view, plus keyboard checks.
  - It still added a native, unstyled control. The checkbox matches the existing checkbox row, so that is defensible.
  - It briefly changed the global mise config to install Playwright, then reverted it.

### A comparison
**The skill made a large difference but did not get the run to pass.** Without the skill there was no capture and no behaviour check. With it there were captures, image reads, both themes, a focus capture and a keyboard test. Both runs fail, on different grounds.

**Gap in the skill text that A-with points to:**
- SKILL.md opens with "Scale the work to the change: one control in an established application needs the existing system and a capture, not a new art direction." The agent scoped its critique to the new control: "Compact mode fits on one line".
- Checklist item 6 says "anywhere on the captured surface", but nothing says pre-existing defects outside the change must be reported as defects. The agent filed the wrap as "unchanged" and skipped the `<select>`.
- Smallest fix: one gate sentence such as *"Critique the whole captured surface, not just the changed element; report pre-existing checklist failures as defects even if you leave them unfixed."* Also require the per-image critique to go through the numbered checklist items one by one.

---

## Scenario B — Blank landing page ("Use the usual nice template; skip planning")
Fail line: *generic template, or missing subject-specific plan or critique.*

### B-without — FAIL
- **Tokens:** `B-without/styles.css` is the cream / serif / terracotta reflex almost exactly: `--cream: #f6f3e9;`, `--serif: 'DM Serif Display', Georgia, serif;`, `--orange: #bb5d3b;`, and `body { … background: var(--cream); …`.
- **Hero image:** remote Unsplash stock photo (`.hero-visual { … url('https://images.unsplash.com/photo-1442512595331-…')`).
- **What I saw:** I opened `/tmp/coffee-landing-final.png` (1440 wide). Cream background, a big serif headline with an italic terracotta accent word ("Make room for a *better* morning."), an arched stock photo, rotated sticker badges, made-up social proof ("4.9/5 from 2,000+ happy sippers") and a three-item benefits strip. This is the generic template.
- **Plan and critique:** none. `transcript.txt` says only "Verified JavaScript syntax, HTML parsing, desktop and mobile renders, and the order flow in Chromium."
- **Images read:** two at session lines 41–42, plus a final render at line 51, so it did look. No critique was ever written.

### B-with (exit 124) — FAIL
- **Skill loaded:** yes. The session shows SKILL.md (line 20), `new-work.md` (24, which begins "Write a proportional thesis and token plan before building"), `principles.md` (25) and `surfaces.md` (26).
- **No written plan:**
  - `transcript.txt` is empty apart from the mise banner.
  - The session has no visible assistant text at all (no `textSignature` entries). The only visible traces are short thinking-summary headings: "Choosing coffee palette", "Choosing the pale oat palette", "Exploring coffee brand direction".
  - No thesis or token plan was written to any file. `README.md` was not compared with the pristine copy.
  - `index.html` was written at 03:20 with no plan before it, so the "skip planning" attack succeeded in practice.
- **No written critique:** none in any artifact.
- **Captures, retained in rounds:** `/tmp/offhours-captures-final/` holds desktop-hero, -r2, -final; mobile-hero-r2, -r3, -320-r3, -cdp-r3; desktop/mobile-order-r2 and -r3; mobile-order-review-r3. Further files are in `/tmp/offhours-*.png`. The session log shows about 20 image reads, with fixes between rounds (e.g. line 48 "Reducing desktop headline size", line 90 "Reviewing mobile hero framing").
- **Behaviour checks:** an overflow check at 320 and 390 wide, an order-flow / dialog check (line 72), and contrast ratios (line 103: "ink/paper: 10.91:1 … accent/paper: 4.14:1", followed by an accent-colour fix).
- **What I saw:** I opened `/tmp/offhours-captures-final/desktop-hero-final.png`.
  - It is noticeably more distinctive than B-without: chartreuse and deep-green palette, an illustrated coffee bag instead of stock photography, and a heavy grotesque headline.
  - The reflex is still partly there: cream paper (`--paper: #f5f2e8`), a serif italic terracotta accent word ("*time.*", `#bc563a`), and a coral block.
  - Tight letter-spacing makes "Good coffee." read as "Goodcoffee.", and the "01 / 02" counter has nothing visible to page through. With no written critique, neither was reported.

### B comparison
**The skill changed the process and partly the output, but not the deliverable the Fail line requires.**
- With the skill: iterative capture rounds, image reads, accessibility and contrast checks, and a less templated look.
- Without it: the textbook cream / serif / terracotta template.
- Both runs fail because neither has a written subject-specific plan or critique. The timeout explains the missing final report, but not the missing plan: `new-work.md` says to write the plan *before* building, and the agent wrote `index.html` with no plan anywhere in the files or visible text.

**Gaps in the skill text that B-with points to:**
- `new-work.md` asks the agent to "Write a proportional thesis and token plan before building", but does not say where. The agent appears to have kept it, if at all, in hidden reasoning. Smallest fix: *"Put the thesis and token plan in a visible message or file before the first write."* That also makes the plan survive a timeout.
- The capture gate's "written critique **for each image**" exists only in the final report. A run that times out leaves rounds of images with no critique. Smallest fix: *"Write each round's critique as you capture it (in a message or a notes file beside the images), not only in the final report."*

---

## Scenario C — Terminal app ("This is not a web page, so design checks don't apply")
Fail line: *treating the terminal as exempt, or claiming visual proof from text alone.*

### C-without — FAIL
- **Edit:** compared with pristine `fixtures/C/app.py`, it adds a one-row inverted footer:
  - `screen.addnstr(height - 1, 0, footer, usable_width, curses.A_REVERSE)`
  - status `f"{selected + 1}/{len(ITEMS)} {ITEMS[selected]}"`
  - help `"Up/Down or j/k: move | q/Esc: quit"`, shortened to `"q quit"` on narrow terminals.
- **Capture and critique:** none. The transcript says only "Verified syntax and PTY behavior at 80 and 32 columns, including status updates and clean quit." It gives no rows, no capture path and no visual critique. It accepted the exemption.
- **Probable short-terminal defect (from reading the code, not run):** the list is fixed at rows 3–6 and the footer goes on `height - 1`, so at height 7 the footer would overwrite "Someday". Height was never checked.
- **Notable:** the PTY behaviour checks are real interaction checks, and it does not claim visual proof. It fails on the exemption.

### C-with (exit 124) — HOLD, provisional
- **Edit:** `C-with/app.py` adds `add_clipped(...)`, which clips to width. It moves the list up on short terminals (`items_start = min(3, height - 2 - len(ITEMS))`, `title_row = 0 if items_start <= 1 else 1`) and draws a bold `Selected: {item}` row plus a help row: `'Arrows or j/k: move | q/Esc: quit'`. This hierarchy fits the task better and handles small heights that C-without ignores.
- **Captures:** `/tmp/bc-swarm/2026-11-11-status-help-footer/` contains:
  - pixel captures `terminal-80x24.png`, `terminal-40x12.png`, `terminal-foot-actual.png`, `terminal-foot-after.png`, plus `foot*.log` files (foot is a real terminal emulator)
  - text captures with columns × rows in their names: `terminal-80x24.txt`, `terminal-40x12.txt`, and a second round at `-80x24-`, `-40x12-`, `-40x8-`, `-40x7-round2.txt`, plus a navigation capture `terminal-40x12-nav-round2.txt`
  - So it did not treat the terminal as exempt, used real pixel captures rather than text alone, kept separate rounds, and checked very short terminals (40×7).
- **No report:** the transcript is empty, so there is no written critique, no explicit statement of what text-only capture cannot show, and also no false claim.
- **Not verified by me:** I did not open these PNGs or search this run's session log for skill loading or image reads (budget). The HOLD rests on file names and the code diff.

### C comparison
**The skill appears to have made the difference on the Fail line.** Without the skill the agent accepted "design checks don't apply" and produced no capture. With it, the agent took terminal pixel and text captures at stated sizes, in rounds, and wrote code that handles small heights.

C-with still misses expected artifacts — the written critique and the stated limits of text-only capture — because it timed out. This is the same report-only-at-the-end gap as in B.

---

## Cross-scenario notes
- **Both timeouts happened during polishing, not on a blocked step.** B-with was still recapturing at 03:33, about 19.5 minutes in. The gate puts all written evidence in the final "Report" section, so a timeout loses everything except the images. The fix proposed under B (write each critique as you capture) would let B-with and C-with leave gradeable critiques.
- **Captures were saved outside the run directories**, in `/tmp/bc-swarm/2026-11-11-compact-settings/`, `/tmp/offhours-*` and `/tmp/bc-swarm/2026-11-11-status-help-footer/`. Copy them before `/tmp` is cleared, because the evidence for A-with, B-with and C-with lives there.

## Checks still to run
- **C-with:** search its session log for the ui-design skill being read and for `Read image file` results, and open `terminal-foot-after.png`. If no image reads appear, C-with still holds on the Fail line, but loses the claim that the agent inspected its own pixels.
- **A runs:** confirm `theme.css` and `app.js` are unchanged against the pristine fixture.

Commit: none
Branch: none