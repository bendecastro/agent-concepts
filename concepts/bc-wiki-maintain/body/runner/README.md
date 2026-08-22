# Scheduled runner

This directory contains a **user-scope** systemd timer for the CV pilot. It is a
reviewable template: these files do not install, enable, or start anything.

The timer runs `bc-wiki-maintain.service` daily at 03:30 local time, with a random
15-minute delay. The service is `Type=oneshot`, writes stdout/stderr to the journal,
and fails visibly when detection, the agent, or the dedicated commit fails. systemd
is intentional here: `journalctl --user` and `systemctl --user status` make silent
scheduler failures observable.

## Install after review

Set `AGENT_CONCEPTS` to the checkout that contains this concept, then copy the units
and wrapper to the user systemd directory. Do not copy the wrapper alone: the service
uses the canonical concept path and the detection/skill files beside it.

```bash
export AGENT_CONCEPTS="$HOME/Sync/Work/PUBLIC/Agents"  # adjust to this checkout
unit_dir="$HOME/.config/systemd/user"
install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-maintain.service" \
  "$unit_dir/bc-wiki-maintain.service"
install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-maintain.timer" \
  "$unit_dir/bc-wiki-maintain.timer"
systemctl --user daemon-reload
systemctl --user enable --now bc-wiki-maintain.timer
```

The supplied unit uses `%h` (the systemd user home specifier) and the pilot paths:

- `AGENT_CONCEPTS=%h/Sync/Work/PUBLIC/Agents`
- `VAULT_ROOT=%h/Sync/Work/CV/.bc-agent`
- `PI_BIN=%h/.local/bin/pi`

If the checkout or Pi binary is elsewhere, edit the copied service before
`daemon-reload` (or use a user drop-in). Keep `VAULT_ROOT` pointed at the CV pilot;
the wrapper requires it as an explicit environment value and never guesses another
vault.

## What the wrapper requires

`run-promotion.sh` is parameterized through these environment variables:

- `VAULT_ROOT` — the project-local vault to inspect. The pilot service sets this to
  `%h/Sync/Work/CV/.bc-agent`.
- `AGENT_CONCEPTS` — canonical concepts checkout; used to locate `wiki_lint.py` and
  `SKILL.md`.
- `PI_BIN` — optional Pi executable/path; defaults to `pi` when run manually.
- `DETECTION_SCRIPT` — optional override for the detection script.
- `PROMOTION_SKILL` — optional override for the loaded skill file.

The detection script receives the vault root as its sole positional argument and must
emit one anchored machine-readable line:

```text
PROMOTION_REQUIRED=0
```

or:

```text
PROMOTION_REQUIRED=1
```

It may emit a human-readable report around that line. A missing or malformed result
fails closed. `PROMOTION_REQUIRED=0` exits before Pi is checked or invoked. The parent
integration must preserve this contract when wiring the detection script.

Before detection, and again before promotion, the wrapper requires a clean Git
worktree. It also checks that the promotion agent did not commit unexpectedly, touched
files outside the vault, or deleted an existing file. The wrapper owns the dedicated
commit; a failed safety check leaves changes uncommitted for inspection rather than
resetting them.

The verified headless command is Pi 0.84.2 with the installed Luna model:

```bash
pi --print --no-session --approve \
  --model openai-codex/gpt-5.6-luna:max --thinking max \
  --skill "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/SKILL.md" \
  "<promotion prompt>"
```

A no-tools probe of this exact model/flag combination returned status 0 on this
machine. The real runner keeps tools enabled because the agent must read and edit the
vault; it passes additive-only, contradiction, and no-commit rules in the prompt and
then performs the commit itself.

## Check a run

```bash
systemctl --user status bc-wiki-maintain.timer
systemctl --user status bc-wiki-maintain.service
journalctl --user -u bc-wiki-maintain.service --since today
```

A successful promotion ends with a dedicated commit. Review it before relying on the
new pages:

```bash
cd "$HOME/Sync/Work/CV"
git show --stat --oneline HEAD
git show HEAD -- .bc-agent/
```

Undo a bad promotion with Git's normal reversible operation:

```bash
git revert HEAD
```

## Disable

Stop and disable the timer without deleting the units:

```bash
systemctl --user disable --now bc-wiki-maintain.timer
```

To remove the installed units after disabling:

```bash
rm -f "$HOME/.config/systemd/user/bc-wiki-maintain.service" \
      "$HOME/.config/systemd/user/bc-wiki-maintain.timer"
systemctl --user daemon-reload
```
