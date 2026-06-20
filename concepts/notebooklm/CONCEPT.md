# notebooklm

Reference skill for driving Google NotebookLM from the terminal via the unofficial `notebooklm` CLI ([teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py)): create notebooks, add sources (URLs, PDFs, YouTube, audio/video), chat with sources, and generate/download artifacts (audio overviews, quizzes, flashcards, slide decks, mind maps) — including features the web UI doesn't expose.

## Design decision: no vendored body (upstream-installer-maintained)

Like [[omarchy]], this concept has **no `body/` directory, on purpose**. The skill is authored upstream inside the notebooklm-py package and deployed by the package's own installer:

- **Canonical body:** `~/.claude/skills/notebooklm/SKILL.md` (plus `~/.agents/skills/notebooklm/SKILL.md`) — a copy written by `notebooklm skill install`, version-stamped to the installed package.
- **Update path:** unlike omarchy there is no auto-updater; after upgrading the package (`uv tool upgrade notebooklm-py`), rerun `notebooklm skill install` to refresh the deployed copy. The deployed file carries a `<!-- notebooklm-py vX.Y.Z -->` stamp to check against `notebooklm --version`.
- **Canon gate note:** the deployed file is upstream-derived output — never hand-edit it; the next `skill install` would silently revert the edit. Our own additions would be a new concept layered on top, or an upstream PR.
- **Per-machine:** the CLI is installed per machine (`uv tool install "notebooklm-py[browser]"`), so the deployed skill exists only where the tool does (installed on the Arch box, 2026-06-13). Auth is per machine too (`notebooklm login`, browser-based Google session).

## Provenance

- `raw/notebooklm-skill-upstream/` — immutable snapshot of the upstream SKILL.md (v0.7.1) with citation. Reference only; never deploy from it.
- Upstream: https://github.com/teng-lin/notebooklm-py (MIT). Uses undocumented Google APIs — may break without notice; not affiliated with Google.

## Tests

Reference concept with no runtime gates of ours; per the test gate only an accuracy check applies, and accuracy is upstream's responsibility. Verified 2026-06-13 that `notebooklm skill install` (v0.7.1) deployed the skill, the version stamp matches the installed CLI, and Claude Code picked the skill up.
