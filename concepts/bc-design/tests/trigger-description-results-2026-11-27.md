# Trigger check: widened description (2026-11-27)

Accuracy check of the description change, not a pressure test. Does the agent load the skill for
CLI wording and a new colour token?

## Setup

- Model `openai-codex/gpt-6.1-terra`, thinking low, Pi headless through `scripts/pi_sandbox.py`
  with `-ne -ns --no-prompt-templates --no-skills`.
- Scratch git repo (`mktemp -d`) holding a one-file Python CLI (`greet.py`, argparse, prints a
  green success line) and a two-line `AGENTS.md`.
- Skills passed with `--skill`: `bc-design` plus decoys `bc-explain-visually`,
  `bc-performance-guardrails`, `bc-tdd`, `bc-writing-plans`.
- Old arm: the description before this change (commit `ced2f75`), with its `name` set to
  `bc-design` so only the description differs. New arm: the committed body.
- Prompts: (a) "Add a --quiet flag to the CLI and write its help text." (b) "The success message
  needs a new warning colour; add it." Two runs per prompt per arm.
- Graded on whether the session log has a `read` of the arm's `bc-design/SKILL.md`.

## Results

| Arm | (a) --quiet flag | (b) warning colour |
| --- | --- | --- |
| old description | 2/2 read | 2/2 read |
| new description | 2/2 read | 2/2 read |

## Outcome

No difference on this model: both descriptions triggered in all 8 runs, so this check does not
show that the new description triggers better. It shows only that the new one does not lose
these triggers. The change was committed because the owner chose it; the gap it targets (agents
skipping the skill for CLI wording, flags, tokens or design decisions) may need a weaker model or
less obvious prompts to show.
