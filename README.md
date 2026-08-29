# Agent concepts

Skills for coding agents that come with the test that tried to break them.

`CLAUDE.md` and `AGENTS.md` are advisory. A model can read a rule and not apply it, and you find
that out in your own repo. Here, every rule that constrains an agent ships with a pressure test
that attacked it in a throwaway workspace first, and `scripts/lint.py` fails when a rule was
deployed without one.

That does not make a model obey. It moves the moment you discover the loophole to before you
depended on it.

Two things are on offer. A loop that takes a feature from idea to landed commit with agents doing
the typing. And a structure for building your own skills — researched, written, attacked, deployed
— instead of collecting prompts.

## The loop

Four concepts chain into a cycle. Each hands the next a durable artifact on disk or in your
tracker, so no stage depends on a session staying alive.

**`/bc-init-agent` — give the repo a memory.** It reads your repo first, asks only about decisions
it cannot infer, proposes a plan, and then scaffolds `.bc-agent/`: an append-only `log.md` for
discoveries, `decisions/` for ADRs, `references/` for commands and gotchas, `conventions/` for how
this project validates and commits, `tasks/active.md` as the live cursor. Additive and idempotent —
it never overwrites or deletes without an explicit flag. Run it on an existing repo safely.

**`/bc-plan-to-issues` — turn an idea into a queue.** Grills you one question at a time until every
branch is resolved, drops canonical vocabulary into the glossary and expensive trade-offs into
ADRs, writes a PRD under `docs/changes/<slug>/`, merges the resolved requirements into
`docs/specs/` as current truth, then slices the work into vertical tracer bullets and publishes
them as GitHub issues in dependency order. The slicing quiz is the last human gate before anything
runs on its own, and the skill is written to refuse to skip it.

**`/bc-drain-issues` — work the queue while you sleep.** Claims an issue by pushing a claim branch
(the remote branch is the lock; labels are advisory), runs a fresh worker in an isolated worktree,
then puts the diff through review. High-risk work gets a read-only audit before any code is
written, mapping each rejection clause to evidence that its inputs can actually differ in
production. Workers own code, tests and
validation, and nothing else: they cannot commit, push, label or close. The driver lands the change
only when every review axis approves the exact final diff.

**`/improve-codebase-architecture` — decide what to build next.** Reviews module depth and seams,
applies the deletion test, and asks which candidate you want to explore. It never writes production
code or files issues; accepted work goes back to planning.

`/triage` handles issues arriving from elsewhere, turning them into the same brief the planner
emits.

## When this fits

Use it if you already keep instruction files for an agent and would rather have them tested than
accumulated. Or if you want a queue worked overnight by workers that cannot commit, push or close
their own change. Or if a project's notes have grown past the point where an agent can read the
index to orient itself.

Take one piece if that is all you need. `bc-init-agent` alone gives a repo a wiki for agents.
`improve-codebase-architecture` needs no tracker at all. `/bc-drain-issues` needs GitHub and a
ready brief, but not the planner that usually writes one.

Everything needs Git. Claude Code and Pi are the tested harnesses; the rest is shared-bus discovery
or manual bootstrap, described under Install.

This is not a session-memory tool and not a model wrapper. The memory it keeps is the project's
rather than the conversation's: durable facts in Git that any fresh agent can retrieve on demand.
If you want recall across past sessions, or an agent that holds the thread through a long one,
nothing here does that.

## Knowledge that grows without getting harder to use

A project's notes decay in a specific way. Appending to a log is easy; filing a fact into the right
page takes judgment. So the easy half happens every time and the hard half never does, orphan pages
pile up, and a cold agent either loads a huge index or greps and hopes.

The fix splits capture from synthesis. Agents append cheap one-line entries to `log.md`.
`bc-wiki-maintain` later detects which entries were never promoted — by diffing the log against the
last promotion commit, so there is no counter to maintain — and files each one into the smallest
page that already covers it. Every entry gets classified exactly once as promoted, skipped with a
reason, or a genuine contradiction, which goes to `open-questions/` with both citations and no
winner. Promotion is gated to new pages and appends only.

