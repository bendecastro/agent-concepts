# Agent concepts

Skills and rules for coding agents. Each concept (one unit of agent guidance) is kept once in
this repository, with its design reasons, sources and tests, and is linked into each harness
(the program that runs the agent) by symlink. Edit the concept here and every harness sees the
change.

## Supported harnesses

Deploying links concept bodies into `~/.agents/skills/` (the shared skill folder) and into the
Pi and Claude Code skill folders.

| Harness | How it gets the skills |
| --- | --- |
| Pi | own skill folder, written by the deploy script |
| Claude Code | own skill folder, written by the deploy script |
| Composer (Cursor) | reads `~/.agents/skills/` |
| Grok | reads `~/.agents/skills/`; Grok's bundled skills can shadow a concept of the same name |
| OpenCode | reads `~/.agents/skills/`; a small plugin turns the skills into slash commands |
| Muse Code | reads `~/.agents/skills/`; its always-on rules file is a copy you make yourself |
| Codex | always-on rules file plus pointers in a repository's `AGENTS.md` |
| Gemini | manual bootstrap prompt; untested |

Details and known problems for each harness: [docs/guides/harnesses.md](docs/guides/harnesses.md).
Prompts for harnesses without skill loading: [docs/guides/bootstrap.md](docs/guides/bootstrap.md).

## Install

You need Git and Python 3. The repository's own gate also needs `pytest` and `hypothesis`.
`/bc-drain-issues` and the issue mode of `/bc-plan-to-pipeline` need the GitHub CLI (`gh`).

```bash
git clone <this-repository-url> agent-concepts
cd agent-concepts

# Some skill bodies run scripts from the checkout, so the shell needs its location.
echo "export AGENT_CONCEPTS=\"$PWD\"" >> ~/.profile   # saves this checkout's path; adjust for your shell
export AGENT_CONCEPTS="$PWD"

python3 scripts/deploy-local-skills.py --dry-run
python3 scripts/deploy-local-skills.py
```

Options: `--dry-run`, `--force` (replaces existing non-symlink files, not directories),
`--harness {all,pi,claude}`, `--skip NAME` (repeatable). The shared `~/.agents/skills/` folder is
always written; `--harness` picks which of the Pi and Claude Code folders are written too. The
links are relative, so the checkout can live anywhere. Concepts whose `CONCEPT.md` says
`deployed: no` are not linked.

Start a new agent session afterwards so it sees the skills.

## Where things are

| Path | What it holds |
| --- | --- |
| [`concepts/`](concepts/) | one folder per concept: `CONCEPT.md` (reasons, sources, test and deploy status), `body/` (what the agent reads), `tests/` |
| [`index.md`](index.md) | catalogue of every concept and every raw source |
| [`glossary.md`](glossary.md) | the meaning of this repository's terms (concept, skill, gate, hard rule, work item and others) |
| [`docs/README.md`](docs/README.md) | map of the human-facing documentation |
| [`docs/status.md`](docs/status.md) | generated board of each concept's test and deploy status |
| [`docs/guides/`](docs/guides/) | how-to guides: harnesses, bootstrap, the planning pipeline, pressure tests |
| [`docs/research/`](docs/research/README.md) | dated investigations, and `raw/`, the raw sources that are never edited |
| [`work/`](work/README.md) | work items for this repository; the folder an item sits in is its status |
| [`scripts/gate`](scripts/gate) | the full gate: lint, the portability check and the tests; [CI](.github/workflows/gate.yml) runs it on every push and pull request |
| [`.bc-agent/`](.bc-agent/AGENTS.md) | agent mechanics: session protocol, journal, conventions, templates |
| [`policies/`](policies/README.md) | documentation and a template for the publish policy, which lives outside the repository |
| [`AGENTS.md`](AGENTS.md) | operating manual for agents working on this repository |

`python3 scripts/lint.py` checks for mechanical drift: broken links, missing sources, stale index
entries and status pages. For each deployed concept it also checks the recorded test status in
`CONCEPT.md`. It reads that record; it does not rerun the pressure tests.

## The loop

Three skills take a project from no structure to landed changes. Each one leaves its result in
files or on GitHub, so the next step does not need the same session.

