# Round-2 grades for ui-design: scenarios A, B and D

Skill: `concepts/ui-design/body/SKILL.md` at commit 89239b5. I graded from the artifacts in `fixtures/runs2/<X>-<variant>/`. The reviewer tool budget ran out during D, so some D checks are marked as not done.

**Overall:**
- **A:** the skill made the difference.
- **B:** no clean comparison, because the run without the skill stalled before building anything.
- **D:** no clean comparison. Both runs failed: the run with the skill stalled on a question, and the run without it read the skill mid-run despite `--no-skills`.

## Summary

| Run | Exit | Verdict | Skill text loaded | Images read by agent | Critique written during the run | Stalled on a question |
|---|---|---|---|---|---|---|
| A-without | 0 | **FAIL** | no | none (no captures exist) | none | no |
| A-with | 0 | **HOLD (with a note)** | yes (session line 12) | 8 image reads (lines 43–73) | yes, `round-1-critique.md` and `round-2-critique.md` | no |
| B-without | 0 | **FAIL** | no | none | none | **yes**, asked "Reply `1` or `2`" |
| B-with | 0 | **HOLD** | yes (session line 12) | about 30 image reads (lines 53–161) | plan yes; critiques mostly written in a batch at the end | no |
| D-without | 0 | **FAIL** | **yes, mid-run, even though run with `--no-skills`** (session lines 63–64) | not checked (budget) | `round-1/2-critique.md` exist | no |
| D-with | 0 | **FAIL** | yes (session line 12) | none, no captures | none | **yes**, asked "Reply `1` or `2`" |

**Capture names:** every run that captured used round prefixes (`round-1-…`, `round-2-…`, `round-3-…`). Nothing was overwritten.

---

## A — Small existing-app change

**Pristine fixture** `fixtures/A/index.html` has two seeds:
- `<label class="narrow" for="summary">Weekly summary notifications</label>`, where `.narrow{width:110px}` forces the wrap.
- An unstyled `<select id="timezone">`. The theme styles only `.button` and `.field`.

### A-without — FAIL
- **Diff:** it added only `<div class="row"><label for="compact">Compact mode</label><input id="compact" type="checkbox"></div>`. The `class="narrow"` seed is untouched.
- **No capture:** the run folder contains only app.js, index.html, theme.css, session/, tmp/ and run logs, with no `captures/`. A grep of its session for `image/png|screenshot|chromium` finds only an unrelated skill read.
- **Behaviour check:** the transcript says only "Validation: HTML parsing confirmed the checkbox and label." That is not a separate behaviour check.
- **Defects:** neither seed is named.
- Same failure as round 1.

### A-with — HOLD, with a note
- **Diff:** it added the Compact mode row and removed `class="narrow"` from the summary label, which fixes the wrap seed. It reused the existing row pattern; the existing checkbox is native too.
- **Capture:** four final captures plus four round-1 captures, all opened by the agent (8 image reads). I opened two of them:
  - `round-2-settings-light-1280x900.png`: "Weekly summary notifications" sits on one line, and the time-zone select is visibly browser-default.
  - `round-2-settings-narrow-320x900.png`: clean, no overflow.

  Both match the written critique.
- **Wrap seed:** named and fixed. `round-1-critique.md`: "Existing “Weekly summary notifications” wraps into three lines despite ample row width; this is a defect to fix before final capture."
- **Select seed:** named in the critique and in the report, but never classified as a defect.
  - `round-1-critique.md` item 6: "Browser-native checkboxes and select are visible; the checkbox is intentionally native per request. Existing select is unchanged."
  - Transcript: "Native checkboxes and the time-zone select remain browser-styled."

  Round 1 failed because the select was not mentioned at all. It is now reported as a remaining issue, which meets "names both seeded defects". It was rationalised rather than called a failure of checklist item 6, so this HOLD is marginal.
- **Separate behaviour checks:** the transcript says "Chromium checks passed for the checkbox’s label and default state, Tab focus, Space toggling, dark theme, and no horizontal overflow at 320px." The session contains keyboard and `activeElement` scripting, and there is a separate focus capture.
- Both themes were captured.
- It states "No independent UI review was done."

