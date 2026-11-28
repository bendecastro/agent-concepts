# Lint catches rules repeated across skills and keeps deliberate copies in sync

Why: The 2026-11-27 modularity scan found one storage paragraph in 11 skills and other rules in 3–12, each drifting, because nothing compares one skill's text with another's. Some copies are deliberate (children do not load the kernel; a skill installed alone must work), so the goal is that every copy is either a load or a tracked copy.
Done when: `scripts/lint.py` warns on a paragraph of about 40+ words repeated near-verbatim in two concept bodies unless one is marked `<!-- copy-of: <concept>#<anchor> -->`; marked copies fail lint when they no longer match their source; the Implement operation in AGENTS.md and `bc-prompting-agents` tell authors to search for an owner before writing a rule; the repeated-text warning becomes an ERROR once 054–058 have landed.
Stage: now
Blocked by: nothing
Kind: build
Source: owner pick 1, 2026-11-27 (drift prevention after the modularity scan)
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes

## Requirements

- Repeated-text check: compare paragraphs (word shingles or similar, standard library only) across `concepts/*/body/**/*.md`; threshold and minimum length are constants with a test; skip code blocks, frontmatter and generated files; report both locations and the overlap.
- `copy-of` marker: names the source concept and a heading anchor; lint resolves it (missing source or anchor = ERROR) and compares the marked block to the source block after whitespace normalization (mismatch = ERROR naming both). Reuse the kernel-copies comparison where it fits.
- Authoring guidance: one sentence in AGENTS.md § Implement/Update, one clause in `bc-prompting-agents`: before writing a rule, `rg` the bodies; owned elsewhere → load or `copy-of`; held by two others already → split into a module. Lint enforces it, so no pressure test (accuracy check only).
- Release audit (`docs/guides/releasing.md`): optional rerun of the modularity scan (brief in `~/.local/state/bc-swarm/2026-11-27-agents-modularity/brief.md`; copy it into `docs/` as a reusable brief).
- On today's tree the check must warn, not fail (the gate stays green); add a follow-up step to switch to ERROR.

## Steps

- [x] Add the repeated-text warning and the `copy-of` sync check with tests. Done when a fixture with a repeated paragraph warns, a marked copy that matches passes, a drifted marked copy fails, and `python3 scripts/lint.py` on the tree has 0 ERROR.
- [x] Add the authoring sentence, the prompting-agents clause and the release-audit note. Done when lint passes and the three places say the same rule.
- [ ] After 054–058 land, switch the repeated-text check to ERROR. Done when lint on that tree has 0 ERROR with the stricter level.

## Outcome

_To be filled when finished or dropped._
