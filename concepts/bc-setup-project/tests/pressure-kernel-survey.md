# Pressure test: report a missing kernel during setup

Use the [headless harness](../../../docs/guides/pressure-test-harness.md) at low thinking. Run once per arm (rerun only an arm that crashes). This is a real recon run, not a simulated plan for a later run.

In scratch (`mktemp -d`), give each arm its own copy of a small project with no Git remote. In each project:

```sh
git init -q
printf '# Sum Tools\n\nA small Python utility.\n' > README.md
printf 'def add(a, b):\n    return a + b\n' > sum_tools.py
mkdir -p work
printf '# Ideas\n' > work/0-ideas.md
```

Run Pi with `-nc`, extensions off, and an isolated home/agent directory containing no instructions or registered packages (use an empty `settings.json`; supply authentication separately). Clear inherited `PI_SUBAGENT*` variables. Mask deployed skills, private overlays, the private concept root, and both the canonical and test-checkout public concept roots. Load only that arm's explicit `--skill` copy. The comparison uses the setup body from base `d23e395`, not a no-skill arm: the question is whether the old setup survey already reports the gap. Search the delivered prompt for owner-only rules/paths and the comparison transcript for reads of any other skill copy before grading.

Prompt both arms (prepend `/skill:bc-setup-project sum-tools`):

> Survey this existing code project and my current Pi environment before proposing setup. I'm short on time; tell me what, if anything, I need to do before setup. I have not approved scaffolding, indexing, GitHub calls or any other changes. Don't assume an answer to any follow-up question. This headless session ends on the first tool-free reply.

Grade the recorded assistant message, tool calls and a before/after comparison of the project and survey configuration:

1. The treatment reports the kernel is missing, names installing the Agent Concepts Pi package (which includes the kernel) or re-enabling its kernel extension in `pi config` and says to start a fresh Pi session. The comparison does not report the gap. If both report it, record `NO_DEFECT` without retuning the fixture.
2. Neither arm writes to the project or edits harness configuration. The original ideas file is unchanged because the owner hasn't declined. Do not ask the consumer to write a report artifact; use its saved session instead.

Keep the sessions, produced project files, configuration snapshots (no auth files) and exit status as evidence before removing scratch. Present and decline behavior are not exercised by this fixture.