**`/bc-init-agent`** sets up a project for agents. It inspects the repository, asks what it
cannot work out, proposes a plan, then creates the layout: work items in `work/`, decisions and
research in `docs/`, a root `glossary.md`, a `scripts/gate` stub that fails until you fill in the
project's checks, a CI workflow that runs it, and agent mechanics in `.bc-agent/`. It only adds
missing files. It overwrites existing files only with `--force` (files under `.bc-agent/`) or
`--force-root` (the root `AGENTS.md`). Learning and knowledge projects get a `.bc-agent/` vault
instead.

**`/bc-plan-to-pipeline`** turns an idea into planned work. It asks questions one at a time until
the idea is settled (for an already-settled design it asks only the open questions together),
writes the requirements, and splits the plan into slices: thin pieces that each work end to end.
The slices become the steps of a work item, GitHub issues labelled `ready-for-agent` in
dependency order, or both. It files issues only when the project already plans in GitHub issues
or you ask for them.

**`/bc-drain-issues`** works through a repository's `ready-for-agent` GitHub issues without you.
The driver claims each issue with a Git ref before any work starts, so two drivers cannot build
the same issue. High-risk issues get a read-only audit first. A worker writes the code in its own
worktree; it cannot commit, push, or change the issue. Independent reviewers check the result.
The driver lands the change only when every review approves the exact final diff.

How the planning skills fit together in more detail: [docs/guides/pipeline.md](docs/guides/pipeline.md).

The other concepts (code review, test-driven development, research, wiki maintenance, subagent routing and more) are listed in [index.md](index.md).

## Keeping projects consistent

Design consistency is handled by the `ui-design` skill's
[design framework](concepts/ui-design/body/design-framework.md). Each project keeps design pages
under `docs/design/` that state its current choices. A new colour, size or wording pattern is
defined once as a design token or shared part and used only from there, never as a literal value.
A rule that text search can find becomes a check in the project's test runner. The capture rule
says a visible change is not done until the report lists screenshots and a written critique of
each one.

Guardrails are automated checks that stop speed, size or structure from getting worse. Today this
repository's guardrail is `scripts/gate`, run in CI.

## Hard rules

[`AGENTS.md`](AGENTS.md) names four hard rules. They are harder to change than other rules
because breaking them is most tempting at the moment they get in the way. Each can be changed
deliberately, with the change logged, but not skipped quietly.

- **Canon rule** — don't hand-edit derived outputs, or anything outside this repository that a
  harness's symlink points into. The next rebuild reverts it.
- **Provenance rule** — every concept names its sources in `CONCEPT.md`.
- **Test rule** — a concept that enforces discipline is not deployed until it has held under a
  pressure test: an agent run against scripted temptations, once without the concept and once
  with it.
- **Immutability rule** — files in `docs/research/raw/` are never edited.

Some skills carry their own hard rules, such as the capture rule in `ui-design` and the recovery
rule in `bc-swarm`.

## Publishing and authorisation

Agents publish (push, open pull requests, release) only on your explicit instruction in the
conversation or a matching rule in `~/.config/agent-concepts/publish.yaml`. That file is yours,
lives outside the repository, and denies by default; with no file, agents ask. A repository's own
instruction files can restrict publishing but cannot grant it. A change to the policy file is
never publishable under the policy itself. `scripts/publish-check.py` checks whether a rule
matches. See [policies/README.md](policies/README.md).

## Private concepts

For guidance that cannot be published (infrastructure details, employer process, or an upstream
text whose licence forbids redistribution), put a concept in
`~/.config/agent-concepts/concepts/<name>/body/SKILL.md`, in the same shape as `concepts/`. The
deploy script links it alongside the public ones. A private concept overrides a public one of the
same name, and the script reports the override.

## Provenance and licensing

Built by reading other people's work and adapting it: Jesse Vincent's
[superpowers](https://github.com/obra/superpowers) (MIT), [Matt Pocock's
skills](https://github.com/mattpocock/skills), and published guidance from Anthropic, OpenAI and
Google. `docs/research/raw/ingested/CITATIONS.md` indexes the sources.

Concept bodies are rewritten and specialised, not copies of upstream. Where a body could not be
written independently, the concept points upstream instead of copying it; the public `herdr`
concept works this way because upstream states no licence. Some licensed upstream snapshots remain
under `docs/research/raw/ingested/` as immutable evidence, under their own terms.
