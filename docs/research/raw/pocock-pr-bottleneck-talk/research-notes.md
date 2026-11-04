# Matt Pocock YouTube video notes

**Video:** https://www.youtube.com/watch?v=LlgiOCmFG_w  
**Research date:** 2026-11-04  
**Status:** complete enough to use — **official YouTube captions / yt-dlp not obtained**; timestamped secondary transcript obtained.

## Transcript availability (read this first)

**Could not obtain official YouTube captions.** Attempts:

- `fetch_content` of the YouTube URL failed: "Could not extract YouTube video content. Sign into Google… or set GEMINI_API_KEY."
- `https://www.youtube.com/api/timedtext?lang=en&v=LlgiOCmFG_w` (and `fmt=vtt`, `type=list`) returned empty / unparseable.
- This researcher has no shell, so `yt-dlp --write-auto-subs --skip-download` was **not run**.
- youtubetranscript.com, youtubetotranscript.com, prepublish.ai, tactiq form: failed or no transcript body.

**Best transcript obtained (secondary ASR, timestamped, appears complete through applause):**  
https://www.usetranscribe.io/yt/LlgiOCmFG_w/pr-bottleneck-fix  

**Supporting near-transcript (live conference captions; includes MC; mid-talk gap around merge-danger / show-me; ASR errors):**  
https://agents.conffab.com/aie-paris-26/live/keynotes/sessions/1790260200.md  

**High-quality official-adjacent essay with YouTube section timestamps (paraphrase, not verbatim):**  
https://ai.engineer/talks/LlgiOCmFG_w-fixing-pr-bottleneck  

Quotes below are short. Verbatim lines are from the usetranscribe transcript unless noted. ASR errors are flagged.

---

## Metadata

| Field | Value | Confidence |
| --- | --- | --- |
| Title | Fixing the PR Bottleneck — Matt Pocock, AIHero | high |
| Speaker | Matt Pocock (AI Hero / AIHero) | high |
| Guests | None. Solo talk. Stage intro by MC **Raouf Shebry**, Replit DevRel (Conffab ASR; name spelling UNVERIFIED). | high no guests; medium MC name |
| Event | AI Engineer Paris 2026, Station F | high |
| Talk date | Conference 23–24 Sep 2026; Conffab session `2026-09-24T14:30:00.000Z → 15:00:00.000Z` | high session; medium that YouTube cut starts after intro |
| YouTube upload | Secondary pages say 25 or 26 Sep 2026 | medium — exact upload datetime UNVERIFIED |
| Duration | ~22:34 (YouTube); usetranscribe "22m"; talk audio ends ~22:14 plus thanks | high ~22.5 min |
| Channel | AI Engineer (`@AIEngineer`), not Matt's personal channel | high |
| Repo plugged | "I'm here at dot dev {slash} skills, and we're shipping version 1.3 this week." | high quote; exact URL likely `aihero.dev/skills` UNVERIFIED from this video alone |

**Sources for metadata:**

- Title/channel: https://www.usetranscribe.io/yt/LlgiOCmFG_w/pr-bottleneck-fix — "Fixing the PR Bottleneck — Matt Pocock, AIHero" / "Creator: AI Engineer" / "Duration: 22m"
- Event: https://ai.engineer/talks/LlgiOCmFG_w-fixing-pr-bottleneck — "In this AI Engineer Paris talk, Matt Pocock…"
- Dates: https://ai.engineer/paris/2026 — "September 23-24, 2026 • Paris"; Conffab session header above
- WhoBuilt (secondary): https://whobuilt.net/video/LlgiOCmFG_w — "Sep 26, 2026· 23 min· 271K views"

---

## Retrieval log

- Output file created before sources were fetched.
- YouTube native extract failed (sign-in / GEMINI_API_KEY).
- Timedtext API empty.
- Conference essay + WhoBuilt + Conffab captions + usetranscribe transcript recovered the talk.
- HumanLayer `show-me` author last name in ASR is "Hadley"/"Holley"; first-party blog/LinkedIn is **Dex / Dexter Horthy**. Treat video last-name as ASR error.

