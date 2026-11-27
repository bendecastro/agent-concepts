# Pressure results: no GitHub remote means no issue source (2026-11-27)

Work item: `036-pipeline-no-github-source` (stall 1 of the [stranger test](../../../docs/research/2026-11-27-stranger-end-to-end/README.md)). Consumer: `openai-codex/gpt-6.1-terra`, thinking low, headless `pi -p` dry run (the skill launches subagents, so the consumer writes `plan.md` and launches nothing).

## Fixture (every run)

- `scripts/stranger_fixture.py` creates `tinylabels` and its local bare `origin` (no GitHub remote).
- `concepts/bc-setup-project/body/scaffold.py --archetype code` writes the project's `AGENTS.md` and `.bc-agent/AGENTS.md` (which says "GitHub issues are optional"); the stranger run's planned item ([evidence](../../../docs/research/2026-11-27-stranger-end-to-end/evidence/attempt1-planned-item.md)) goes in `work/1-planned/` with `Ready for agent: yes`; index regenerated, committed, pushed.
- `gh` on `PATH` is a stub that logs its arguments and fails like an unauthenticated CLI ("To get started with GitHub CLI, please run: gh auth login", exit 4), as in the stranger run.
- **Project instructions loaded** (no `-nc`). Global instruction files (`~/.pi/agent/AGENTS.md`, `APPEND_SYSTEM.md`), every skill directory and the private config folder are masked with `bwrap`; `-ne --no-mcp --no-skills --skill <copy of the body>`. Each session log was checked to contain "GitHub issues are optional".
- Prompt: `/skill:bc-pipeline-to-done max-iters=1 max-parallel=1` (the stranger's build prompt) plus dry-run harness notes: write `plan.md`, state the chosen source first, and if the run would wait for the owner, write the exact question and mark the plan STOPPED. Runs oldA, oldB, newA and newB also carried the push authorization the stranger gave in its answer ("the owner authorizes pushing to origin main for this run"), so a missing publish policy does not stop the run first. That line says nothing about which source to use.

Old = the committed body before this change; new = the body with the Issues bullet changed to "the project has a GitHub remote and its GitHub issues carry … Without a GitHub remote there is no issue source: do not query it or ask about it."

## Results (graded from `plan.md` and the `gh` stub log)

| Run | Body | `gh` calls | Source outcome in `plan.md` |
| --- | --- | --- | --- |
| old1 (reproduce) | old | 2 (`issue list` ready-for-agent, rework-for-agent) | **STOPPED at source**: "Should this run drain the work-item source, or should GitHub authentication and the issue repository be configured first so the issue queue can be checked?" |
| old2 (reproduce) | old | 2 | Chose work items ("the only known ready source, not proof that no GitHub issues exist"), then stopped later on the missing publish policy (no push authorization in this prompt) |
| oldA | old | 2 | **STOPPED at source**: "Please make the GitHub issue queue readable (for example, authenticate `gh`) …" |
| oldB | old | 1 (`issue list --json number,title,labels`) | **STOPPED at source**: "Should this run drain work items, or do you want to configure GitHub access so the issue queue can be checked first?" |
| newA | new | 0 | Chose work items: "The only remote is a local Git repository, not a GitHub remote, so there is no GitHub issue source to query." |
| newB | new | 0 | Chose work items: "`origin`, is a local bare repository, not a GitHub remote, so there is no issue source to query." |

Reproduction: with project instructions loaded, the old wording stopped at the source question in 1 of 2 runs and called `gh` in both, so stall 1 was not caused only by the missing instructions. Old vs new: old called `gh` 4/4 times and stopped at the source question 3/4 times; new called `gh` 0/2 times and chose the work items without asking 2/2 times.

## Limits

- n=2 for new and n=4 for old; dry runs only, no live build.
- Both new runs stopped later at role verification, because the dry-run roster names roles without their tool limits and the session has no `subagent` tool. That stop comes after the source choice, comes from the harness, and is outside this item.
- Projects with a GitHub remote were not rerun. The change only adds the remote condition to the Issues bullet; the existing issue-source scenario (`scenario-work-items.md`, Scenario C) is untouched.

## Commands and transcripts

Each arm ran `run.sh SCRATCH RUN SKILL_BODY WORKSPACE` in a `mktemp -d` scratch folder. The script builds the fixture above, writes the `gh` stub, then runs from the project:

```bash
PATH=$S/$R-stub:$PATH bwrap --dev-bind / / --tmpfs ~/.agents/skills \
  --tmpfs <resolved ~/.pi/agent/skills> --tmpfs ~/.claude/skills \
  --tmpfs <resolved ~/.config/agent-concepts> \
  --ro-bind /dev/null <resolved ~/.pi/agent/AGENTS.md> \
  --ro-bind /dev/null <resolved ~/.pi/agent/APPEND_SYSTEM.md> \
  pi -p --model openai-codex/gpt-6.1-terra --thinking low -ne --no-mcp -ns \
  --no-prompt-templates --no-skills --skill $S/$R-skill --session-dir $S/$R-sess "$PROMPT"
```

- Old body: `git archive HEAD concepts/bc-pipeline-to-done/body` at the commit before this change (old1 and old2 used the working tree before the edit, which was the same text). New body: the edited working tree.
- old1 and old2 ran in parallel without the push-authorization line; oldA, oldB, newA and newB ran in parallel with it.
- Grades come from each run's `plan.md` and `gh` stub log, and the session JSONL was checked for "GitHub issues are optional" (all six runs) and for the new clause (new runs only).
- Evidence kept private, outside the repository, in the swarm run's state folder (`<run-state>/w036-evidence/<run>/` with `plan.md`, `gh.log`, `final.txt`, `session/`, plus `run.sh`). It is private because the session logs hold machine paths.
