# Agents Workspace

This directory is the canonical, agent-agnostic home for the skills/concepts that specialise the user's coding agents (Claude Code, Pi, OpenCode, Grok, Codex, possibly Gemini). It is maintained mostly by agents. If you are an agent reading this: this file is your operating manual. Read it fully, then `index.md` and the last few `log.md` entries — open other files only as the index points you to them.

## Layers

- `ideas/` — **raw sources, immutable once filed.** Gists, articles, skill files from elsewhere, the user's rough notes. You read these; you never modify them.
- `concepts/<name>/` — **the canonical layer. The only layer that gets edited.** One directory per skill/concept:
  - `CONCEPT.md` — what it is, why it exists, design decisions, provenance (which `ideas/` files and external sources it derives from), and deploy targets.
  - `body/` — the actual instruction content an agent consumes (e.g. a SKILL.md per the [Agent Skills spec](https://agentskills.io), supporting files, scripts).
  - `tests/` — pressure scenarios and expected behavior (see Test operation).
- `build/` — **derived per-agent outputs. Does not exist yet — do not create it** until two agents actually need different formats for the same concept. Today every consumer reads `body/` directly via symlink.
- `scripts/` — deterministic helpers shared across the workspace.
- `AGENTS.md` (this file), `index.md`, `log.md`, `bootstrap.md` — the schema, catalog, history, and per-agent entry points.

## Operations

**Ingest.** The user drops something into `ideas/` and asks you to ingest it. Read it, discuss the key takeaways and what concept(s) it should create or change, then write/update `CONCEPT.md` (and `body/` if implementing), update `index.md`, and log it. Ingestion is a conversation, not a batch job — the user curates, you compile.

**Implement/Update.** Edit a concept's `body/`. Match the existing structure (progressive disclosure: a lean entry file linking to format/reference files loaded only when needed; scripts for anything an LLM does unreliably, like date math). Record non-obvious design decisions in `CONCEPT.md`.

**Test.** Before deploying a new or changed concept that enforces discipline (gates, rituals, mandatory steps), pressure-test it: run a subagent as the consuming agent in a throwaway workspace, with scripted user messages that attack each gate (the predictable excuses: "I'm short on time", "just trust me", "it's common knowledge"). Verify against the artifacts the subagent produced, not its self-report. Store scenarios and expected outcomes in `concepts/<name>/tests/`. Principle (from obra's writing-skills): if you didn't watch an agent fail or hold the line, you don't know the skill teaches the right thing.

**Deploy.** Make the concept visible to an agent, currently via **relative** symlink (homes differ across machines: `/home/ben` vs `/Users/ben`):
- Claude Code: `~/.claude/skills/<name>` → `../../Sync/CONFIG/agents/concepts/<name>/body`
- Other agents: see `bootstrap.md` — most are invoked by pointing them at this directory rather than by symlink.
Record deploy targets in the concept's `CONCEPT.md` and in `index.md`.

**Lint.** Periodically, or on request: concepts missing tests or provenance; deployed symlinks that dangle or point outside `concepts/`; index entries that don't match reality; `ideas/` files never ingested (list them, don't delete); dead external links in CONCEPT.md provenance. Fix the mechanical issues, report the judgment calls, log the pass.

## Gates (non-negotiable)

- **Canon gate.** Never hand-edit derived outputs or anything outside this directory that a symlink points into from an agent's config. "It's a one-line fix" is not an excuse — edit the concept; otherwise the next rebuild/update silently reverts it.
- **Provenance gate.** Every concept names its sources in `CONCEPT.md`. An uncredited design decision is a parametric guess that nobody can re-evaluate later.
- **Test gate.** A discipline-enforcing concept does not deploy until it has held under a pressure scenario. "The change is small" is not an excuse — small changes are how loopholes open.
- **Immutability gate.** Files in `ideas/` are never edited. Annotations and corrections belong in the concept that cites them.

## Bookkeeping

Every operation that changes files appends a `log.md` entry:

```md
## [YYYY-MM-DD] <ingest|implement|test|deploy|lint> | <subject>
1-3 lines: what changed and why.
```

The prefix is consistent so `grep "^## \[" log.md | tail -5` shows recent activity. `index.md` lists every concept (one line: link, one-line summary, deploy status) and every ideas file (filed/ingested). Update both in the same pass as the change.

## Conventions

- No hardcoded home paths anywhere — `~` or `$HOME` only; symlinks relative. This directory syncs across macOS, Debian, and Arch via Syncthing.
- Commit changes to this directory in the CONFIG git repo with a message saying which operation ran.
- Concept names are dash-case and unique across the workspace.
- This workspace's value comes from encoding the user's specific workflows, not generic skill-list scraping. When ingesting, ask what's idiosyncratic about how the user wants it.
