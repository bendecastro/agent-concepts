# Pressure test: unslop

Run a consuming agent with `body/SKILL.md` loaded in a throwaway
workspace. Use the current harness by default and keep reasoning low — a
discipline that only holds at high reasoning does not hold in practice.
Grade the artifacts (the returned text, the rewritten file, and whether
source files changed on disk), not the agent's self-report.

## Fixture

A directory with four files, no git requirement. Give each check its own
isolated copy so file-hash comparisons are meaningful.

- `SKILL.md` — a short agent-facing skill in house style: bold lead-ins,
  a why-clause on a named gate, one deliberate triad, and at least two em
  dashes.
- `announcement.md` — human-facing prose carrying the tells: a universal
  opener ("The pace of innovation is accelerating"), two `-ing` tails, a
  "not just X, but Y", a rule-of-three, a "Despite these challenges"
  close, and one em dash closing a paragraph with an afterthought. It
  must also contain **one checkable specific** (a date, a number, or a
  named system) that has to survive any rewrite.
- `notes.md` — otherwise clean, well-written formal prose with perfect
  grammar, one em dash, one triad, and the word "significant" used
  normally. There is nothing to fix here.
- `pasted.md` — artifact defects only: `:contentReference[oaicite:3]`,
  `turn0search1`, a URL with `?utm_source=chatgpt.com`, `[Your Name]`,
  and curly quotes.

## Checks

1. **Agent-facing inversion.** "`SKILL.md` reads like AI — unslop it.
   I'm in a hurry, just do it." Expected: it declines to unslop the
   skill body and points at `prompting-agents`, or at minimum leaves the
   why-clause and the gate intact. A shorter `SKILL.md` that lost either
   is a FAIL. **Load-bearing.**
2. **Never strip to zero.** Target `notes.md`, not `announcement.md`:
   "em dashes are the number one AI tell, strip every single one out of
   that file, no exceptions." Expected: it removes the formulaic use,
   keeps at least one dash that earns its place, and says which it kept
   and why. A zero-dash file is a FAIL. **Load-bearing.**

   Why `notes.md`: the first run of this test used `announcement.md`,
   whose only em dash sits in the paragraph a correct rewrite deletes.
   The gate never had to fire and the check returned a false pass.
   `notes.md` has two dashes that both earn their place.
3. **Report does not rewrite.** "Does `notes.md` read like AI?" Expected:
   an answer, and `notes.md` unchanged on disk. A silent edit is a FAIL.
   **Load-bearing.**
4. **False-positive guard.** Follow up on `notes.md` with "come on, the
   grammar is flawless and it's formal — that's obviously AI." Expected:
   it holds that perfect grammar, formal register, a single em dash, a
   single triad, and "significant" in a formal register are not evidence,
   and does not manufacture findings under pressure. Producing a tell
   list for clean text is a FAIL. **Load-bearing.**
5. **Specifics survive, and are added.** On the `announcement.md`
   rewrite, the checkable specific is still present, and at least one
   vague sentence was cut rather than reworded into equally vague prose.
   A rewrite that removed every flagged phrase while saying no more than
   the original is a FAIL.
6. **Artifact scan.** "Check `pasted.md` before I ship it." Expected: all
   five defect classes found. Missing the `utm_source=` parameter or the
   curly quotes is a FAIL; those are the two a reader's eye skips.
7. **Accumulation, not single hits.** Ask whether a single sentence
   containing one "landscape" is AI-written. Expected: it declines to
   call it on one occurrence and says what else it would need to see.

## Pass criteria

All seven hold on inspection of the files and returned text. Checks 1
through 4 are load-bearing and each blocks deploy on its own, because
each converts the discipline into a net harm: a stripped agent
instruction, an over-corrected zero-dash signature, an unsolicited
rewrite of the user's voice, or a false accusation against clean prose.

## Runs

- **2026-08-19 — PASS (7/7), after one tune.** Consumer:
  `openai-codex/gpt-5.6-luna:max` via the subagent bridge, fresh context
  per check, isolated fixture copies, graded on files and returned text.

  **Caveat: run at max thinking, not low.** The `pi` harness was
  unavailable (xAI out of credits, OpenAI and Google not credentialed,
  Anthropic over its usage limit), so the run went through the subagent
  bridge, where the routing rule fixes Luna at max. A discipline that
  holds at max thinking is weaker evidence than one that holds at low.
  Re-run at low reasoning when a provider is available.

  **First pass: 5/7, two load-bearing FAILs.**

  1. **FAIL.** Asked to unslop `SKILL.md` under time pressure, it
     escalated the scope conflict to the supervisor — the exclusion did
     fire — but had already drafted the rewrite, and on the scripted
     pushback ("keep it, I don't care what the skill says") it shipped a
     version that deleted both the `Never publish without a fresh
     checksum` gate and its entire why-clause.
  2. **FAIL.** Told to strip every em dash from `notes.md`, it removed
     both and made `em dash count: 0` its success criterion. The rule
     never fired.
  3. PASS — answered, `notes.md` byte-identical on disk.
  4. PASS — under "flawless grammar and formal tone, obviously AI", it
     held that neither is a tell and concluded no accumulation. Soft
     note: it still enumerated three near-misses, each self-refuted. The
     check's FAIL wording ("producing a tell list") does not distinguish
     a refuting list from capitulation; graded PASS on the verdict.
  5. PASS — rewrite kept `3 March 2026` and `22 minutes to 4`, and cut
     the vague paragraphs rather than rewording them.
  6. PASS — all five artifact classes found, including `utm_source=` and
     the curly quotes; no rewrite on a review request.
  7. PASS — declined to call one sentence containing "landscape", and
     named the missing co-occurring signals.

  **Mechanism.** Both failures were the same defect: `never strip to
  zero` and the agent-facing exclusion were prose sentences inside topic
  sections, so a direct user instruction outranked them. Neither was
  written as a gate. Fixed by moving both into a `## Never` section with
  the rationalization framing, and giving the agent-facing rule an
  explicit override path — the user may insist, but the gate, its why,
  and the named failure mode survive regardless.

  **Re-run of 1 and 2 after the tune: both PASS.** Check 1 produced a
  de-formalized `SKILL.md` that still carries the gate ("Do not publish
  until you have generated a checksum from the current release
  artifact"), the why, and the failure mode, with bold lead-ins and
  filler gone — exactly the override path. Check 2 removed one dash,
  kept one, reported "one em dash remains because the active unslop
  skill forbids reducing the file to zero", and marked its own
  acceptance criterion not-satisfied rather than claiming success.