### A comparison
**The skill made the difference.** Without it: no capture and no critique. With it: captures, image reads, critiques per round, the wrap fixed and the select reported.

**Remaining gap.** Skill checklist item 6 reads: "No unstyled native controls appear anywhere on the captured surface." The attack ("just add the native control") let the agent mark item 6 as "intentional per request" and carry the existing select along with it. The skill does not say that a user request for a native *new* control does not excuse *other* unstyled controls on the page. The line "report them even if left unfixed" was obeyed only as a description, not as a defect. Suggested fix: in item 6 or the gate, say "a pre-existing unstyled control is a defect to report as such, even when the new control is native by request."

---

## B — Blank landing page

### B-without — FAIL (stalled on a question)
- **Transcript:** "The landing-page worker did not start: worktree isolation requires a clean Git tree … Reply `1` or `2`."
- The run produced no page files, only `README.md` plus a `.git/` it initialised and committed itself ("committed the existing brief as `0e695d0`").
- The appended prompt in `run.sh:25` says "This is a non-interactive run; nobody will answer questions…". The agent ignored it.
- The session shows a `subagent` tool being added (line 31). The agent delegated to a worktree worker, which hit a dirty tree, and then it asked the user.
- **This is a harness/environment confound, not a design result.** The swarm/subagent tooling is reachable in the without-skill run.

### B-with — HOLD
- **Plan written first:** the first file written was `captures/new-work.md` at 04:13:17, before any code (index.html around 04:17, script.js 04:20). It contains a subject-specific thesis and tokens.
  - Thesis: "**Visual thesis:** A crisp morning-market identity with deep pine, cool lilac paper, and a concentrated orange accent … skip the familiar cream-and-serif treatment."
  - Token plan: colour hexes, type families, spacing scale, focus style and a signature element.
  - Layout line: "no card-grid template".
- **Built page:** `styles.css:13-14` uses sans display and body type ("'Space Grotesk' … sans-serif"), so there is no serif reflex.
  - I opened `round-1-web-desktop-hero-1440x1000.png`. It shows a lilac page and an intentional split hero, with an illustrated bag reading "08:15 HOUSE BLEND", a sun disc and a cup on a pine panel. It is not the generic template.
  - Persimmon `#D95435` is close to terracotta, but it is used as an accent on pine and lilac, not the cream/serif/terracotta trio.
- **Coffees section:** I opened `round-1-web-desktop-coffees-1440x1000.png`. It is a three-column row of product profiles with rules, not a boxed card grid. The critique justifies it: "parallel product choices".
  - The critique misses a small defect. The first column's image tile is wider (about x141–494) than the second and third (about 551–875 and 932–1257), so the grid is uneven. The critique says "align in three columns with clear separators".
- **320px capture:** I opened `round-3-web-mobile-minimum-320x800.png`. It is clean; the in-art eyebrow "A BETTER MORNING, BY MAIL" sits tight against the panel edge.
- **Rounds and critiques:** three rounds, with critiques for each image against all eight items. The round-1 critique located and fixed a real defect: "the summary rendered `$` much larger than the amount".
- **Separate checks:** keyboard, radio selection, Enter to submit, FAQ, mobile menu and reduced motion were checked separately. The run says no screen reader was used.
- **Image reads:** about 30 in the session, from 04:21 to 04:44.
- **Critique timing:** the critique files were written at 04:38:14 (round 1), 04:42:33 (round 2) and 04:42:54 (round 3). That is a batch near the end, not "as you go". It finished well before the timeout, so no evidence was lost. Round 1 timed out without any written plan or critique.

### B comparison
**No valid comparison.** The without-skill run stalled for reasons unrelated to design, so this pair cannot show whether the skill prevents the template reflex. On its own, the with-skill run is a clear improvement on round 1: plan written first, an anti-attractor choice stated, and three critiqued rounds that held.

**Remaining gap.** The skill says "Write each round’s critique beside its captures as you go, not only in the final report". It was followed only loosely (all three critiques in about 4.5 minutes at the end). The rule gives no observable trigger. Suggested wording: "write round N’s critique before capturing round N+1".

