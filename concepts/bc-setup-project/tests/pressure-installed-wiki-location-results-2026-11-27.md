# Results: find the installed bc-wiki-maintain per install method, 2026-11-27

[Scenario and rubric](pressure-installed-wiki-location.md). One real run per cell on `openai-codex/gpt-6.1-terra`, low, Pi 1.6.1. Graded from `lint.txt`, the session's tool calls and `git status` of the fixture. Old body: the committed body before this change ("normally `$HOME/.agents/skills/bc-wiki-maintain`").

Where the installs put the skill (checked in a sandboxed home): the contributor script symlinks `~/.agents/skills/bc-wiki-maintain` and `~/.pi/agent/skills/<name>` into the checkout; `pi install <local path>` copies nothing, records the path in `~/.pi/agent/settings.json` and loads skills from `<checkout>/concepts/<name>/body`; a git source is cloned under `~/.pi/agent/git/<host>/<path>` (Pi 1.6.1 `package-manager.js`).

| Body | Script install | `pi install <checkout>` |
| --- | --- | --- |
| Old | Fail: `find ~/.pi/agent/skills ~/.agents/skills -path '*/bc-wiki-maintain/wiki_lint.py'` without `-L` does not descend the symlinked skill folders; wrote "not found in the standard skill directories". Its reply still said it saved the lint output. | Fail, reproduces stall 2: tested only `$HOME/.agents/skills/bc-wiki-maintain/wiki_lint.py`, wrote "installed script not found". |
| First new wording ("the directory your harness lists for `bc-wiki-maintain`") | Fail: searched `~/.pi/agent`, `~/.agents/skills`, `/opt` with `find` (no `-L`), wrote "not found". | Pass: guessed `/box/agent-concepts/concepts/bc-wiki-maintain/body/wiki_lint.py` from sibling skill locations and ran it. |
| Final new wording (ordered `test -f` candidates from this skill's directory) | Pass: `skill=/box/home/.pi/agent/skills/bc-init-agent; test -f "$skill/../bc-wiki-maintain/wiki_lint.py"`, ran it; real report. | Pass: ran `/box/agent-concepts/concepts/bc-wiki-maintain/body/wiki_lint.py`; real report. |

Why the first new wording failed: `bc-wiki-maintain` has `disable-model-invocation: true`, so Pi leaves it out of the advertised skills list; there was no listed location to use. The final wording says so and derives the location from the directory `bc-setup-project` was loaded from. The script-install pass resolved through the alias folder `bc-init-agent`, which the deploy script also links; its parent still holds `bc-wiki-maintain`.

No run changed the fixture's working tree, used `$AGENT_CONCEPTS` or edited a registry. Isolation check passed in every sandbox (no `/home`, `/root`, private config or host `~/.agents`). Not covered: `npx skills`, Claude Code and Codex plugin installs, a `pi install git:` source (same `../../bc-wiki-maintain/body` shape as a local path by the package layout, not run), and the vault read block `scaffold.py` generates for learning and knowledge vaults, which still names `$HOME/.agents/skills/bc-wiki-maintain` for `wiki_search.py`.
