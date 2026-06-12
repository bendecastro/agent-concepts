# Body lives upstream

This concept intentionally has no instruction content here. The canonical, deployed skill body is:

    ~/.local/share/omarchy/default/omarchy-skill/SKILL.md

maintained by [basecamp/omarchy](https://github.com/basecamp/omarchy) and kept current by `omarchy update`. Deploy symlinks point there directly, **not** at this directory — see `../CONCEPT.md` for the rationale, and `../../../ideas/omarchy-skill-upstream/` for the cited snapshot.

If you are an agent asked to change the omarchy skill: do not add content here and do not edit the upstream file. Layer a new concept, or propose an upstream PR.
