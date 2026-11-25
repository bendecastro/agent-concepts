# Agent concepts

Skills and rules for coding agents. Each concept (one unit of agent guidance) is kept once in
this repository, with its design reasons, sources and tests, and is linked into each harness
(the program that runs the agent) by symlink. Edit the concept here and every harness sees the
change.

## Supported harnesses

The contributor install (below) links concept bodies into `~/.agents/skills/` (the shared skill folder) and into the
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

Install a release, not the newest code: the newest code changes many times a day and can hold
unfinished work. A release is a fixed, named version of the skills; its name (such as `v0.3.0`)
is called a tag. The newest release is `v0.3.0`; check the
[releases page](https://github.com/bendecastro/agent-concepts/releases) and use the newest tag
listed there in place of `v0.3.0` in the commands below.

Before you start:

- **Pick one method per agent.** Two methods for the same agent install each skill twice.
  Several agents (Pi, Cursor, Grok, OpenCode, Muse) also read the shared folder
  `~/.agents/skills/`. The contributor install and `npx skills -a pi` both write there, so an
  agent that already has the skills by another method will see them twice.
- **After installing, start a new agent session.** Sessions that are already open do not see new
  skills.
- **The six `bc-council-*` skills work only in Pi, and only with the
  [`pi-subagents`](https://www.npmjs.com/package/pi-subagents) package installed.** They start
  subagents (helper agents) through it, and installing this repository does not install it. To
  install it: `pi install npm:pi-subagents`. The other methods install the council skills too,
  but they will not run there.
- **Two skills can work with GitHub issues.** For that, `/bc-plan-to-pipeline` and
  `/bc-pipeline-to-done` need the GitHub CLI (`gh`).
- **What has been tested.** On Linux and macOS: the Pi, Claude Code and Codex methods with
  Pi 1.6.0, Claude Code 2.1.329 and Codex 0.153.1; and `npx skills` (version 1.9.0) installing
  for Pi only. `npx skills` for any other agent, and Windows, have not been tested.
- **To move to a newer release**, run the Uninstall commands for your agent, then the Install
  commands with the new tag. The Refresh commands below do not change your release. Moving from
  one release to a newer one this way has not been tested yet.

### Claude Code

The first command adds this repository as a source of plugins (Claude Code calls it a
marketplace); the second installs the plugin, the package that holds the skills. Codex uses the
same words.

```bash
# Install
claude plugin marketplace add bendecastro/agent-concepts#v0.3.0
claude plugin install agent-concepts@agent-concepts

# Refresh (stays on the release you installed)
claude plugin marketplace update agent-concepts
claude plugin update agent-concepts@agent-concepts

# Uninstall
claude plugin uninstall agent-concepts@agent-concepts
claude plugin marketplace remove agent-concepts
```

### Codex

```bash
# Install
codex plugin marketplace add bendecastro/agent-concepts --ref v0.3.0
codex plugin add agent-concepts@agent-concepts

# Refresh (stays on the release you installed)
codex plugin marketplace upgrade agent-concepts
codex plugin add agent-concepts@agent-concepts

# Uninstall
codex plugin remove agent-concepts@agent-concepts
codex plugin marketplace remove agent-concepts
```

### Pi

```bash
# Install
pi install git:github.com/bendecastro/agent-concepts@v0.3.0

# Refresh (stays on the release you installed)
pi update --extensions

# Uninstall (use the same tag you installed)
pi remove git:github.com/bendecastro/agent-concepts@v0.3.0
```

### Other agents (`npx skills`)

For other agents, use the [`skills` command-line tool](https://github.com/vercel-labs/skills)
through `npx`. `npx` comes with [Node.js](https://nodejs.org); it downloads and runs a
command-line tool in one step. It downloads the newest `skills` tool, which may be newer than
the tested 1.9.0.

[docs/guides/install-packs.md](docs/guides/install-packs.md) has the command for all skills and
a smaller command for each pack (one skill plus the skills it needs). In those commands, replace
`<source>` with `bendecastro/agent-concepts@v0.3.0` and `<agent>` with your agent's id from
[the `skills` agent list](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)
(for example `pi`).

For example, this installs one skill, `bc-self-improve`, for Cursor (an agent we have not tested; only `-a pi` has been):

```bash
npx skills add bendecastro/agent-concepts@v0.3.0 -g -a cursor -y --skill bc-self-improve
```

- `bendecastro/agent-concepts@v0.3.0` is where the skills come from, at release `v0.3.0`.
- `-a cursor` is the agent to install for; use your agent's id from the list instead, for
  example `gemini-cli` or `github-copilot`.
- `--skill` lists the skills to install, by name. The commands on the packs page list
  every skill a pack needs, so copy them rather than typing names yourself.
- `-g` installs for you in every project, not just the current one; `-y` skips the tool's
  questions.

```bash
# Refresh (stays on the release you installed)
npx skills update -g -y

# Uninstall: use the same <agent>, and copy every name after --skill from the install command you ran
npx skills remove -g -a <agent> -y <skill names>
```

### Install from a checkout (contributors)

This is the way to work on the skills themselves: it links the skills to a local copy of this
repository (a checkout), so your edits take effect at once. This installs the newest code, not a
release, so expect unfinished work. Do not combine it with a method above for the same agent.

You need Git and Python 3. To run the repository's checks (`scripts/gate`), also install
`pytest` and `hypothesis`, for example with `pip install pytest hypothesis`.

```bash
git clone https://github.com/bendecastro/agent-concepts.git agent-concepts
cd agent-concepts
export AGENT_CONCEPTS="$PWD"
```

Some skills run scripts from this folder, so your shell needs to know where it is in every new
terminal. Save the path once:

- On macOS (zsh): `echo "export AGENT_CONCEPTS=\"$PWD\"" >> ~/.zshrc`
- On Linux (bash): `echo "export AGENT_CONCEPTS=\"$PWD\"" >> ~/.profile`

Then link the skills:

```bash
python3 scripts/deploy-local-skills.py --dry-run
python3 scripts/deploy-local-skills.py
```

The script makes symlinks (shortcuts to a folder). Its options:

- **`--uninstall`** removes only the links this script created; other skills are left alone.
  Add `--dry-run` to preview it.
- `--dry-run` shows what would change without changing anything.
- `--force` replaces existing files that are not symlinks; it does not replace folders.
- `--harness {all,pi,claude}` picks which of the Pi and Claude Code folders are written. The
  shared `~/.agents/skills/` folder is always written.
- `--skip NAME` leaves one skill out; repeat it for more.

A symlink to a skill this checkout does not own is reported and left alone. The links are
relative, so the checkout can live anywhere. Concepts whose `CONCEPT.md` says `deployed: no`
are not linked.

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

Two skills set up a project and plan its work; you then build it with your agent, or hand it to a
third skill to build while you are away. Each skill leaves its result in files or on GitHub, so the next step does not need the same session.

**`/bc-setup-project`** sets up a project for agents. It inspects the repository, asks what it
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

**Building the planned work.** Open a session and tell your agent to continue the work. It follows the project's work rules: it finishes what is in `work/2-active/`, then takes the next item in the pipeline order and ticks the steps as they land. It works the way your own setup does, with your agent, your skills and your checks, and it asks you when something is unclear. This is the standard way.

When you want to be away, **`/bc-pipeline-to-done`** builds the same work without you. It takes the items marked `Ready for agent: yes`, which `/bc-plan-to-pipeline` marks for you, or the GitHub issues labelled `ready-for-agent`. Since nobody is there to answer, it makes up for that with checking. It claims each item so two drivers can't build the same thing. A builder works in its own worktree, and independent reviewers check every step before it lands. When it needs a decision, it parks the item with your question and moves on. That review costs extra tokens and takes longer than the same work done with you there.

How the planning skills fit together in more detail: [docs/guides/pipeline.md](docs/guides/pipeline.md).

Every concept is listed in [index.md](index.md).

## Workflows

When to run each one, what it asks and what you get, and which skills to give your subagents: [docs/guides/workflows.md](docs/guides/workflows.md).

- [`/bc-setup-project`](docs/guides/workflows.md#bc-setup-project): set up a project for agents, once.
- [`/bc-diagnosing-bugs`](docs/guides/workflows.md#bc-diagnosing-bugs): find a bug's cause from a failing command, then fix it with a test.
- [`/bc-code-review`](docs/guides/workflows.md#bc-code-review): review a change for what was asked and for project standards, separately.
- [`/bc-delegate-investigation`](docs/guides/workflows.md#bc-delegate-investigation): hand independent parts of a task to parallel subagents without losing their results.
- [`/bc-optimize-code`](docs/guides/workflows.md#bc-optimize-code): make code measurably faster or smaller, keeping only proven gains.
- [`/bc-prototype`](docs/guides/workflows.md#bc-prototype): answer a design question with throwaway code.
- [`/bc-self-improve`](docs/guides/workflows.md#bc-self-improve): after a session, propose changes that make the next one faster.
- [`/bc-council-challenge-plan`](docs/guides/workflows.md#bc-council-challenge-plan): have several models attack a plan before it is split into steps.
- [`/bc-to-spec` and `/bc-to-tickets`](docs/guides/workflows.md#bc-to-spec-and-bc-to-tickets): turn a conversation into a GitHub spec and ready-to-build issues.
- [`/bc-triage`](docs/guides/workflows.md#bc-triage): sort incoming issues into ready for an agent, ready for a person, needs information, or rejected.
- [`/bc-find-bugs` and `/bc-council-find-bugs`](docs/guides/workflows.md#bc-find-bugs-and-bc-council-find-bugs): hunt an area for bugs and prove each with a failing test.
- [`/bc-council-audit-security`](docs/guides/workflows.md#bc-council-audit-security): a security audit where every finding is checked by a fresh reviewer.
- [`/bc-improve-codebase-architecture` and `/bc-council-improve-architecture`](docs/guides/workflows.md#bc-improve-codebase-architecture-and-bc-council-improve-architecture): find modules worth reshaping and plan one.
- [`/bc-work-sync`](docs/guides/workflows.md#bc-work-sync): bring work items in line with the project's documents.
- [`/bc-wiki-maintain`](docs/guides/workflows.md#bc-wiki-maintain): health-check the agent's notes folder.
- [`/bc-teach`](docs/guides/workflows.md#bc-teach): learn a subject over many sessions with spaced review.

How agents test the code they change, at three levels: [How the skills test code](docs/guides/workflows.md#how-the-skills-test-code).

## Keeping projects consistent

Design consistency is handled by the `bc-ui-design` skill's
[design framework](concepts/bc-ui-design/body/design-framework.md). Each project keeps design pages
under `docs/design/` that state its current choices. A new colour, size or wording pattern is
defined once as a design token or shared part and used only from there, never as a literal value.
A rule that text search can find becomes a check in the project's test runner. The capture rule
says a visible change is not done until the report lists screenshots and a written critique of
each one.

Guardrails are automated checks that stop speed, size or structure from getting worse: performance
budgets (limits on time, size or memory) and fitness functions (checks for a structural rule).
The [`bc-performance-guardrails`](concepts/bc-performance-guardrails/body/SKILL.md) skill is the method. Each project lists its
limits and checks on `docs/guardrails/README.md`, and the checks run inside the project's gate.
Agents set limits themselves, from today's measurement or a published guideline, and mark each
one as their choice so you can change it; a limit you set is never loosened without asking.
After fixing a slowdown, an agent adds a check so it cannot come back. This repository's own
guardrail is `scripts/gate`, run in CI.

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

Some skills carry their own hard rules, such as the capture rule in `bc-ui-design` and the recovery
rule in `bc-delegate-investigation`.

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
