# Herdr skill accuracy check

Reference skill: accuracy-check the vendored source and non-mutating CLI guidance. Do not create, split, move, close, prompt, or stop anything during this check.

## Checks

1. Confirm `body/SKILL.md` SHA-256 matches the pinned upstream snapshot in `CONCEPT.md`.
2. Parse the YAML frontmatter and confirm the skill name is `herdr`, its description limits invocation to explicit Herdr requests, and it requires `HERDR_ENV=1`.
3. In a Herdr-managed pane, confirm `HERDR_ENV=1` and run `herdr --version` plus `herdr --help`.
4. Run only read-only discovery commands used by the skill:
   - `herdr pane current --current`
   - `herdr workspace list`
   - `herdr tab list --workspace "$HERDR_WORKSPACE_ID"`
   - `herdr pane list --workspace "$HERDR_WORKSPACE_ID"`
   - `herdr agent list`
5. After deployment, confirm the `herdr` links under `~/.agents/skills/`, `~/.pi/agent/skills/`, and `~/.claude/skills/` all resolve to the canonical `body/` directory.

## Result — 2026-07-22

**PASS** on Herdr 0.7.4. The vendored hash and metadata matched; all read-only commands succeeded inside `HERDR_ENV=1`; all three deployment links resolved to the canonical body.
