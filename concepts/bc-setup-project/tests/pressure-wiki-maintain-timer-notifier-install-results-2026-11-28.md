# Results: timer install includes the failure notifier, 2026-11-28

**Result: PASS.** The bash block of `concepts/bc-wiki-maintain/body/INSTALL-TIMER.md` (work item `065-timer-install-includes-notifier`), run as written in the timer pressure sandbox, installs `bc-wiki-notify@.service` beside the slug units, and `systemd-analyze --user verify` accepts all three.

Consumer: none. This checks the install recipe itself, so the block was extracted from the file and executed by a script, not by an agent; the gate wording is covered by the existing [timer results](pressure-wiki-maintain-timer-results-terra-2026-11-28.md), which this change does not touch.

Sandbox (the recipe of the timer pressure scenario, reduced to what a scripted run needs): scratch `mktemp -d` as `HOME`, so `unit_dir="$HOME/.config/systemd/user"` resolved inside scratch; the real `~/.config` bound read-only with `bwrap`; scratch `XDG_RUNTIME_DIR`; `systemctl` shimmed to log and do nothing; `wiki_skill_dir` a `cp -rL` copy of the worktree's `bc-wiki-maintain` body at `$HOME/.agents/skills/bc-wiki-maintain`. Only the substitutions the file asks for were made: `slug=demo-proj`, the vault path, and the placeholder edits (WorkingDirectory, VAULT_ROOT, SyslogIdentifier, timer `Unit=`) by `sed`.

Observed:

- Unit folder after the run: `bc-wiki-notify@.service`, `bc-wiki-maintain-demo-proj.service`, `bc-wiki-maintain-demo-proj.timer`. The notifier copy is byte-identical to `runner/bc-wiki-notify@.service` (sha256 `ecf23974…1d86d`); its `ExecStart=%h/.agents/skills/bc-wiki-maintain/runner/notify-failure.sh %i` matches the installed-skill path, so it needed no edit.
- `systemd-analyze --user verify` exited 0 with no output for the notifier template, the service and the timer.
- Shim log: `daemon-reload`, `enable --now bc-wiki-maintain-demo-proj.timer`, `status` — nothing reached the real user manager.
- Real `~/.config/systemd/user`: no file newer than the run's start.

First attempt note: without `XDG_RUNTIME_DIR` set, `systemd-analyze --user verify` fails with "Failed to lookup RuntimeDirectory path"; that is the sandbox's empty environment, not the recipe. A normal user session sets it.

Not covered: the agent confirm path (the user says yes to the shown units and an agent runs the install) was not exercised; the lint-all and all-vault installs in `runner/README.md` keep their own unit commands.
