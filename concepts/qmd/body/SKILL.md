---
name: qmd
description: Search the user's markdown knowledge bases (bc-agent wikis, CONFIG agents workspace, personal Wiki, ops notes) with qmd local hybrid search. Use when you need prior decisions, concepts, or notes — one query across all registered collections beats walking directory trees. Also covers who may run indexing and why project-local indexes are banned here.
---

# qmd — local hybrid search over the user's knowledge bases

[qmd](https://github.com/tobi/qmd) is an on-device search engine (BM25 + vector embeddings + LLM reranking, all local GGUF models). This machine runs it in **global mode**: one index, with a collection per knowledge base, registered from the synced canon at `~/Sync/Scripts/config/qmd-collections.yml` (currently: `agents` = CONFIG agents workspace, `wiki` = personal knowledge graph, `music`/`scripts`/`image-maze` = project bc-agent vaults). Searchable from **any** working directory.

Reach for it whenever the question is "has this been decided/ingested/tried before?" — prior ADRs, rejected ideas, concepts, findings. Check availability with `qmd collection list` (is qmd installed, and does a collection cover the corpus you need?). For a corpus small enough to read whole, grep and its own index files are still fine.

## Searching

- `qmd query "<terms>"` — hybrid + reranking, best quality; the default. Add `--intent "<what you're actually after>"` when terms are ambiguous. Unscoped queries search all collections; scope with `-c <collection>` (repeatable).
- `qmd search "<terms>"` — BM25 keyword only, fast, no LLM; use for exact identifiers. `qmd vsearch` — semantic only.
- Latency (measured on the Arch box, ~1k docs, cold CLI): `search` ≈ 0.5s, `query --no-rerank` ≈ 20s, full `query` ≈ 55s (models reload per invocation). Pick the cheapest tier that answers: identifiers → `search`; exploring → `--no-rerank`; full `query` when ranking quality actually matters.
- Machine output: `--json`; threshold sweeps: `--all --files --min-score 0.3`.
- Retrieve: `qmd get "#<docid>"` (docids appear in results), `qmd get <path>:<from>:<count>` for line ranges, `qmd multi-get "<glob>"` for batches.
- Score guide: ≥0.8 highly relevant, 0.5–0.8 moderately; below that, treat as a lead, not an answer. Read the returned `Context:` line — collections are seeded with **authority labels** ("ADRs — binding unless superseded" vs "exploratory research — not authoritative"), so a hit tells you how much to trust it before you open it.

## Never create project-local indexes

Do not run `qmd init` inside a repo, even though upstream docs suggest it. A project-local `.qmd/` **shadows the entire global registry** from anywhere inside that repo (verified v2.5.3) — every collection above silently becomes unreachable there, and the local index can't travel anyway (absolute paths, per-machine binary). If a repo's vault should be searchable, register it as a global collection instead: add an entry to `~/Sync/Scripts/config/qmd-collections.yml` and run `bc-qmd-setup`.

## Who runs indexing

Searching is always safe. Index mutation has owners:

- **Adding/changing collections or contexts:** edit the synced canon (`qmd-collections.yml`) and run `bc-qmd-setup` — never ad-hoc `qmd collection add` outside it, or machines drift apart. New `.bc-agent` vaults are registered by default at init (`bc-init-agent` step; user can opt out).
- **Freshness:** a daily systemd timer (`bc-qmd-refresh.timer`) runs `qmd update && qmd embed`. In an AFK pipeline (`bc-drain-issues`) only the **driver** refreshes, once at preflight; workers are search-only — concurrent re-embeds race for zero benefit, and a worker silently rebuilding the index can mask a broken corpus instead of parking.
- Never modify the index SQLite directly; everything goes through the CLI. First-time machine setup: `bc-install qmd` (runs `bc-qmd-setup`), then `qmd pull && qmd embed` (~2GB one-time model download, Node ≥ 22).