---

## Condensed timestamped transcript (secondary ASR)

Source: https://www.usetranscribe.io/yt/LlgiOCmFG_w/pr-bottleneck-fix  
This is **not** official CC. Keep for search; prefer quoted claims in the sections below.

- **0:01** PR bottleneck predates AI; backlog worse under AI constraints. Will use "the rubric of my skills"; announces new skills to speed reviewing/doing PRs.
- **1:03** "Software factory": agents (not only humans) initiate work. Classifier → fix/reproduction; Planet Scale slow-query reports as another trigger. Deterministic code accelerating the factory.
- **2:05** Without brakes you get a **"slop cannon"** of unreviewable PRs. Code is the agent's environment; bad code begets bad code. Three brakes to go faster.
- **3:04** Layer 1 **automated checks**: lint, tests, type checking, code-quality metrics (deterministic, since "the '50s"). Layer 2 **automated review** (agents for what tests miss / structure). Layer 3 **human review**. Cake. Goal: faster human review via first two layers. **"Stop the slop."** Higher quality → fewer human interventions.
- **4:09** Checks are cheap (CPU, not tokens/humans). Agent-fix tokens after a failing test are "pretty well spent." Teams underuse checks / aren't creative enough.
- **4:49** **Checks can lie.** Green CI ≠ merge-ready. Human + automated review are **"lie detectors."**
- **5:24** Lie 1: **tautological tests**. "Opus 5 got addicted to these." `X_POST_CHARACTER_LIMIT = 280` tested with `expect … to be 280`. Structure-sensitive; rename/change constant fails the test without proving behavior.
- **6:41** Lie 2: **structure-sensitive UI test**. Pitch detail page: Videos after Content Plan. Test `readFileSync`s the module and compares string indices (`>Content Plan<` vs `title="Videos"`) instead of rendering. Source reorder fails it.
- **7:11** Lie 3: **tests that cannot fail**. `useAudioBoost` stubs `AudioContext` with fake methods; real API error modes never fire → production-only failures. Agent is not cheating in bad faith; it follows "write tests" by coupling to structure instead of executing behavior.
- **7:55** How to make checks **harder to cheat** → quality bar.
- **8:25** **Deep modules** (John Ousterhout, *A Philosophy of Software Design*): hide complex behavior behind a small interface. Shallow modules: many functions that do little. Force agents to test the interface, not internals.
- **9:05** **Module-deepening skill**: HTML report of before/after opportunities (e.g. reduce duplication, deep testable module); then implement. Audience hand-raise: some have used it.
- **10:13** **Codebase-design skill** vocabulary vs "20 different approaches… all called DDD": **locality**, **leverage**, **seam**. "I was using seams before they were cool." Locality = related code together / change ripple. Leverage = value from a simple call into a deep module. Good for humans and agents.
- **11:12** How to make the agent actually do this: **"don't put coding standards in your implementer agent."** Implementer context already: explore, change files, debug via checks. Adding standards makes it **perform worse**. Implementation is **overloaded**.
- **12:10** **Code-review skill**: receives a diff; reads repo `coding standards` file; checks compliance. Runs in a **subagent** with its own context/budget. Some exploration for wider context; **no implementation, no debugging**. Review is **underloaded** → can take many standards.
- **13:29** Two-part process: implement = **make it work**; code-review = **make it good**. Maps to **red-green-refactor** across **two context windows**. Anecdote: "very successful for me" (no measured comparison). Put standards in `coding standards.md` / `codingstandards.md` / slide `CODING_STANDARDS.md`, **not** `agents.md` (drowns implementer).
- **14:26** Don't outsource automated review to Cursor Bugbot / CodeRabbit. Generic bug+security reviewer is too general (false positives) or too specific (TS vs Rust). **Build your own** standards over time; dump unread docs into them.
- **15:34** Default reviewer output should be **commits/fixes**, not verbose PR comments (those create more human work). Comment only on genuine questions.
- **16:04** **"Stop trying to one-shot good code."**
- **16:34** **PR skill** "coming into the repo… currently in progress… releasing it soon." Steal best PR-body ideas. Some reviews more important than others.
- **16:58** AWS **one-way vs two-way door**. Most PRs two-way (revert). Civil-engineering contrast. Nuance: a "very simple change" that "accidentally blasts out an email to 60,000 people" is one-way; expensive migrations / data loss too. **"Review the hell out of that PR."**
- **18:06** Also **blast radius**. **"Merge danger"** summary at bottom of PRs (door + localized vs not). Example in slides: two-way, localized error-message text.
- **18:38** Understand what the PR does via **pseudocode**. Credits **"the show me skill from the human layer skills repo by Dex Hadley"** (ASR; author is Dex Horthy). **"Phenomenal skill"** — dispenses with most text; images/diagrams. Mermaid, UML/sequence, simple CLI diagram (new command + two flags). Make understanding the **why** as fast as possible.
- **19:36** Human review should review **the system that produces the code**, not only the diff. Shared skill/steering files. **"Never want to write the same comment twice."**
- **20:36** **Retro** skill. Inputs: one agent session; PR + session; or last week's PRs+reviews. Suggests automated checks and coding-standards updates. Compounding: this review makes the next one cheaper.
- **21:14** Retro also: **navigation pointers** in `agents.md`; **tool economy** (token-efficient tools; hard to debug from outside); **bloat** (steering files / skills). Goal: layer checks + automated review; make human review optional for two-way doors; **always review one-way doors**.
- **22:14** "these are my skills. I'm here at dot dev {slash} skills, and we're shipping version 1.3 this week." Lobby for questions. Thanks Paris.

