<div align="center">

# Agent concepts

**Skills that make coding agents plan first, test first, and remember.**

[![Gate](https://github.com/bendecastro/agent-concepts/actions/workflows/gate.yml/badge.svg)](https://github.com/bendecastro/agent-concepts/actions/workflows/gate.yml)
[![Release](https://badgen.net/github/release/bendecastro/agent-concepts)](https://github.com/bendecastro/agent-concepts/releases)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue)](LICENSE)

[How it works](#how-these-skills-work) · [The workflow](#the-workflow) · [Install](#install) · [Contributing](#working-on-this-repository)

</div>

---

Most coding agents rush into code, guess what you meant, and forget everything once the chat closes. Here, questions get settled first, every test proves it can fail before anyone trusts it, and work lives in files so your project builds intrinsic long-term memory.

Install them once and use them in **Claude Code**, **Codex**, **Pi**, Cursor, or almost any other coding tool. Every skill starts with `bc-` so nothing clashes with what you already have, and uninstalling is clean.

<br>

## How these skills work

Seven ideas run through the whole set.

### Settle questions before building

An agent that guesses what you wanted only builds the wrong thing faster. These skills slow it down first: exploring rough ideas with you, asking questions one at a time until every decision is settled, and bringing real choices to you instead of quietly picking a side.

**Skills:** [bc-grilling](concepts/bc-grilling/body/SKILL.md) · [bc-brainstorming](concepts/bc-brainstorming/body/SKILL.md) · [bc-plan-to-pipeline](concepts/bc-plan-to-pipeline/body/SKILL.md) · the [agent kernel](concepts/agent-kernel/body/AGENT-KERNEL.md), a short set of rules the agent reads in every session

<br>

### Test first, and prove the test can fail

Once a plan is settled, the agent writes a test and watches it fail before writing the code that makes it pass. A test that never failed proves nothing (it might approve anything), so on existing code the agent breaks things on purpose, checks the test catches it, and undoes the break.

Every change gets ordinary example tests. Rule-based logic (calculations, sorting, or reading structured text) also gets automated tests that try hundreds of inputs at once. Mathematical proof stays off unless you turn it on, suggested only where mistakes are costly.

Agents often call a job done too early, so "done" comes with proof: the agent runs the tests, reads the output, and shows you. Bugs follow the same rule — first made to happen on demand, so the fix can be shown to stop them.

**Skills:** [bc-tdd](concepts/bc-tdd/body/SKILL.md) · [bc-diagnosing-bugs](concepts/bc-diagnosing-bugs/body/SKILL.md)

<br>

### Simple on purpose

Simple code is easier to trust, test and change, yet it rarely happens by accident. Before writing anything new, the agent looks for the smallest move that works: something the project already has, a feature built into the language, or a single line. New code comes only when those fall short. What it does build gets shaped into tidy parts that are easy to use from outside, with the hard work tucked inside, so the next person or agent can use a part without understanding all of it.

**Skills:** [bc-minimal-solution-ladder](concepts/bc-minimal-solution-ladder/body/SKILL.md) · [bc-codebase-design](concepts/bc-codebase-design/body/SKILL.md)

<br>

### Independent checking

The agent that wrote the code is the worst judge of it, just as writers struggle to proofread their own drafts. A separate agent reviews every change with fresh eyes, checking whether it does what was asked and is well made. On big questions, several AI models challenge each other's answers.

**Skills:** [bc-code-review](concepts/bc-code-review/body/SKILL.md) · [bc-pipeline-to-done](concepts/bc-pipeline-to-done/body/SKILL.md) · the [council skills](#running-several-agents)

<br>

### Work lives in files, not chat

A chat vanishes when a session ends, while files stay put. Plans, work items and handoff notes live inside the project, surviving crashes so the next agent or a dashboard can read them. Over time they become the project's long-term memory: past facts any session can look up.

**Skills:** [bc-setup-project](concepts/bc-setup-project/body/SKILL.md) · [bc-handoff](concepts/bc-handoff/body/SKILL.md) · [bc-swarm](concepts/bc-swarm/body/SKILL.md) · [bc-wiki-maintain](concepts/bc-wiki-maintain/body/SKILL.md) · the [work-data format](concepts/bc-setup-project/body/work-data.md) a dashboard reads

<br>

### Keep the project consistent, and stop it getting worse

Many short-lived agents on one project will slowly pull it apart unless something holds it together. Every colour, size and wording pattern is defined once and reused. Automatic checks guard the rest, failing whenever a change makes things slower, bigger or more tangled: performance budgets cap time, size or memory, and structural checks (fitness functions) enforce ground rules such as "the screen code never talks to the database directly".

**Skills:** [bc-design](concepts/bc-design/body/SKILL.md) · [bc-performance-guardrails](concepts/bc-performance-guardrails/body/SKILL.md)

<br>

### The instructions are sourced, tested and improved from use

The same care goes into the skills themselves. Every skill records where its ideas came from ([hard rules](AGENTS.md)), and no discipline skill ships until it passes a pressure test: a test agent faces scripted excuses ("I'm short on time", "just trust me"), and wording gets tightened until it holds the line.

When a session ends, the agent can also look back and suggest sharper instructions for itself, plus improvements to the setup you built for it to work in (recursive self-improvement 😉).

**Skills:** [bc-self-improve](concepts/bc-self-improve/body/SKILL.md) · [bc-prompting-agents](concepts/bc-prompting-agents/body/SKILL.md)

<br>

## The workflow

```mermaid
flowchart LR
    A["Set up<br/><code>/bc-setup-project</code>"] --> B["Plan<br/><code>/bc-plan-to-pipeline</code><br/>you answer questions"]
    B --> C["Build<br/>test first"]
    C --> D["Review<br/>fresh eyes"]
    D --> E["Merged"]
    D -- "changes needed" --> C
```

Prepare your project with `/bc-setup-project`, talk through the plan with `/bc-plan-to-pipeline`, and let your agent build. It finishes work already under way before taking the next planned item, ticks off each step as it lands, and asks whenever something is unclear.

> [!TIP]
> **Working while you are away.** `/bc-pipeline-to-done` keeps the same work moving when you step away. It takes only items marked `Ready for agent: yes` (set by `/bc-plan-to-pipeline`) or GitHub issues labelled `ready-for-agent`. Since nobody is there to answer, it takes on only the work those marks cover, because you already settled its questions, and then diligently verifies the work before merging. It claims each item so two agents never collide, builds in a separate copy of the project, and has other agents review every step before merging. When a genuine decision comes up, it sets the item aside with your question and moves on.

<br>

### Running it as a software factory

A factory is more than its machines. Nothing enters the line until its questions are settled, every piece is checked along the way, and each defect that slips out changes the line itself so it cannot escape twice. These skills cover each step.

**Once, when you start a project**
- `/bc-setup-project` gets the project ready for agents.

**For each idea**
- `/bc-triage` first, if the idea arrives as a GitHub issue.
- `/bc-plan-to-pipeline` settles open questions and turns the idea into planned work.
- `/bc-council-challenge-plan` for a large or risky plan, bringing in several AI models to spot shaky assumptions before anything is built (Pi only).
- `/bc-pipeline-to-done` to build while you are away.

**At the end of each session**
- `/bc-self-improve` suggests tweaks to skills, checks or tools so the next session goes better.

**Regularly, as the code grows**

Agents write code quickly, and speed quietly builds up tangles and unreported bugs. Every few finished pieces of work, or whenever one area has grown rapidly:
- `/bc-improve-codebase-architecture` finds parts that would be simpler if reshaped.
- `/bc-find-bugs` hunts for bugs in the newest or busiest code and proves each with a failing test.

**As needed**

| Situation | Run |
|---|---|
| A release is coming, or the code handles logins, payments or personal data | `/bc-security-audit` |
| The list of planned work no longer matches what is actually happening | `/bc-work-sync` |
| The project's agent notes contradict each other or have gone stale | `/bc-wiki-maintain` |

```mermaid
flowchart TD
    setup["Once<br/><span style='color:dodgerblue;font-weight:bold;font-family:monospace;white-space:nowrap'>/bc-setup-project</span>"] --> plan
    idea(["<span style='font-size:22px;font-weight:bold;padding:6px 14px;display:inline-block;white-space:nowrap'>Your idea</span>"]) --> plan
    issue(["GitHub issue"]) --- triage["<span style='color:dodgerblue;font-weight:bold;font-family:monospace;white-space:nowrap'>/bc-triage</span>"] --> plan
    plan["Plan<br/><span style='color:dodgerblue;font-weight:bold;font-family:monospace;white-space:nowrap'>/bc-plan-to-pipeline</span>"] --> queue[("Planned work")]
    plan -. "#nbsp;large or risky#nbsp;" .-> challenge["<span style='color:dodgerblue;font-weight:bold;font-family:monospace;white-space:nowrap'>/bc-council-challenge-plan</span>"]
    challenge -.-> queue
    queue --> build["Build and review<br/><span style='color:dodgerblue;font-weight:bold;font-family:monospace;white-space:nowrap'>/bc-pipeline-to-done</span><br/>when you are away"]
    build --> merged(["Merged"])
    merged -- "#nbsp;as the code grows#nbsp;" --> sweep["<span style='color:dodgerblue;font-weight:bold;font-family:monospace;white-space:nowrap'>/bc-improve-codebase-architecture</span><br/><span style='color:dodgerblue;font-weight:bold;font-family:monospace;white-space:nowrap'>/bc-find-bugs</span>"]
    sweep -- "#nbsp;findings#nbsp;" --> queue
    build -- "#nbsp;end of session#nbsp;" --> improve["<span style='color:dodgerblue;font-weight:bold;font-family:monospace;white-space:nowrap'>/bc-self-improve</span>"]
    improve -- "#nbsp;better skills and checks#nbsp;" --> build
```

When a bug gets out, fix it, then ask what would have caught it: a test, a guardrail or a change to a skill? Add that too. That is how both the line and the product get better.

<br>

### The skills, stage by stage

Each skill writes its output to files or GitHub issues, so the next step never needs the same session. See how the planning skills connect in [pipeline.md](docs/guides/pipeline.md).

Skills marked `/name` are ones you type yourself; the rest load automatically when they fit. Skills linked to [workflows.md](docs/guides/workflows.md) have a fuller guide there (when to run, what it asks, what you get back).

<details>
<summary><b>Set up</b> — get a project ready for agents</summary>

| Skill | What it does | How it starts |
|---|---|---|
| [bc-setup-project](concepts/bc-setup-project/body/SKILL.md) | Prepares a project for agents: a folder for planned work, a place for its docs, and an automatic check on every change. It only adds missing files and never overwrites yours unless you ask (`--force`, `--force-root`). Learning projects get a notes vault instead. | [`/bc-setup-project`](docs/guides/workflows.md#bc-setup-project) |
| [bc-using-git-worktrees](concepts/bc-using-git-worktrees/body/SKILL.md) | Gives a piece of work its own separate copy of the project so unfinished changes never collide with what you are working on, then tidies the copy away afterwards. | automatically |

</details>

<details>
<summary><b>Decide and plan</b> — turn an idea into settled, agent-ready work</summary>

| Skill | What it does | How it starts |
|---|---|---|
| [bc-grilling](concepts/bc-grilling/body/SKILL.md) | Asks you questions one at a time until every decision in a plan is made, so the agent never has to guess what you wanted. | automatically |
| [bc-brainstorming](concepts/bc-brainstorming/body/SKILL.md) | Explores an idea with you, its options and trade-offs, before anyone commits to a plan. | automatically |
| [bc-domain-modeling](concepts/bc-domain-modeling/body/SKILL.md) | Pins down the words your project uses so everyone, agents included, means the same thing by them. Keeps a glossary and a record of hard decisions. | automatically |
| [bc-prd-drafting](concepts/bc-prd-drafting/body/SKILL.md) | Writes up what was already decided in the conversation as a requirements document, without asking you again. | automatically |
| [bc-writing-plans](concepts/bc-writing-plans/body/SKILL.md) | Turns agreed requirements into a step-by-step build plan before any code is touched. | automatically |
| [bc-plan-slicing](concepts/bc-plan-slicing/body/SKILL.md) | Cuts a plan into small pieces that each work end to end on their own, ordered by what depends on what, so an agent can pick one up and finish it. | automatically |
| [bc-plan-to-pipeline](concepts/bc-plan-to-pipeline/body/SKILL.md) | Runs the whole planning sequence in one go: questions, requirements, then slicing into work items. For a settled design, it asks only what is still open; it opens GitHub issues only if the project already uses them or you ask. | `/bc-plan-to-pipeline` |
| [bc-to-spec](concepts/bc-to-spec/body/SKILL.md) | Turns what you have discussed into a written spec on GitHub. | [`/bc-to-spec`](docs/guides/workflows.md#bc-to-spec-and-bc-to-tickets) |
| [bc-to-tickets](concepts/bc-to-tickets/body/SKILL.md) | Breaks a plan into GitHub issues that agents can each pick up on their own. | [`/bc-to-tickets`](docs/guides/workflows.md#bc-to-spec-and-bc-to-tickets) |
| [bc-triage](concepts/bc-triage/body/SKILL.md) | Sorts incoming GitHub issues: checks each one, asks you what is unclear, and marks it ready for an agent or rejected with a reason. | [`/bc-triage`](docs/guides/workflows.md#bc-triage) |
| [bc-prototype](concepts/bc-prototype/body/SKILL.md) | Builds a quick, throwaway version to answer a design question ("would this work?", "which layout reads better?") before real work starts. | [`/bc-prototype`](docs/guides/workflows.md#bc-prototype) |

</details>

<details>
<summary><b>Build</b> — write the code, test first, and keep it consistent</summary>

| Skill | What it does | How it starts |
|---|---|---|
| [bc-tdd](concepts/bc-tdd/body/SKILL.md) | Test-driven development: write the test first and watch it fail, then write the code. Logic with clear rules also gets tests that try many inputs automatically; formal proof only where you turn it on. | automatically |
| [bc-executing-plans](concepts/bc-executing-plans/body/SKILL.md) | Works through a written plan step by step in the current session. | automatically |
| [bc-subagent-driven-development](concepts/bc-subagent-driven-development/body/SKILL.md) | Works through a written plan by giving each step to a fresh helper agent, with a review after each one. | automatically |
| [bc-pipeline-to-done](concepts/bc-pipeline-to-done/body/SKILL.md) | Builds the work you already planned and settled while you are away, with every step reviewed by a separate agent before it is merged. | `/bc-pipeline-to-done` |
| [bc-finishing-development-branch](concepts/bc-finishing-development-branch/body/SKILL.md) | When a piece of work is done, helps you decide whether to merge it, open a pull request, keep it for later or throw it away. | automatically |
| [bc-design](concepts/bc-design/body/SKILL.md) | Keeps what users see consistent: colours, sizes and wording are defined once and reused. A visual change counts as done only with screenshots and a written critique of each. | automatically |
| [bc-minimal-solution-ladder](concepts/bc-minimal-solution-ladder/body/SKILL.md) | Stops the agent from building more than needed. Before writing code it asks: does this need to exist? Does the project already have it? Would one line do? It stops at the first yes. | automatically |
| [bc-performance-guardrails](concepts/bc-performance-guardrails/body/SKILL.md) | Sets limits on speed, size and structure, plus automatic checks that fail when a change breaks them, so the project cannot quietly get slower or messier. | automatically |

**Design consistency.** Each project records its design choices in `docs/design/`. A colour, size or wording pattern is defined once, as a named value or shared building block, and every screen reuses it instead of typing the value again. Rules that can be checked by scanning the code become automatic checks, and a visual change is not done until the agent has taken screenshots and critiqued each one.

**Guardrails and fitness functions.** Each project lists its limits and checks in `docs/guardrails/README.md`, and they run alongside the project's other tests on every change. An agent can set a limit from a measurement or published guideline, marking it as its own choice so you can adjust it; a limit you set is never loosened without asking. After fixing something that got slower, bigger or more tangled, the agent adds a check so it cannot return.

</details>

<details>
<summary><b>Check and review</b> — review changes, find bugs and security holes, speed things up</summary>

| Skill | What it does | How it starts |
|---|---|---|
| [bc-code-review](concepts/bc-code-review/body/SKILL.md) | Reviews a change with fresh eyes: does it do what was asked, and is it well made? Also helps decide which review comments to act on. | automatically |
| [bc-diagnosing-bugs](concepts/bc-diagnosing-bugs/body/SKILL.md) | Finds the real cause of a bug by first making it happen on demand, then fixes it with a test that keeps it from coming back. | [`/bc-diagnosing-bugs`](docs/guides/workflows.md#bc-diagnosing-bugs) |
| [bc-find-bugs](concepts/bc-find-bugs/body/SKILL.md) | Goes looking for bugs nobody has reported yet in a part of the code, and proves each one with a failing test. | [`/bc-find-bugs`](docs/guides/workflows.md#bc-find-bugs-and-bc-council-find-bugs) |
| [bc-security-audit](concepts/bc-security-audit/body/SKILL.md) | Looks for security holes, answers security questions, and in a full audit proves each finding before reporting it. Council version: [`/bc-council-audit-security`](docs/guides/workflows.md#bc-council-audit-security). | automatically for security questions; [`/bc-security-audit`](docs/guides/workflows.md#bc-council-audit-security) for a full audit |
| [bc-optimize-code](concepts/bc-optimize-code/body/SKILL.md) | Makes code faster or smaller in measured steps, keeping a change only when the measurement shows a real gain and nothing broke. | [`/bc-optimize-code`](docs/guides/workflows.md#bc-optimize-code) |

</details>

<details>
<summary><b>Improve the codebase</b> — make code simpler, writing clearer, and the next session better</summary>

| Skill | What it does | How it starts |
|---|---|---|
| [bc-codebase-design](concepts/bc-codebase-design/body/SKILL.md) | Shapes code into parts with a simple outside and the complexity hidden inside, so it is easy to use, test and change. | automatically |
| [bc-improve-codebase-architecture](concepts/bc-improve-codebase-architecture/body/SKILL.md) | Looks over a codebase for parts that would be simpler if reshaped, shows you the options, and plans the one you pick. | [`/bc-improve-codebase-architecture`](docs/guides/workflows.md#bc-improve-codebase-architecture-and-bc-council-improve-architecture) |
| [bc-unslop](concepts/bc-unslop/body/SKILL.md) | Makes writing stop sounding machine-written: cuts filler, hype and stock phrases, and puts real details back in their place. | automatically |
| [bc-self-improve](concepts/bc-self-improve/body/SKILL.md) | Looks back at a session and suggests changes to the checks, skills or tools that would make the next one go faster or with fewer mistakes. | [`/bc-self-improve`](docs/guides/workflows.md#bc-self-improve) |

</details>

<details>
<summary><b>Keep track of the work</b> — pick up where you left off and see what is happening</summary>

| Skill | What it does | How it starts |
|---|---|---|
| [bc-handoff](concepts/bc-handoff/body/SKILL.md) | Writes down where a session got to, so another session, agent or day can pick up right where it left off. | automatically |
| [bc-work-sync](concepts/bc-work-sync/body/SKILL.md) | Checks that the project's list of planned work matches its docs: finds missing, finished or stale items and proposes fixes before changing anything. | [`/bc-work-sync`](docs/guides/workflows.md#bc-work-sync) |

**Dashboard.** Each project's work items are machine-readable. `python3 .bc-agent/scripts/work_index.py --json` prints every item as JSON (stage, steps, blockers, holding agent, review and gate results, time and cost), and `python3 .bc-agent/scripts/work_spent.py <item>` estimates one item's time and cost from session files. See the [work-data reference](concepts/bc-setup-project/body/work-data.md) for fields and [workflows.md § Building your own dashboard](docs/guides/workflows.md#building-your-own-dashboard) to build a dashboard on them.

</details>

<details>
<summary><b>Writing, knowledge and learning</b> — docs, clear writing, research, notes and learning</summary>

| Skill | What it does | How it starts |
|---|---|---|
| [bc-codebase-docs](concepts/bc-codebase-docs/body/SKILL.md) | Keeps a project's documentation true: each fact is written in one place, describes how things are now, and is updated in the same change as the code. | automatically |
| [bc-plain-language](concepts/bc-plain-language/body/SKILL.md) | Writes or reviews text so the people it is for can find what they need, understand it and act on it. | automatically |
| [bc-explain-visually](concepts/bc-explain-visually/body/SKILL.md) | Explains how something works with the smallest picture that makes it clear, such as a short diagram. | automatically |
| [bc-seo](concepts/bc-seo/body/SKILL.md) | Helps a website get found in search engines and AI search. | automatically |
| [bc-teach](concepts/bc-teach/body/SKILL.md) | Teaches you a subject over many sessions, keeps notes of what you learned, and brings back old material so it sticks. | [`/bc-teach`](docs/guides/workflows.md#bc-teach) |
| [bc-wiki-maintain](concepts/bc-wiki-maintain/body/SKILL.md) | Keeps a project's agent notes healthy: finds broken or contradicting notes and promotes what is worth keeping, without silently rewriting anything. | [`/bc-wiki-maintain`](docs/guides/workflows.md#bc-wiki-maintain) |
| [bc-research](concepts/bc-research/body/SKILL.md) | Researches a technical question in trustworthy original sources, such as official documentation, and cites them. | automatically |
| [bc-qmd](concepts/bc-qmd/body/SKILL.md) | Searches all your Markdown notes and agent wikis at once, so past decisions are found instead of re-made. | automatically |
| [bc-prompting-agents](concepts/bc-prompting-agents/body/SKILL.md) | A collection of proven wording for writing instructions to agents, used when writing or improving skills like these. | automatically |
| [naming-things](concepts/naming-things/body/SKILL.md) | Helps choose clear names for the things in a project and its code. | automatically |
| [bc-json-canvas](concepts/bc-json-canvas/body/SKILL.md) | Creates and checks visual boards (mind maps, flowcharts) in the `.canvas` format Obsidian uses. | automatically |
| [bc-obsidian-markdown](concepts/bc-obsidian-markdown/body/SKILL.md) | Writes notes in Obsidian's style of Markdown, with links between notes, embeds and callouts. | automatically |
| [bc-obsidian-bases](concepts/bc-obsidian-bases/body/SKILL.md) | Creates and checks Obsidian Bases, table-like views over your notes. | automatically |

</details>

<a name="running-several-agents"></a>
<details>
<summary><b>Running several agents</b> — split work across helpers, or have several AI models debate</summary>

| Skill | What it does | How it starts |
|---|---|---|
| [bc-swarm](concepts/bc-swarm/body/SKILL.md) | Splits a big investigation across multiple helper agents working in parallel, and saves each result to a file so nothing is lost if a session dies. | [`/bc-swarm`](docs/guides/workflows.md#bc-swarm) |
| [bc-dispatching-parallel-agents](concepts/bc-dispatching-parallel-agents/body/SKILL.md) | How to hand separate tasks to several agents at once: what each one needs to know and how to put their results together. | automatically |

**Council skills** (Pi only; need [`pi-subagents`](https://www.npmjs.com/package/pi-subagents)): put the same question to several models and have them cross-examine each other's answers. Each council skill wraps a parent skill through the advisor council.

| Skill | What it does | How it starts |
|---|---|---|
| [bc-council-mode](concepts/bc-council-mode/body/SKILL.md) | Puts one question to several different AI models, has them challenge each other's answers, and brings you the result. | automatically |
| [bc-council-chain](concepts/bc-council-chain/body/SKILL.md) | Shared recipe the council skills below are built on; you do not run it directly. | automatically |
| [bc-council-challenge-plan](concepts/bc-council-challenge-plan/body/SKILL.md) | Has several models attack a plan for wrong assumptions, missed cases and cheaper routes before it is built. You only answer the objections that survive. | [`/bc-council-challenge-plan`](docs/guides/workflows.md#bc-council-challenge-plan) |
| [bc-council-find-bugs](concepts/bc-council-find-bugs/body/SKILL.md) | Bug hunting with several models, each searching from a different angle and checking the others' finds. | [`/bc-council-find-bugs`](docs/guides/workflows.md#bc-find-bugs-and-bc-council-find-bugs) |
| [bc-council-audit-security](concepts/bc-council-audit-security/body/SKILL.md) | A security audit with several models, each attacking different weak points and trying to disprove the others' findings. | [`/bc-council-audit-security`](docs/guides/workflows.md#bc-council-audit-security) |
| [bc-council-improve-architecture](concepts/bc-council-improve-architecture/body/SKILL.md) | Several models propose ways to reshape the code, cross-examine each other, and rank the ideas they agree are best. | [`/bc-council-improve-architecture`](docs/guides/workflows.md#bc-improve-codebase-architecture-and-bc-council-improve-architecture) |

</details>

The [agent kernel](concepts/agent-kernel/body/AGENT-KERNEL.md) supplies always-on rules for how the agent behaves and checks its work. The skills do not load it. To use it, [install the optional kernel](#optional-agent-kernel) separately.

Every concept is listed in [index.md](index.md). To see how agents test the code they change, read [workflows.md § How the skills test code](docs/guides/workflows.md#how-the-skills-test-code).

<br>

## Install

Pick your agent, open its box, and paste the command. Each installs a **release** — a fixed, named version (its name, such as `v0.5.0`, is called a tag) — not the newest code, which can hold unfinished work. The newest release is `v0.5.0`; if the [releases page](https://github.com/bendecastro/agent-concepts/releases) lists a newer tag, use it in place of `v0.5.0`.

| Agent | Method |
|---|---|
| Pi (recommended) | [Pi package](#pi) |
| Claude Code | [Claude Code plugin](#claude-code) |
| Codex | [Codex plugin](#codex) |
| Any other agent (Cursor, Gemini CLI, GitHub Copilot, …) | [`npx skills`](#other-agents-npx-skills) |
| An agent that cannot load skills | [bootstrap prompt](docs/guides/bootstrap.md) |
| Contributors | [install from a checkout](#install-from-a-checkout-contributors) |

Details and known problems for each agent live in [harnesses.md](docs/guides/harnesses.md); prompts for agents without skill loading live in [bootstrap.md](docs/guides/bootstrap.md).

> [!IMPORTANT]
> - **Pick one method per agent.** Two methods install each skill twice. Several agents also read `~/.agents/skills/`; the contributor install and `npx skills -a pi` both write there.
> - **After installing, start a new agent session.** Open sessions do not see new skills.

**Report a problem:** an install that fails or a skill that misfires goes in a [new issue](https://github.com/bendecastro/agent-concepts/issues/new/choose); a security problem goes privately through [SECURITY.md](SECURITY.md).

<a name="pi"></a>
<details open>
<summary><b>Pi</b> — recommended: the only agent that runs every skill</summary>

**Install** — the skills, the agent kernel, and the pipeline's roles from npm, plus [`pi-subagents`](https://www.npmjs.com/package/pi-subagents), which runs the council and pipeline skills:

```bash
pi install npm:agent-concepts
pi install npm:pi-subagents
```

The council skills run only in Pi, through `pi-subagents`; other install methods include them, but they do not run there.

<details>
<summary>Try a release early, or stay on one release</summary>

`pi install npm:agent-concepts` installs the release on npm's `latest` tag, and `pi update --extensions` moves you to each new one. A new release goes first to the `next` tag and moves to `latest` after it passes an end-to-end test; to try it before then, install `pi install npm:agent-concepts@next`, which `pi update --extensions` keeps on `next`. To stay on one release instead, name its version (updates then skip it): `pi install npm:agent-concepts@0.5.0`, or from GitHub by tag, `pi install git:github.com/bendecastro/agent-concepts@v0.5.0`.

</details>

The package includes the [agent kernel](#optional-agent-kernel) as a Pi extension; to turn it off, disable that extension in `pi config`.

**Update** to the newest release (a pinned install stays where it is):

```bash
pi update --extensions
```

**Uninstall** (use the same source you installed; also run `pi remove npm:pi-subagents` if nothing else uses it):

```bash
pi remove npm:agent-concepts
```

</details>

<a name="claude-code"></a>
<details>
<summary><b>Claude Code</b></summary>

**Install** — adds this repository as a plugin source and installs the plugin:

```bash
claude plugin marketplace add bendecastro/agent-concepts#v0.5.0 && \
  claude plugin install -y agent-concepts@agent-concepts
```

**Refresh** (stays on the release you installed):

```bash
claude plugin marketplace update agent-concepts && \
  claude plugin update agent-concepts@agent-concepts
```

**To move to a newer release**, uninstall, then install again with the new tag.

**Uninstall:**

```bash
claude plugin uninstall agent-concepts@agent-concepts && \
  claude plugin marketplace remove agent-concepts
```

</details>

<a name="codex"></a>
<details>
<summary><b>Codex</b></summary>

**Install:**

```bash
codex plugin marketplace add bendecastro/agent-concepts --ref v0.5.0 && \
  codex plugin add agent-concepts@agent-concepts
```

**Refresh** (stays on the release you installed):

```bash
codex plugin marketplace upgrade agent-concepts && \
  codex plugin add agent-concepts@agent-concepts
```

**To move to a newer release**, uninstall, then install again with the new tag.

**Uninstall:**

```bash
codex plugin remove agent-concepts@agent-concepts && \
  codex plugin marketplace remove agent-concepts
```

</details>


<a name="other-agents-npx-skills"></a>
<details>
<summary><b>Other agents (<code>npx skills</code>)</b></summary>

Use the [`skills` command-line tool](https://github.com/vercel-labs/skills) through `npx`, which comes with [Node.js](https://nodejs.org) and downloads and runs a tool in one step. `-g` installs for you in every project; `-y` skips the prompts. Skills land in `~/.agents/skills/`, which Codex and Pi also read, so they show up there too, and removing them for one agent leaves them in place for the others.

For a smaller install (one skill plus the skills it needs), see [docs/guides/install-packs.md](docs/guides/install-packs.md).

<details>
<summary><b>Cursor</b></summary>

Install all public skills:

```bash
npx -y skills add bendecastro/agent-concepts@v0.5.0 -g -a cursor -y \
  --skill bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs \
  bc-council-audit-security bc-council-chain bc-council-challenge-plan \
  bc-council-find-bugs bc-council-improve-architecture bc-council-mode \
  bc-delegate-investigation bc-diagnosing-bugs bc-dispatching-parallel-agents \
  bc-domain-modeling bc-executing-plans bc-explain-visually bc-find-bugs \
  bc-finishing-development-branch bc-grilling bc-handoff \
  bc-improve-codebase-architecture bc-json-canvas bc-minimal-solution-ladder \
  bc-obsidian-bases bc-obsidian-markdown bc-optimize-code \
  bc-performance-guardrails bc-pipeline-to-done bc-plain-language \
  bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents \
  bc-prototype bc-qmd bc-research bc-security-audit bc-self-improve bc-seo \
  bc-setup-project bc-subagent-driven-development bc-tdd bc-teach bc-to-spec \
  bc-to-tickets bc-triage bc-design bc-unslop bc-using-git-worktrees \
  bc-wiki-maintain bc-work-sync bc-writing-plans
```

Uninstall:

```bash
npx -y skills remove -g -a cursor -y \
  --skill bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs \
  bc-council-audit-security bc-council-chain bc-council-challenge-plan \
  bc-council-find-bugs bc-council-improve-architecture bc-council-mode \
  bc-delegate-investigation bc-diagnosing-bugs bc-dispatching-parallel-agents \
  bc-domain-modeling bc-executing-plans bc-explain-visually bc-find-bugs \
  bc-finishing-development-branch bc-grilling bc-handoff \
  bc-improve-codebase-architecture bc-json-canvas bc-minimal-solution-ladder \
  bc-obsidian-bases bc-obsidian-markdown bc-optimize-code \
  bc-performance-guardrails bc-pipeline-to-done bc-plain-language \
  bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents \
  bc-prototype bc-qmd bc-research bc-security-audit bc-self-improve bc-seo \
  bc-setup-project bc-subagent-driven-development bc-tdd bc-teach bc-to-spec \
  bc-to-tickets bc-triage bc-design bc-unslop bc-using-git-worktrees \
  bc-wiki-maintain bc-work-sync bc-writing-plans
```

Add the [agent kernel](#optional-agent-kernel) (needs Python 3). Cursor has no global instructions file, so run this from each project's root to add the kernel to that project's `AGENTS.md`:

```bash
npx -y agent-concepts kernel install AGENTS.md
```

Remove it with `npx -y agent-concepts kernel remove AGENTS.md`; this deletes only the kernel's marked block.

</details>

<details>
<summary><b>Gemini CLI</b></summary>

Install all public skills:

```bash
npx -y skills add bendecastro/agent-concepts@v0.5.0 -g -a gemini-cli -y \
  --skill bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs \
  bc-council-audit-security bc-council-chain bc-council-challenge-plan \
  bc-council-find-bugs bc-council-improve-architecture bc-council-mode \
  bc-delegate-investigation bc-diagnosing-bugs bc-dispatching-parallel-agents \
  bc-domain-modeling bc-executing-plans bc-explain-visually bc-find-bugs \
  bc-finishing-development-branch bc-grilling bc-handoff \
  bc-improve-codebase-architecture bc-json-canvas bc-minimal-solution-ladder \
  bc-obsidian-bases bc-obsidian-markdown bc-optimize-code \
  bc-performance-guardrails bc-pipeline-to-done bc-plain-language \
  bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents \
  bc-prototype bc-qmd bc-research bc-security-audit bc-self-improve bc-seo \
  bc-setup-project bc-subagent-driven-development bc-tdd bc-teach bc-to-spec \
  bc-to-tickets bc-triage bc-design bc-unslop bc-using-git-worktrees \
  bc-wiki-maintain bc-work-sync bc-writing-plans
```

Uninstall:

```bash
npx -y skills remove -g -a gemini-cli -y \
  --skill bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs \
  bc-council-audit-security bc-council-chain bc-council-challenge-plan \
  bc-council-find-bugs bc-council-improve-architecture bc-council-mode \
  bc-delegate-investigation bc-diagnosing-bugs bc-dispatching-parallel-agents \
  bc-domain-modeling bc-executing-plans bc-explain-visually bc-find-bugs \
  bc-finishing-development-branch bc-grilling bc-handoff \
  bc-improve-codebase-architecture bc-json-canvas bc-minimal-solution-ladder \
  bc-obsidian-bases bc-obsidian-markdown bc-optimize-code \
  bc-performance-guardrails bc-pipeline-to-done bc-plain-language \
  bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents \
  bc-prototype bc-qmd bc-research bc-security-audit bc-self-improve bc-seo \
  bc-setup-project bc-subagent-driven-development bc-tdd bc-teach bc-to-spec \
  bc-to-tickets bc-triage bc-design bc-unslop bc-using-git-worktrees \
  bc-wiki-maintain bc-work-sync bc-writing-plans
```

Add the [agent kernel](#optional-agent-kernel) (needs Python 3). Gemini CLI loads `~/.gemini/GEMINI.md`:

```bash
npx -y agent-concepts kernel install ~/.gemini/GEMINI.md
```

Remove it with `npx -y agent-concepts kernel remove ~/.gemini/GEMINI.md`; this deletes only the kernel's marked block.

</details>

<details>
<summary><b>GitHub Copilot</b></summary>

Install all public skills:

```bash
npx -y skills add bendecastro/agent-concepts@v0.5.0 -g -a github-copilot -y \
  --skill bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs \
  bc-council-audit-security bc-council-chain bc-council-challenge-plan \
  bc-council-find-bugs bc-council-improve-architecture bc-council-mode \
  bc-delegate-investigation bc-diagnosing-bugs bc-dispatching-parallel-agents \
  bc-domain-modeling bc-executing-plans bc-explain-visually bc-find-bugs \
  bc-finishing-development-branch bc-grilling bc-handoff \
  bc-improve-codebase-architecture bc-json-canvas bc-minimal-solution-ladder \
  bc-obsidian-bases bc-obsidian-markdown bc-optimize-code \
  bc-performance-guardrails bc-pipeline-to-done bc-plain-language \
  bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents \
  bc-prototype bc-qmd bc-research bc-security-audit bc-self-improve bc-seo \
  bc-setup-project bc-subagent-driven-development bc-tdd bc-teach bc-to-spec \
  bc-to-tickets bc-triage bc-design bc-unslop bc-using-git-worktrees \
  bc-wiki-maintain bc-work-sync bc-writing-plans
```

Uninstall:

```bash
npx -y skills remove -g -a github-copilot -y \
  --skill bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs \
  bc-council-audit-security bc-council-chain bc-council-challenge-plan \
  bc-council-find-bugs bc-council-improve-architecture bc-council-mode \
  bc-delegate-investigation bc-diagnosing-bugs bc-dispatching-parallel-agents \
  bc-domain-modeling bc-executing-plans bc-explain-visually bc-find-bugs \
  bc-finishing-development-branch bc-grilling bc-handoff \
  bc-improve-codebase-architecture bc-json-canvas bc-minimal-solution-ladder \
  bc-obsidian-bases bc-obsidian-markdown bc-optimize-code \
  bc-performance-guardrails bc-pipeline-to-done bc-plain-language \
  bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents \
  bc-prototype bc-qmd bc-research bc-security-audit bc-self-improve bc-seo \
  bc-setup-project bc-subagent-driven-development bc-tdd bc-teach bc-to-spec \
  bc-to-tickets bc-triage bc-design bc-unslop bc-using-git-worktrees \
  bc-wiki-maintain bc-work-sync bc-writing-plans
```

Add the [agent kernel](#optional-agent-kernel) (needs Python 3). Copilot CLI loads `~/.copilot/copilot-instructions.md`:

```bash
npx -y agent-concepts kernel install ~/.copilot/copilot-instructions.md
```

Remove it with `npx -y agent-concepts kernel remove ~/.copilot/copilot-instructions.md`; this deletes only the kernel's marked block.

</details>

<details>
<summary><b>OpenCode</b></summary>

Install all public skills:

```bash
npx -y skills add bendecastro/agent-concepts@v0.5.0 -g -a opencode -y \
  --skill bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs \
  bc-council-audit-security bc-council-chain bc-council-challenge-plan \
  bc-council-find-bugs bc-council-improve-architecture bc-council-mode \
  bc-delegate-investigation bc-diagnosing-bugs bc-dispatching-parallel-agents \
  bc-domain-modeling bc-executing-plans bc-explain-visually bc-find-bugs \
  bc-finishing-development-branch bc-grilling bc-handoff \
  bc-improve-codebase-architecture bc-json-canvas bc-minimal-solution-ladder \
  bc-obsidian-bases bc-obsidian-markdown bc-optimize-code \
  bc-performance-guardrails bc-pipeline-to-done bc-plain-language \
  bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents \
  bc-prototype bc-qmd bc-research bc-security-audit bc-self-improve bc-seo \
  bc-setup-project bc-subagent-driven-development bc-tdd bc-teach bc-to-spec \
  bc-to-tickets bc-triage bc-design bc-unslop bc-using-git-worktrees \
  bc-wiki-maintain bc-work-sync bc-writing-plans
```

Uninstall:

```bash
npx -y skills remove -g -a opencode -y \
  --skill bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs \
  bc-council-audit-security bc-council-chain bc-council-challenge-plan \
  bc-council-find-bugs bc-council-improve-architecture bc-council-mode \
  bc-delegate-investigation bc-diagnosing-bugs bc-dispatching-parallel-agents \
  bc-domain-modeling bc-executing-plans bc-explain-visually bc-find-bugs \
  bc-finishing-development-branch bc-grilling bc-handoff \
  bc-improve-codebase-architecture bc-json-canvas bc-minimal-solution-ladder \
  bc-obsidian-bases bc-obsidian-markdown bc-optimize-code \
  bc-performance-guardrails bc-pipeline-to-done bc-plain-language \
  bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents \
  bc-prototype bc-qmd bc-research bc-security-audit bc-self-improve bc-seo \
  bc-setup-project bc-subagent-driven-development bc-tdd bc-teach bc-to-spec \
  bc-to-tickets bc-triage bc-design bc-unslop bc-using-git-worktrees \
  bc-wiki-maintain bc-work-sync bc-writing-plans
```

Add the [agent kernel](#optional-agent-kernel) (needs Python 3). OpenCode V1 loads `~/.config/opencode/AGENTS.md` (for the V2 plugin, see [Optional agent kernel](#optional-agent-kernel)):

```bash
npx -y agent-concepts kernel install ~/.config/opencode/AGENTS.md
```

Remove it with `npx -y agent-concepts kernel remove ~/.config/opencode/AGENTS.md`; this deletes only the kernel's marked block.

</details>

<details>
<summary><b>Any other agent</b></summary>

Change `<agent>` to your agent's id from [the `skills` agent list](https://github.com/vercel-labs/skills/blob/main/docs/agents.md).

Install all public skills:

```bash
npx -y skills add bendecastro/agent-concepts@v0.5.0 -g -a <agent> -y \
  --skill bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs \
  bc-council-audit-security bc-council-chain bc-council-challenge-plan \
  bc-council-find-bugs bc-council-improve-architecture bc-council-mode \
  bc-delegate-investigation bc-diagnosing-bugs bc-dispatching-parallel-agents \
  bc-domain-modeling bc-executing-plans bc-explain-visually bc-find-bugs \
  bc-finishing-development-branch bc-grilling bc-handoff \
  bc-improve-codebase-architecture bc-json-canvas bc-minimal-solution-ladder \
  bc-obsidian-bases bc-obsidian-markdown bc-optimize-code \
  bc-performance-guardrails bc-pipeline-to-done bc-plain-language \
  bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents \
  bc-prototype bc-qmd bc-research bc-security-audit bc-self-improve bc-seo \
  bc-setup-project bc-subagent-driven-development bc-tdd bc-teach bc-to-spec \
  bc-to-tickets bc-triage bc-design bc-unslop bc-using-git-worktrees \
  bc-wiki-maintain bc-work-sync bc-writing-plans
```

Uninstall (use the same `-a <agent>` you installed for):

```bash
npx -y skills remove -g -a <agent> -y \
  --skill bc-brainstorming bc-code-review bc-codebase-design bc-codebase-docs \
  bc-council-audit-security bc-council-chain bc-council-challenge-plan \
  bc-council-find-bugs bc-council-improve-architecture bc-council-mode \
  bc-delegate-investigation bc-diagnosing-bugs bc-dispatching-parallel-agents \
  bc-domain-modeling bc-executing-plans bc-explain-visually bc-find-bugs \
  bc-finishing-development-branch bc-grilling bc-handoff \
  bc-improve-codebase-architecture bc-json-canvas bc-minimal-solution-ladder \
  bc-obsidian-bases bc-obsidian-markdown bc-optimize-code \
  bc-performance-guardrails bc-pipeline-to-done bc-plain-language \
  bc-plan-slicing bc-plan-to-pipeline bc-prd-drafting bc-prompting-agents \
  bc-prototype bc-qmd bc-research bc-security-audit bc-self-improve bc-seo \
  bc-setup-project bc-subagent-driven-development bc-tdd bc-teach bc-to-spec \
  bc-to-tickets bc-triage bc-design bc-unslop bc-using-git-worktrees \
  bc-wiki-maintain bc-work-sync bc-writing-plans
```

Add the [agent kernel](#optional-agent-kernel) (needs Python 3). Name the instructions file your agent loads:

```bash
npx -y agent-concepts kernel install /path/to/instructions.md
```

Remove it with `npx -y agent-concepts kernel remove /path/to/instructions.md`; this deletes only the kernel's marked block.

</details>

**Refresh, for every agent** (stays on the release you installed; to move to a newer release, remove the skills and install again with the new tag):

```bash
npx -y skills update -g -y
```

</details>

<a name="install-from-a-checkout-contributors"></a>
<details>
<summary><b>Install from a checkout (contributors)</b></summary>
This links the skills to a local copy of this repository so your edits take effect at once. It tracks the newest code instead of a release, so expect unfinished work, and do not combine it with a method above for the same agent.

You need Git and Python 3. To run the repository's checks (`scripts/gate`), also install `pytest` and `hypothesis`, for example with `pip install pytest hypothesis`.

**Install** — clones the repository, saves the path for future terminals, and links the skills (requires bash or zsh as your login shell):

```bash
case "$SHELL" in */bash) rc="$HOME/.bashrc" ;; */zsh) rc="$HOME/.zshrc" ;; *) echo "Set SHELL to bash or zsh first" >&2; false ;; esac && \
  git clone https://github.com/bendecastro/agent-concepts.git agent-concepts && \
  cd agent-concepts && \
  export AGENT_CONCEPTS="$PWD" && \
  printf 'export AGENT_CONCEPTS=%q\n' "$AGENT_CONCEPTS" >> "$rc" && \
  python3 scripts/deploy-local-skills.py
```

**Refresh** (from the checkout; `git pull` can fail on local changes):

```bash
cd "$AGENT_CONCEPTS" && git pull --ff-only && python3 scripts/deploy-local-skills.py
```

**Uninstall** (removes links only; keeps the checkout and shell setting):

```bash
cd "$AGENT_CONCEPTS" && python3 scripts/deploy-local-skills.py --uninstall
```

The script makes symlinks (shortcuts pointing to a folder). Its options:

- **`--uninstall`** removes only the links this script created and leaves other skills alone. Add `--dry-run` to preview it.
- `--dry-run` shows what would change without changing anything.
- `--force` replaces existing files that are not symlinks; it does not replace folders.
- `--harness {all,pi,claude}` picks which of the Pi and Claude Code folders are written. The shared `~/.agents/skills/` folder is always written.
- `--skip NAME` leaves one skill out; repeat it for more.

A symlink pointing to a skill this checkout does not own is reported and left alone. The links are relative so the checkout can live anywhere, and concepts whose `CONCEPT.md` says `deployed: no` are skipped.

</details>

<br>

### Optional agent kernel

The kernel is a short instruction file loaded into every session, whatever the task: answer questions before editing, check claims before reporting them, keep changes small, and ask before choices you might weigh differently. The [Pi package](#pi) already includes it; for other agents it is a separate, optional install.

<details>
<summary><b>Install, disable or remove the kernel</b> (Claude Code, Codex, OpenCode, other agents)</summary>

The commands below use a local Agent Concepts checkout. Use one kernel source per agent: a package, a manual include or a marked block, not several. To pin the kernel, check out a release tag that contains the kernel package, or a full commit SHA, in a dedicated checkout and use that path; to upgrade, select another revision and refresh or reinstall from it.

| Harness | Install | Disable | Remove |
|---|---|---|---|
| Pi 1.6.1+ | Included in the [Pi package](#pi). Only with the contributor install (no package): from the checkout root, `pi install ./packages/agent-kernel-pi`. | Disable the kernel extension in `pi config`. | Package: remove the package. Standalone: from the same checkout root, `pi remove ./packages/agent-kernel-pi`. |
| Claude Code (requires `python3`) | `claude plugin marketplace add /path/to/agent-concepts`, then `claude plugin install agent-kernel@agent-concepts --scope user`. If the marketplace is already registered, use its checkout if it contains the package. | `claude plugin disable agent-kernel@agent-concepts --scope user`. | `claude plugin uninstall agent-kernel@agent-concepts --scope user`. Keep the marketplace if you still use its skills. |
| Codex (requires `python3`) | `codex plugin marketplace add /path/to/agent-concepts`, then `codex plugin add agent-kernel@agent-concepts`. If the marketplace is already registered, use its checkout if it contains the package. Review and trust the SessionStart hook with `/hooks`; it won't load until trusted. | Disable the kernel plugin in `/plugins`. | `codex plugin remove agent-kernel@agent-concepts`. Keep the marketplace if you still use its skills. |
| OpenCode V2 | In global `opencode.json(c)`, add the absolute path to `packages/agent-kernel-opencode/` to `plugins`. | Delete that entry from `plugins`; leave the package files in place to re-enable later. | Delete the same entry; the checkout can stay. |
| OpenCode V1 | In global `opencode.json(c)`, add the absolute path to the checkout's `packages/agent-kernel/AGENT-KERNEL.md` to `instructions`. There is no V1 kernel plugin. | Delete that entry from `instructions`; keep the file to re-enable later. | Delete the same entry; the checkout can stay. |
| Other harnesses or manual file install | `npx -y agent-concepts kernel install /path/to/instructions.md` (needs Node.js and Python 3), naming the instructions file your harness loads. From a checkout, `python3 packages/agent-kernel/install.py /path/to/instructions.md` does the same. | There is no separate switch; remove the block and rerun install to re-enable it. | Run `npx -y agent-concepts kernel remove /path/to/instructions.md` (or the checkout command with `--remove`); it removes only the marked block. |

Start a fresh session after install, disable or removal; an old session may still carry earlier instructions. For OpenCode, restart the server before starting the new session. The manual installer pins the **copied bytes**: to change versions, rerun install (from the new package or pinned checkout) against the same file. See [delivery behavior and manual deltas](docs/guides/harnesses.md#standalone-kernel) for details.

</details>

<br>

## Working on this repository

How this repository is organised and the rules for changing it. You only need this section if you want to edit the skills themselves.

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

`python3 scripts/lint.py` checks for mechanical drift: broken links, missing sources, stale index entries and status pages. For each deployed concept it also checks the recorded test status in `CONCEPT.md`, reading that record without rerunning the pressure tests. It also warns if a deployed body names a workflow moment without a handoff or load from the skill that owns that moment.

<br>

### Hard rules

[`AGENTS.md`](AGENTS.md) sets four hard rules. They are harder to change than other rules because breaking them is most tempting when they get in the way; each can be changed deliberately with the change logged, never skipped quietly.

- **Canon rule** — don't hand-edit derived outputs, or anything outside this repository that a harness's symlink points into; the next rebuild reverts it.
- **Provenance rule** — every concept names its sources in `CONCEPT.md`.
- **Test rule** — a concept that enforces discipline is not deployed until it has held under a pressure test.
- **Immutability rule** — files in `docs/research/raw/` are never edited.

<br>

### Publishing and authorisation

Agents publish (push, open pull requests, release) only on your explicit instruction or a matching rule in `~/.config/agent-concepts/publish.yaml`. That file belongs to you, lives outside the repository, and denies by default; when it is missing, agents ask first. A repository's own instructions can restrict publishing, never grant it, and a change to the policy file is never publishable under the policy itself. `scripts/publish-check.py` checks whether a rule matches; see [policies/README.md](policies/README.md).

<br>

### Private concepts

For guidance that cannot be published (infrastructure details, employer process, or an upstream text whose licence forbids redistribution), put a concept in `~/.config/agent-concepts/concepts/<name>/body/SKILL.md`, in the same shape as `concepts/`. The deploy script links it alongside the public ones; a private concept overrides a public one of the same name, and the script reports the override.

<br>

### Provenance and licensing

This repository is released under the [MIT licence](LICENSE), so you may use, copy and change it freely as long as you keep the copyright notice. It grew out of reading and adapting other people's work: Jesse Vincent's [superpowers](https://github.com/obra/superpowers) (MIT), [Matt Pocock's skills](https://github.com/mattpocock/skills), and published guidance from Anthropic, OpenAI and Google. `docs/research/raw/ingested/CITATIONS.md` indexes the sources.

Concept bodies are rewritten and specialised, not copies of upstream. Where a body could not be written independently, the concept points upstream instead; the public `herdr` concept works this way because upstream states no licence. Some licensed upstream snapshots stay under `docs/research/raw/ingested/` as immutable evidence, under their own terms.
