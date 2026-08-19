# Concept: unslop

Model-invoked discipline for removing the tells that make human-facing
text read as machine-generated, and for putting specifics back where the
tells were. Covers shipped prose (docs, READMEs, announcements, copy,
research writeups) and shipped artifacts (commit messages, PR and issue
bodies). Adapted from Cursor's `unslop` plugin skill, rebuilt against the
primary field guide it descends from and corrected where 2026 evidence
contradicts it.

## Design decisions

- **Provenance tells only; reader outcomes belong to `plain-language`.**
  Six of Cursor's 31 rules (filler phrases, hedging, dense sentences,
  active voice, adverbs, plain-word swaps) are general prose quality that
  `plain-language`'s *understandable* principle already owns. They were
  cut and replaced with a pointer. Why: one home per rule, and the two
  skills answer different questions — text can be perfectly plain and
  still obviously machine-written. The plain-word swaps survive in a
  single compressed line because they double as AI vocabulary.
- **Model-invoked, not always-on.** Cursor's version declares "Must
  always apply." That would fight this workspace's own house style
  (`index.md`, `log.md`, and every skill body use em dashes, bold
  lead-ins and deliberate triads) and would spend always-on budget on a
  minority of turns. The always-on slot here is `agent-kernel`, which is
  deliberately tiny.
- **Agent-facing text is inverted out of scope.** Skill bodies,
  `AGENTS.md`, kernels and gates go to `prompting-agents`. Why: those
  documents deliberately use the structures this skill flags, and their
  why-clauses are exactly what an unslop pass would strip. Same inversion
  `plain-language` carries, for the same reason. Not raised during the
  grill; derived from the branch-2 seam and flagged to the user on
  delivery.
- **The em dash ban was replaced with a formulaic-use rule.** Cursor's
  rule 13 ("avoid em dashes entirely", and no parentheses as a
  substitute) is the list's most absolute rule and its least supported.
  The Economist's July 2026 corpus found only Claude exceeds professional
  human writers on em dashes, ChatGPT uses markedly fewer than any human
  corpus measured, and GPT-5.1 was tuned to suppress them; the same study
  found AI already uses hardly any parentheses. An absolute ban would
  flag this repository's entire documentation as slop, and pushing to
  zero walks into the next signature. The skill names over-correction as
  its own tell.
- **Artifacts are a first-class class.** Placeholders, vendor paste junk,
  `utm_source=`, curly quotes, and canned assurance in commit messages
  and PR bodies. Wikipedia keeps a whole edit-summary section that maps
  onto agent commit messages, and `bc-drain-issues` writes those here.
  These tells are mechanical and do not decay, unlike vocabulary.
- **An `rg` block, not a scanner.** The exact-string class is pure
  mechanism, and one `rg` alternation is the lowest rung that holds.
  Verified 2026-08-19 against a five-defect fixture (all matched) and a
  clean file (no false positives). A real scanner with counting is the
  next rung if the block proves insufficient; nothing needs it yet.