**Conffab-only prefix (not on the YouTube cut, or trimmed):** MC intro that Pocock was "the typescript wizard," Vercel, then skills; "fix your PI bottlenecks" (ASR). Source: Conffab session markdown.

**Conffab ASR gap:** after two-way doors it jumps to process/retro; merge-danger, 60k email, and show-me are **missing** there. Use usetranscribe + AI Engineer essay for that span.

---

## Claims / practices: testing with AI coding agents

Each claim cites URL + quoted supporting line.

1. **Green CI is not merge-ready; checks can lie.**  
   **Source:** https://www.usetranscribe.io/yt/LlgiOCmFG_w/pr-bottleneck-fix ~4:49  
   **Quote:** "Does a green CI mean that the code is ready for merge? No, it does not."  
   **Kind:** direct evidence (ASR). **Confidence:** high.

2. **Automated + human review exist as "lie detectors" for checks.**  
   **Quote:** "the human review and automated review, these are lie detectors. These are for finding lies in the automated checks." (~4:49)  
   **Confidence:** high.

3. **Tautological tests reassert implementation; Opus 5 "got addicted" to them.** Example: character-limit constant 280 vs `expect … toBe(280)`. Structure-sensitive (rename/constant change).  
   **Quote:** "The first is tautological tests. A test that just reasserts the implementation. Opus 5 got addicted to these." (~5:24)  
   **Slide evidence:** Conffab `export const X_POST_CHARACTER_LIMIT = 280;`  
   **Confidence:** high on the pattern; "Opus 5" is what ASR captured.

4. **Structure-sensitive tests inspect source order instead of rendered UI.** Pitch detail: Videos after Content Plan via `fs.readFileSync` + `indexOf`.  
   **Quote:** "it doesn't render it to a screen, it just reads the actual file… expects the videos to be after it in the source material." (~6:41)  
   **Slide (Conffab):** `expect(videosIndex).toBeGreaterThan(contentPlanIndex)`  
   **YouTube frame:** https://www.youtube.com/watch?v=LlgiOCmFG_w&t=394s (AI Engineer essay)  
   **Confidence:** high.

5. **Over-mocking yields tests that cannot fail.** `useAudioBoost` / stubbed `AudioContext`; real error modes untested → production failures.  
   **Quote:** "There are also tests that literally cannot fail." (~7:11)  
   **Slide:** `vi.stubGlobal("AudioContext", () => ({ createMediaElementSource: fakeFn(), …}))`  
   **Confidence:** high.

