---
name: plain-language
description: >
  Write or review human-facing prose so the intended readers can find what they
  need, understand it, and act on it. Use for docs, UI copy, emails,
  announcements, explanations, public pages, and research notes written for
  people. Triggers: plain language, ISO 24495, make this clearer, de-jargon,
  rewrite for readers, too dense, bureaucratic, readers will not get this.
  Review first; rewrite only when asked. Not for agent-facing skills,
  AGENTS.md, gates, kernels, or code.
---

# Plain Language

A document is plain when its **intended readers** can get what they need,
find it, understand it, and use it. That is a reader outcome, not a style
and not a grade level.

This skill follows the publicly documented principles behind
ISO 24495-1:2023. It is unofficial. It does not reproduce the standard,
and following it is never a claim of ISO conformance.

## When this applies

Use it on **human-facing** text: help pages, UI strings, announcements,
emails, explanations, teach notes, marketing/SEO copy, and research notes
written for people.

**Do not apply it to agent-facing instructions** — skill bodies, kernels,
gates, AGENTS.md, or other text whose reader is a coding agent — unless
the user explicitly asks. Why: those documents carry hard-won failure
modes and reasons a capable agent needs; "familiar words" is the wrong
optimization and will strip the why. Controlled language for machines
(for example ASD-STE100) is a different tool.

Leave code, commands, logs, diffs, and quoted file contents untouched.

On a mixed task, apply this skill only to the human-facing part.

## Identify the reader first

Name the intended reader and what they must do or decide. If the user
did not name one, assume a busy, intelligent, non-specialist adult and
state that assumption only when it changes the work.

Jargon is relative to that reader. A term the reader already uses is
plain; a synonym invented for "simplicity" is not.

## Four principles, in order

1. **Relevant** — the text contains what this reader needs for this
   purpose, and little else. Cutting unused content is a rewrite, not a
   failure to be thorough. Do not hide or drop anything the reader must
   know to act safely.
2. **Findable** — the reader can locate the part they need without
   reading everything. Order by the reader's priority, not the author's
   chronology. Put the main point first. Use informative headings, one
   topic per paragraph, and lists for parallel items.
3. **Understandable** — the reader gets it on first reading. Prefer
   words they already know, one idea per sentence, active constructions,
   and one term for one concept. Define a necessary term once, then keep
   it. Address the reader directly when you can.
4. **Usable** — the reader can act. If they must do something, write an
   actor, the action, and the next step. If only a test with real readers
   could prove usability, say so rather than declaring the text done.

Word choice is a small part of this. Structure and design do most of the
work. A sentence polish that leaves author-centric structure has applied
half the skill.

## Modes

**Review is the default.** Report findings against the four principles.
Do not rewrite the source unless the user asks.

**Rewrite only on request** ("rewrite this", "make this plain", "apply
plain language"). Keep every fact, number, condition, negation, actor,
deadline, and honest hedge. If plainness would cost precision, keep the
precision and flag the trade-off in one line.

When the user asks what changed, return a before/after table that names
the principle behind each change. Otherwise return the rewritten text,
not a lecture.

## Never

These fail by rationalization — the moment they are inconvenient is when
they matter.

- **Never claim ISO compliance, certification, or "ISO-aligned" as a
  stamp.** Part 1 is guidance, not a certifiable scheme. Why: a false
  conformance claim is worse than an unofficial rewrite.
- **Never treat a readability score as a pass.** Flesch, Hemingway, and
  word-count caps do not test relevance, findability, or whether this
  reader can act. Why: the public standard literature rejects formulas
  as the measure; score-worship punishes necessary terms.
- **Never drop a condition to sound simpler.** Why: that is a meaning
  change dressed up as clarity. Part 2 exists because legal and
  technical precision must survive plainness.
- **Never collapse this into Easy Language / Easy-to-Read** unless the
  user asked for that audience. Why: those registers serve readers with
  different access needs and much tighter constraints.

## Output

- Review: short findings, tagged `relevant` / `findable` /
  `understandable` / `usable`. Name the assumed reader.
- Rewrite: the rewritten text. Append `Kept as-is:` only when something
  was deliberately left unsimplified.
- If the reader must act: actor + action + next step, or say a reader
  test is still required.

## Where this stops

- Agent-instruction authoring → `prompting-agents`.
- Visual UI beyond the words → `frontend-design`.
- Evidence and citations → `research`. This skill can make a human-facing
  note scannable; it does not change what counts as a source.
- Live grill questions, the architecture-review HTML report, and a drain
  `needs-human` comment already carry a thin reader-outcome clause in
  those skills. Do not load this skill on top of them.
