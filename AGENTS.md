# Agents Workspace

This directory is the canonical, agent-agnostic home for the skills/concepts that specialise the user's coding agents (Claude Code, Pi, OpenCode, Grok, Codex, possibly Gemini). It is maintained mostly by agents. If you are an agent reading this: this file is your operating manual.

## Quick start for agents

1. Read this file, then `index.md`, then the last few `log.md` entries.
2. Identify the requested operation: ingest, implement/update, tune, test, deploy, or lint.
3. Open only the concept/source files the index points you to; don't dump the whole workspace.
4. Make the smallest canonical change in `concepts/` (never `ideas/` or derived deploys), update `index.md`/`log.md` plus `harnesses.md` for deploy/portability changes, run `python3 scripts/lint.py`, then commit.

## Spirit

This workspace exists to **liberate and improve agents, not to constrain them**. Everything in it — concepts, gates, formats — was written by past agents and a human collaborator who assume that *you may be more capable than they were*. So:

- Rules here are **defaults with reasons**, not commandments. Each carries its rationale so you can generalize it correctly — and recognize when it doesn't apply.
- If you conclude a rule or concept is wrong, the legitimate move is to **say so and improve it**. During the task, propose the change and keep following the current canon unless the user explicitly approves changing course; after the task, make the canonical improvement and log your reasoning. Silent deviation is never legitimate: it hides the disagreement that would have improved the concept. Blind obedience is barely better: it preserves a known flaw.
- **Concepts must evolve.** Every operation below is also an opportunity to notice that a concept has been outgrown. Treat friction between a rule and your judgment as signal, not noise.
- Prefer guidance at the **right altitude**: specific enough to transmit hard-won lessons, flexible enough that a capable agent applies its own reasoning — neither brittle if-else process steps nor vague platitudes (see `ideas/anthropic-context-engineering.md`).

## Layers

- `ideas/` — **raw sources, immutable once filed.** Gists, articles, skill files from elsewhere, the user's rough notes. You read these; you never modify them.
- `concepts/<name>/` — **the canonical layer. The only layer that gets edited.** One directory per skill/concept:
  - `CONCEPT.md` — what it is, why it exists, design decisions, provenance (which `ideas/` files and external sources it derives from), and deploy targets.
  - `body/` — the actual instruction content an agent consumes (e.g. a SKILL.md per the [Agent Skills spec](https://agentskills.io), supporting files, scripts).
  - `tests/` — pressure scenarios and expected behavior (see Test operation).
- `build/` — **derived per-agent outputs. Does not exist yet — do not create it** until two agents actually need different formats for the same concept. Today every consumer reads `body/` directly via symlink.
- `scripts/` — deterministic helpers shared across the workspace.
- `AGENTS.md` (this file), `index.md`, `log.md`, `bootstrap.md`, `harnesses.md` — the schema, catalog, history, bootstrap prompts, and harness compatibility matrix.

## Operations

**Ingest.** The user drops something into `ideas/` and asks you to ingest it. Read it, discuss the key takeaways and what concept(s) it should create or change, then write/update `CONCEPT.md` (and `body/` if implementing), update `index.md`, and log it. Ingestion is a conversation, not a batch job — the user curates, you compile.

**Implement/Update.** Edit a concept's `body/`. Match the existing structure (progressive disclosure: a lean entry file linking to format/reference files loaded only when needed; scripts for anything an LLM does unreliably, like date math). When writing instruction language — gates, rituals, behavioral rules — adapt blocks from `concepts/prompting-agents/body/SKILL.md` rather than inventing phrasing. Record non-obvious design decisions in `CONCEPT.md`.

**Tune (metaprompting).** When an agent underperforms while running a concept from this workspace, ask it at the end of the bad turn to critique its own instructions and propose targeted-but-generalized changes. Repeat a couple of times; adopt only suggestions that recur, simplified to their general form; then the test gate applies before redeploy.

**Test.** Before deploying a new or changed concept that enforces discipline (gates, rituals, mandatory steps), pressure-test it: run a subagent as the consuming agent in a throwaway workspace, with scripted user messages that attack each gate (the predictable excuses: "I'm short on time", "just trust me", "it's common knowledge"). Verify against the artifacts the subagent produced, not its self-report. Store scenarios and expected outcomes in `concepts/<name>/tests/`. Principle (from obra's writing-skills): if you didn't watch an agent fail or hold the line, you don't know the skill teaches the right thing.

**Deploy.** Make the concept visible to an agent, currently via **relative** symlink (homes differ across machines: `/home/ben` vs `/Users/ben`):
- Claude Code: `~/.claude/skills/<name>` → `../../Sync/CONFIG/agents/concepts/<name>/body`
- Pi: `~/.pi/agent/skills/<name>` → relative symlink to `agents/concepts/<name>/body` from the synced CONFIG vault.
- Other agents: see `bootstrap.md` and `harnesses.md` — most are invoked by pointing them at this directory rather than by symlink until a real deploy path is tested.
Record deploy targets in the concept's `CONCEPT.md`, `index.md`, and `harnesses.md`.

**Lint.** Periodically, or on request: run `python3 scripts/lint.py` for mechanical drift (missing tests/provenance, broken relative links, stale index entries, unindexed ideas, missing harness docs, dangling deploy symlinks). Fix objective issues, report judgment calls, and log the pass. External link rot in provenance is a judgment call unless the user asked for web validation.

## Gates

Gates are the rules that have earned a higher bar for revision, because their failure modes are *in-the-moment rationalization* — the moment a gate blocks you is precisely when your judgment about it is least trustworthy. They still follow the Spirit: each states its why, and each can be changed — deliberately, out loud, with the change logged — just not skipped quietly mid-task because it's inconvenient right now.

- **Canon gate.** Don't hand-edit derived outputs or anything outside this directory that a symlink points into from an agent's config. Why: the next rebuild/update silently reverts the fix, and "it's a one-line fix" is exactly how canon and deploys drift apart.
- **Provenance gate.** Every concept names its sources in `CONCEPT.md`. Why: an uncredited design decision is a parametric guess that no future agent can re-evaluate, supersede, or trust.
- **Test gate.** A discipline-enforcing concept doesn't deploy until it has held under a pressure scenario. Why: discipline instructions fail in ways their authors can't see; "the change is small" is how loopholes open. (Reference concepts with no runtime gates need only an accuracy check.)
- **Immutability gate.** Files in `ideas/` are never edited. Why: they are the evidence base — annotations and corrections belong in the concepts that cite them, where they carry provenance.

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
