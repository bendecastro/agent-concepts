# Accuracy check (reference concept)

No runtime gates of ours to pressure-test; accuracy of the skill content is upstream's responsibility. Our check, performed on ingest and worth repeating after a package upgrade:

1. `~/.claude/skills/notebooklm/SKILL.md` exists and its `<!-- notebooklm-py vX.Y.Z -->` stamp matches `notebooklm --version`.
2. The frontmatter still parses as a valid skill (name + description) and the harness picks it up.
3. `raw/notebooklm-skill-upstream/SOURCE.md` still correctly describes the upstream repo and install path.

Result 2026-06-13: all three pass (v0.7.1; Claude Code surfaced the skill immediately after install).