6. **Agents often write bad tests in good faith** — following "write tests" by coupling to structure instead of executing behavior.  
   **Quote:** "the AI isn't trying to write bad tests here. It's just taking our instructions and writing tests that are too tied into the structure instead of actually executing code." (~7:55)  
   **Confidence:** high.

7. **Make checks harder to cheat via codebase design (deep modules / small test interface).** Ousterhout. Force agents to use the interface.  
   **Quote:** "your job here is to force the agents to use that little interface instead of reaching into the implementation" (~9:05)  
   **Confidence:** high.

8. **Layer many cheap deterministic checks** (lint, tests, **type checking**, quality metrics). Underused / not creative enough. Tokens spent fixing a test-caught agent bug are well spent.  
   **Quote:** "you're probably not using enough of them or not being creative enough with your use." (~4:09)  
   **Confidence:** high.

9. **Seams / locality / leverage** are the shared design language for agents and reviewers (not "everything is DDD").  
   **Quote:** "I have a little code base design skill that defines what locality is, defines what leverage is, defines what a seam is." (~10:13)  
   **Confidence:** high he said it; definitions are brief in-talk.

10. **TDD mapping: red-green in implementer context, refactor in a separate review context.**  
    **Quote:** "this is essentially a red-green-refactor approach. We use one context window to make it okay, do the red-green, and then we do another context window to refactor it." (~13:29)  
    **Confidence:** high as analogy; he does not walk a failing-test-first TDD ritual in this talk.

11. **No evals framework** (LLM-as-judge evals, eval datasets) is discussed in the recovered transcript.  
    **Kind:** researcher inference from absence. **UNVERIFIED that he never said the word** if ASR dropped it; no hit in usetranscribe/Conffab/essay.

12. **Types** appear only as "type checking" inside cheap automated checks, not as a substitute for tests.  
    **Quote:** "linting and tests and type checking and code quality metrics" (~3:04)

---

## Claims: skills / agent instructions / workflows

1. **Three-layer "cake" of brakes:** automated checks → automated review → human review. Accelerators (agent-initiated work, classifiers, PlanetScale slow queries) without brakes = slop cannon.  
   **Quote:** "If you just have permanent acceleration… you're going to end up with a slop cannon." (~2:05)

2. **Stop the slop:** raise shipped quality so humans intervene less.  
   **Quote:** "if you raise the quality of the code that you're shipping, you're going to end up doing less human review" (~3:33)

3. **Code is the agent's environment (AX).** Bad code begets bad code.  
   **Quote:** "code is the environment your agent operates in. And if you have bad code in your code base, that is going to beget more bad code." (~2:35)

4. **Do not put detailed coding standards in the implementer / `agents.md`.** Implementer is overloaded (explore + edit + debug). Standards belong in a file the **review subagent** reads.  
   **Quote:** "don't put coding standards in your implementer agent." (~11:12)  
   **Quote:** "You don't put them in agents.md, cuz then they sort of drown out your implementer… You put them in coding standards.md" (~14:00)  
   **Filename variants in sources:** `coding standards.md` (ASR), `codingstandards.md` (essay), `CODING_STANDARDS.md` (Conffab slide). Treat exact filename as **inconsistent across sources**.

5. **Specialize contexts:** implementer = make it work; reviewer subagent = make it good, with its own window/budget. Reviewer **underloaded** so it can take a pile of standards.  
   **Quote:** "while implementation is overloaded, review is actually underloaded." (~12:43)

6. **Reviewer should commit fixes by default**, comment only when uncertain. Comments are more work for the human.  
   **Quote:** "The reviewer should commit. It should make fixes." (~15:34)

7. **Stop trying to one-shot good code** via a single overloaded implementer.  
   **Quote:** "Stop trying to one-shot good code." (~16:04)

8. **Don't outsource automated review** to generic Bugbot/CodeRabbit-style products; build repo-specific standards (generic vs language-specific trap).  
   **Quote:** "don't outsource automated review. Build your own." (~14:59)

