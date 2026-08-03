# Concept: qmd

Reference skill for [tobi/qmd](https://github.com/tobi/qmd), a fully local CLI search engine over markdown corpora (SQLite FTS5 BM25 + vector embeddings + LLM reranking via node-llama-cpp GGUF models). The skill teaches agents the **global-mode** architecture used here (one index, collections per knowledge base, searchable from any cwd), the search/retrieval command conventions, the indexing-authority rules (canon file + setup script own collections; timer/driver own freshness; workers search-only), and the context-tree-as-authority-map pattern.

## Requirements

`qmd` installed, plus at least one collection registered in the global index. This
workspace assumes global mode: one index, collections per knowledge base. Project-local
`.qmd/` directories are deliberately unsupported — they shadow the global registry.

## Why it exists

The bc-agent wiki pattern hands cold agents a growing markdown vault and tells them to read "relevant" ADRs/pages — which degrades into grep-and-hope as `decisions/`, `research/`, `findings/`, and `out-of-scope/` accumulate. qmd's hybrid search plus its per-path context descriptions give a fresh drain worker or triage agent the right three documents *pre-labeled with authority* instead of a directory listing. The same failure this guards against is on record: an agent once built a parallel PRD in `docs/` because it never found the vault's authoritative plan.

## Design decisions

- **CLI over MCP.** qmd ships an MCP server and a Claude Code plugin, but an MCP config helps exactly one harness. The CLI is the cross-vendor surface every agent (Claude Code, Pi, Grok, Codex) can use, matching this workspace's agent-agnostic posture; upstream's own README says CLI use works fine. MCP/HTTP-daemon integration can be layered per-harness later without changing this canon.
- **Driver-owns-indexing, adapted from upstream.** Upstream's `CLAUDE.md` says agents must never run indexing commands — right for a human's personal notes, wrong for an AFK pipeline where nobody is present to run `qmd update`. The adaptation keeps the rule's intent (no concurrent agent mutation of the index) while keeping the loop autonomous: the drain **driver** refreshes once at preflight; workers are search-only; interactive sessions may index with the user.
- **Contexts encode authority, not just topics.** The vault schema already defines what each directory means; seeding `qmd context add` entries with authority levels ("binding unless superseded" vs "exploratory") makes every search result self-describing for a cold agent. This is the highest-leverage use of qmd's headline feature.
- **Global mode only; project-local indexes banned (supersedes the 2026-07-13 morning `--qmd` per-repo design, user decision same day).** Verified against v2.5.3: a project-local `.qmd/` **shadows the entire global registry** from anywhere inside that repo, and its config stores absolute paths (per-machine, can't be committed) — so per-repo indexes create search blind spots while delivering none of the "travels with the repo" benefit. Drain worktrees live outside the main checkout, so workers could never see a gitignored `.qmd/` anyway; global collections are reachable from any cwd, including worktrees. The `bc-init-agent --qmd` scaffold flag and per-vault `references/qmd.md` page were removed in the same pass.
- **Synced canon + convergence script own the collection set.** The registry lives at `~/Sync/Scripts/config/qmd-collections.yml` (`~/`-based paths; contexts with authority labels; five initial collections: agents, wiki, music, scripts, image-maze); `Scripts/bin/setup/bc-qmd-setup` idempotently converges each machine via the qmd CLI (ignore lists are YAML-only upstream, so those alone are patched into the machine registry), installs the daily `bc-qmd-refresh.timer` where systemd exists, and is run by `qmd.pkg`'s `post_install`. Ad-hoc `qmd collection add` outside the canon is disallowed — machines would drift.
- **New vaults register by default (opt-out).** `bc-init-agent`'s close-out appends the new vault to the canon and runs `bc-qmd-setup`, asking only whether the user wants the vault *excluded*. Chosen over opt-in because the realistic failure is a vault silently never joining the index.
- **Body describes the pattern, not one machine's commands (2026-08-03).** The skill body originally named this workspace's own wrapper scripts and collections file, which made it useless to anyone else and implied tooling they do not have. It now states the rule — collection definitions in one version-controlled file, applied by a single setup command, one owner for mutations — and marks the author's implementation as one example. The durable findings (project-local `.qmd/` shadowing, latency tiers, authority-labelled contexts) are the reusable part and stay stated plainly.
- **Reference concept.** No runtime discipline gates of its own (the indexing-authority rule is enforced by the consuming pipeline concepts), so the test bar is an accuracy check against the live tool, not a pressure scenario.

## Provenance

- [tobiqmd mini cli search engine for your docs, knowledge bases, meeting notes, whatever. Tracking current sota approaches while being all local.md](https://github.com/tobi/qmd) — web clipping of the upstream README (captured 2026-07-13), the primary source for commands, MCP details, architecture, and config schema.
- https://github.com/tobi/qmd — upstream repo; `CLAUDE.md` (agents-never-index rule, `qmd query` preference, no direct SQLite writes) and `CHANGELOG.md` (v2.6.3 current as of 2026-06-24; `qmd init` project-local indexes; `qmd skills list|get|path`) checked 2026-07-13.
- `concepts/bc-init-agent/` — the vault schema whose directory meanings seed the context tree; its close-out registers new vaults in the canon by default.
- `concepts/bc-drain-issues/` and `concepts/triage/` — the consuming pipeline concepts whose retrieval steps this skill backs.
- `~/Sync/Scripts/config/qmd-collections.yml` + `~/Sync/Scripts/bin/setup/bc-qmd-setup` + `Scripts/systemd/bc-qmd-refresh.{service,timer}` — the synced canon, convergence script, and refresh timer implementing global mode (authored 2026-07-13).

## Tests

`tests/accuracy-check.md` — verify commands/flags against a live qmd install before deploy (reference concept, no pressure scenario). **Run 2026-07-13 on Arch (qmd 2.5.3): PASS**; surfaced the absolute-collection-paths finding that fed the global-mode decision.

`tests/grep-baseline-comparison.md` — A/B against a grep-only cold agent. **Run 2026-07-14: PASS.** Keyword-friendly questions are a tie (grep is equally fast/cheap/correct); paraphrase questions with zero keyword overlap are grep-unanswerable (0 hits) while `qmd query --no-rerank` hit ground truth first attempt. Also validated that a cold agent picks the correct latency tier from the skill text alone. Grounds the skill's "when to reach for it" line empirically.

## Deploy targets

- Deployed 2026-07-13 via `scripts/deploy-local-skills.py`: relative symlinks at `~/.agents/skills/qmd` (shared bus: Pi, Composer, Grok, Codex), `~/.pi/agent/skills/qmd`, and `~/.claude/skills/qmd`, all resolving to `body/` (verified; Claude Code advertised the skill immediately).
- Other harnesses: manual bootstrap per `../../harnesses.md`.