Reading uses ranked search rather than an index load. `wiki_search.py` runs BM25 over the vault's
tracked Markdown and prints a bounded list of paths; the agent opens two or three. On a 20-question
benchmark authored before any of the retrieval methods existed, that cost a median 171 output
tokens against 4,543 for loading `index.md`. Miss rates were 0.15 against 0.30. The tool needs no install, no index that can go stale, and no
registration. `qmd` remains available for hybrid search across vaults when you have it.

The archive still grows. What stays flat is what an agent must read to orient.

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

Support is uneven and worth knowing before you commit. Claude Code and Pi are the tested paths.
Composer and Grok read the shared bus (Grok's bundled skills can shadow same-named concepts).
OpenCode needs a small plugin to expose skills as slash commands. Codex runs the always-on kernel
globally and reaches everything else through repo `AGENTS.md` pointers. Gemini is manual bootstrap.
See [`docs/harnesses.md`](docs/harnesses.md) and [`docs/bootstrap.md`](docs/bootstrap.md).

## Build your own skill

You do this in chat. Drop a source into `docs/research/raw/` — an article, a gist, someone else's
skill, your notes — and tell the agent to ingest it. The agent researches, writes the concept,
attacks it with a pressure test, deploys, and lints. You decide what the source should actually
change, and whether a failing test is a loophole or a bad test.

What you get that a prompt file does not: named sources so a rule can be re-evaluated later, a test
that tried to break it before it shipped, and a linter that fails if either is missing.

When a skill underperforms, tell the agent to fix the instruction, not the output.

## Authorisation

`~/.config/agent-concepts/publish.yaml` is user-owned, lives outside this repo, and is default-deny.
An agent may push, open a PR, or close an issue only when a rule there matches or you say so in the
conversation.

Repo-local instruction files can restrict publishing. They cannot grant it. Changes under
`policies/` are never publishable under the policy itself, including by rules added later — a
policy that can publish its own amendments is default-allow wearing a disguise. See
[`policies/README.md`](policies/README.md).

## Four gates

These get a higher bar for revision than anything else here, because each fails through
in-the-moment rationalisation. The moment a gate blocks you is when your judgment about that gate
is least trustworthy.

- **Canon** — never hand-edit a derived output or anything a deploy symlink points into. The next
  rebuild reverts it, and "it's a one-line fix" is how canon and deploys drift apart.
- **Provenance** — every concept names its sources. An uncredited decision is a guess nobody can
  re-evaluate.
- **Test** — nothing that constrains an agent deploys until it has held under pressure. These
  instructions fail in ways their authors cannot see.
- **Immutability** — ingested sources are never edited in place. Annotations belong in the concept
  that cites them, where they carry provenance.

Each states its reason, so you can tell where it does not apply and argue that it should change —
out loud, and logged.

## Private concepts

Infrastructure topology, employer process, an upstream body whose licence forbids redistribution:
things an agent needs to know that you cannot publish.

Put them in `~/.config/agent-concepts/concepts/<name>/body/SKILL.md`, the same shape as `concepts/`
here, and the deploy script picks them up. A private concept overrides a public one of the same
name and reports the collision rather than swallowing it. The directory is optional.

## Design stance

Written to liberate agents rather than constrain them, assuming the next reader may be more capable
than the last. Rules carry their reasoning so they can be generalised correctly.

Disagreeing with a rule here is legitimate; the move is to say so and change it. Silent deviation
hides the disagreement that would have improved the rule. Blind obedience preserves a known flaw.

## Provenance and licensing

Built by reading other people's work and adapting it: Jesse Vincent's
[superpowers](https://github.com/obra/superpowers) (MIT), [Matt Pocock's
skills](https://github.com/mattpocock/skills), and published guidance from Anthropic, OpenAI and
Google. `docs/research/raw/ingested/CITATIONS.md` indexes the corpus.

Concept bodies are adaptations — re-voiced, merged, specialised — not copies. Where a body could
not be written independently, the concept points upstream instead of vendoring it; public `herdr`
works this way because upstream states no licence. Some licensed upstream snapshots remain under
`docs/research/raw/ingested/` as immutable evidence, under their own terms.
