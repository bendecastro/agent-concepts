# Accuracy check (reference concept)

No runtime gates of ours to pressure-test; accuracy of `/last30days` behavior is upstream's responsibility. Our ingest-time check:

1. `ideas/last30days-skill-upstream/SKILL.md` was copied from upstream `skills/last30days/SKILL.md` at commit `122158415ae421da83e739f2668032f6bc78d39c`.
2. The snapshot frontmatter reports `name: last30days`, `version: "3.3.2"`, repository `https://github.com/mvanhorn/last30days-skill`, and license `MIT`.
3. `concepts/last30days/body/UPSTREAM.md` documents that this workspace does not vendor/deploy the body because the skill depends on the full upstream package.

Result 2026-06-15: all three pass by direct inspection of the cloned upstream repository and local snapshot.
