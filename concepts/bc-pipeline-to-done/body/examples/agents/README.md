# Example roles for Pi

`bc-pipeline-to-done` launches three jobs (see [Jobs](../../SKILL.md#jobs)). These are example Pi profiles, for `pi-subagents`, that meet each job's limits:

- `bc-drain-auditor` — the auditor: read-only pre-code contract audit for high-risk units.
- `bc-drain-worker` — the builder: writes the change for one unit or rework packet in its worktree; never commits.
- `bc-drain-reviewer` — the reviewer: read-only Spec or Standards review axis.

To use them, copy the files into your user agent directory (`~/.pi/agent/agents/`) or a project's `.pi/agents/`, and name the roles you use for each job in `~/.config/agent-concepts/overlays/bc-pipeline-to-done.md`. They set no model on purpose: the drain sets model and effort per launch. To pin one, add `model: provider/your-model-id` (and optionally `thinking:`) to the frontmatter.

The names are examples; rename them freely. Keep the tool lists and authority lines: the drain's correctness gates assume the auditor and reviewer cannot write and the builder cannot commit.