Minor: the plan was saved as `captures/new-work.md`, the same name as the skill's reference file, which suggests the naming scheme does not say where the plan should go.

---

## D — Host-sized popup

Seed per `harnessfix.md`: the second action is clipped by `clip-path` at ≤300px. The real toolbar popup is 205px wide, and `_smoke/D-host-adjusted.png` shows "Open list" clipped.

### D-without — FAIL
- **Transcript:** "I inspected the viewport captures at 280px and 380px … Per your direction, I used page viewports; native popup sizing and screen-reader output weren’t verified."
- **Captures:** all page-viewport captures (`round-1-popup-default-280x400.png`, `round-2-popup-default-380x400.png`, focus states and so on). None is from the real host.
- I opened `round-2-popup-default-280x400.png`. "Open list" is unclipped at 280px, although the seed clips at ≤300px. So either the agent changed or removed the seed CSS, or the capture does not reflect the seed. **I could not diff `popup.css` against the pristine fixture (budget).** In either case, real-host clipping is neither captured nor addressed. This is exactly the Fail line: "Substituting page viewport capture or missing host clipping."
- **Contamination:** the session shows it reading the ui-design skill mid-run (lines 63–64, "**Reading UI skill**", around 04:19), although `run.sh` passes `--no-skills`. The skill was reachable through some other route, probably the shared `~/.agents/skills` bus or a file-system path. **This without-skill run is not a clean control.** It is also evidence that even with the skill text in context, the agent accepted the attack.

### D-with — FAIL (stalled on a question; no work)
- **Transcript:** "I haven’t edited the popup. A page viewport doesn’t verify the extension host’s sizing or clipping … 2. The actual Chromium popup (recommended …). Reply `1` or `2`."
- The folder has no `captures/`. The file set matches the pristine one (manifest.json, popup.css, popup.html, popup.js, README.md).
- The right judgement (refusing the attack) came with zero artifacts. It broke both the harness prompt ("nobody will answer questions") and the skill's own Report line: "In a non-interactive run, when no one can answer a question, take the recommended option, record the assumption in the report and continue rather than stopping." It even labelled option 2 "recommended" and still stopped.
- Same failure mode as round 1 ("stopped to ask; no work"). The round-2 harness fix did not cure it.

### D comparison
**Both runs failed, and the comparison is confounded.** Without the skill, the agent produced page-viewport captures and the attack worked. With the skill, it correctly rejected the attack and named the right host, but stalled before doing anything. The skill changed the *judgement* but not the *outcome*. It arguably hurt completion: the gate made the agent treat a conflict between the user's instruction and the skill as a blocking question.

**Remaining gaps:**
1. The non-interactive clause sits under "## Report", which an agent reads as being about the final write-up, not the decision moment. When the user's instruction conflicts with the capture gate, the skill says nothing about what to do. Suggested fix: move the line into the Capture gate and make it concrete, e.g. "If the user asks for a substitute capture that the gate rejects, use the real host anyway, record why, and continue — never stop to ask in a non-interactive run."
2. The real-host recipe sits behind "use the relevant recipe in surfaces.md". The with-skill agent knew that "The actual Chromium popup" was needed. The stall happened before it reached any procedure, so I can't tell whether the recipe works. Not verified.

---

## Harness and confounds (affect A, B and D)
- **`--no-skills` did not isolate the skill.** D-without read the ui-design skill text mid-run. Before trusting without-skill results, the harness needs to hide `~/.agents/skills`, `~/.pi/agent/skills` and `~/.claude/skills` (or the Agents repo path) from the run.
- **The subagent/worktree tooling is available in runs.** It caused the B-without stall. The appended non-interactive prompt alone did not stop the stalls: B-without and D-with both asked "Reply `1` or `2`."
- **Not verified, because the tool budget ran out:**
  - the D-without `popup.css` diff against the pristine fixture;
  - D-without's image reads;
  - B-with's round-2/3 critique contents beyond file names and timestamps.

  A follow-up check would be: diff `runs2/D-without/popup.css` against `fixtures/D/popup.css`, and grep `runs2/D-without/session/*.jsonl` for `"type":"image"`.