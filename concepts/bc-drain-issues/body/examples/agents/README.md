# Example drain roles for Pi

The three minimal fresh roles that `bc-drain-issues` names on Pi with `pi-subagents`:

- `bc-drain-auditor` — read-only pre-code contract audit for high-risk issues.
- `bc-drain-worker` — writes the change for one issue or rework packet in its worktree; never commits.
- `bc-drain-reviewer` — read-only Spec or Standards review axis.

To use them, copy the files into your user agent directory (`~/.pi/agent/agents/`) or a project's `.pi/agents/`. They set no model on purpose: the drain sets model and effort per launch. To pin one, add `model: provider/your-model-id` (and optionally `thinking:`) to the frontmatter.

Keep the names: the skill launches these roles by name. Keep the tool lists and authority lines too; the drain's correctness gates assume the auditor and reviewer cannot write and the worker cannot commit.
