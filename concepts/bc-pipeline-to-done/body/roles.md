# Pipeline roles for Pi

`bc-pipeline-to-done` launches three jobs (see [Jobs](SKILL.md#jobs)). The Agent Concepts Pi package ships one `pi-subagents` profile per job, in [agents/](agents/); `pi-subagents` finds them through the package manifest, so installing the package and `pi-subagents` is the whole setup:

- `bc-drain-auditor` — the auditor: read-only pre-code contract audit for high-risk units.
- `bc-drain-worker` — the builder: writes the change for one unit or rework packet in its worktree; never commits.
- `bc-drain-reviewer` — the reviewer: read-only Spec or Standards review axis.

They set no model on purpose: a child takes the session's model, and the pipeline sets thinking per launch. To pin a model, set it for the role in `pi-subagents`' agent overrides, or copy the profile into `~/.pi/agent/agents/` (a user profile of the same name wins over the package's) and add `model: provider/your-model-id`.

To use other roles for a job, name them in `~/.config/agent-concepts/overlays/bc-pipeline-to-done.md`. Any replacement keeps these tool lists and authority lines: the pipeline's correctness gates assume the auditor and reviewer cannot write and the builder cannot commit.

Only the three profiles live in `agents/`: `pi-subagents` reads every Markdown file there as a profile.
