# Agent concepts

Skills and rules for coding agents — a way of working where questions get settled before code
is written, every test is proved able to fail before it is trusted, and work lives in files so
it survives a closed terminal. The skills are kept once here and linked into whichever agent
you use.

## How these skills work

The set encodes a handful of principles. Each one names the skills that carry it.

**Settle questions before building.** [bc-grilling](concepts/bc-grilling/body/SKILL.md)
interviews you one question at a time until a plan has no open branches.
[bc-brainstorming](concepts/bc-brainstorming/body/SKILL.md) explores an idea before it
becomes a plan. [bc-plan-to-pipeline](concepts/bc-plan-to-pipeline/body/SKILL.md) runs the
full sequence — grill, requirements, slicing — so nothing is built on a guess. The
[agent kernel](concepts/agent-kernel/body/AGENT-KERNEL.md) (always-on rules every session
loads) requires the agent to surface judgment calls and let the owner decide.

**Test first, and prove the test can fail.** [bc-tdd](concepts/bc-tdd/body/SKILL.md) is
central: write a test, plant a bug, watch the test catch it, revert, then write the code. A
test that has never failed proves nothing. Three test levels — example-based, property-based,
and formal verification — are chosen per change, not per project.

**Evidence before claims.** The kernel's verification rules require checking work against the
codebase, not trusting a report. [bc-diagnosing-bugs](concepts/bc-diagnosing-bugs/body/SKILL.md)
reproduces a bug as a failing command before guessing at the cause.

**Smallest solution that works, shaped as deep modules.**
[bc-minimal-solution-ladder](concepts/bc-minimal-solution-ladder/body/SKILL.md) climbs an
ordered ladder — does it already exist? stdlib? one line? — and stops at the first rung that
holds. [bc-codebase-design](concepts/bc-codebase-design/body/SKILL.md) shapes what remains
as deep modules: a small interface hiding a lot of behaviour.