9. **Unread team docs** should become reviewer criteria.  
   **Quote:** "if you've got some docs sitting around that no one reads, this is the place to put them in." (~14:59)

10. **Human-friendly PRs:** not every review is essential; classify **one-way vs two-way doors** + **blast radius**; **merge danger** blurb. Always review one-way doors; two-way can be light/optional.  
    **Quote:** "You really don't need to review every single two-way door. Every single one-way door you do." (~21:46–22:14)

11. **Visual PR explanation (pseudocode/diagrams) beats walls of text.**  
    **Quote:** "the best thing I've come up with is using pseudo code." (~18:38)

12. **Review the producing system, not only the diff.** Shared skills/steering = shared failure modes.  
    **Quote:** "when you do a human review, you're not just reviewing the code, you're reviewing the system that creates it." (~20:09)  
    **Quote:** "you never want to write the same comment twice." (~20:09)

13. **Retro compounds review:** session and/or PR(s) → new checks, standards, `agents.md` pointers, cheaper tools, less bloat.  
    **Quote:** "it will suggest automated checks and coding standards to make the next one better." (~20:36)

14. **Work can start without a human request** (classifier / monitoring). That is an accelerator, not a quality strategy.  
    **Quote:** "All of this is not humans triggering it, it's deterministic code triggering it" (~2:05)  
    ASR "classifier like Jeff" is likely garbage; essay says "A classifier might turn an incoming item into a fix, a reproduction or a notification."

---

## Tools / skills / repos shown (with timestamps)

YouTube timestamps from usetranscribe unless noted. Conffab slide times are **session clock** (includes pre-roll) and are **not** YouTube times.

| Time (YouTube) | What | Notes |
| --- | --- | --- |
| 0:29 | "rubric of my skills"; new skills to announce | mattpocock/skills / AI Hero skills |
| 1:03 | Software-factory accelerators | Classifier; **Planet Scale** slow-query reports |
| ~6:34–7:11 | Bad-test slides | `X_POST_CHARACTER_LIMIT`; pitch-detail `readFileSync` test; `vi.stubGlobal("AudioContext"…)` `useAudioBoost` |
| ~9:05–10:13 | **Module-deepening / architecture-review skill** | HTML before/after; demo scoped to `course-video-manager` (Conffab slide 00:13:37, dated 18 Sep 2026). usetranscribe ASR "I've got to go for this" vs Conffab "I've got a skill for this" — treat as **module-deepening skill**. Essay: "Pocock's module-deepening skill… HTML report". Frame: https://www.youtube.com/watch?v=LlgiOCmFG_w&t=608s |
| ~10:13 | **Codebase-design skill** | locality, leverage, seam |
| ~12:10 / WhoBuilt **12:31** (`t=751s`) | **`/code-review`** | Diff + coding-standards file; **subagent**. Slide: `/code-review` reads `CODING_STANDARDS.md` (Conffab 00:16:06) |
| ~13:29 | `/implement` vs `/code-review` | Slide: `/implement` = Make It Work; `/code-review` = Make It Good |
| ~14:26 | Cursor **Bugbot**, **CodeRabbit** | Cited as third-party automated review he does **not** recommend outsourcing to |
| ~16:34 / WhoBuilt **16:35** (`t=995s`) | **PR skill** | "currently in progress"; "releasing it soon"; later shipped in skills v1.3 (outside this video) |
| ~18:06 / WhoBuilt **17:14** (`t=1034s`) | **Merge danger** block | Door + blast radius. Slide example mentions `/compact` error-message text (Conffab 00:22:07) |
| **18:38–19:12** / WhoBuilt **18:40** (`t=1120s`) | **HumanLayer `show-me`** | "the show me skill from the human layer skills repo by Dex Hadley" (ASR). "Phenomenal skill." Mermaid, UML/sequence, CLI command+flags diagram. Frame: https://www.youtube.com/watch?v=LlgiOCmFG_w&t=1162s (`clip restore` / `--archived` in essay caption). First-party: https://www.humanlayer.com/blog/show-me-skill ; https://github.com/humanlayer/skills ; author **Dexter Horthy** |
| **20:36** / WhoBuilt `t=1236s` | **`/retro`** | New skill announced; session / PR+session / week of PRs |
| 21:14 | Retro outputs | checks; `coding standards.md`; `agents.md` navigation pointers; tool economy; bloat |
| 22:14 | **skills v1.3 this week**; "dot dev / skills" | Conference week of 23–24 Sep 2026 |

