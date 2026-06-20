# Body lives upstream

This concept intentionally has no instruction content here. The canonical `/last30days` skill body is the installed upstream package/plugin from [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill), not this workspace.

Install/update through upstream's supported channels, for example Claude Code's plugin marketplace or `npx skills add mvanhorn/last30days-skill -g`. Do not copy only `SKILL.md` into this concept: the skill invokes bundled scripts and assumes the full upstream package layout. See `../CONCEPT.md` for the rationale, and `../../../raw/last30days-skill-upstream/` for the cited snapshot.

If you are an agent asked to change `/last30days`, make the change upstream or propose an upstream PR. Do not edit an installed generated copy unless explicitly doing a throwaway local experiment.
