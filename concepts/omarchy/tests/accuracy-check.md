# Accuracy check (reference concept)

No runtime gates of ours to pressure-test; accuracy of the skill content is upstream's responsibility. Our check, performed on ingest and worth repeating after `omarchy update` if something looks off:

1. `~/.claude/skills/omarchy` resolves to `~/.local/share/omarchy/default/omarchy-skill/` and `SKILL.md` exists there.
2. The frontmatter still parses as a valid skill (name + description).
3. `ideas/omarchy-skill-upstream/SOURCE.md` still correctly describes the upstream repo/path.

Result 2026-06-12: all three pass (repo HEAD `8e03151`).
