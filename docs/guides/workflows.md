# Workflows

This page is for people who have installed these skills and want to know which ones to run, when, and what each run gives back. It covers the workflows you start yourself. The skills that steer an agent's everyday work, such as test-driven development, load on their own and are listed in [index.md](../../index.md).

The planning loop (`/bc-setup-project`, `/bc-plan-to-pipeline`, `/bc-pipeline-to-done`) has its own page: [pipeline.md](pipeline.md).

## How to start a skill

Type a slash command with the skill's name, for example `/bc-find-bugs src/billing`. In Pi the form is `/skill:bc-find-bugs src/billing`. Text after the name is the skill's argument.

Some skills also start when you ask for them by name or describe the job ("diagnose this crash", "swarm this"). Others start only from the slash command, because they write reports or files you should ask for on purpose. The entries below say which.

Most of these skills use the folders that `/bc-setup-project` creates: work items in `work/`, decisions and research in `docs/`, and a "Where things go" table in `.bc-agent/AGENTS.md`. Without that setup most of them still run and report what they found, but they do not create work items. `bc-work-sync` needs the setup and stops without it.

Words with a set meaning here, such as gate, worktree and seam, are defined in the [glossary](../../glossary.md).

## When to run what

| When | Workflows |
|---|---|
| Once per project | [bc-setup-project](#bc-setup-project) |
| During a task, when the need comes up | [bc-diagnosing-bugs](#bc-diagnosing-bugs), [bc-code-review](#bc-code-review), [bc-delegate-investigation](#bc-delegate-investigation), [bc-optimize-code](#bc-optimize-code), [bc-prototype](#bc-prototype) |
| At a set point in your work | [bc-self-improve](#bc-self-improve) at the end of a session, and weekly over many sessions; [bc-council-challenge-plan](#bc-council-challenge-plan) before a plan is split into steps; [bc-to-spec and bc-to-tickets](#bc-to-spec-and-bc-to-tickets) after a planning conversation; [bc-triage](#bc-triage) when issues arrive; [bc-find-bugs](#bc-find-bugs-and-bc-council-find-bugs) and [bc-council-audit-security](#bc-council-audit-security) before a release |
| Every few weeks | [bc-improve-codebase-architecture](#bc-improve-codebase-architecture-and-bc-council-improve-architecture), [bc-work-sync](#bc-work-sync), [bc-wiki-maintain](#bc-wiki-maintain) |
| Across many sessions | [bc-teach](#bc-teach) |

Where a skill states its own timing, the entry gives it. Where it does not, the entry gives a suggested cadence and labels it as a suggestion.

## Council skills

Skills whose names start with `bc-council-` run another skill through a council: two to four advisor subagents, ideally on different models, each working on a share of the job and then attacking each other's results.

They need Pi with the [pi-subagents](https://github.com/nicobailon/pi-subagents) extension. Advisors are agent profiles whose names start with `council-`. With fewer than two, the council fills in with the general `oracle` and `reviewer` agents. The `bc-council-mode` skill ships example profiles in its `examples/agents/` folder. If you have more than four advisor profiles, each council skill first asks which four to use. A council run costs more tokens and time than the plain skill.

## How the skills test code

When an agent changes code with these skills, the `bc-tdd` skill decides how it is tested. There are three levels, each catching more than the one before:

- **Level 1: example tests.** Tests that check chosen inputs give the expected result. Every change gets them.
- **Level 2: property-based tests.** A test states a rule that must always hold, such as "sorting never loses an item", and a tool tries many generated inputs to break it. Required when the change touches logic with a rule you can state, such as calculations, parsers or filters.
- **Level 3: formal verification.** A machine-checked proof that the code meets its rule for every possible input. Off unless you, the project owner, turn it on for a particular part of the project. When a change touches risky code such as money, permissions or stored data, the agent suggests it instead.

Why: examples cover the inputs someone thought of, a property searches for the ones nobody thought of, and a proof covers them all.

Every change report shows a **Test levels** block with one line per level, saying what was added or why it was not needed. A `bc-code-review` review checks those lines against the change and reports a missing block, so a level cannot be skipped quietly. Only the project owner can waive a required level. The full rules are in the `bc-tdd` skill.

## One-time setup

### bc-setup-project

- **When:** once per project, before you plan work in it. Running it again is safe: it only adds missing files.
- **Start:** `/bc-setup-project` (slash command only). Optional argument: the project's short name.
- **What it asks:** what it could not work out from the repository, such as the kind of project (code, operations, learning, knowledge or a mix). It shows a plan before writing anything.
- **What you get:** `work/` for work items, `docs/` for decisions and research, a root `glossary.md` and `AGENTS.md`, a `scripts/gate` check script that fails until you fill in your project's checks, a CI workflow that runs it, and agent rules in `.bc-agent/`. Existing files are kept unless you pass `--force` (files in `.bc-agent/`) or `--force-root` (the root `AGENTS.md`).
- **Example:** in a new repository, run `/bc-setup-project`, answer that it is a code project, approve the plan, then fill in `scripts/gate` with your test command.

### Building your own dashboard

The setup gives you what a dashboard needs, but no dashboard. Build your own on these two commands:

- `python3 .bc-agent/scripts/work_index.py --json` prints every work item as JSON: its stage, steps, what it waits for, which agent holds it, its history from git, review and gate results, and its time and cost once finished. It changes no files, so a dashboard can run it as often as it likes.
- `python3 .bc-agent/scripts/work_spent.py <item-name>` estimates the time, tokens and cost of one item from the agent tools' session files; add `--json` for the list of sessions it counted. It is a rough estimate: read its limits first.

Every field, where it comes from and how far you can rely on it are listed in the [work data reference](../../concepts/bc-setup-project/body/work-data.md). An older project picks these up with the steps in [MIGRATIONS.md](../../concepts/bc-setup-project/MIGRATIONS.md#work-data).

## During a task

### bc-diagnosing-bugs

- **When:** each time something is broken, throws, fails or got slower and the cause is not obvious.
- **Start:** `/bc-diagnosing-bugs`, or say "diagnose" or "debug" and describe the symptom.
- **What it asks:** steps to reproduce, only if it cannot build them itself. It shows its ranked guesses at the cause so you can redirect it.
- **What you get:** first a command that fails on this exact bug. The agent will not change code on a guessed cause until that command exists. Then three to five testable hypotheses, a fix, a regression test written before the fix where the code allows one, and removal of temporary debug logging. If no good place for the test exists, it recommends an architecture review of that spot.
- **Example:** "Diagnose: exporting a report with an empty date range crashes." The agent writes a test that reproduces the crash, ranks causes, checks them one at a time, fixes the bug and keeps the test.

### bc-code-review

- **When:** the skill names its moments: before merging, after a major task, after a complex bug fix, or when you are stuck. Also when you receive review comments and must decide which to act on.
- **Start:** `/bc-code-review`, or ask for a review of a branch or pull request.
- **What it asks:** the base commit or branch to compare against, if you did not give one.
- **What you get:** two separate reports. **Spec** says whether the change does what the issue or plan asked, with nothing missing and nothing extra. **Standards** says whether it follows the project's conventions and avoids quality, test, security and documentation problems. Each finding is Critical, Important or Minor with the file and lines; Critical and Important block merging. The reviewers see the diff and the requirements, never the author's explanation.
- **Example:** "Review this branch against main for issue 42." You get the Spec and Standards findings and a line saying whether a mistake would be easy to undo.

### bc-delegate-investigation

- **When:** a task has several independent parts (reading many files, comparing options, reviewing several areas) and you want them done in parallel.
- **Start:** say "swarm", "go wide" or "fan out", or `/bc-delegate-investigation`.
- **What it asks:** nothing up front. It shows you each part it hands out, which kind of helper gets it and on which model.
- **What you get:** parallel subagents, each writing its results to a file as it works, in a run folder whose path the agent states. If the session dies, the agent can recover from those files instead of starting again. It is meant for reading, comparing and reviewing. For code changes in parallel, the agent hands over to `/bc-pipeline-to-done`. The dispatch instructions are written for Pi with pi-subagents.
- **Example:** "Swarm this: find every place we parse dates and how each one handles time zones." Three scouts each read part of the codebase and write findings; the agent merges them into one answer.

### bc-optimize-code

- **When:** you want something measurably faster, smaller or cheaper without changing what it does.
- **Start:** ask the agent to optimize something by a number, or `/bc-optimize-code`.
- **What it asks:** nothing, as long as the number to improve is clear. If it is not, it stops and says so.
- **What you get:** a baseline measurement, then one small change at a time. A change is kept only when the tests still pass and the number improved; otherwise it is reverted. Each kept change records the number before and after and the check that held.
- **Example:** "Make the import of a 10,000-row CSV faster." The agent times the import, tries changes one by one, and reports, for example, the median time going from 4.1 s to 1.3 s with the import tests still passing.

### bc-prototype

- **When:** before planning, when you cannot decide how something should behave or look without trying it.
- **Start:** `/bc-prototype` (slash command only), with the question as the argument.
- **What it asks:** only which question the prototype must answer.
- **What you get:** throwaway code marked as such: a small terminal program that runs the logic through hard cases, or several very different versions of a screen you can switch between. Once you have chosen, it writes a short note with the question, your verdict and the rejected options, then deletes the prototype or folds the decision into real work.
- **Example:** `/bc-prototype Should the filter panel be a sidebar, a top bar or a popover?` gives three switchable versions on one page.

## At a set point in your work

### bc-self-improve

- **When:** the skill sets no schedule. Suggested: at the end of a session that went slowly or wrong, and a batch run over many sessions about once a week. It reads Pi's session logs, so it works only with Pi.
- **Start:** `/bc-self-improve` (slash command only). Arguments: a session id, or `since 2026-11-01`, or `last 20`, optionally a project name.
- **What it asks:** which of its numbered proposals to act on. If an earlier report is still undecided, it shows that one first.
- **What you get:** a list ordered by cost, each item naming what went wrong, the evidence in the session log, and a change that would prevent it: a new check, a review rule, a pointer in an instruction file, a cheaper tool call. It changes nothing until you pick. Batch mode also writes a report file and records what you decided.
- **Example:** after a session spent rerunning a slow test suite, `/bc-self-improve` proposes running only the affected tests while working, with the timestamps that show the wasted time.

### bc-council-challenge-plan

- **When:** after a plan or requirements document is written and before it is split into steps.
- **Start:** `/bc-council-challenge-plan path/to/plan.md` (slash command only). Needs the council setup above.
- **What it asks:** one question at a time, only about objections that survived the advisors' cross-examination, each with a recommended answer.
- **What you get:** a scout maps the code the plan touches; advisors look for wrong assumptions, missing cases, cheaper paths and risky step order. Your answers are written into the plan, then `bc-plan-to-pipeline` splits it into steps. The advisors never edit the plan themselves.
- **Example:** an advisor shows the plan assumes a cache that the code does not have; you decide whether to build it or drop the step.

### bc-to-spec and bc-to-tickets

- **When:** after you have talked a feature through with the agent and want it on GitHub. They need the `gh` command-line tool. If you want the full guided path instead, use `/bc-plan-to-pipeline` ([pipeline.md](pipeline.md)).
- **Start:** `/bc-to-spec`, then `/bc-to-tickets` (both slash command only).
- **What it asks:** `bc-to-tickets` asks nothing. `bc-to-spec` asks you to confirm where the tests will plug into the code, and asks questions first if the conversation left the scope unclear.
- **What you get:** `bc-to-spec` publishes a requirements document as a GitHub issue. `bc-to-tickets` splits a plan or that issue into small issues that each work end to end, published blockers first with the `ready-for-agent` label.
- **Example:** after discussing a CSV export, `/bc-to-spec` opens "PRD: CSV export" (PRD: product requirements document) and `/bc-to-tickets` opens four issues, each linked to the ones it waits on.

### bc-triage

- **When:** when new issues, pull requests or bug reports arrive. The skill sets no schedule; going through the queue weekly is a suggestion.
- **Start:** `/bc-triage` (slash command only) to see the queue, or `/bc-triage 42` for one issue.
- **What it asks:** what to do with each item after it recommends a state; for a nearly-ready issue, the missing decisions one at a time.
- **What you get:** each item checked against the code (a bug is reproduced if possible) and moved to one state: needs more information, ready for an agent (with a written brief and acceptance criteria), ready for a person, or rejected with the reason recorded. Every comment it posts says it was written by AI.
- **Example:** `/bc-triage` lists three unlabelled issues; for one you approve "ready for agent" and it posts a brief that `/bc-pipeline-to-done` can build from.

### bc-find-bugs and bc-council-find-bugs

- **When:** the skills set no schedule. Suggested: before a release, and after a large change to one area (use `--since` with the commit before it).
- **Start:** `/bc-find-bugs <area>` or `/bc-council-find-bugs <area>` (slash command only). Options: `--since <commit>`, `--max-repro N` (default 12). Without an area it hunts the whole repository only if the repository is small.
- **What it asks:** which findings to file, after the report. Confirmed bugs are pre-selected.
- **What you get:** a report on a separate branch. **Confirmed** bugs each have a test on that branch that fails for the stated reason. **Suspected** bugs explain why they are not confirmed. It does not fix anything. Filed bugs become planned work items. The council version has several advisors hunt with different focuses and attack each other's candidates before the tests are written.
- **Example:** `/bc-find-bugs src/invoices` reports two confirmed bugs (a rounding error and a lost discount on save) with failing tests, and one suspected race.

### bc-council-audit-security

- **When:** the skill sets no schedule. Suggested: before a first public release, and after changes to login, permissions or input handling.
- **Start:** `/bc-council-audit-security` (slash command only), optionally with a scope and `--max-verify N`. Needs the council setup above.
- **What it asks:** which findings to file, after the report. Confirmed findings are pre-selected.
- **What you get:** a run folder `.security-audit/run-N/` with an architecture note listing the places where input from a less-trusted user or system enters the code (trust boundaries), a coverage record, a findings file whose format is checked by a script, and `REPORT.md`. Advisors hunt the boundaries dealt to them; every candidate is then checked by a fresh reviewer, because advisors agreeing is not proof. For a single-model audit, type `/bc-security-audit`, optionally with a scope; asking for a full audit in words works too.
- **Example:** the audit confirms that a file-upload route lets a signed-in user overwrite another user's file, with the code path from request to file write.

## Every few weeks

### bc-improve-codebase-architecture and bc-council-improve-architecture

- **When:** in a project set up with `bc-setup-project`, agents suggest a review once three or more plans have been committed since the last architecture review, or when the code shows structural trouble (unclear module boundaries, code that is hard to test, repeated bugs in the same place). `bc-diagnosing-bugs` also suggests one when a bug had no good place for a test.
- **Start:** `/bc-improve-codebase-architecture` (slash command only), optionally with an area or problem. `/bc-council-improve-architecture` runs the same review through the council.
- **What it asks:** "Which of these would you like to explore?", then questions about the chosen change one at a time.
- **What you get:** an HTML report you can open in a browser, with one card per candidate: the files involved, the problem, the suggested direction, the benefit, a before-and-after diagram and how strongly it is recommended. It changes no code. The change you choose becomes a planned work item, a rejected one is recorded with your reason so it is not suggested again, and the rest stay in the ideas list. The council version adds how many advisors agreed with each card.
- **Example:** the report suggests merging three thin wrappers around the payment API into one module with a single interface; you pick it, answer five questions, and get a planned work item.

### bc-work-sync

- **When:** the skill sets no schedule. Suggested: once a month, or after you change a requirements document or record decisions. It treats active items untouched for 60 days as stale.
- **Start:** `/bc-work-sync` (slash command only), optionally with a focus such as a stage or one document. Needs the `bc-setup-project` layout.
- **What it asks:** approval of one plan, plus numbered questions where your documents disagree with each other.
- **What you get:** a plan listing planned work with no work item, finished items not yet moved to done, stale items, work that already landed, and missing stage or blocker lines. It writes nothing until you approve, then commits the approved changes and has them reviewed.
- **Example:** the plan shows a requirement added last week with no work item and an item whose steps are all ticked; you approve both fixes.

### bc-wiki-maintain

- **When:** the skill sets no schedule. Suggested: when the project's agent notes have grown by many log entries since the last pass, or about once a month in an active project.
- **Start:** `/bc-wiki-maintain .bc-agent` (slash command only); the folder is required.
- **What it asks:** nothing. In a project set up by `bc-setup-project` it reports problems and fixes none of them.
- **What you get:** a health report on the agent's notes folder: broken links, orphan pages and missing search setup. In the older single-folder layout it also moves lasting facts from the log into the right page, and records any log entry that conflicts with a page as an open question instead of choosing one.
- **Example:** the report lists a link to a page that was renamed and a page that nothing links to.

## Across many sessions

### bc-teach

- **When:** you want to learn a subject over many sessions. Each session starts with the review questions that are due, before anything new. A health check of the learning folder runs about every five sessions.
- **Start:** `/bc-teach`, or ask the agent to teach you a subject. Use a separate folder per subject.
- **What it asks:** what you want to learn, then questions you answer from memory.
- **What you get:** lessons pitched just above what you can already do, a review queue whose intervals grow when you answer correctly (2, 4, 9, 20, 45 days, at most 60), a glossary, notes and a record of what you have shown you understand.
- **Example:** in a folder for learning SQL, the first session sets the goal and teaches joins; two days later the session opens with a question on joins before moving on.

## Skills to give every subagent of a role

When an agent hands work to subagents, each subagent starts with a clean context. It does not see your conversation, and in Pi it may not see the installed skills unless you say so. Attaching a skill to a subagent role gives every subagent of that role the same habits.

Skills worth attaching to most roles that read or write code:

| Skill | What it adds to a subagent's work |
|---|---|
| `bc-minimal-solution-ladder` | Before writing code, it checks in order whether the code needs to exist, whether the codebase, the standard library, the platform or an installed dependency already does it, and whether one line would do. Subagents add less code. |
| `bc-codebase-design` | Shared words for module design (module, interface, depth, seam). Subagents spot shallow modules and put tests at the right boundary. |
| `bc-codebase-docs` | Updates the README or docs page that owns a fact in the same change as the code, keeping each fact in one place. |
| `bc-diagnosing-bugs` | A subagent that meets a bug builds a failing command first instead of guessing at a fix. |
| `bc-tdd` | Tests are written first and watched failing before the code that makes them pass. |
| `bc-code-review` | Reviewer subagents report Spec and Standards findings separately, with severities and evidence. |
| `bc-qmd` | Searches your local Markdown notes with the [qmd](https://github.com/tobi/qmd) search tool, so a subagent finds earlier decisions. Useful only if qmd is installed. |

Skills worth attaching to one role:

| Skill | Role | What it adds |
|---|---|---|
| `bc-research` | researcher | Every claim traced to a primary source (official docs, specifications, source code), with facts, recommendations and open questions kept apart. |
| `bc-design` | anyone changing screens | The project's design rules, and screenshots with a written critique before a visible change counts as done. |
| `bc-plain-language` | anyone writing for people | Documents written so the intended readers can find what they need, understand it and act on it. |

### Pi (pi-subagents)

Agent definitions are Markdown files in `~/.pi/agent/agents/` (yours) or `.pi/agents/` (one project). In the frontmatter (the settings block between `---` lines at the top of the file), `skills` lists the skills the subagent receives, whatever `inheritSkills` says:

```yaml
---
name: worker
description: Implementation subagent
inheritSkills: false
skills: bc-minimal-solution-ladder, bc-codebase-design, bc-tdd, bc-diagnosing-bugs
---
```

To add skills to an agent you did not write, including the built-in ones, set `skills` under `subagents.agentOverrides.<agent>` in `~/.pi/agent/settings.json`:

```json
{
  "subagents": {
    "agentOverrides": {
      "reviewer": { "skills": "bc-code-review, bc-codebase-design" }
    }
  }
}
```

A single run can override this with `skill: "bc-research"`, or turn skills off with `skill: false`. Source: the pi-subagents [agents documentation](https://github.com/nicobailon/pi-subagents/blob/main/docs/agents.md).

### Claude Code

Subagents are Markdown files in `~/.claude/agents/` (yours) or `.claude/agents/` (one project). The `skills` frontmatter field loads each listed skill's full text into the subagent when it starts:

```yaml
---
name: implementer
description: Implements small, planned changes
skills:
  - bc-minimal-solution-ladder
  - bc-tdd
  - bc-codebase-docs
---
```

Use the skill's name as Claude Code shows it; a skill installed from a plugin has the plugin name in front (`<plugin>:<skill>`). Skills that can only be started by slash command cannot be attached this way; none of the skills in the tables above have that restriction. Source: Claude Code's [subagents documentation](https://code.claude.com/docs/en/sub-agents).

### Codex

Codex custom agents (TOML files in `~/.codex/agents/` or `.codex/agents/`) see every skill the main session sees; there is no field that attaches a skill to one agent. To make a role use a skill, name it in the agent's `developer_instructions` ("Use the bc-tdd skill for every behaviour change"). To keep a skill away from a role, disable it with a `[[skills.config]]` entry (`path` to its `SKILL.md`, `enabled = false`). Source: Codex's [subagents documentation](https://developers.openai.com/codex/subagents).
