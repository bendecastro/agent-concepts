# Concept: qmd

Reference skill for [tobi/qmd](https://github.com/tobi/qmd), a fully local CLI search engine over markdown corpora (SQLite FTS5 BM25 + vector embeddings + LLM reranking via node-llama-cpp GGUF models). The skill teaches agents when to reach for it, the search/retrieval command conventions, the indexing-authority rule (who may mutate the index in interactive vs AFK sessions), and the context-tree-as-authority-map pattern for structured corpora like `.bc-agent/` vaults.

## Why it exists

The bc-agent wiki pattern hands cold agents a growing markdown vault and tells them to read "relevant" ADRs/pages — which degrades into grep-and-hope as `decisions/`, `research/`, `findings/`, and `out-of-scope/` accumulate. qmd's hybrid search plus its per-path context descriptions give a fresh drain worker or triage agent the right three documents *pre-labeled with authority* instead of a directory listing. The same failure this guards against is on record: an agent once built a parallel PRD in `docs/` because it never found the vault's authoritative plan.

## Design decisions

- **CLI over MCP.** qmd ships an MCP server and a Claude Code plugin, but an MCP config helps exactly one harness. The CLI is the cross-vendor surface every agent (Claude Code, Pi, Grok, Codex) can use, matching this workspace's agent-agnostic posture; upstream's own README says CLI use works fine. MCP/HTTP-daemon integration can be layered per-harness later without changing this canon.
- **Driver-owns-indexing, adapted from upstream.** Upstream's `CLAUDE.md` says agents must never run indexing commands — right for a human's personal notes, wrong for an AFK pipeline where nobody is present to run `qmd update`. The adaptation keeps the rule's intent (no concurrent agent mutation of the index) while keeping the loop autonomous: the drain **driver** refreshes once at preflight; workers are search-only; interactive sessions may index with the user.
- **Contexts encode authority, not just topics.** The vault schema already defines what each directory means; seeding `qmd context add` entries with authority levels ("binding unless superseded" vs "exploratory") makes every search result self-describing for a cold agent. This is the highest-leverage use of qmd's headline feature.
- **The scaffold does not generate `.qmd/index.yml`.** `qmd init` owns its config format; the documented schema requires collection paths whose absolute/relative semantics in project-local mode were not verified, and a generated file with absolute paths would break the repo on other machines. Instead `bc-init-agent --qmd` writes a setup page (`references/qmd.md`) with the exact commands, and the agent runs them with the user, letting qmd write its own config. **Resolved 2026-07-13:** the accuracy check confirmed `qmd collection add` writes absolute paths even in a project-local `.qmd/index.yml` (v2.5.3), so the whole `.qmd/` directory is gitignored and setup is per-machine.
- **Opt-in, not default.** A young vault (a dozen files) is better served by `index.md` + grep; qmd adds a per-machine Node ≥ 22 + ~2GB model dependency. So the scaffold flag is opt-in (`--qmd`), and the consuming skills (`triage`, `bc-drain-issues` worker) gate their qmd steps on the index actually existing, falling back to manual vault reading.
- **Reference concept.** No runtime discipline gates of its own (the indexing-authority rule is enforced by the consuming pipeline concepts), so the test bar is an accuracy check against the live tool, not a pressure scenario.

## Provenance

- `raw/ingested/tobiqmd mini cli search engine for your docs, knowledge bases, meeting notes, whatever. Tracking current sota approaches while being all local.md` — web clipping of the upstream README (captured 2026-07-13), the primary source for commands, MCP details, architecture, and config schema.
- https://github.com/tobi/qmd — upstream repo; `CLAUDE.md` (agents-never-index rule, `qmd query` preference, no direct SQLite writes) and `CHANGELOG.md` (v2.6.3 current as of 2026-06-24; `qmd init` project-local indexes; `qmd skills list|get|path`) checked 2026-07-13.
- `concepts/bc-init-agent/` — the vault schema whose directory meanings seed the context tree; carries the `--qmd` scaffold flag.
- `concepts/bc-drain-issues/` and `concepts/triage/` — the consuming pipeline concepts whose retrieval steps this skill backs.

## Tests

`tests/accuracy-check.md` — verify commands/flags against a live qmd install before deploy (reference concept, no pressure scenario). Not yet run: qmd was not installed on this machine at authoring time.

## Deploy targets

- Deployed 2026-07-13 via `scripts/deploy-local-skills.py`: relative symlinks at `~/.agents/skills/qmd` (shared bus: Pi, Composer, Grok, Codex), `~/.pi/agent/skills/qmd`, and `~/.claude/skills/qmd`, all resolving to `body/` (verified; Claude Code advertised the skill immediately).
- Other harnesses: manual bootstrap per `../../harnesses.md`.
