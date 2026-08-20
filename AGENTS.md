# Agents Workspace

This directory is the canonical, agent-agnostic home for the skills/concepts that specialise the user's coding agents (Claude Code, Pi, OpenCode, Grok, Codex, possibly Gemini). It is maintained mostly by agents. If you are an agent reading this: this file is your operating manual.

## Quick start for agents

1. Read this file, then `index.md`, then the last few `log.md` entries.
2. Identify the requested operation: ingest, implement/update, tune, test, deploy, or lint.
3. Open only the concept/source files the index points you to; don't dump the whole workspace.
4. Make the smallest canonical change in `concepts/` (never `raw/` or derived deploys), update `index.md`/`log.md` plus `docs/harnesses.md` for deploy/portability changes, run `python3 scripts/lint.py`, then commit.

## Spirit

This workspace exists to **liberate and improve agents, not to constrain them**. Everything in it — concepts, gates, formats — was written by past agents and a human collaborator who assume that *you may be more capable than they were*. So:

- Rules here are **defaults with reasons**, not commandments. Each carries its rationale so you can generalize it correctly — and recognize when it doesn't apply.
- If you conclude a rule or concept is wrong, the legitimate move is to **say so and improve it**. During the task, propose the change and keep following the current canon unless the user explicitly approves changing course; after the task, make the canonical improvement and log your reasoning. Silent deviation is never legitimate: it hides the disagreement that would have improved the concept. Blind obedience is barely better: it preserves a known flaw.
- **Concepts must evolve.** Every operation below is also an opportunity to notice that a concept has been outgrown. Treat friction between a rule and your judgment as signal, not noise.
- Prefer guidance at the **right altitude**: specific enough to transmit hard-won lessons, flexible enough that a capable agent applies its own reasoning — neither brittle if-else process steps nor vague platitudes (see [Anthropic on context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

## Layers

- `raw/` — **raw sources, immutable once filed.** Gists, articles, skill files from elsewhere, the user's rough notes. You read these; you never modify them. The top level is the **inbox** (filed, awaiting ingestion); `raw/ingested/` holds sources whose ideas have been taken up. Moving a file between them (and updating links to it) is bookkeeping, not an edit — the immutability gate is about content.
- `concepts/<name>/` — **the canonical layer. The only layer that gets edited.** One directory per skill/concept:
  - `CONCEPT.md` — what it is, why it exists, design decisions, provenance (which `raw/` files and external sources it derives from), and deploy targets. It opens with **status frontmatter** (`test_kind`, `test_status`, `tested`, `deployed`) — the single home for that state. Why: it used to live as prose in 43 files in about ten phrasings, so "what is untested?" could not be answered without reading all of them, and the test gate had no mechanical check. Update it in the same pass as the run or deploy it describes, then run `python3 scripts/lint.py --write-status` to refresh `docs/status.md`; lint fails while that page is stale, so the two cannot drift.
  - `body/` — the actual instruction content an agent consumes (usually `SKILL.md` per the [Agent Skills spec](https://agentskills.io); always-injected concepts may use a named Markdown file such as `AGENT-KERNEL.md`; plus supporting files/scripts).
  - `tests/` — pressure scenarios and expected behavior (see Test operation).
- `build/` — **derived per-agent outputs. Does not exist yet — do not create it** until two agents actually need different formats for the same concept. Today every consumer reads `body/` directly via symlink.
- `docs/` — **how to install and operate this workspace**, for humans: `status.md` (generated — what needs testing, what is undeployed), `harnesses.md` (compatibility matrix), `bootstrap.md` (copy-paste session prompts), `pipeline.md` (the plan→execute loop). Reference pages, not canon: an instruction an agent must follow belongs in a concept `body/` or in this file.
- `scripts/` — deterministic helpers shared across the workspace.
- **Private concepts** live outside this repository at `~/.config/agent-concepts/concepts/<name>/body/SKILL.md`, in the same shape as `concepts/` here, and `scripts/deploy-local-skills.py` deploys them alongside the public ones. Use this for anything that must not be published to be useful: infrastructure topology, employer-specific process, or an upstream body whose licence does not permit redistribution. A private concept of the same name overrides the public one, and the override is reported. Never move something private *into* this repository to make tooling simpler — the whole point of the seam is that publishing and using are separate decisions.
- `policies/` — **documentation for user-owned authorization only.** The real policy lives outside this repository at `~/.config/agent-concepts/publish.yaml`; what is tracked here is `publish.example.yaml`, a template. Agents follow the user's policy and may propose changes, but a policy change is never publishable under the policy itself — pushing one requires current explicit user instruction (self-amendment immunity). Never add a real (non-example) publish policy to this repository: a private authorization file in a public checkout is one `git add -f` from being published, and would be inherited by everyone who clones.
- `AGENTS.md` (this file), `index.md`, `log.md`, `docs/bootstrap.md`, `docs/harnesses.md` — the schema, catalog, history, bootstrap prompts, and harness compatibility matrix.

## Operations

**Ingest.** The user drops something into `raw/` (the top-level inbox) and asks you to ingest it. Read it, discuss the key takeaways and what concept(s) it should create or change, then write/update `CONCEPT.md` (and `body/` if implementing), update `index.md`, and log it. Ingestion is a conversation, not a batch job — the user curates, you compile. Ingestion doesn't require exhaustively mining the source: adopting even a couple of ideas or improvements from it counts. Once a source is ingested, move it to `raw/ingested/` and update its index entry and any links — what remains at the top level is exactly the to-ingest backlog.

**Implement/Update.** Edit a concept's `body/`. Match the existing structure (progressive disclosure: a lean entry file linking to format/reference files loaded only when needed; scripts for anything an LLM does unreliably, like date math). When writing instruction language — gates, rituals, behavioral rules — adapt blocks from `concepts/prompting-agents/body/SKILL.md` rather than inventing phrasing. Record non-obvious design decisions in `CONCEPT.md`.

**Tune (metaprompting).** When an agent underperforms while running a concept from this workspace, fix the instructions rather than the output. **Self-critique** (ask it at the end of the bad turn to critique its own instructions) surfaces friction the agent felt, but is blind where it believes it complied — for that, **grade the artifact the next reader will meet**, which is the code, not the agent's report. Locate the failure's mechanism before rewriting; adopt only what recurs, simplified to its general form; prefer replacing over appending; re-run the check that failed. Full operation: `concepts/prompting-agents/body/SKILL.md` § Maintenance technique: metaprompting. The test gate applies before redeploy. Tuning can also fire *mid-run*: when the same defect pattern recurs across parallel workers, fix the shared prompt/packet that generates the work instead of hand-fixing outputs (see `bc-drain-issues`' recurring-defect tune for the bounded AFK version) — promoting such a run-local patch into canon still comes back through this operation and the test gate.

**Test.** Before deploying a new or changed concept that enforces discipline (gates, rituals, mandatory steps), pressure-test it: run a subagent as the consuming agent in a throwaway workspace, with scripted user messages that attack each gate (the predictable excuses: "I'm short on time", "just trust me", "it's common knowledge"). Verify against the artifacts the subagent produced, not its self-report. Store scenarios and expected outcomes in `concepts/<name>/tests/`. Principle (from obra's writing-skills): if you didn't watch an agent fail or hold the line, you don't know the skill teaches the right thing.

**Deploy.** Make the concept visible to an agent, currently via **relative** symlink (homes differ across machines: `/home/<user>` vs `/Users/<user>`):
- **Bulk local concepts:** run `scripts/deploy-local-skills.py` from this workspace. It exposes every `concepts/*/body/SKILL.md` through `~/.agents/skills/<name>`, `~/.pi/agent/skills/<name>`, and `~/.claude/skills/<name>` using relative symlinks. OpenCode's `canonical-skill-commands.ts` plugin turns the CONFIG-backed entries on the shared bus (including aliases) into same-named slash commands without duplicating skill bodies; explicit command files may override a generated wrapper but must still load the canonical skill.
- **Consumers of `~/.agents/skills/`:** Pi, Claude Code (also has its own `~/.claude/skills/` mirror), Composer (Cursor), and Grok. The latter two discover the shared bus automatically — no extra deploy targets needed. Restart sessions after deploy if the advertised skill list is stale.
- **Other agents:** see `docs/bootstrap.md` and `docs/harnesses.md` — Codex/Gemini still use AGENTS.md deltas or manual bootstrap until a native skills path is verified.
Record deploy targets in the concept's `CONCEPT.md`, `index.md`, and `docs/harnesses.md`.

**Lint.** Periodically, or on request: run `python3 scripts/lint.py` for mechanical drift (missing tests/provenance, invalid or missing status frontmatter, deployed-but-never-run test-gate violations, broken relative links, stale index entries, unindexed raw sources, missing harness docs, dangling deploy symlinks). `python3 scripts/lint.py --status` prints the test/deploy board, worst first; `--write-status` regenerates [`docs/status.md`](docs/status.md), the human-readable version of the same data. Never hand-edit that page — it is generated, and lint fails when it drifts from the frontmatter. Fix objective issues, report judgment calls, and log the pass. External link rot in provenance is a judgment call unless the user asked for web validation.

## Gates

Gates are the rules that have earned a higher bar for revision, because their failure modes are *in-the-moment rationalization* — the moment a gate blocks you is precisely when your judgment about it is least trustworthy. They still follow the Spirit: each states its why, and each can be changed — deliberately, out loud, with the change logged — just not skipped quietly mid-task because it's inconvenient right now.

- **Canon gate.** Don't hand-edit derived outputs or anything outside this directory that a symlink points into from an agent's config. Why: the next rebuild/update silently reverts the fix, and "it's a one-line fix" is exactly how canon and deploys drift apart.
- **Provenance gate.** Every concept names its sources in `CONCEPT.md`. Why: an uncredited design decision is a parametric guess that no future agent can re-evaluate, supersede, or trust.
- **Test gate.** A discipline-enforcing concept doesn't deploy until it has held under a pressure scenario. Why: discipline instructions fail in ways their authors can't see; "the change is small" is how loopholes open. (Reference concepts with no runtime gates need only an accuracy check.)
- **Immutability gate.** Files in `raw/` are never edited. Why: they are the evidence base — annotations and corrections belong in the concepts that cite them, where they carry provenance.

## Bookkeeping

Every operation that changes files appends a `log.md` entry:

```md
## [YYYY-MM-DD] <ingest|implement|test|deploy|lint> | <subject>
1-3 lines: what changed and why.
```

The prefix is consistent so `grep "^## \[" log.md | tail -5` shows recent activity. `index.md` lists every concept (one line: link, one-line summary, deploy status) and every raw source file (filed/ingested). Update both in the same pass as the change.

## Conventions

- **Nothing in this repository may assume one person's machine.** It is public and installable, so
  a path only the author has is a bug. Two mechanisms, chosen by context:
  - `$AGENT_CONCEPTS/...` in anything a **shell executes** — commands inside deployed skill
    bodies, scripts. The shell expands it at runtime.
  - `<agent-concepts>/...` in anything a **human reads and pastes** — `docs/bootstrap.md`,
    `docs/harnesses.md`. An environment variable would not expand in a chat window; a placeholder
    tells the reader to substitute.
  `scripts/lint.py` checks inline repo-relative paths, so a stale reference is caught
  mechanically; it cannot catch a path that is merely personal, which stays a review concern.
- `log.md` is a historical journal and is exempt: its paths were accurate when written.
- No hardcoded home paths anywhere — `~` or `$HOME` only; symlinks relative.
- Commit changes to this directory in the CONFIG git repo with a message saying which operation ran. Publishing follows `~/.config/agent-concepts/publish.yaml`; that user-owned policy currently authorizes pushing agent-authored CONFIG commits after status/diff inspection and validation.
- Concept names are dash-case and unique across the workspace.
- This workspace's value comes from encoding the user's specific workflows, not generic skill-list scraping. When ingesting, ask what's idiosyncratic about how the user wants it.