**Repos (named or clearly implied):**

- Matt Pocock skills repo (talk's "my skills"; v1.3). Public: https://github.com/mattpocock/skills — **not opened on camera in the recovered transcript**; URL spoken as "dot dev / skills".
- HumanLayer skills: **show-me**. https://github.com/humanlayer/skills  
- No other GitHub org names spoken except Planet Scale as a product, Cursor, CodeRabbit.

**What he shows visually (from essay + Conffab slides, not a screen recording we watched):**

- Tautological constant test
- Source-order UI test (full TypeScript in Conffab)
- AudioContext mock
- Deep vs shallow module diagram
- Architecture-review HTML (duplicated visibility checks → shared predicates)
- Implementer vs reviewer load diagrams
- Merge-danger YAML-like blurb
- `/show-me` CLI diagram (`clip restore <id>`, `--archived` on `clip list` / `clip get` — from AI Engineer image caption, not from ASR)

---

## Actionable ideas for this workspace's skills

Target skills named in the task: `tdd`, `code-review`, `diagnosing-bugs`, `prompting-agents`, `research`. These are **researcher recommendations** inspired by the talk, not claims he made about this repo.

1. **`tdd` — Ban tautological / structure-sensitive tests by name.** Add a short "tests that lie" checklist: no asserting constants equal themselves; no `readFile`/`indexOf` stand-ins for UI; no mocks that delete failure modes. Quote the 280 and pitch-detail examples as anti-patterns.

2. **`tdd` — Require a behavioral seam.** Instruct the agent to test through a small public interface (deep module), not internals. If the only way to assert is by reading source or private identifiers, the design is wrong — deepen first, then test.

3. **`tdd` — Treat green as a lie-detector input, not a merge certificate.** After tests pass, a second pass (or the code-review skill) must ask "what behavior is still unexecuted?" especially error paths.

4. **`tdd` — Split red-green from refactor across contexts** if one window is already exploring+implementing+debugging. Don't pile coding-standards into the TDD implementer.

5. **`code-review` — Two-axis is not enough if standards live in the implementer prompt.** Keep detailed standards in a file the reviewer loads; keep `AGENTS.md` / implementer instructions lean (navigation, not style essays).

6. **`code-review` — Default to fixing, not commenting.** Gate: if the finding is mechanical and in-scope, commit/patch; comment only on judgment, risk, or questions. Explicitly say verbose comment dumps *increase* human review work.

7. **`code-review` — Add merge-danger / one-way-door / blast radius** to the review artifact (or to a PR-description companion). Diff size is not risk. Email/send, migration, data-loss = mandatory human.

8. **`code-review` — Prefer a compact visual of the change** (pseudocode, mermaid, CLI/flag sketch) over a prose essay. Consider depending on / adapting HumanLayer `show-me` rather than reinventing diagram rules.

9. **`code-review` — Don't try to be a generic Bugbot.** Prefer repo-specific standards that grow from real recurrences over a universal security/bug laundry list that false-positives.

10. **`diagnosing-bugs` — Distrust tests that cannot fail.** When a production error "shouldn't be possible," inspect mocks/stubs and tautological assertions before trusting CI history.

11. **`diagnosing-bugs` — Prefer executing the real interface** (repro through the deep module / real AudioContext-class dependency) over reconstructing intent from source-order tests.

12. **`prompting-agents` — Overloaded vs underloaded context as a design rule.** One agent: explore, edit, run checks. Another: standards. Do not one-shot "be amazing." Encode "stop trying to one-shot good code."

13. **`prompting-agents` — Retro loop:** never write the same human comment twice — turn it into a check, a standard, an `AGENTS.md` pointer, a cheaper tool, or a skill trim. Session logs matter more than the final diff.

14. **`prompting-agents` — Tool economy + bloat as first-class retro categories.** Bloated steering/skills are failure modes, not completeness.

15. **`research` — When summarizing a change or a paper, demand the smallest visual that makes the point** (show-me posture): skip preamble, pick pseudocode/tree/diff/diagram, then short prose. Same "make understanding the why as fast as possible" bar.

---

## Contradictions / disputes

- **Dex's last name:** usetranscribe "Dex Hadley"; other ASR "Dex Holley"; first-party HumanLayer/LinkedIn **Dexter Horthy**. Video last-name is ASR. Use Horthy when naming the author; keep the on-tape phrase as "Human Layer skills repo" + show-me.
- **Coding-standards filename:** `coding standards.md` vs `codingstandards.md` vs `CODING_STANDARDS.md`. Slide supports `CODING_STANDARDS.md`.
- **YouTube publish date:** WhoBuilt 26 Sep 2026; thiagotn summary "published September 25, 2026"; Conffab live 24 Sep 2026. Talk date ≠ upload date.
- **usetranscribe vs Conffab wording** on the module skill ("got to go" vs "got a skill") and a mid-talk Conffab gap (merge danger / show-me omitted). Prefer usetranscribe for that span.
- **WhoBuilt timestamps** vs usetranscribe: show-me ~18:40 vs 18:38; both in the same breath. Fine.
- **View count 271K** (WhoBuilt): UNVERIFIED and stale-sensitive.

## Missing evidence / UNVERIFIED

- Official YouTube caption file / yt-dlp VTT (not obtained).
- Exact YouTube upload datetime from YouTube itself.
- Exact spoken URL for "dot dev / skills".
- Exact CLI command/flag names on the show-me demo (essay caption: `clip restore`, `--archived`) — not in ASR.
- Measured quality comparison for split implement/review (he says it worked for him).
- Whether he said "evals" (no evidence in recovered text).
- MC name spelling (Raouf Shebry / Rou Chevrey across ASR).
- Whether the YouTube cut includes the MC intro (Conffab has it; usetranscribe starts at "All right. I'm here to talk…").

## Sources

**Kept**

- https://www.usetranscribe.io/yt/LlgiOCmFG_w/pr-bottleneck-fix — timestamped secondary transcript (primary evidence for quotes)
- https://agents.conffab.com/aie-paris-26/live/keynotes/sessions/1790260200.md — live captions + slides (MC, code samples)
- https://ai.engineer/talks/LlgiOCmFG_w-fixing-pr-bottleneck — official-adjacent essay + YouTube deep-links
- https://whobuilt.net/video/LlgiOCmFG_w — skill timestamps / quoted lines
- https://whobuilt.net/product/show-me — show-me @ 18:40
- https://thiagotn.com/en/posts/resumo-fixing-pr-bottleneck/ — structured summary (secondary)
- https://www.humanlayer.com/blog/show-me-skill — first-party show-me (author Dex, 12 Aug 2026)
- https://ai.engineer/paris/2026 — event dates
- https://github.com/mattpocock/skills — repo implied by v1.3 plug (not watched in-video)

**Rejected / deprioritized**

- youtubetranscript.com, youtubetotranscript.com, prepublish.ai, tactiq landing — no usable transcript body / 403
- YouTube timedtext — empty
- Medium "Stop the Slop Cannon" (Pramitha) — third-party rewrite, not his words
- cldnavi.com praise article — SEO, not the talk
- waylonwalker.com txt — viewer blog, not a transcript
- youtubesummary.com — business paraphrase, "garbage cannon" wording drift

## Next steps

- If a machine with `yt-dlp` is available, dump auto-subs into this directory and diff against usetranscribe.
- Pair with the sibling `showme.md` track for HumanLayer skill body vs what he demoed.

---

## Durability

- Commit: none
- Branch: none
- Artifact: `/tmp/bc-swarm/2026-11-04-pocock-video/video.md`
