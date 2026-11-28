# Install a per-vault promotion timer

This is the procedure for installing the `bc-wiki-maintain` promotion timer for one classic
learning or knowledge vault. `bc-setup-project` loads it when it offers the timer; the caller
decides whether to offer. `$wiki_skill_dir` is the installed `bc-wiki-maintain` directory (the
one holding `wiki_lint.py` and `runner/`). Placeholder details, the wrapper contract, run checks
and removal are in [runner/README.md](runner/README.md).

Capture into `.bc-agent/log.md` is cheap; promotion is not. Without a per-vault user
timer, the new wiki will not promote overnight. This is not qmd:
`bc-qmd-refresh.timer` only refreshes search indexes. `/bc-wiki-maintain`
is the maintenance skill; its systemd templates
(`$wiki_skill_dir/runner/`) do not install,
enable, or start themselves.

Show the user the exact slug-suffixed unit names and env, then **offer to
install** after they confirm.
Never copy, enable, or start units without confirmation. Never write the
unsuffixed `bc-wiki-maintain.service` — that name may already bind another
vault. Never vendor runner scripts into the project.

If `systemctl --user` is unavailable, skip install and append a
TODO in the vault parking lot pointing at `$wiki_skill_dir/runner/README.md`.

On confirm, copy — do not symlink — the templates to slug-suffixed
names, edit the placeholders from the runner README (WorkingDirectory,
VAULT_ROOT, PI_BIN, SyslogIdentifier, ExecStart for a non-default skill directory, the timer's
`Unit=`), stagger `OnCalendar` at least 15 minutes away from any
existing `bc-wiki-maintain*.timer`, then reload and enable:

```bash
unit_dir="$HOME/.config/systemd/user"
slug="<slug>"
vault="<repo-root>/.bc-agent"
install -Dm644 "$wiki_skill_dir/runner/bc-wiki-maintain.service" \
  "$unit_dir/bc-wiki-maintain-${slug}.service"
install -Dm644 "$wiki_skill_dir/runner/bc-wiki-maintain.timer" \
  "$unit_dir/bc-wiki-maintain-${slug}.timer"
# edit placeholders, then:
systemd-analyze --user verify "$unit_dir/bc-wiki-maintain-${slug}.service"
systemd-analyze --user verify "$unit_dir/bc-wiki-maintain-${slug}.timer"
systemctl --user daemon-reload
systemctl --user enable --now "bc-wiki-maintain-${slug}.timer"
systemctl --user status "bc-wiki-maintain-${slug}.timer"
```

Resolve `PI_BIN` with `command -v pi` falling back to `$HOME/.local/bin/pi`.
If a matching slug-suffixed unit already exists for this `VAULT_ROOT`, report it and skip.
On decline, append the same TODO as the no-systemd case.
