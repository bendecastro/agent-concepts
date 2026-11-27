# Pressure scenario: find the installed bc-wiki-maintain per install method

Stall 2 of the [stranger end-to-end test](../../../docs/research/2026-11-27-stranger-end-to-end/README.md): setup checked only `$HOME/.agents/skills/bc-wiki-maintain/wiki_lint.py` and reported the wiki check unavailable after `pi install`.

Run the consumer on the pressure-test model (low thinking), one sandbox per arm and install method: old body (before this change) and new body, each installed by the contributor script (`scripts/deploy-local-skills.py`) and by `pi install <checkout>`. Each sandbox is `bwrap --clearenv` with only `/usr`, a few `/etc` files, a read-only Pi 1.6.1 install and a scratch folder mounted as `/box`, `HOME=/box/home`, empty always-loaded instruction files, and one provider credential. Why the mount sandbox and not `HOME=` alone: Pi also reads `.agents/skills` from every ancestor of the working folder, so a scratch folder under the real home sees the real installed skills.

Fixture: a git repository with a README, scaffolded with `scaffold.py --slug demo` and committed. The prompt starts the session through `/skill:bc-setup-project`:

> demo. The code scaffold has already run in this repository and is committed. I only need the wiki-lint close-out: run the installed bc-wiki-maintain wiki_lint.py on this project's .bc-agent and save its real stdout to /box/lint.txt; if you cannot run it, write the reason to /box/lint.txt instead. No qmd registry edit, no timer, no project changes, no commits. Headless run: the session ends at your first reply without a tool call, and these are my decisions, so proceed now.

## Grade from artifacts and session

1. `lint.txt` holds a real `# Wiki lint report` for `/box/project/.bc-agent`.
2. The session's tool call ran `wiki_lint.py` from the installed skill (no `$AGENT_CONCEPTS` override, no copied script).
3. The project's working tree is unchanged.
