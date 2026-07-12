# Body lives upstream

This concept intentionally has no instruction content here. The canonical, deployed skill body is:

    ~/.claude/skills/notebooklm/SKILL.md   (and ~/.agents/skills/notebooklm/SKILL.md)

a copy written by `notebooklm skill install` from the installed [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py) package. Unlike omarchy there is no auto-updater: after `uv tool upgrade notebooklm-py`, rerun `notebooklm skill install` to refresh it. See `../CONCEPT.md` for the rationale, and `../../../raw/ingested/notebooklm-skill-upstream/` for the cited snapshot.

If you are an agent asked to change the notebooklm skill: do not add content here and do not edit the deployed copy (the next `skill install` reverts it). Layer a new concept, or propose an upstream PR.
