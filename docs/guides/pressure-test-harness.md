# Pressure-test harness (Pi, headless)

How to run a consuming agent for the Test operation in `AGENTS.md` with Pi headless (in a terminal, with no interactive chat), so it sees only the
concept under test. This page records the mechanics; what to test and how to grade stay in each
concept's `tests/`. Worked examples: `concepts/bc-council-find-bugs/tests/scenario.md`,
`concepts/bc-council-audit-security/tests/scenario.md`.

## Setup

1. Make a scratch folder with `mktemp -d` (no path argument) and delete it when done. Put the
   practice project in it and keep any answer key out of it.
2. Copy each skill body the run needs with `cp -rL` into the scratch folder. Why: deployed skill
   folders are symlinks, and a symlinked skill folder is not found when loaded with `--skill`.
3. Unset every `PI_SUBAGENT*` environment variable. Why: when the harness runs inside a subagent,
   those variables mark the run as a nested child and hide the `subagent` tool.

## Command

```sh
bwrap --dev-bind / / \
  --tmpfs ~/.agents/skills --tmpfs ~/.pi/agent/skills --tmpfs ~/.claude/skills \
  --tmpfs ~/.config/agent-concepts/overlays \
  pi -p --model <pressure-test model> --thinking low \
  --no-swarm -nc -ns --no-prompt-templates --no-skills \
  --skill <scratch>/<skill-a> --skill <scratch>/<skill-b> \
  --session-dir <scratch>/sess-<run> '/skill:<name> <arguments, then harness notes>'
```

- The `--tmpfs` mounts (empty temporary folders laid over the real ones for this run only) hide every deployed skill and private overlay, so the run sees only the
  bodies passed with `--skill`. The comparison run (without the concept) keeps the mounts and
  omits that concept's `--skill`; search its transcript for reads of the concept path before
  grading (see the Test operation).
- A skill with `disable-model-invocation: true` loads only through its slash command, so the
  prompt must start with `/skill:<name>`.
- Headless `pi -p` ends the session at the first reply without a tool call. Say so in the
  harness notes, and give the owner's answers to any question the skill asks (for example
  "the owner answers `all` at the filing question").
- Grade from the files the run produced and its session log (a JSONL file: one JSON record per line), never from its final reply.

## Dry runs for skills that launch subagents

A skill whose job is to launch and coordinate subagents (council chains, drains, swarms) is
tested as a dry run: the prompt tells the consumer to launch nothing and write `plan.md` stating
every launch (role, model and thinking, skills, worktree, branch), each brief and relay, the
formats and rules it applies, and the report and filing it would produce. Give it a fictional
roster (for example "assume `subagent list` returns `council-alpha`, `council-beta`,
`council-gamma`, `scout`, `worker`, `reviewer`"). Grade numbered criteria, each checkable from
`plan.md`. The first real run of the skill is its live test; record that in its `CONCEPT.md`.

Why: on 2026-11-24 a live end-to-end test of a council chain on the pressure-test model took four
rounds, and 6 of 7 runs stopped early. Dry runs of the same chain, and of three other chains, passed
first time or after one wording fix, because they check the instructions rather than the
model's stamina.
