# Agents Workspace

This directory is the canonical, agent-agnostic home for the skills/concepts that specialise the user's coding agents (Claude Code, Pi, OpenCode, Grok, Codex, possibly Gemini). It is maintained mostly by agents. If you are an agent reading this: this file is your operating manual.

## Quick start for agents

Project mechanics (work items, decisions, validation, the Where things go table) live in [.bc-agent/AGENTS.md](.bc-agent/AGENTS.md); read it before non-trivial work. This file stays the operating manual for concepts.

1. Read this file, then `index.md`, then the last few `.bc-agent/log.md` entries.
2. Identify the requested operation: ingest, implement/update, tune, test, deploy, or lint.
3. Open only the concept/source files the index points you to; don't dump the whole workspace.
4. Make the smallest canonical change in `concepts/` (never `docs/research/raw/` or derived deploys), update `index.md`/`.bc-agent/log.md` plus `docs/guides/harnesses.md` for deploy/portability changes, run `python3 scripts/lint.py`, then commit.

## Spirit

This workspace exists to **liberate and improve agents, not to constrain them**. Everything in it — concepts, gates, formats — was written by past agents and a human collaborator who assume that *you may be more capable than they were*. So:

- Rules here are **defaults with reasons**, not commandments. Each carries its rationale so you can generalize it correctly — and recognize when it doesn't apply.
- If you conclude a rule or concept is wrong, the legitimate move is to **say so and improve it**. During the task, propose the change and keep following the current canon unless the user explicitly approves changing course; after the task, make the canonical improvement and log your reasoning. Silent deviation is never legitimate: it hides the disagreement that would have improved the concept. Blind obedience is barely better: it preserves a known flaw.
- **Concepts must evolve.** Every operation below is also an opportunity to notice that a concept has been outgrown. Treat friction between a rule and your judgment as signal, not noise.
- Prefer guidance at the **right altitude**: specific enough to transmit hard-won lessons, flexible enough that a capable agent applies its own reasoning — neither brittle if-else process steps nor vague platitudes (see [Anthropic on context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).

## Layers

- `docs/research/raw/` — **raw sources, immutable once filed.** Gists, articles, skill files from elsewhere, the user's rough notes. You read these; you never modify them. The top level is the **inbox** (filed, awaiting ingestion); `docs/research/raw/ingested/` holds sources whose ideas have been taken up. Moving a file between them (and updating links to it) is bookkeeping, not an edit — the immutability gate is about content.
- `concepts/<name>/` — **the canonical layer. The only layer that gets edited.** One directory per skill/concept:
  - `CONCEPT.md` — what it is, why it exists, design decisions, provenance (which `docs/research/raw/` files and external sources it derives from), and deploy targets. It opens with **status frontmatter** (`test_kind`, `test_status`, `tested`, `deployed`) — the single home for that state. Why: it used to live as prose in 43 files in about ten phrasings, so "what is untested?" could not be answered without reading all of them, and the test gate had no mechanical check. Update it in the same pass as the run or deploy it describes, then run `python3 scripts/lint.py --write-status` to refresh `docs/status.md`; lint fails while that page is stale, so the two cannot drift.
  - `body/` — the actual instruction content an agent consumes (usually `SKILL.md` per the [Agent Skills spec](https://agentskills.io); always-injected concepts may use a named Markdown file such as `AGENT-KERNEL.md`; plus supporting files/scripts).
  - `tests/` — pressure scenarios and expected behavior (see Test operation).
- `build/` — **derived per-agent outputs. Does not exist yet — do not create it** until two agents actually need different formats for the same concept. Today every consumer reads `body/` directly via symlink.
- `docs/` — **human-facing workspace documentation**, mapped page by page in [docs/README.md](docs/README.md): how-to guides in `docs/guides/` (`harnesses.md`, `bootstrap.md`, `pipeline.md`, `pressure-test-harness.md`), the generated `docs/status.md`, private-config templates in `docs/examples/`, dated research plus immutable evidence in `docs/research/`, decision records and design notes. Plans are work items under `work/`. Reference pages, not canon: an instruction an agent must follow belongs in a concept `body/` or in this file.
- `scripts/` — deterministic helpers shared across the workspace.
- **Private concepts** live outside this repository at `~/.config/agent-concepts/concepts/<name>/body/SKILL.md`, in the same shape as `concepts/` here, and `scripts/deploy-local-skills.py` deploys them alongside the public ones. Use this for anything that must not be published to be useful: infrastructure topology, employer-specific process, or an upstream body whose licence does not permit redistribution. A private concept of the same name overrides the public one, and the override is reported. Never move something private *into* this repository to make tooling simpler — the whole point of the seam is that publishing and using are separate decisions.
- `policies/` — **documentation for user-owned authorization only.** The real policy lives outside this repository at `~/.config/agent-concepts/publish.yaml`; what is tracked here is `publish.example.yaml`, a template. Agents follow the user's policy and may propose changes, but a policy change is never publishable under the policy itself — pushing one requires current explicit user instruction (self-amendment immunity). Never add a real (non-example) publish policy to this repository: a private authorization file in a public checkout is one `git add -f` from being published, and would be inherited by everyone who clones.
- `AGENTS.md` (this file), `index.md`, `.bc-agent/log.md`, `docs/guides/bootstrap.md`, `docs/guides/harnesses.md` — the schema, catalog, history, bootstrap prompts, and harness compatibility matrix.

## Operations

**Ingest.** The user drops something into `docs/research/raw/` (the top-level inbox) and asks you to ingest it. Read it, discuss the key takeaways and what concept(s) it should create or change, then write/update `CONCEPT.md` (and `body/` if implementing), update `index.md`, and log it. Ingestion is a conversation, not a batch job — the user curates, you compile. Ingestion doesn't require exhaustively mining the source: adopting even a couple of ideas or improvements from it counts. Once a source is ingested, move it to `docs/research/raw/ingested/` and update its index entry and any links — what remains at the top level is exactly the to-ingest backlog.

**Implement/Update.** Edit a concept's `body/`. Match the existing structure (progressive disclosure: a lean entry file linking to format/reference files loaded only when needed; scripts for anything an LLM does unreliably, like date math). When writing instruction language — gates, rituals, behavioral rules — adapt blocks from `concepts/prompting-agents/body/SKILL.md` rather than inventing phrasing. Record non-obvious design decisions in `CONCEPT.md`.

Before changing a concept's behavioral contract, read its `RELATIONSHIPS.md` and account for every incoming **and outgoing** edge. For each affected contract, update the consumer/producer in the same change, record an evidence-backed reason it is unaffected, or leave the impact unresolved and escalate; an absent edge is not proof of independence. Why: the generated view is the only place a callee can see its callers, and it exposes the assumptions a producer makes about its targets. When a clause adds, removes, or changes a `loads`, `adapts`, `depends_on_contract`, or `hands_off` relationship, edit `concepts/relationships.json` in the same change and regenerate with `python3 scripts/lint.py --write-relationships`. Never hand-edit a generated view — the next regeneration reverts it, so the fix disappears exactly when someone starts trusting it.

**Tune (metaprompting).** When an agent underperforms while running a concept from this workspace, fix the instructions rather than the output. **Self-critique** (ask it at the end of the bad turn to critique its own instructions) surfaces friction the agent felt, but is blind where it believes it complied — for that, **grade the artifact the next reader will meet**, which is the code, not the agent's report. Locate the failure's mechanism before rewriting; adopt only what recurs, simplified to its general form; prefer replacing over appending; re-run the check that failed. Full operation: `concepts/prompting-agents/body/SKILL.md` § Maintenance technique: metaprompting. The test gate applies before redeploy. Tuning can also fire *mid-run*: when the same defect pattern recurs across parallel workers, fix the shared prompt/packet that generates the work instead of hand-fixing outputs (see `bc-drain-issues`' recurring-defect tune for the bounded AFK version) — promoting such a run-local patch into canon still comes back through this operation and the test gate.

**Test.** Before deploying a new or changed concept that enforces discipline (gates, rituals, mandatory steps), pressure-test it: run a subagent as the consuming agent in a throwaway workspace, with scripted user messages that attack each gate (the predictable excuses: "I'm short on time", "just trust me", "it's common knowledge"). Verify against the artifacts the subagent produced, not its self-report. Store scenarios and expected outcomes in `concepts/<name>/tests/`. Run the consuming agent on the model named in private `~/.config/agent-concepts/pressure-test.json` (see [example](docs/examples/pressure-test.example.json)), once without the concept and once with it; if that model is unavailable, ask the user what to use instead rather than substituting. Why: strong models often pass with or without the concept, so only a weaker model that fails without it and holds with it shows the concept works. Principle (from obra's writing-skills): if you didn't watch an agent fail or hold the line, you don't know the skill teaches the right thing. The Pi harness (mounts, flags, headless pitfalls) is in [docs/guides/pressure-test-harness.md](docs/guides/pressure-test-harness.md). A skill whose job is to launch subagents is tested there as a dry run: the consumer writes `plan.md` and launches nothing, and the skill's first real run is its live test. Why: the pressure-test model cannot carry a live multi-agent chain end to end, so a live test grades its stamina rather than the instructions.

Keep the without-concept run blind to the concept. Turning skills off is not enough: a consumer with file tools can find the deployed body and follow it. Hide the concept and skill directories from that run (for example `bwrap --bind / / --tmpfs <dir>` over each), word its prompt without the concept's name, and search its transcript for reads of the concept path before grading. Why: in one run the baseline found the skill with `find`, read it and followed it, which would have made the skill look useless.

**Deploy.** Make the concept visible to an agent, currently via **relative** symlink (homes differ across machines: `/home/<user>` vs `/Users/<user>`):
- **Bulk local concepts:** run `scripts/deploy-local-skills.py` from this workspace. It exposes every `concepts/*/body/SKILL.md` whose `CONCEPT.md` is not marked `deployed: no` (set `deployed: yes` in the same change that deploys) through `~/.agents/skills/<name>`, `~/.pi/agent/skills/<name>`, and `~/.claude/skills/<name>` using relative symlinks. OpenCode's `canonical-skill-commands.ts` plugin turns the CONFIG-backed entries on the shared bus (including aliases) into same-named slash commands without duplicating skill bodies; explicit command files may override a generated wrapper but must still load the canonical skill.
- **Consumers of `~/.agents/skills/`:** Pi, Claude Code (also has its own `~/.claude/skills/` mirror), Composer (Cursor), Grok, OpenCode, and Muse Code. Composer, Grok, OpenCode, and Muse discover the shared bus automatically — no extra deploy targets needed. Restart sessions after deploy if the advertised skill list is stale. Never `muse skills import` / `muse skills install` corpus skills (copies into `~/.config/muse/skills/` and freeze).
- **Other agents:** see `docs/guides/bootstrap.md` and `docs/guides/harnesses.md` — Codex/Gemini still use AGENTS.md deltas or manual bootstrap until a native skills path is verified. Muse's kernel is the user-rules file `~/.config/muse/AGENTS.md` (regular-file copy from its machine-local configured source), not a skill.
Record deploy targets in the concept's `CONCEPT.md`, `index.md`, and `docs/guides/harnesses.md`.

**Lint.** Copied kernel-delta drift produces warnings using optional private `~/.config/agent-concepts/kernel-copies.json` (see [example](docs/examples/kernel-copies.example.json)). Project skill-copy drift also warns using optional private `~/.config/agent-concepts/skill-copies.json` (see [example](docs/examples/skill-copies.example.json)). Periodically, or on request: run `python3 scripts/lint.py` for mechanical drift (missing tests/provenance, invalid or missing status frontmatter, deployed-but-never-run test-gate violations, broken relative links, stale index entries, unindexed raw sources, missing harness docs, dangling deploy symlinks, personal terms from the optional private denylist, invalid relationship-graph edges, stale or missing generated relationship views). `python3 scripts/lint.py --status` prints the test/deploy board, worst first; `--write-status` regenerates [`docs/status.md`](docs/status.md), the human-readable version of the same data. Never hand-edit that page — it is generated, and lint fails when it drifts from the frontmatter. Fix objective issues, report judgment calls, and log the pass. External link rot in provenance is a judgment call unless the user asked for web validation.

## Gates

Gates are the rules that have earned a higher bar for revision, because their failure modes are *in-the-moment rationalization* — the moment a gate blocks you is precisely when your judgment about it is least trustworthy. They still follow the Spirit: each states its why, and each can be changed — deliberately, out loud, with the change logged — just not skipped quietly mid-task because it's inconvenient right now.

- **Canon gate.** Don't hand-edit derived outputs or anything outside this directory that a symlink points into from an agent's config. Why: the next rebuild/update silently reverts the fix, and "it's a one-line fix" is exactly how canon and deploys drift apart.
- **Provenance gate.** Every concept names its sources in `CONCEPT.md`. Why: an uncredited design decision is a parametric guess that no future agent can re-evaluate, supersede, or trust.
- **Test gate.** A discipline-enforcing concept doesn't deploy until it has held under a pressure scenario. Why: discipline instructions fail in ways their authors can't see; "the change is small" is how loopholes open. (Reference concepts with no runtime gates need only an accuracy check.)
- **Immutability gate.** Files in `docs/research/raw/` are never edited. Why: they are the evidence base — annotations and corrections belong in the concepts that cite them, where they carry provenance.

## Bookkeeping

Every operation that changes files appends a `.bc-agent/log.md` entry:

```md
## [YYYY-MM-DD] <ingest|implement|test|deploy|lint> | <subject>
1-3 lines: what changed and why.
```

The prefix is consistent so `grep "^## \[" .bc-agent/log.md | tail -5` shows recent activity. `index.md` lists every concept (one line: link, one-line summary, deploy status) and every raw source file (filed/ingested). Update both in the same pass as the change.

## Conventions

- **Nothing in this repository may assume one person's machine.** It is public and installable, so
  a path only the author has is a bug. Two mechanisms, chosen by context:
  - `$AGENT_CONCEPTS/...` in anything a **shell executes** — commands inside deployed skill
    bodies, scripts. The shell expands it at runtime.
  - `<agent-concepts>/...` in anything a **human reads and pastes** — `docs/guides/bootstrap.md`,
    `docs/guides/harnesses.md`. An environment variable would not expand in a chat window; a placeholder
    tells the reader to substitute.
  `scripts/lint.py` checks inline repo-relative paths, so a stale reference is caught
  mechanically.
- **Only what a stranger can copy and use as-is.** The owner's machines, personal paths,
  personal tools and commands that live outside this repository, and personal services or
  projects go into a private concept (see Layers) or an optional private overlay that a public
  skill loads only when present. Why: the repository is meant to be copied whole, and a personal
  reference is either noise or a leak to everyone who does. `scripts/lint.py` reports each hit
  from an optional private denylist, `~/.config/agent-concepts/personal-terms.txt` (path
  override: `AGENT_CONCEPTS_PERSONAL_TERMS`; format: [example](docs/examples/personal-terms.example.txt)),
  as an ERROR (concept bodies and mixed pressure-test results warn instead); without the file the check is skipped. Captured evidence under `docs/research/raw/**`, `docs/research/*/evidence/**`, and `concepts/agent-kernel/tests/pressure-concurrent-sessions/**` is skipped because it is immutable. Pushed history is left alone; current
  files get fixed.
- **Private skill overlays.** A public skill that needs the owner's specifics describes each step generically and adds one line: if `~/.config/agent-concepts/overlays/<skill-name>.md` exists, read it. An overlay supplies only the tool names and invocation forms that the machine's always-loaded agent instructions do not already name; it states no rules, and the project's own instructions take precedence over it. The overlay is private and machine-local (never committed here; no template needed — it is plain prose), and every tool must work when it is absent: deploy symlinks only `body/`, and the skill's generic wording is the stranger's complete instruction. Why: one home per skill for the specifics keeps the public body copyable while the owner's agents, reading the same live symlink, still get their tool names.
- `.bc-agent/log.md` is a historical journal: its stale paths are exempt because they were accurate when
  written, but personal terms are not — scrub them like any other file.
- No hardcoded home paths anywhere — `~` or `$HOME` only; symlinks relative.
- **Externally owned authority has one home.** An instruction file names where an authoritative rule lives and how to query it; it never states what the rule decides. Why: a restatement is a second copy that drifts silently, and drift is discovered only when it blocks correct action — as happened here, costing 128 unpushed commits. For publishing, the canonical policy is `~/.config/agent-concepts/publish.yaml`; get the objective path/remote/branch answer from `python3 scripts/publish-check.py --repo "$PWD" --remote "$(git remote get-url origin)" --branch "$(git branch --show-current)"`, then verify the matched rule's `when:` conditions yourself before pushing. Do not restate the policy's rules here.
- Concept names are dash-case and unique across the workspace.
- Skills that run a parent skill through the advisor council (`council-mode`) are named `bc-council-<job>`, with the job as verb-object (`bc-council-improve-codebase`). Why: the owner is building a family of council chains, and a shared prefix groups them in skill lists and slash-command completion.
- This workspace's value comes from encoding the user's specific workflows, not generic skill-list scraping. When ingesting, ask what's idiosyncratic about how the user wants it — then encode the workflow in a generic, copyable form and put the personal specifics (which machine, which path, which private tool) in a private concept or overlay.
