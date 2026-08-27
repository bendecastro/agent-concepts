# Research: agent-maintained knowledge wikis (Karpathy gist + Perplexity Brain)

Fetch: both primaries succeeded. Quotes exact. Unquoted synthesis marked INFERENCE.

- Source 1: [Karpathy gist / llm-wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- Source 2: [Perplexity Brain](https://www.perplexity.ai/hub/blog/brain-agentic-memory-as-a-knowledge-wiki)

## Summary

Karpathy is a human-triggered pattern: immutable raw sources, LLM-owned markdown wiki, schema (`CLAUDE.md`/`AGENTS.md`), ingest/query/lint, `index.md`+`log.md`. Perplexity implements that wiki *format* in Computer: foreground agents traverse a compact index + local working set; background **Dream** agents compile updates with staged writes, dual verification, and Git. Brain links the gist.

## 1. Verbatim mechanisms

### Source 1 — Karpathy

| Slot | Mechanism | Quote |
|---|---|---|
| Trigger | User ingest; query; periodic lint | “You drop a new source into the raw collection and tell the LLM to process it.” / “You ask questions against the wiki.” / “Periodically, ask the LLM to health-check the wiki.” |
| Who writes | LLM owns wiki; human sources/questions; schema co-evolved | “You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it.” / “You and the LLM co-evolve this over time” |
| What/where | Immutable raw; LLM markdown wiki; schema file | “These are immutable — the LLM reads from them but never modifies them.” / “The LLM owns this layer entirely.” |
| Ingest writes | Summary, index, entity/concept pages, log | “writes a summary page… updates the index, updates relevant entity and concept pages… appends an entry to the log. A single source might touch 10-15 wiki pages.” |
| Query writes | File answers back | “good answers can be filed back into the wiki as new pages.” |
| Links | Cross-refs; no wikilink grammar | “maintains cross-references, and keeps everything consistent.” |
| Contradict/stale | Note on ingest; lint flags | “noting where new data contradicts old claims” / “contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links” |
| Cheap find | Index first, then drill | “the LLM reads the index first to find relevant pages, then drills into them.” |
| Verify | Human review preferred; lint; no harness | “I read the summaries, check the updates, and guide the LLM on what to emphasize.” |
| NOT done | Query-time RAG rediscovery; LLM editing raw; required embeddings; fixed impl | “the LLM is rediscovering knowledge from scratch on every question. There's no accumulation.” / “avoids the need for embedding-based RAG infrastructure.” / “This document is intentionally abstract.” |

### Source 2 — Perplexity Brain

| Slot | Mechanism | Quote |
|---|---|---|
| Trigger | Foreground query; Dream on new/updated sessions | “foreground agents that use memory to answer queries, and background agents that update and improve memory.” / “For each session that is new (or has had new turns) since the last update, the agent writes (or updates) a short summary” |
| Who writes | Dream writes; foreground reads; Memory Agent materializes; multi-agent Git | “Brain is maintained by background agents we call Dream.” / “multiple agents may be using and updating Brain at once.” |
| What/where | `memory/{knowledge,notes,sessions}/` | “`knowledge/` is the Brain itself… `notes/` contains distilled snippets… `sessions/` holds indexes, summaries, and full transcripts” |
| Links | Context vs evidence edges | “`[[wikilinks]]` are context edges… `[cite:N]` references are evidence edges.” |
| Contradict/stale | Revise, delete, or no-op; Git | “outdated context should be seasonably removed.” / “It can also choose to make no changes when the current graph is already correct.” |
| Cheap find | Index in first message; grep; follow edges; don’t copy whole tree | “We include a compact index of Brain within the initial user message” / “Copying the whole tree locally every time a sandbox is booted is expensive and unnecessary” |
| Verify | Staged tree; format checks; semantic evidence+graph checks; sync | “Deterministic validation checks ensure that pages are well-formed… Semantic verification checks ensure that a proposed synthesis is supported by the gathered evidence and remains consistent with the rest of the graph.” |
| NOT done | Stuff-all-memory-in-context; rebuild-from-scratch; remote FUSE grep; main agent searching full corpus | “Stuffing static memory files directly into model context… classic precision-recall tradeoff.” / “Each run begins from the Brain produced by earlier runs rather than rebuilding the user's context from scratch.” |

Dream phases (verbatim): Orient → Summarize sessions → Attach facts to subjects → Update knowledge wiki.

## 2. Retrieval / traversal cost

**Karpathy**
- “index.md is content-oriented. It's a catalog of everything in the wiki — each page listed with a link, a one-line summary…”
- “works surprisingly well at moderate scale (~100 sources, ~hundreds of pages)”
- “at small scale the index file is enough, but as the wiki grows you want proper search” ([qmd](https://github.com/tobi/qmd) BM25/vector + rerank).
- `log.md` “append-only”; `grep "^## \[" log.md | tail -5`.
- Human: “Obsidian's graph view… hubs… orphans.”
- Page size / hierarchy depth: **not stated**.

**Perplexity**
- Index prefill; experiment: “increased Brain usage and reduced memory-related dissatisfaction by 6.9%.”
- Loop: `cat memory/knowledge/index.md` → `grep` → `cat` page → follow `[[wikilink]]` → resolve `[cite:N]` only if needed.
- “self-directed loop, rather than a fixed pipeline.”
- Notes for “simple, single-hop”; knowledge for “stitching evidence across weeks or months.”
- Preload recent map; Memory Agent “semantic search and load a new set of files”; “batched retrieval.”
- “`grep` … over a remote FUSE-backed path were roughly 400 to 500 times slower than … local files.”
- Brain-enabled: “approximately 15% fewer tokens, cost 10% less, and completed generation 10% faster.”
- Page size / max depth: **not stated**.

## 3. Automation degree

**Karpathy — on-demand, human-gated, per-source default.** Ingest/query/lint when asked. “I prefer to ingest sources one at a time and stay involved… But you could also batch-ingest many sources at once with less supervision.” Business: “Possibly with humans in the loop reviewing updates.” No scheduler.

**Perplexity — on-demand read / background write.** Dream “run offline”; “sole goal is to improve context for future sessions.” “staged output tree. No permanent changes… until the agent has made all of the updates it deems necessary,” then “controlled synchronization.” Memory Agent mid-task. Human not in write loop; Git “inspectable.” Cadence (cron vs post-session) **unspecified** beyond new/updated sessions. INFERENCE: after-session batch, not per-turn wiki rewrite.

## 4. Divergences

1. HITL ingest vs Dream compile without a human ingest prompt.
2. Human-curated immutable files vs sessions+connectors (`pplx://sessions/`, `connector://google-calendar`).
3. Unspecified markdown cross-refs vs `[[wikilinks]]` + `[cite:N]`.
4. Lint *flags* stale/orphans vs Brain *removes* outdated context (deletion log is an Orient input) or no-ops.
5. Index-until-hundreds, RAG optional vs index+grep+links **plus** semantic Memory Agent (sandbox boot cost).
6. Human eyeball vs staged commit + two verifiers + evals.
7. Karpathy files Q&A pages; Brain does not say it files the user’s answer as a wiki page.
8. User-evolved `AGENTS.md` vs Dream [Skill](https://research.perplexity.ai/articles/designing-refining-and-maintaining-agent-skills-at-perplexity).
9. Only Brain publishes metrics.
10. Brain: “formatted as an LLM wiki” → gist. Gist does not mention Computer/Dream.

## 5. Unsupported / not said

**Karpathy (idea file, no evals)**
- “~100 sources / hundreds of pages” and “cost of maintenance is near zero”; “LLMs don't… forget to update a cross-reference” — unmeasured.
- Memex: analogy, not a test.
- Text does **not** specify: `[[wikilink]]` syntax, required Git, page caps, scheduled jobs, embedding index, contradiction *resolution* (flag only), deletion.
- Commonly attributed but absent: canonical directory tree; background maintainers; production metrics.

**Perplexity**
- +6.1 pp correctness / +5.2 pp evidence recall on internal 640 Q / 44 synthetic personas — not public.
- LoCoMo −4.6 pp without wiki; LongMemEval-S n.s. — “benchmark subsets… not definitive.”
- June 18 “+25% correctness / +16% recall” is relative; later “9.3 / 8.0 / 8.9 points” absolute on a different online protocol — not interchangeable.
- FUSE 400–500× — “internal testing.”
- “competitiveness will only increase” — forecast.
- Does **not** say: open-source Brain; HITL required; page-size/depth; exact Dream schedule; how “seasonable” deletion is chosen.

## 6. Adjacent prior art (≤8; steal one)

- [Letta hierarchy / MemFS](https://docs.letta.com/guides/core-concepts/memory/context-hierarchy/) — always-on core blocks vs on-demand files; git-backed FS the agent already `cat`/`grep`s.
- [Graphiti/Zep](https://github.com/getzep/graphiti) — temporal edges: new facts **invalidate** old ones, not just flag them.
- [Mem0](https://docs.mem0.ai/core-concepts/how-it-works) — extract → dedup/conflict → `search()` before the next prompt.
- [Claude Code memory](https://code.claude.com/docs/en/memory) — `MEMORY.md` index load cap (first 200 lines or 25KB); topic files on demand; remind-to-shorten near limit.
- [Cursor Rules](https://cursor.com/docs/context/memories) — that URL now serves **Rules**, not a wiki. INFERENCE: Cursor is instruction persistence, not compiled knowledge.
- [Obsidian MOCs](https://www.dsebastien.net/2022-05-15-maps-of-content/) — hub notes as cheap traversal; many maps can point at one page.
- [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — finite context; just-in-time retrieve, don’t dump the store.
- [Anthropic memory tool](https://www.anthropic.com/news/context-management) — file-backed memory + context editing so long tasks don’t keep the full transcript in-window.

## Sources / gaps

Kept: both primaries; Letta, Graphiti, Mem0, Claude Code memory, Cursor Rules (redirect), MOC guide, Anthropic posts. Dropped: unofficial Cursor-memory SEO.

Gaps: no page-size or max-depth numbers; Dream cadence unspecified; Karpathy merge algorithm absent; Brain evals unreproducible from the post.
