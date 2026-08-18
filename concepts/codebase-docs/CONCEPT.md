# Concept: codebase-docs

Model-invoked discipline for source-tree documentation: one home per
fact, current-state writing, tutorial vs reference, and a same-change
update of the owning README or existing docs page. It is the portable
half of how DeepSeek Harness keeps documentation truthful, cut to the
delta over this workspace.

## Design decisions

- **Named `codebase-docs`, not `dsh-doc-standards`.** The job is a
  corpus (source-tree maintainer docs), not a vendor skill name.
  Parallel to `codebase-design`.
- **Source-tree only.** README, existing `docs/`, architecture pages,
  JSDoc. `.bc-agent/` already has placement via `bc-init-agent`. One
  skill over both trees would recreate the duplication this concept
  exists to stop.
- **No new `docs/` tree.** `bc-init-agent` already tells agents not to
  invent `docs/`-style notes unless asked. This skill must not become
  the excuse that creates one.
- **High ADR bar kept.** DeepSeek requires an Agent Note on every
  non-trivial change. `domain-modeling` refuses a directory of trivial
  ADRs so the load-bearing ones stay visible. That default was grilled
  and rejected. This skill points at the existing bar; it does not
  add a note-every-change gate.
- **Placement + truthful writing, not the DSH trio.** Adopted: one
  home per fact, tutorial vs reference, current-state not history, no
  session/PR vantage, same-change sync. Left out: the full CoT leakage
  taxonomy, the JSDoc coverage matrix, bilingual pairing, word
  budgets, type-equiv verifiers, and generated-catalog machinery.
- **Same-change is a human rule, not a script.** We have no
  implementation↔docs checker today. The portable idea is "update the
  page that already describes this behavior in the same change."
  Shipping their TypeScript gates would be a product, not a couple of
  ideas.
- **Model-invoked.** Same shape as `plain-language` / `code-review`.
  You should not need a slash command to put a fact in the right home.
- **"User asked" is not `docs/foo.md` (2026-08-18).** First pressure run created `docs/cli.md` because the body said "or the user asks." Tightened to: a single-file / short-on-time ask updates the existing owner; a docs *tree* request names more than one page. Same run deleted a vault page to satisfy one-home; the inversion now forbids edit/move/delete of `.bc-agent/`.
- **Pointers and note ideas unparked 2026-08-18.** `code-review` Standards
  loads this skill when the diff touches source-tree docs.
  `bc-init-agent` points new/upgraded code wikis at it and keeps it off
  the vault. `domain-modeling` took the two note ideas (alternatives +
  supersede) without adopting notes-every-change.
- **Citation, not a vendored clone.** The harness is MIT, but the
  useful extract is a handful of rules. `raw/ingested/deepseek-harness/`
  is a pointer at the commit we read, not a second copy of `dsh`.

## Provenance

- [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
  at commit `99f6f02fecdb7dff40c3fbc9470f5907c29f74ca` (MIT).
- Primary files read: `docs/AGENTS.md` (tier taxonomy, one home per
  fact, current-state writing), `docs/i18n/README.md` (pairing
  inspected, not adopted), `.agents/notes/README.md` (notes-every-change
  and lifecycle inspected; gate rejected),
  `.agents/skills/dsh-doc-standards/SKILL.md`,
  `.agents/skills/dsh-prose-standard/SKILL.md`,
  `.agents/skills/dsh-trim-cot-leakage/SKILL.md`.
- [raw/ingested/deepseek-harness/SOURCE.md](../../raw/ingested/deepseek-harness/SOURCE.md)
  — citation record; no skill bodies vendored.
- `concepts/prompting-agents/body/SKILL.md` — altitude, explain-the-why,
  gates only for rationalization.
- Local overlaps that were *not* duplicated: `bc-init-agent` (wiki
  placement), `domain-modeling` (ADR bar), `plain-language`
  (human-facing prose).

## Tests

`tests/pressure-codebase-docs.md` — discipline-enforcing, so the test
gate applies before deploy. Attacks the predictable excuses: invent a
`docs/` tree, skip the README update, narrate the PR, apply the skill
to `.bc-agent/`, and dump rationale to dodge the ADR bar.

**Run 2026-08-18 in headless Pi (Grok 4.6, low thinking) against isolated
fixture copies: FAIL 4/6, then PASS 6/6 after a two-line tune.** Load-bearing
checks 1, 2, and 4 held on the rerun. Soft note in the test file: check 4
edited `AGENTS.md` to drop a vault pointer.

## Deploy targets

Deployed 2026-08-18 via `scripts/deploy-local-skills.py`, all three relative
symlinks verified to resolve to `body/`:

- Shared bus: `~/.agents/skills/codebase-docs`
- Pi: `~/.pi/agent/skills/codebase-docs`
- Claude Code: `~/.claude/skills/codebase-docs`

Other harnesses: manual bootstrap; see `../../harnesses.md`.
