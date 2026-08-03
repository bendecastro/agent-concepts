---
name: qmd
description: Search local Markdown knowledge bases (agent wikis, notes, project vaults) with qmd local hybrid search. Use when you need prior decisions, concepts, or notes — one query across all registered collections beats walking directory trees. Also covers who may run indexing and why project-local indexes are a trap.
---

# qmd — local hybrid search over Markdown knowledge bases

[qmd](https://github.com/tobi/qmd) is an on-device search engine (BM25 + vector embeddings + LLM
reranking, all local GGUF models). Run it in **global mode**: one index, with a collection per
knowledge base, searchable from **any** working directory.

Reach for it whenever the question is "has this been decided/ingested/tried before?" — prior ADRs,
rejected ideas, concepts, findings. Check availability with `qmd collection list` (is qmd
installed, and does a collection cover the corpus you need?). For a corpus small enough to read
whole, grep and a repo's own index files are still fine.

## Searching

- `qmd query "<terms>"` — hybrid + reranking, best quality; the default. Add `--intent "<what
  you're actually after>"` when terms are ambiguous. Unscoped queries search all collections;
  scope with `-c <collection>` (repeatable).
- `qmd search "<terms>"` — BM25 keyword only, fast, no LLM; use for exact identifiers.
  `qmd vsearch` — semantic only.
- Latency (measured, ~1k docs, cold CLI): `search` ≈ 0.5s, `query --no-rerank` ≈ 20s, full
  `query` ≈ 55s (models reload per invocation). Pick the cheapest tier that answers: identifiers
  → `search`; exploring → `--no-rerank`; full `query` when ranking quality actually matters.
- Machine output: `--json`; threshold sweeps: `--all --files --min-score 0.3`.
- Retrieve: `qmd get "#<docid>"` (docids appear in results), `qmd get <path>:<from>:<count>` for
  line ranges, `qmd multi-get "<glob>"` for batches.
- Score guide: ≥0.8 highly relevant, 0.5–0.8 moderately; below that, treat as a lead, not an
  answer. Read the returned `Context:` line — seed collections with **authority labels** ("ADRs —
  binding unless superseded" vs "exploratory research — not authoritative"), so a hit tells you
  how much to trust it before you open it.

## Never create project-local indexes

Do not run `qmd init` inside a repo, even though upstream docs suggest it. A project-local
`.qmd/` **shadows the entire global registry** from anywhere inside that repo (verified v2.5.3) —
every global collection silently becomes unreachable there, and the local index can't travel
anyway (absolute paths, per-machine binary). If a repo's vault should be searchable, register it
as a global collection instead.

If you inherit a repo that already has one, `.qmd/` should be gitignored entirely: its
`index.yml` stores absolute paths, so committing it breaks every other machine.

## Who runs indexing

Searching is always safe. Index mutation has owners, and the pattern matters more than the exact
commands:

- **Adding/changing collections or contexts:** keep the collection definitions in one
  version-controlled file and apply them with a single setup command. Never run ad-hoc
  `qmd collection add` outside that file, or machines drift apart and a query means something
  different depending on where you run it.
- **Freshness:** run `qmd update && qmd embed` on a schedule (a daily user timer works well). In
  an AFK pipeline, only the **driver** refreshes, once at preflight; workers are search-only.
  Concurrent re-embeds race for zero benefit, and a worker silently rebuilding the index can mask
  a broken corpus instead of parking the run.
- Never modify the index SQLite directly; everything goes through the CLI. First-time machine
  setup is `qmd pull && qmd embed` (~2GB one-time model download, Node ≥ 22).

> This workspace's own setup keeps `qmd-collections.yml` in a synced repo and applies it with a
> wrapper script, registering new `.bc-agent` vaults by default at init. That is one
> implementation of the rule above, not a requirement.