**Independent checking.** [bc-code-review](concepts/bc-code-review/body/SKILL.md) reviews a
diff on two axes (does it match the spec? does it meet standards?) with enough context for
someone who was not there. [bc-pipeline-to-done](concepts/bc-pipeline-to-done/body/SKILL.md)
sends every step to a reviewer before landing. The
[council skills](#running-several-agents) run several models against the same question and
have them cross-examine each other.

**Work lives in files, not chat.** Work items, plans and handoffs are written to disk so they
survive a crashed session and so another agent — or a dashboard — can read them.
[bc-handoff](concepts/bc-handoff/body/SKILL.md) captures state for the next session.
[bc-delegate-investigation](concepts/bc-delegate-investigation/body/SKILL.md) writes every
child's result to a file before the parent reads it. The
[work-data format](concepts/bc-setup-project/body/work-data.md) is what a dashboard consumes.

**The instructions themselves are sourced, pressure-tested and improved from use.** Every
concept names where it came from ([hard rules](AGENTS.md)). A concept that enforces
discipline is not deployed until it has held under a pressure test — an agent run against
scripted temptations, once without the concept and once with it.
[bc-self-improve](concepts/bc-self-improve/body/SKILL.md) looks back at a session and
proposes changes to the instructions.
[bc-prompting-agents](concepts/bc-prompting-agents/body/SKILL.md) is the library of proven
instruction blocks the other skills adapt.

## The workflow

Set up a project with `/bc-setup-project`, plan its work with `/bc-plan-to-pipeline`, then
build it with your agent — or hand the settled items to `/bc-pipeline-to-done`, which builds
them while you are away. `/bc-pipeline-to-done` takes only the items that
`/bc-plan-to-pipeline` already settled, then sends every step through independent review
before merging. Each skill writes its result to files or GitHub issues, so the next step
does not need the same session. How the planning skills fit together:
[pipeline.md](docs/guides/pipeline.md).

Skills marked `/name` are ones you type; the rest load on their own when they fit. Skills
with a link to [workflows.md](docs/guides/workflows.md) have a longer description there
(when to run, what it asks, what you get back).

<details>
<summary><b>Set up</b> — scaffold a project and isolate feature work</summary>

| Skill | What it does | Invocation |
|---|---|---|
| [bc-setup-project](concepts/bc-setup-project/body/SKILL.md) | Scaffold a project's work layout, gate stub, CI workflow and agent mechanics so it is ready for the plan→build loop. | [`/bc-setup-project`](docs/guides/workflows.md#bc-setup-project) |
| [bc-using-git-worktrees](concepts/bc-using-git-worktrees/body/SKILL.md) | Start, switch or clean up a git worktree for isolated feature work. | auto |

</details>

<details>
<summary><b>Decide and plan</b> — settle questions, write requirements, slice into agent-ready work</summary>

| Skill | What it does | Invocation |
|---|---|---|
| [bc-grilling](concepts/bc-grilling/body/SKILL.md) | Interview you about a plan until every branch is resolved. | auto |
| [bc-brainstorming](concepts/bc-brainstorming/body/SKILL.md) | Explore a feature or design idea before it becomes a plan. | auto |
| [bc-domain-modeling](concepts/bc-domain-modeling/body/SKILL.md) | Sharpen a project's terms, stress-test with edge cases, update the glossary. | auto |
| [bc-prd-drafting](concepts/bc-prd-drafting/body/SKILL.md) | Synthesize an already-resolved conversation into a structured PRD. | auto |
| [bc-writing-plans](concepts/bc-writing-plans/body/SKILL.md) | Turn an approved spec into a detailed implementation plan. | auto |
| [bc-plan-slicing](concepts/bc-plan-slicing/body/SKILL.md) | Break a plan into dependency-ordered vertical slices an agent can grab independently. | auto |
| [bc-plan-to-pipeline](concepts/bc-plan-to-pipeline/body/SKILL.md) | Run the full sequence — grill, requirements, slicing — in one pass. | `/bc-plan-to-pipeline` |
| [bc-to-spec](concepts/bc-to-spec/body/SKILL.md) | Turn the current conversation into a GitHub issue spec. | [`/bc-to-spec`](docs/guides/workflows.md#bc-to-spec-and-bc-to-tickets) |
| [bc-to-tickets](concepts/bc-to-tickets/body/SKILL.md) | Break a plan or spec into independently-grabbable GitHub issues. | [`/bc-to-tickets`](docs/guides/workflows.md#bc-to-spec-and-bc-to-tickets) |
| [bc-triage](concepts/bc-triage/body/SKILL.md) | Move issues through intake: verify, grill, write agent briefs, mark ready or rejected. | [`/bc-triage`](docs/guides/workflows.md#bc-triage) |
| [bc-prototype](concepts/bc-prototype/body/SKILL.md) | Build throwaway code to answer a design question before committing to a plan. | [`/bc-prototype`](docs/guides/workflows.md#bc-prototype) |

</details>

<details>
<summary><b>Build</b> — test-driven development, execution, design and guardrails</summary>

| Skill | What it does | Invocation |
|---|---|---|
| [bc-tdd](concepts/bc-tdd/body/SKILL.md) | Write a test, prove it fails, write the code. Three levels: example-based, property-based, formal. | auto |
| [bc-executing-plans](concepts/bc-executing-plans/body/SKILL.md) | Execute a written plan task by task in the current session. | auto |
| [bc-subagent-driven-development](concepts/bc-subagent-driven-development/body/SKILL.md) | Execute a plan with fresh agents for individual tasks and review checkpoints. | auto |
| [bc-pipeline-to-done](concepts/bc-pipeline-to-done/body/SKILL.md) | Build the settled work queue while you are away: isolated worktrees, independent review, driver-owned landing. | `/bc-pipeline-to-done` |
| [bc-finishing-development-branch](concepts/bc-finishing-development-branch/body/SKILL.md) | Merge, PR, keep or discard a finished branch. | auto |
| [bc-ui-design](concepts/bc-ui-design/body/SKILL.md) | Create or change what users see — layout, styling, controls — with a design framework and capture rule. | auto |
| [bc-minimal-solution-ladder](concepts/bc-minimal-solution-ladder/body/SKILL.md) | Climb an ordered ladder (already exists → stdlib → one line → …) and stop at the first rung that holds. | auto |
| [bc-performance-guardrails](concepts/bc-performance-guardrails/body/SKILL.md) | Set or protect speed, size and memory limits; add checks so regressions cannot come back. | auto |

</details>

<details>
<summary><b>Check and review</b> — independent review, bug hunting, security and optimisation</summary>

| Skill | What it does | Invocation |
|---|---|---|
| [bc-code-review](concepts/bc-code-review/body/SKILL.md) | Review a diff for spec fidelity and standards quality, independently. | auto |
| [bc-diagnosing-bugs](concepts/bc-diagnosing-bugs/body/SKILL.md) | Reproduce a bug as a failing command, then fix it with a test. | [`/bc-diagnosing-bugs`](docs/guides/workflows.md#bc-diagnosing-bugs) |
| [bc-find-bugs](concepts/bc-find-bugs/body/SKILL.md) | Hunt an area for wrong behaviour and prove each find with a failing test. | [`/bc-find-bugs`](docs/guides/workflows.md#bc-find-bugs-and-bc-council-find-bugs) |
| [bc-security-audit](concepts/bc-security-audit/body/SKILL.md) | Source security review or a full repository audit with evidence-calibrated findings. | [`/bc-council-audit-security`](docs/guides/workflows.md#bc-council-audit-security) |
| [bc-optimize-code](concepts/bc-optimize-code/body/SKILL.md) | Improve code against an objective metric, keeping only proven gains. | [`/bc-optimize-code`](docs/guides/workflows.md#bc-optimize-code) |

</details>

<details>
<summary><b>Improve the codebase</b> — deep-module design, architecture, unslopping, self-improvement</summary>

| Skill | What it does | Invocation |
|---|---|---|
| [bc-codebase-design](concepts/bc-codebase-design/body/SKILL.md) | Vocabulary and method for designing deep modules. | auto |
| [bc-improve-codebase-architecture](concepts/bc-improve-codebase-architecture/body/SKILL.md) | Find modules worth reshaping and plan one improvement. | [`/bc-improve-codebase-architecture`](docs/guides/workflows.md#bc-improve-codebase-architecture-and-bc-council-improve-architecture) |
| [bc-unslop](concepts/bc-unslop/body/SKILL.md) | Strip machine-generated tells from prose and put specifics back. | auto |
| [bc-self-improve](concepts/bc-self-improve/body/SKILL.md) | After a session, propose changes to checks, concepts or tools that would make the next one faster. | [`/bc-self-improve`](docs/guides/workflows.md#bc-self-improve) |

</details>

<details>
<summary><b>Keep track of the work</b> — handoffs, work sync, dashboard data</summary>

| Skill | What it does | Invocation |
|---|---|---|
| [bc-handoff](concepts/bc-handoff/body/SKILL.md) | Capture a session into a portable document so another session can continue it. | auto |
| [bc-work-sync](concepts/bc-work-sync/body/SKILL.md) | Bring a project's work items in line with its docs. | [`/bc-work-sync`](docs/guides/workflows.md#bc-work-sync) |

**Dashboard.** Each project's work items are machine-readable.
`python3 .bc-agent/scripts/work_index.py --json` prints every item as JSON — stage, steps,
blockers, which agent holds it, review and gate results, time and cost.
`python3 .bc-agent/scripts/work_spent.py <item>` estimates one item's time and cost from
session files. Field definitions:
[work-data reference](concepts/bc-setup-project/body/work-data.md). How to build a dashboard on
these: [workflows.md § Building your own dashboard](docs/guides/workflows.md#building-your-own-dashboard).

</details>

<details>
<summary><b>Writing, knowledge and learning</b> — docs, prose, visuals, Obsidian formats, teaching</summary>

| Skill | What it does | Invocation |
|---|---|---|
| [bc-codebase-docs](concepts/bc-codebase-docs/body/SKILL.md) | Keep source-tree docs truthful: one home per fact, current state not history. | auto |
| [bc-plain-language](concepts/bc-plain-language/body/SKILL.md) | Write or review prose so its intended readers can find, understand and act on it. | auto |
| [bc-explain-visually](concepts/bc-explain-visually/body/SKILL.md) | Explain how a system works using the smallest useful visual. | auto |
| [bc-seo](concepts/bc-seo/body/SKILL.md) | Improve a site's search visibility, structured data and AI-search presence. | auto |
| [bc-teach](concepts/bc-teach/body/SKILL.md) | Learn a subject over many sessions with spaced review. | [`/bc-teach`](docs/guides/workflows.md#bc-teach) |
| [bc-wiki-maintain](concepts/bc-wiki-maintain/body/SKILL.md) | Health-check the agent wiki: lint, promote durable evidence, flag contradictions. | [`/bc-wiki-maintain`](docs/guides/workflows.md#bc-wiki-maintain) |
| [bc-prompting-agents](concepts/bc-prompting-agents/body/SKILL.md) | Library of proven instruction blocks for writing agent prompts. | auto |
| [naming-things](concepts/naming-things/body/SKILL.md) | Choose clear domain and public code names. | auto |
| [bc-json-canvas](concepts/bc-json-canvas/body/SKILL.md) | Author and validate JSON Canvas `.canvas` files. | auto |
| [bc-obsidian-markdown](concepts/bc-obsidian-markdown/body/SKILL.md) | Author Obsidian-flavoured Markdown with wikilinks, embeds, callouts. | auto |
| [bc-obsidian-bases](concepts/bc-obsidian-bases/body/SKILL.md) | Author and validate Obsidian Bases `.base` files. | auto |

</details>

<details>
<summary><b>Running several agents</b> — delegation, dispatching, council cross-examination</summary>

| Skill | What it does | Invocation |
|---|---|---|
| [bc-delegate-investigation](concepts/bc-delegate-investigation/body/SKILL.md) | Hand independent parts of a task to parallel agents without losing results. | [`/bc-delegate-investigation`](docs/guides/workflows.md#bc-delegate-investigation) |
| [bc-dispatching-parallel-agents](concepts/bc-dispatching-parallel-agents/body/SKILL.md) | Split work across agents: what goes in a packet, how to integrate. | auto |

**Council skills** (Pi only; need [`pi-subagents`](https://www.npmjs.com/package/pi-subagents)):
run several models against the same question, then cross-examine each other's answers. Each
council skill wraps a parent skill through the advisor council.

| Skill | Parent skill | Invocation |
|---|---|---|
| [bc-council-mode](concepts/bc-council-mode/body/SKILL.md) | (the council itself) | auto |
| [bc-council-chain](concepts/bc-council-chain/body/SKILL.md) | (shared recipe for chain skills) | auto |
| [bc-council-challenge-plan](concepts/bc-council-challenge-plan/body/SKILL.md) | bc-grilling + bc-plan-to-pipeline | [`/bc-council-challenge-plan`](docs/guides/workflows.md#bc-council-challenge-plan) |
| [bc-council-find-bugs](concepts/bc-council-find-bugs/body/SKILL.md) | bc-find-bugs | [`/bc-council-find-bugs`](docs/guides/workflows.md#bc-find-bugs-and-bc-council-find-bugs) |
| [bc-council-audit-security](concepts/bc-council-audit-security/body/SKILL.md) | bc-security-audit | [`/bc-council-audit-security`](docs/guides/workflows.md#bc-council-audit-security) |
| [bc-council-improve-architecture](concepts/bc-council-improve-architecture/body/SKILL.md) | bc-improve-codebase-architecture | [`/bc-council-improve-architecture`](docs/guides/workflows.md#bc-improve-codebase-architecture-and-bc-council-improve-architecture) |

</details>

The always-on [agent kernel](concepts/agent-kernel/body/AGENT-KERNEL.md) loads in every session
and carries the base rules (operating posture, verification, context economy). It is installed
separately by each method below.

Every concept is listed in [index.md](index.md). How agents test the code they change:
[workflows.md § How the skills test code](docs/guides/workflows.md#how-the-skills-test-code).

## Install

Install a release, not the newest code: the newest code changes many times a day and can hold
unfinished work. A release is a fixed, named version of the skills; its name (such as `v0.3.0`)
is called a tag. The newest release is `v0.3.0`; check the
[releases page](https://github.com/bendecastro/agent-concepts/releases) and use the newest tag
listed there in place of `v0.3.0` in the commands below.

| Agent | Method |
|---|---|
| Claude Code | [Claude Code plugin](#claude-code) |
| Codex | [Codex plugin](#codex) |
| Pi | [Pi extension](#pi) |
| Cursor, Grok, OpenCode, Muse, Gemini CLI, GitHub Copilot | [`npx skills`](#other-agents-npx-skills) (reads `~/.agents/skills/`) |
| Gemini | untested; [bootstrap prompt](docs/guides/bootstrap.md) |
| Contributors | [install from a checkout](#install-from-a-checkout-contributors) |

Details and known problems for each agent: [harnesses.md](docs/guides/harnesses.md).
Prompts for agents without skill loading: [bootstrap.md](docs/guides/bootstrap.md).

Before you start:

- **Pick one method per agent.** Two methods install each skill twice. Several agents also read `~/.agents/skills/`; the contributor install and `npx skills -a pi` both write there.
- **After installing, start a new agent session.** Open sessions do not see new skills.
- **Council skills work only in Pi** with [`pi-subagents`](https://www.npmjs.com/package/pi-subagents) installed. To install it: `pi install npm:pi-subagents`.
- **GitHub issues.** `/bc-plan-to-pipeline` and `/bc-pipeline-to-done` need the GitHub CLI (`gh`) for issue flows.
- **What has been tested.** On Linux and macOS: Pi 1.6.0, Claude Code 2.1.329, Codex 0.153.1, and `npx skills` 1.9.0 installing for Pi. `npx skills` for other agents, and Windows, have not been tested.
- **To move to a newer release**, uninstall first, then install with the new tag.

<details>
<summary><b>Claude Code</b></summary>

**Install**

The first command adds this repository as a plugin source; the second installs the plugin.

```bash
claude plugin marketplace add bendecastro/agent-concepts#v0.3.0
```

```bash
claude plugin install agent-concepts@agent-concepts
```

**Refresh** (stays on the release you installed)

```bash
claude plugin marketplace update agent-concepts
```

```bash
claude plugin update agent-concepts@agent-concepts
```

**Uninstall**

```bash
claude plugin uninstall agent-concepts@agent-concepts
```

```bash
claude plugin marketplace remove agent-concepts
```

</details>

<details>
<summary><b>Codex</b></summary>

**Install**

```bash
codex plugin marketplace add bendecastro/agent-concepts --ref v0.3.0
```

```bash
codex plugin add agent-concepts@agent-concepts
```

**Refresh** (stays on the release you installed)

```bash
codex plugin marketplace upgrade agent-concepts
```

```bash
codex plugin add agent-concepts@agent-concepts
```

**Uninstall**

```bash
codex plugin remove agent-concepts@agent-concepts
```

```bash
codex plugin marketplace remove agent-concepts
```

</details>

<details>
<summary><b>Pi</b></summary>

**Install**

```bash
pi install git:github.com/bendecastro/agent-concepts@v0.3.0
```

**Refresh** (stays on the release you installed)

```bash
pi update --extensions
```

**Uninstall** (use the same tag you installed)

```bash
pi remove git:github.com/bendecastro/agent-concepts@v0.3.0
```

</details>

<details>
<summary><b>Other agents (<code>npx skills</code>)</b></summary>

Use the [`skills` command-line tool](https://github.com/vercel-labs/skills) through `npx`.
`npx` comes with [Node.js](https://nodejs.org); it downloads and runs a command-line tool in
one step.

[docs/guides/install-packs.md](docs/guides/install-packs.md) has the command for all skills and
a smaller command for each pack (one skill plus the skills it needs). In those commands, replace
`<source>` with `bendecastro/agent-concepts@v0.3.0` and `<agent>` with your agent's id from
[the `skills` agent list](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)
(for example `pi`).

For example, this installs one skill for Cursor (only `-a pi` has been tested):

```bash
npx skills add bendecastro/agent-concepts@v0.3.0 -g -a cursor -y --skill bc-self-improve
```

`<agent>` is your agent's id from the list (for example `gemini-cli` or `github-copilot`).
`<skill names>` is the list of skill names from your install command.

**Refresh** (stays on the release you installed)

```bash
npx skills update -g -y
```

**Uninstall** — use the same `<agent>`, and copy every name after `--skill` from your install command:

```bash
npx skills remove -g -a <agent> -y <skill names>
```

</details>

<details>
<summary><b>Install from a checkout (contributors)</b></summary>

This links the skills to a local copy of this repository, so your edits take effect at once.
This installs the newest code, not a release, so expect unfinished work. Do not combine it
with a method above for the same agent.

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
```

```bash
python3 scripts/deploy-local-skills.py
```

The script makes symlinks. Its options:

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

</details>

## Working on this repository

### Where things are

| Path | What it holds |
|---|---|
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

### Hard rules

[`AGENTS.md`](AGENTS.md) names four hard rules. They are harder to change than other rules
because breaking them is most tempting when they get in the way. Each can be changed
deliberately, with the change logged, but not skipped quietly.

- **Canon rule** — don't hand-edit derived outputs, or anything outside this repository that a
  harness's symlink points into. The next rebuild reverts it.
- **Provenance rule** — every concept names its sources in `CONCEPT.md`.
- **Test rule** — a concept that enforces discipline is not deployed until it has held under a
  pressure test.
- **Immutability rule** — files in `docs/research/raw/` are never edited.

### Publishing and authorisation

Agents publish (push, open pull requests, release) only on your explicit instruction or a
matching rule in `~/.config/agent-concepts/publish.yaml`. That file is yours, lives outside the
repository, and denies by default; with no file, agents ask. A repository's own instruction
files can restrict publishing but cannot grant it. A change to the policy file is never
publishable under the policy itself. `scripts/publish-check.py` checks whether a rule matches.
See [policies/README.md](policies/README.md).

### Private concepts

For guidance that cannot be published (infrastructure details, employer process, or an upstream
text whose licence forbids redistribution), put a concept in
`~/.config/agent-concepts/concepts/<name>/body/SKILL.md`, in the same shape as `concepts/`. The
deploy script links it alongside the public ones. A private concept overrides a public one of the
same name, and the script reports the override.

### Provenance and licensing

Built by reading other people's work and adapting it: Jesse Vincent's
[superpowers](https://github.com/obra/superpowers) (MIT), [Matt Pocock's
skills](https://github.com/mattpocock/skills), and published guidance from Anthropic, OpenAI and
Google. `docs/research/raw/ingested/CITATIONS.md` indexes the sources.

Concept bodies are rewritten and specialised, not copies of upstream. Where a body could not be
written independently, the concept points upstream instead of copying it; the public `herdr`
concept works this way because upstream states no licence. Some licensed upstream snapshots remain
under `docs/research/raw/ingested/` as immutable evidence, under their own terms.
