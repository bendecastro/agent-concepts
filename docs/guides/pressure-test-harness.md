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

Run it from inside the practice project, so its own `AGENTS.md` loads:

```sh
python3 <agent-concepts>/scripts/pi_sandbox.py --prompt-out <scratch>/prompt-<run>.json -- \
  pi -p --model <pressure-test model> --thinking low \
  -ne -ns --no-prompt-templates --no-skills \
  --skill <scratch>/<skill-a> --skill <scratch>/<skill-b> \
  --session-dir <scratch>/sess-<run> '/skill:<name> <arguments, then harness notes>'
```

- `scripts/pi_sandbox.py` runs the command in `bwrap` with Pi's global instruction files
  (`AGENTS.md`, `APPEND_SYSTEM.md`, `SYSTEM.md` and the other names Pi reads from its agent
  folder) replaced by empty files, and with every deployed skill folder, the private overlays
  and any `.agents/skills` above the working folder replaced by empty folders. The run then sees
  only the bodies passed with `--skill`. The comparison run (without the concept) uses the same
  helper and omits that concept's `--skill`; search its transcript for reads of the concept
  path before grading (see the Test operation).
- Before the run, the helper starts the same command once, takes the system prompt Pi records
  before its first model reply, and stops with exit 3 when it holds a term from the private
  denylist (`~/.config/agent-concepts/personal-terms.txt`) or misses the text of the project's
  `AGENTS.md`. Keep the `--prompt-out` file with the grading evidence; it shows what both arms
  were told. `--check-only` checks without running.
- No `-nc`. Why: in the 2026-11-26 drain, and in the stranger test's driver, `-nc` was used to
  keep out the global files and also hid the project's own `AGENTS.md`, so the run never saw
  the project's rules. The helper masks
  the global files instead, and its check fails a run with `-nc` in a project that has an
  `AGENTS.md`.
- `-ne` turns off extensions; name each one the run needs with `-e <path>` (for example
  pi-subagents for a run that must see the `subagent` tool), and pass extension flags such as
  `--no-swarm` only when that extension is loaded. Why: the owner's extensions add text to the
  tools and rules sections of the prompt, and the check fails on it.
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
