---
test_kind: pressure
test_status: pass
tested: 2026-08-17
deployed: 2026-08-17
---
# Concept: minimal-solution-ladder

Model-invoked discipline for deciding **how much to build** before writing code: an ordered ladder (need it at all → already in this codebase → stdlib → native platform feature → installed dependency → one line → minimum that works), stopped at the first rung that holds, with an absolute never-simplify list and a marker convention for deliberate corner-cuts. Adapted from DietrichGebert/ponytail.

## Design decisions

- **Adapted, not vendored — because the conflicts had to be arbitrated locally.** Precedent split: `herdr` and `notebooklm` keep upstream bodies verbatim (they are references to someone else's tool), while `obra-superpowers` and the Pocock skills were rewritten into local canon (they are disciplines that must interoperate with the rest of this workspace). This is the second kind: three of its rules pull against existing concepts, and a verbatim copy would leave an agent holding two instructions and no precedence.
- **Renamed from `ponytail`.** The upstream name is a persona joke, opaque cold. Local convention is descriptive dash-case. The user's trigger phrases (`"ponytail"`, `"be lazy"`, `"yagni"`, `"simplest solution"`) are preserved in the skill `description` so the words people actually say still fire it. `lazy-ladder` was the user's first choice, rejected as still under-descriptive; `solution-sizing` rejected because "sizing" reads as estimation.
- **~95% of the upstream repository was discarded as distribution machinery.** Plugin manifests for ~20 harnesses, lifecycle hooks, an MCP server, a statusline, a Pi extension, and a promptfoo suite. This workspace deploys by symlink through `scripts/deploy-local-skills.py`; none of that is substance.
- **Only the primary skill was adapted.** The five companions (`ponytail-audit`, `-debt`, `-gain`, `-review`, `-help`) are workflow wrappers around the same ladder; `-help` exists only to explain the plugin's own mode commands, which do not exist here. Adapting them would add five near-duplicate bodies for one idea. They remain in the raw snapshot so the decision stays auditable.
- **Arbitration 1 — vs `codebase-design`.** Upstream's "fewest files, shortest diff" pulls toward inlining; deep modules pull toward *more* implementation behind a small interface. Resolved by scope, stated in the body: this skill governs *whether and how much* to build, `codebase-design` governs *shape once you build*, and "fewest files" never overrides a real seam. Without this line an agent holding both gets a genuine conflicting pull. The two already agree on the sharpest case — upstream's "no interface with one implementation" is `codebase-design`'s "one adapter means a hypothetical seam."
- **Arbitration 2 — vs `tdd` and `bc-drain-issues`.** Upstream mandates ONE assert-based check and forbids frameworks and fixtures, which directly contradicts red-green-refactor and the drain's review axes. Kept as a **floor outside those disciplines**, explicitly subordinate when either is active. Deleting it entirely was rejected: outside a TDD flow it is the only thing preventing "minimal" from meaning "unverified."
- **Arbitration 3 — vs harness built-ins.** Claude Code's own system prompt already carries YAGNI, no-premature-abstraction, and no-speculative-error-handling; `agent-kernel` already carries "smallest safe change set" and "implement exactly what was requested." The body was cut to the **delta**: the ladder's ordering (especially rung 4, native platform features, which nothing local encodes), root-cause-as-the-lazy-fix, the ceiling marker, and the auditable-skip output line. Restating the shared material would spend context to say what the harness already said.
- **"Explicitly requested" was scoped to behavior, not shape (2026-08-18 tune).** Upstream's never-simplify list ends with "anything explicitly requested," which in practice **absorbed rung 2**: asked to "add a function" for something `utils.slugify` already did, agents shipped a forwarding wrapper and called it reuse — 3/3, and the no-skill control did it too, so the skill was failing to prevent baseline behavior rather than causing it. Both instruments agreed on the mechanism, and self-critique on two models independently proposed the same fix. Adopted as the general rule (the phrasing of a request pre-commits a shape — function, class, file, endpoint — and the noun is not the order) rather than as the reported symptom ("don't wrap helpers"). The same tune **deleted** "Two rungs work → take the higher one and move on," which both models nominated unprompted: "higher" is undefined on a numbered list and it adds nothing over stop-at-the-first-rung.
- **`ponytail:` marker renamed to `ceiling:`.** A greppable marker must be self-explanatory; `ceiling:` names what the comment records. This is a deliberate divergence from upstream and breaks grep-compatibility with upstream-marked codebases — acceptable, since nothing in the user's repos carries the old marker.
- **The ceiling comment is an explicit exception to the local no-comments default,** and the body says why it earns it: the ceiling is a hidden constraint unrecoverable from the code, and an unmarked shortcut is indistinguishable from an oversight.
- **Persistence deliberately not implemented.** Upstream's "ACTIVE EVERY RESPONSE" is not a prompt property — it is enforced by per-turn hook re-injection plus mode state in its Pi extension. Options considered: (a) skill-only, model-invoked; (b) a two-line ladder pointer in the always-on `agent-kernel`; (c) vendoring the Pi extension. Chose **(a)**: (c) takes a runtime code dependency this workspace has never taken and breaks the concepts-not-plugins shape, and (b) spends deliberately scarce always-on budget before any evidence that drift matters. Escalate to (b) only if a pressure run shows the ladder decaying across turns. Consequence to accept: without hooks, the discipline fades over a long session and may need re-invoking.
- **Intensity collapsed from persistent mode state to an invocation argument.** With no mode store, `lite|full|ultra` cannot persist; `argument-hint` is the honest equivalent. `full` remains the default.
- **Upstream's effect sizes are cited but not relied on.** The headline (−54% LOC, −22% tokens, 100% safety-preserved, Haiku 4.5, n=4) is self-measured. It is more credible than a typical README claim because upstream publicly retracted an earlier inflated 80–94% figure after issue #126 identified a conversational-baseline artifact — but it is still the author's own benchmark, and the local test gate governs deployment, not their numbers.

## Provenance

- [`raw/ingested/ponytail-upstream/`](../../raw/ingested/ponytail-upstream/SOURCE.md) — immutable MIT snapshot of `DietrichGebert/ponytail` at commit `2ed6c52c9d7e5e56942508591085fd45dea277d3` (2026-08-07): `skills/ponytail/SKILL.md` (the adapted body), the five companion skills, upstream `AGENTS.md`, `README.md`, `LICENSE`, and the 2026-06-18 agentic benchmark writeup.
- `concepts/codebase-design/body/SKILL.md` — the deep-module vocabulary this skill defers to for shape; source of arbitration 1.
- `concepts/tdd/` and `concepts/bc-drain-issues/` — the test disciplines this skill is subordinate to; source of arbitration 2.
- `concepts/agent-kernel/body/AGENT-KERNEL.md` — the always-on baseline whose overlap determined what to cut; also the precedent for the anti-duplication reasoning in arbitration 3.
- `concepts/prompting-agents/body/SKILL.md` — gate/why phrasing.

## Tests

`tests/pressure-minimal-solution-ladder.md` — discipline-enforcing, so the test gate applies. Attacks the predictable failure modes: build-it-for-later, drop the "internal" validation, the small-diff-in-the-wrong-place fix, truncating an explanation the user explicitly asked for, and the tdd precedence conflict.

**Run 2026-08-17 in headless Pi (Grok 4.6, low thinking) against a fixture repo carrying every bait: PASS 10/10, after one skill fix.** All three load-bearing checks held first time, including two rounds of pressure to drop trust-boundary validation. Check 7 failed twice — the model named a real O(n²) ceiling in its *response* but left no marker in the code, because the Output section's `skipped:` line was absorbing the obligation. The body now states that the response line does not discharge the code marker, with the why; the re-run produced `# ceiling: O(n^2) SequenceMatcher; fine for tens of rows` in the source. Full transcript-level detail and three soft findings are recorded in the test file.

## Deploy targets

Deployed 2026-08-17 via `scripts/deploy-local-skills.py`, all three relative symlinks verified to resolve:

- Shared bus: `~/.agents/skills/minimal-solution-ladder` → `body/` (also reaches Composer and Grok).
- Pi: `~/.pi/agent/skills/minimal-solution-ladder` → `body/`.
- Claude Code: `~/.claude/skills/minimal-solution-ladder` → `body/`.

Other harnesses: manual bootstrap; see `../../docs/harnesses.md`.
