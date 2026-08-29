# Agent concepts

Skills for coding agents that come with the test that tried to break them.

`CLAUDE.md` and `AGENTS.md` are advisory. A model can read a rule and not apply it, and you find
that out in your own repo. Here, every rule that constrains an agent ships with a pressure test
that attacked it in a throwaway workspace first, and `scripts/lint.py` fails when a rule was
deployed without one.

That does not make a model obey. It makes you discover the loophole before you depend on it.

Two things are on offer. A structure for building your own skills. And a loop that takes a feature
from idea to landed commit.

## The loop

Four concepts chain into a cycle. Each hands the next a durable artifact on disk or in your
tracker, so no stage depends on a session staying alive.

**`/bc-init-agent` — give the repo a memory.** Reads the repo, asks only what it cannot infer, then
scaffolds `.bc-agent/`: `log.md`, `decisions/`, `references/`, `conventions/`, `tasks/active.md`.
Additive: it never overwrites or deletes without an explicit flag.

**`/bc-plan-to-issues` — turn an idea into a queue.** Grills one question at a time until every
branch is resolved, writes a PRD under `docs/changes/<slug>/`, merges requirements into
`docs/specs/`, then publishes GitHub issues in dependency order. The slicing quiz is the last human
gate; the skill refuses to skip it.

**`/bc-drain-issues` — work the queue while you sleep.** Claims an issue by pushing a branch (that
branch is the lock). High-risk work gets a read-only audit before any code is written. A worker in
a worktree writes the code; it cannot commit, push, label or close. The driver lands the change
only when every review axis approves the exact final diff.

**`/improve-codebase-architecture` — decide what to build next.** Reviews module depth and seams,
then asks which candidate to explore. It never writes production code or files issues; accepted
work goes back to planning.

`/triage` handles issues arriving from elsewhere, turning them into the same brief the planner
emits.

## When this fits

Use it if:

- you already keep instruction files for an agent and want them tested
- you want a queue worked overnight by workers that cannot commit, push or close their own change
- a project's notes have grown past the point where an agent can read the index to orient itself

Take one piece if that is all you need. `bc-init-agent` alone gives a repo a wiki for agents.
`improve-codebase-architecture` needs no tracker at all. `/bc-drain-issues` needs GitHub and a
ready brief, but not the planner that usually writes one.

Everything needs Git. Claude Code and Pi are the tested harnesses; the rest is described under
Install.

The memory it keeps is long-term project memory: durable facts in Git that any fresh agent can
retrieve on demand. It does not recall past sessions or hold a thread through a long one.

## Install

```bash
git clone https://github.com/bendecastro/agent-concepts.git
cd agent-concepts

# Some skill bodies run scripts from the checkout, so the shell needs its location.
echo 'export AGENT_CONCEPTS="$PWD"' >> ~/.profile   # adjust for your shell
export AGENT_CONCEPTS="$PWD"

python3 scripts/deploy-local-skills.py --dry-run
python3 scripts/deploy-local-skills.py
```

Flags: `--dry-run`, `--force`, `--harness {all,pi,claude}`, `--skip NAME` (repeatable). The shared
`~/.agents/skills/` bus is always updated; `--harness` picks which harness-specific mirror is
written alongside it. The checkout can live anywhere — the script finds itself and writes relative
symlinks, so they survive a different `$HOME`.

After deploy, start a new agent session so it sees the skills. `/bc-init-agent` is a reasonable
first run.

Support is uneven. Claude Code and Pi are the tested paths. Composer and Grok read the shared bus
(Grok's bundled skills can shadow same-named concepts). OpenCode needs a small plugin to expose
skills as slash commands. Codex runs the always-on kernel globally and reaches everything else
through repo `AGENTS.md` pointers. Gemini is manual bootstrap. See
[`docs/harnesses.md`](docs/harnesses.md) and [`docs/bootstrap.md`](docs/bootstrap.md).

## Knowledge that grows without getting harder to use

The archive can grow. What an agent must read to orient stays bounded.

A project's notes decay in a specific way. Appending to a log is easy; filing a fact onto the page
that a later search will return takes judgment. So the easy half happens every time and the hard half
never does, orphan pages pile up, and a cold agent either loads a huge index or greps and hopes.

The fix splits capture from synthesis. Agents append cheap one-line entries to `log.md`.
`bc-wiki-maintain` later detects which entries were never promoted — by diffing the log against the
last promotion commit, so there is no counter to maintain — and files each one into the smallest
page that already covers it. Promotion only creates pages or appends to them. It does not rewrite
what is already there.

Reading is ranked search. `wiki_search.py` runs BM25 over the vault's tracked Markdown and prints a
bounded list of paths; the agent opens two or three. On a 20-question benchmark authored before any
of the retrieval methods existed, that cost a median 171 output tokens against 4,543 for loading
`index.md`. Miss rates were 0.15 against 0.30. The tool has no extra install and no index to go
stale. `qmd` remains available for hybrid search across vaults when you have it.

## Build your own skill

You do this in chat. Describe an idea, or point at something that already exists — drop an
article, gist, skill or notes into `docs/research/raw/`, or paste a link. The agent researches,
writes the concept, attacks it with a pressure test, deploys, and lints. You decide what should
actually change, and whether a failing test is a loophole or a bad test.

What you get that a prompt file does not: named sources so a rule can be re-evaluated later, a test
that tried to break it before it shipped, and a linter that fails if either is missing.

When a skill underperforms, tell the agent to fix the instruction, not the output.

Four rules here get a higher bar than the rest, because each fails when you most want to skip it:

- **Canon** — don't edit a deploy symlink. The next rebuild reverts it.
- **Provenance** — every concept names its sources.
- **Test** — a constraining rule doesn't ship until a pressure test has held.
- **Immutability** — don't edit ingested sources in place.

Each can be changed out loud and logged. None can be skipped quietly.

## Authorisation

`~/.config/agent-concepts/publish.yaml` is user-owned, lives outside this repo, and is default-deny.
An agent may push, open a PR, or close an issue only when a rule there matches or you say so in the
conversation.

Repo-local instruction files can restrict publishing. They cannot grant it. Changes under
`policies/` are never publishable under the policy itself, including by rules added later — a
policy that can publish its own amendments is default-allow wearing a disguise. See
[`policies/README.md`](policies/README.md).

## Private concepts

Use this for infrastructure topology, employer process, or an upstream body whose licence forbids
redistribution.

Put them in `~/.config/agent-concepts/concepts/<name>/body/SKILL.md`, the same shape as `concepts/`
here, and the deploy script picks them up. A private concept overrides a public one of the same
name and reports the collision. The directory is optional.

## Provenance and licensing

Built by reading other people's work and adapting it: Jesse Vincent's
[superpowers](https://github.com/obra/superpowers) (MIT), [Matt Pocock's
skills](https://github.com/mattpocock/skills), and published guidance from Anthropic, OpenAI and
Google. `docs/research/raw/ingested/CITATIONS.md` indexes the corpus.

Concept bodies are re-voiced and specialised, not copies of upstream. Where a body could not be
written independently, the concept points upstream instead of vendoring it; public `herdr` works
this way because upstream states no licence. Some licensed upstream snapshots remain under
`docs/research/raw/ingested/` as immutable evidence, under their own terms.
