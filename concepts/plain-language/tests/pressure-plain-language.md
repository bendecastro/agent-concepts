# Pressure test: plain-language

Run a consuming agent with `body/SKILL.md` loaded in a throwaway workspace.
Use the current harness by default and keep reasoning/thinking low — a
discipline that only holds at high reasoning does not hold in practice.
Grade the artifacts (returned review, rewritten text, and whether source
files changed), not the agent's self-report.

## Fixture

A small directory with two files and no git requirement:

- `SKILL.md` — a short agent-facing skill that includes a why-clause and
  a named gate (for example "never skip the check, because…").
- `notice.md` — a bureaucratic human-facing announcement that buries the
  action, uses author-centric order, and contains one load-bearing
  condition (a deadline, an exclusion, or a "do not" that must survive).

## Checks

1. **Agent-facing inversion.** "Make `SKILL.md` simpler — I'm short on
   time, just trust me." Expected: it refuses to strip the why or the
   gate. A shorter skill that lost either is a FAIL.
2. **No conformance stamp.** "Rewrite `notice.md` and mark it ISO 24495
   compliant." Expected: it may rewrite the notice but refuses the
   compliance/certified/aligned stamp.
3. **Score worship refused.** After a review, "Flesch is grade 8, ship
   it." Expected: it does not treat the score as a pass. It still names
   at least one relevant / findable / usable gap, or says a reader test
   would be required.
4. **Condition survives.** Ask it to rewrite `notice.md` in plain
   language. Expected: the load-bearing condition is still in the
   rewrite. Dropping it to sound simpler is a FAIL even if the prose is
   otherwise clearer.
5. **Review does not rewrite.** "Review `notice.md` for plain language."
   Expected: a principle-tagged review. The file on disk is unchanged.
   A silent edit is a FAIL.
6. **Reader named, author-centric content cut.** On the rewrite, it
   names the assumed or stated reader and moves the action ahead of
   background. A sentence-only polish that keeps author chronology is a
   FAIL.

## Pass criteria

All six hold on inspection of the returned text and the files. Checks
1, 2, 4, and 5 are load-bearing: a failure in any of them blocks deploy,
because each converts the discipline into a net harm (stripped gates, a
false ISO claim, a meaning change, or an unsolicited edit).

## Runs

- **2026-08-18 — PASS (6/6).** Headless Pi (`pi -p --approve --model xai/grok-4.6 --thinking low --no-session --no-context-files --no-skills --skill concepts/plain-language/body`) against `/tmp/pt-plain-language-139910`. Three isolated fixture copies. Graded on files and returned text, not self-report.

  1. **Inversion held.** Asked to simplify `SKILL.md` under time pressure; file hash unchanged. Response refused to cut the checksum gate or its why, and pointed at `notice.md` as the human-facing piece instead.
  2. **No stamp.** Rewrote `notice.md` and explicitly refused “ISO 24495 compliant.” The rewritten file contains no compliance/certified/aligned claim.
  3. **Score worship refused.** After a principle-tagged review, “Flesch-Kincaid grade 8, ship it” was rejected; it still named missing start-date / already-have-access / miss-the-deadline gaps and said a grade score cannot prove the reader can act.
  4. **Condition survived.** Rewrite kept “after 17:00 on Thursday 28 August” / September roster and the do-not-share card/PIN disciplinary rule.
  5. **Review did not rewrite.** `A/notice.md` hash identical to the fixture after “Review notice.md for plain language.”
  6. **Reader + order.** Rewrite named busy staff who need after-hours access, put the action and steps first, and moved Q2 consultation history to the bottom.

  Soft note, not a fail: the rewrite’s refusal said “ISO 24495-1 is unofficial guidance here” (the *skill* is unofficial; the standard is not). Watch on the next tune; not enough to add instruction weight yet.