- **No statistical thresholds.** The Economist scalars (word length
  5.02 vs 6.17, Latinate ratio 0.094 vs 0.131, semicolons 7.32 vs 0.43
  per 1000) were deliberately not shipped. The article is paywalled and
  could not be read at source; the figures come from a third-party
  summary whose own author warns the study publishes no frequency counts
  and that its baseline corpus differs from the register being linted.
  Shipping unvalidated thresholds would be false confidence. The signals
  survive qualitatively ("every sentence in the same band, no semicolons,
  no parentheses") as accumulation evidence.
- **The two "never" rules live in a `## Never` section, not in their
  topic sections (2026-08-19, from the pressure test).** Both were
  originally prose sentences inside the em dash and scope sections, and
  both failed on first run: a direct user instruction outranked them
  every time. Moving them into a gate block with the rationalization
  framing fixed both. The agent-facing rule also carries an explicit
  override path — the user may insist on a skill body, but the gate, its
  why, and the named failure mode survive — because a flat refusal is not
  what the user needs and a flat capitulation is what strips the file.
- **Guard rails against the skill itself.** Three, all absent upstream:
  a dated vocabulary tier ranked below constructions because word tics
  decay once mocked while constructions persist; an explicit *do not
  flag these* list; and a symptoms-not-disease opener stating that
  removing tells without adding specifics is a failed pass. Without
  these, the skill's own failure mode is over-correction into a
  different signature.
- **Register caveat kept visible.** "Significant" is AI-overused against
  news and fiction and ordinary in law, finance and science. A word list
  applied across registers fires on good prose, and a skill with a high
  false-positive rate gets ignored.
- **Accumulation, not single hits.** The skill requires two co-occurring
  patterns from different sections before calling text machine-written,
  and states that humans judge this near chance while heavy LLM users
  reach roughly 90%. Why: the upstream list reads as a checklist of
  individually damning items, which is how false accusations happen.
- **Modes split by ownership.** Silent self-edit on the agent's own
  drafts; report-first on text it did not write. Asking permission to fix
  your own unshipped draft is noise; silently rewriting the user's voice
  is a meaning change they did not authorize.
- **Name kept as `unslop`.** Cursor's name and the user's word for it.

## Provenance

- [cursor/plugins `pstack/skills/unslop/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md)
  — the source skill. Structure, mode framing, and the majority of the
  content/language/style tells. Upstream declares no license (checked
  2026-08-19, GitHub API reports `license: null`), so the body is cited,
  not redistributed. See
  [`raw/ingested/unslop-cursor/`](../../raw/ingested/unslop-cursor/SOURCE.md).
- [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
  (WikiProject AI Cleanup, CC BY-SA) — the primary field guide the Cursor
  list descends from; read as raw wikitext 2026-08-19. Source of the
  regression-to-the-mean frame, the symptoms-not-disease warning, the
  negative-parallelism variants, vague connection, phrasal placeholders,
  vendor paste artifacts, edit-summary canned assurance, document-shape
  and heading pathologies, and the *ineffective indicators* list.
- [Dragonfly Editorial, "AI Tells, and How to Fix Them"](https://dragonflyeditorial.com/ai-tells/)
  — sentence schemas absent from both lists above: "whether X or Y",
  fragment question-answer, general-colon-specific, the general purpose
  clause tacked onto a specific sentence, and the four-move paragraph
  template.
- ["How to spot AI writing", The Economist, 30 July 2026](https://www.economist.com/culture/2026/07/30/how-to-spot-ai-writing)
  — the em dash correction. **Not read at source** (paywalled; archive
  mirrors rate-limited 2026-08-19). Reached through
  [edwinhu/workflows `12-economist-2026-corpus-study.md`](https://github.com/edwinhu/workflows/blob/main/skills/ai-anti-patterns/references/12-economist-2026-corpus-study.md),
  whose account of the em dash finding is independently corroborated by
  the Wikipedia guide's own citation of the same study. The scalar
  figures from that summary were deliberately not adopted.
- [Geng & Trotta, "Human-LLM Coevolution: Evidence from Academic Writing", ACL Findings 2025](https://aclanthology.org/2025.findings-acl.657/)
  — measured decline of "delve" and related tics after public mockery;
  the basis for dating the vocabulary tier and ranking it below
  constructions.
- [Ars Technica on GPT-5.1 em dash suppression](https://arstechnica.com/ai/2025/11/forget-agi-sam-altman-celebrates-chatgpt-finally-following-em-dash-formatting-rules/)
  — cited via the Wikipedia guide.
- `concepts/plain-language/body/SKILL.md` — the seam, and the model for
  the agent-facing inversion and the mode split.
- `concepts/prompting-agents/body/SKILL.md` — altitude, explain-the-why,
  gates reserved for rationalization failure modes.

**Considered and not adopted:** holdyourvoice.com's four-signal framework
(sentence-length variance, transition fingerprint, vocabulary specificity
ratio, structural adherence). The ideas are sound and appear in the body
qualitatively, but the supporting figures are vendor-published
self-reported studies with no method disclosure, so nothing numeric was
taken. Stylometric detection papers (StyloAI, SemEval-2024 Task 8) were
read and left out: they build classifiers, not editing guidance.

## Tests

`tests/pressure-unslop.md` — discipline-enforcing, so the test gate
applies before deploy. Attacks the three gates that convert this skill
into a net harm: the agent-facing inversion, the strip-to-zero
over-correction, and the report-does-not-rewrite boundary; plus the
false-positive guard and the symptoms-not-disease rule.

**Run 2026-08-19 against isolated fixture copies: PASS 7/7, after one
tune.** First pass was 5/7 with both em-dash and agent-facing gates
failing; both were prose sentences rather than gates, both now live in
`## Never`, and both re-ran PASS. Two caveats recorded in the test file:
the run used Luna at max thinking because no low-reasoning provider was
available, and check 2's original fixture target could not fire the gate
(fixed). Consumer was `openai-codex/gpt-5.6-luna:max`, not the author's
model.

## Deploy targets

Deployed 2026-08-19 via `scripts/deploy-local-skills.py`, all three
relative symlinks verified to resolve:

- Shared bus: `~/.agents/skills/unslop` → `body/` (also reaches Composer
  and Grok).
- Pi: `~/.pi/agent/skills/unslop` → `body/`.
- Claude Code: `~/.claude/skills/unslop` → `body/`.

Other harnesses: manual bootstrap; see `../../harnesses.md`.
