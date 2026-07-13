---
name: qmd
description: Search a repo's markdown knowledge base (bc-agent wiki, notes, docs) with qmd local hybrid search. Use when a qmd index exists (`.qmd/index.yml` at the repo root or a registered collection) and you need to find the relevant pages — search before walking directory trees. Also covers who may run indexing.
---

# qmd — local hybrid search over markdown

[qmd](https://github.com/tobi/qmd) is an on-device search engine (BM25 + vector embeddings + LLM reranking, all local GGUF models). When a corpus has an index, one `qmd query` beats walking directories and grepping: results come back scored, snippeted, and — the tool's key feature — tagged with **context** describing what each part of the corpus is and how much authority it carries.

Detect an index with `.qmd/index.yml` at the repo root (project-local) or `qmd status` (global collections). No index, or a corpus small enough to read whole? Use grep and the corpus's own index files — qmd earns its cost only at scale.

## Searching

- `qmd query "<terms>"` — hybrid + reranking, best quality; the default. Add `--intent "<what you're actually after>"` when the terms are ambiguous.
- `qmd search "<terms>"` — BM25 keyword only, fast, no LLM; use for exact identifiers. `qmd vsearch` — semantic only.
- Scope with `-c <collection>`; get machine output with `--json`; threshold-sweep with `--all --files --min-score 0.3`.
- Retrieve: `qmd get "#<docid>"` (docids appear in results), `qmd get <path>:<from>:<count>` for line ranges, `qmd multi-get "<glob>"` for batches.
- Score guide: ≥0.8 highly relevant, 0.5–0.8 moderately; below that, treat as a lead, not an answer. Read the returned `Context:` line — it tells you whether a hit is authoritative (an ADR) or exploratory (research notes) before you open it.

## Who runs indexing

Searching is always safe. Indexing (`qmd collection add`, `qmd context add`, `qmd update`, `qmd embed`, `qmd init`) mutates shared state and downloads models, so who runs it depends on the session:

- **Interactive session, user present:** run setup/refresh commands with the user's agreement (first `qmd embed` downloads ~2GB of models and needs Node ≥ 22).
- **AFK pipeline (e.g. `bc-drain-issues`):** only the **driver** refreshes the index, once at preflight (`qmd update && qmd embed`). Workers are search-only — parallel workers re-embedding concurrently would race each other for zero benefit, and a worker that silently rebuilds the index can mask a broken corpus instead of parking.
- Never modify `index.sqlite` directly; everything goes through the CLI. Never commit `index.sqlite` (binary, per-machine); config (`index.yml`) may be committed only if its collection paths are portable across machines.

## Contexts carry the authority map

When setting up an index over a structured corpus (a `.bc-agent/` vault, a wiki), seed `qmd context add` entries that state each directory's **authority level**, not just its topic — e.g. `decisions/` → "ADRs, binding unless superseded", `out-of-scope/` → "rejected enhancements — check before proposing", `research/` → "exploratory, not authoritative". Every future search result then arrives pre-labeled with how much to trust it, which is exactly what a cold agent lacks. A bc-agent vault scaffolded with `bc-init-agent --qmd` gets a ready-made setup page at `.bc-agent/references/qmd.md`.
