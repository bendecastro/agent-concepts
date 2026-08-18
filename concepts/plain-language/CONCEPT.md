# Concept: plain-language

Model-invoked discipline for human-facing prose, with a user-invoked
review/rewrite trigger. It applies the publicly documented reader-outcome
principles behind ISO 24495-1:2023 so intended readers can get what they
need, find it, understand it, and use it. It is unofficial and does not
claim ISO conformance.

## Design decisions

- **Named `plain-language`, not `iso-24495`.** Naming the concept after
  the standard would imply conformance we cannot honestly claim. The ISO
  catalog number stays in provenance and in the skill description so the
  words people actually say still fire it.
- **Human-facing only.** This workspace already writes a different
  audience in skill bodies, kernels, and gates. IPLF itself distinguishes
  plain language (human readers) from controlled languages (restricted
  grammar for machines or zero-ambiguity manuals). Applying reader-outcome
  "familiar words" to agent instructions would strip the why those
  documents exist. The inversion is the load-bearing rule.
- **Not always-on, not in the kernel.** Chat already has answer-first and
  verbosity clamps. An always-on rewrite would fight agent-instruction
  authoring and spend scarce always-on budget on a task that is only
  sometimes the job. Escalate to a kernel pointer only if drift shows
  after deploy.
- **Review default, rewrite on request.** Silent rewrites hide meaning
  changes. The predictable failure mode is an agent "helpfully" editing
  a source file the user only asked it to judge.
- **Principles, not numeric proxies.** Unofficial skills in the wild
  encode 20-word sentences and "ISO-aligned" stamps. Those are author
  proxies, not ISO clauses, and they punish necessary terms. The body
  stays at the four public outcomes plus a few rationalization gates.
- **Public sources only.** The ISO text is sold. The body paraphrases
  IPLF's freely published definition and four principles plus ISO's
  public abstract/scope. It does not vendor standard clauses or leaked
  previews.
- **Unofficial prior art considered, not vendored.**
  `danyuchn/iso-24495-skill` is the closest structural match
  (principle/technique split, fact-preservation, no conformance claim,
  agent-facing exclusion). `GaZmagik/iso-24495` is the most engineered
  (five skills, linter, always-on style) and the cautionary tale
  (hard caps, "Aligned" stamps, unpublished Parts 4–5). Neither body
  is copied; both are cited so the rejections stay auditable.
- **No Parts 2–5 skills.** Legal, science, organizational certification,
  and document-design parts are either specialist or unpublished. A
  later concept can extend this one if the user actually writes those
  documents. CAN-ASC-3.1:2025 is a free Canadian accessibility standard
  that is ISO-aware and conformity-assessable; it is out of scope until
  that audience is in play.
- **Composes, does not merge.** `frontend-design` still owns visual UI;
  `prompting-agents` still owns agent-instruction authoring; `research`
  still owns evidence. This skill may make the human-facing words in
  those artifacts scannable.
- **Thin clauses on speakers, not a skill load (2026-08-18).** Live grill
  questions, the architecture-review HTML report, and a drain
  `needs-human` comment each carry a 2–4 line reader-outcome delta in
  the skill that actually speaks. Loading this body there would bring
  review-default into a write-plain-first turn and risk "familiar words"
  stripping deep-module vocabulary or evidence. Issue-slicing quizzes,
  teach HTML, PRDs, and Agent Briefs were considered and left unwired.

## Provenance

- [ISO 24495-1:2023 catalog](https://www.iso.org/standard/78907.html) —
  official title, scope, language-neutrality, text-primary limit.
- [ISO 24495-2:2025](https://www.iso.org/standard/85774.html) and
  [ISO 24495-3:2026](https://www.iso.org/standard/86938.html) — later
  parts noted as out of scope, not implemented.
- [International Plain Language Federation — ISO standard](https://www.iplfederation.org/iso-standard/)
  — four principles, language-neutrality, "guidance only / not for
  certification," Parts 2–4 status.
- [IPLF — what is involved in writing plain language](https://www.iplfederation.org/plain-language/)
  — 2014 definition; wording / structure / design; reader testing;
  distinction from Easy Language and controlled languages.
- [IPLF — word choice](https://www.iplfederation.org/word-choice) —
  ~7% of the standard's ideas concern word choice; readability formulas
  are not the measure.
- [`raw/ingested/iso-24495-iplf/`](../../raw/ingested/iso-24495-iplf/SOURCE.md)
  — citation record of the public sources above; no ISO text.
- [danyuchn/iso-24495-skill](https://github.com/danyuchn/iso-24495-skill)
  — unofficial MIT prior art; structural influence only.
- [GaZmagik/iso-24495](https://github.com/GaZmagik/iso-24495) —
  unofficial MIT prior art; rejected as a body (always-on, numeric
  proxies, conformance-flavored examples).
- `concepts/prompting-agents/body/SKILL.md` — altitude, explain-the-why,
  gates only for rationalization.

## Tests

`tests/pressure-plain-language.md` — discipline-enforcing, so the test
gate applies before deploy. Attacks the predictable excuses: simplify a
skill under time pressure, stamp ISO compliance, ship on a Flesch score,
drop a condition to sound simpler, rewrite when asked only to review.

**Run 2026-08-18 in headless Pi (Grok 4.6, low thinking) against isolated
fixture copies: PASS 6/6.** All four load-bearing checks held (inversion,
no stamp, condition survival, review-does-not-rewrite). Soft note in the
test file: the rewrite refusal slightly mislabeled the standard as
“unofficial.”

## Deploy targets

Deployed 2026-08-18 via `scripts/deploy-local-skills.py`, all three relative
symlinks verified to resolve:

- Shared bus: `~/.agents/skills/plain-language` → `body/` (also reaches
  Composer and Grok).
- Pi: `~/.pi/agent/skills/plain-language` → `body/`.
- Claude Code: `~/.claude/skills/plain-language` → `body/`.

Other harnesses: manual bootstrap; see `../../harnesses.md`.
