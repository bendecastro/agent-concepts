# Scheduled runner

This directory contains a **user-scope** systemd timer template for one vault. It is a
reviewable template: these files do not install, enable, or start anything.

The timer runs `bc-wiki-maintain.service` daily at 03:30 local time, with a random
15-minute delay. The service is `Type=oneshot`, writes stdout/stderr to the journal,
and fails visibly when detection, the agent, or the dedicated commit fails. systemd
is intentional here: `journalctl --user` and `systemctl --user status` make silent
scheduler failures observable.

## Failure notifications

All runner services set `OnFailure=bc-wiki-notify@%n.service`. When any service exits nonzero,
systemd starts the `bc-wiki-notify@.service` template with the failed unit name as `%i`. The
runner-local `notify-failure.sh` resolves that unit's `VAULT_ROOT` when it has one, or its
`VAULT_LIST` for the list-driven service, reads a short error from its user journal, and sends a
critical desktop notification with `notify-send`. If the vault/list or journal cannot be inspected,
the message says so; if `notify-send` is missing or fails, the notifier exits nonzero instead of
silently succeeding.

A healthy no-op does not fire the notifier: the promotion runner exits 0 for
`PROMOTION_REQUIRED=0` before invoking Pi, and the lint runner exits 0 when all detectors pass.
The notifier is only a failure path; it does not replace the journal or `systemctl --user`
status checks.

Install the notifier template alongside whichever runner service(s) you use, after editing its
`AGENT_CONCEPTS` placeholder:

```bash
export AGENT_CONCEPTS="$HOME/path/to/agent-concepts"
unit_dir="$HOME/.config/systemd/user"
install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-notify@.service" \
  "$unit_dir/bc-wiki-notify@.service"
$EDITOR "$unit_dir/bc-wiki-notify@.service"  # set AGENT_CONCEPTS
systemd-analyze --user verify "$unit_dir/bc-wiki-notify@.service"
```

Copy the notifier template, the matching runner service, and its timer before running
`systemctl --user daemon-reload`. Do not symlink the templates: the copied unit's
`AGENT_CONCEPTS` value must point at the checkout containing this runner.

## Lint all configured vaults (detection only)

The separate `bc-wiki-lint.service` runs `run-lint.sh` against a list of vault roots. It is
**detection only**: it never invokes Pi or another agent, edits files, writes Git state, or
commits. Each vault gets a human-readable header and the normal `wiki_lint.py` report. The
runner continues after a missing vault or detector failure so one bad path cannot hide the other
reports, then exits nonzero if any path failed. Orphans, missing index entries, stale references,
and unpromoted-log findings are advisory; only a detector nonzero result (currently broken or
ambiguous links) fails the overall run.

The list file contains one path per line. Blank lines and lines beginning with `#` are ignored;
leading `~` and `~/` expand to `$HOME`. Use absolute paths or paths whose meaning is stable from
the service working directory:

```text
# Project vaults to inspect
~/path/to/project-a/.bc-agent
~/path/to/project-b/.agent
/absolute/path/to/project-c/agent/wiki
```

Install the lint-only timer after editing the copied service's two placeholders:

```bash
export AGENT_CONCEPTS="$HOME/path/to/agent-concepts"
unit_dir="$HOME/.config/systemd/user"
list_file="$HOME/.config/agent-concepts/wiki-lint-vaults.txt"
mkdir -p "$(dirname "$list_file")"
$EDITOR "$list_file"
install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-lint.service" \
  "$unit_dir/bc-wiki-lint.service"
install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-lint.timer" \
  "$unit_dir/bc-wiki-lint.timer"
$EDITOR "$unit_dir/bc-wiki-lint.service"  # set AGENT_CONCEPTS and VAULT_LIST
systemd-analyze --user verify "$unit_dir/bc-wiki-lint.service"
systemd-analyze --user verify "$unit_dir/bc-wiki-lint.timer"
systemctl --user daemon-reload
systemctl --user enable --now bc-wiki-lint.timer
```

The lint timer is scheduled at 04:15 with a 15-minute random delay, separate from the
promotion timer's 03:30 schedule. Check it with:

```bash
systemctl --user status bc-wiki-lint.timer
systemctl --user status bc-wiki-lint.service
journalctl --user -u bc-wiki-lint.service --since today
```

The journal shows one `=== wiki lint: ... ===` section per configured path and a final failure
count. A successful service means every listed directory ran the detector and every detector
returned zero; it does **not** mean the vaults have no advisory findings. To run the same check
manually without installing a timer:

```bash
export AGENT_CONCEPTS="$HOME/path/to/agent-concepts"
export VAULT_LIST="$HOME/.config/agent-concepts/wiki-lint-vaults.txt"
"$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/run-lint.sh"
```

To disable only the lint-all timer:

```bash
systemctl --user disable --now bc-wiki-lint.timer
```

The lint-all runner is intentionally separate from the one-vault promotion runner below.

## Promote all configured vaults (list-driven alternative)

`run-promotion-all.sh` reads a configured `VAULT_LIST`, prints one header per entry, and invokes
`run-promotion.sh` once for each directory. The child runner retains every
per-vault safety check and commit rule. A missing directory or failed child is reported and does
not stop later vaults; the all-vault runner exits nonzero when any vault fails and its final
summary lists each failing path on its own line.

Each child runs under `timeout --kill-after`, defaulting to 30 minutes with a 30-second grace
period, overridable with `PROMOTION_TIMEOUT` and `PROMOTION_KILL_AFTER`. One unit covers every
vault, so an agent that hangs would otherwise consume the whole `TimeoutStartSec` budget and the
vaults after it would never run — an exposure the one-vault units never had. `--kill-after` is
load-bearing rather than defensive: plain `timeout` sends SIGTERM and then waits indefinitely, so
a child that traps or ignores it is not bounded at all.

A timed-out vault is reported as a failure and the batch continues, but **it is not self-healing**.
The timeout can land mid-write, and `run-promotion.sh` refuses to start on a dirty tree, so that
vault fails closed on every subsequent run until a human inspects it and either commits or resets
the leftover changes. The runner says so on stderr when it times a vault out.

Use a separate list from `wiki-lint-vaults.txt`. Lint only reads vaults, while promotion invokes
an agent that writes and commits, so adding a vault to the lint list must not silently authorise a
scheduled write. The promotion list is machine-local and uses the same syntax as the lint list:

```text
# Vaults explicitly authorised for scheduled promotion
~/path/to/project-a/.bc-agent
~/path/to/project-b/.bc-agent
/absolute/path/to/project-c/agent/wiki
```

This list-driven timer is an **alternative** to the one-vault promotion timers, not an addition
to them. Disable the per-vault promotion timers before enabling this timer, so a vault cannot be
processed concurrently by two agents.

Install the all-vault timer after review; this only copies templates and does not install anything
by itself:

```bash
export AGENT_CONCEPTS="$HOME/path/to/agent-concepts"
unit_dir="$HOME/.config/systemd/user"
list_file="$HOME/.config/agent-concepts/wiki-promotion-vaults.txt"
mkdir -p "$(dirname "$list_file")"
$EDITOR "$list_file"
install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-maintain-all.service" \
  "$unit_dir/bc-wiki-maintain-all.service"
install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-maintain-all.timer" \
  "$unit_dir/bc-wiki-maintain-all.timer"
install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-notify@.service" \
  "$unit_dir/bc-wiki-notify@.service"
$EDITOR "$unit_dir/bc-wiki-maintain-all.service"  # set AGENT_CONCEPTS, VAULT_LIST, and PI_BIN
$EDITOR "$unit_dir/bc-wiki-notify@.service"       # set AGENT_CONCEPTS
systemd-analyze --user verify "$unit_dir/bc-wiki-maintain-all.service"
systemd-analyze --user verify "$unit_dir/bc-wiki-maintain-all.timer"
systemd-analyze --user verify "$unit_dir/bc-wiki-notify@.service"
# Disable every installed bc-wiki-maintain-*.timer for the one-vault alternative first.
systemctl --user daemon-reload
systemctl --user enable --now bc-wiki-maintain-all.timer
```

Check the all-vault run and its per-vault failure summary with:

```bash
systemctl --user status bc-wiki-maintain-all.timer
systemctl --user status bc-wiki-maintain-all.service
journalctl --user -u bc-wiki-maintain-all.service --since today
```

The all-vault service has no single `VAULT_ROOT`; when it fails, the runner's final journal
summary names every failed vault path so the notifier's short excerpt remains actionable.

Disable the list-driven timer without deleting its copied units:

```bash
systemctl --user disable --now bc-wiki-maintain-all.timer
```

## Migrate from per-vault promotion timers to the batch timer

This is a one-time machine-local migration. The batch timer is an alternative to the per-vault
promotion timers, not an additional schedule. Keep `bc-wiki-lint.timer` enabled: it is
read-only detection and is independent of promotion.

### Why the old promotion timers must be disabled first

The batch template runs at 02:30 with a 15-minute random delay and allows up to five hours for
serial vault runs. The one-vault template runs at 03:30 with the same delay. Those windows overlap.
Nothing mechanically prevents two agents from processing the same vault: `run-promotion.sh`'s
clean-tree check is a time-of-check/time-of-use check, not a lock, and a PID lock is deliberately
not part of this design. Disable every per-vault promotion timer before enabling the batch timer.

### Ordered migration

Set the checkout and unit/list locations first. These are placeholders; use the values appropriate
for the machine where the templates will be installed.

```bash
export AGENT_CONCEPTS="$HOME/path/to/agent-concepts"
unit_dir="$HOME/.config/systemd/user"
list_file="$HOME/.config/agent-concepts/wiki-promotion-vaults.txt"
```

1. **Enumerate before disabling.** Do not assume the four names from one installation. List every
   installed timer whose unit name uses the promotion prefix:

   ```bash
   systemctl --user list-unit-files 'bc-wiki-maintain*.timer' --no-legend --no-pager
   ```

   One installation had `bc-wiki-maintain.timer`,
   `bc-wiki-maintain-imagemaze.timer`, `bc-wiki-maintain-homeflix.timer`, and
   `bc-wiki-maintain-homeflix-prod.timer`, alongside `bc-wiki-lint.timer`. That is an example,
   not a portable inventory. The batch unit, if already present, is named
   `bc-wiki-maintain-all.timer`; do not disable it as part of this step. Do not disable or pass
   `bc-wiki-lint.timer` to the command below.

2. **Disable the per-vault promotion timers.** The filter excludes the batch unit while retaining
   the base unit and any slug-suffixed per-vault units found on this machine. It prints the selected
   names before changing state:

   ```bash
   mapfile -t per_vault_timers < <(
     systemctl --user list-unit-files 'bc-wiki-maintain*.timer' --no-legend --no-pager |
       awk '$1 ~ /^bc-wiki-maintain(-[^.]*)?\.timer$/ && $1 != "bc-wiki-maintain-all.timer" { print $1 }'
   )
   ((${#per_vault_timers[@]} > 0)) || {
     printf 'No per-vault promotion timers found; stop and inspect the inventory.\n' >&2
     exit 1
   }
   printf 'Disabling per-vault promotion timers:\n'
   printf '  %s\n' "${per_vault_timers[@]}"
   systemctl --user disable --now "${per_vault_timers[@]}"
   ```

   Disabling a timer prevents its next trigger; it does not imply that an already-running service
   has finished. Before enabling the batch, check for an active old promotion service and let it
   finish or stop its corresponding service deliberately:

   ```bash
   systemctl --user list-units --type=service --state=running 'bc-wiki-maintain*.service' --no-legend --no-pager
   ```

   Leave `bc-wiki-lint.timer` untouched. Check it separately if it was already enabled:

   ```bash
   systemctl --user is-enabled bc-wiki-lint.timer
   ```

3. **Create the separate promotion list.** Use the machine-local lint list as a source of
   candidate paths, but copy only the vaults you explicitly authorise for scheduled writes. Do not
   use `cp` to clone the lint list: lint reads, while promotion invokes an agent that writes and
   commits.

   ```bash
   mkdir -p "$(dirname "$list_file")"
   $EDITOR "$HOME/.config/agent-concepts/wiki-lint-vaults.txt"
   $EDITOR "$list_file"
   ```

   Put one approved vault root per line in `wiki-promotion-vaults.txt`; blank lines and `#`
   comments are ignored, and `~`/`~/` entries are expanded by `run-promotion-all.sh`.

4. **Install and verify the batch units.** Copy the batch service, timer, and the notifier it
   references. Do not symlink the templates. Edit the copied service's `AGENT_CONCEPTS`,
   `VAULT_LIST`, and `PI_BIN` values, and edit the notifier's `AGENT_CONCEPTS` value.

   ```bash
   install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-maintain-all.service" \
     "$unit_dir/bc-wiki-maintain-all.service"
   install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-maintain-all.timer" \
     "$unit_dir/bc-wiki-maintain-all.timer"
   install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-notify@.service" \
     "$unit_dir/bc-wiki-notify@.service"
   $EDITOR "$unit_dir/bc-wiki-maintain-all.service"
   $EDITOR "$unit_dir/bc-wiki-notify@.service"
   systemd-analyze --user verify "$unit_dir/bc-wiki-maintain-all.service"
   systemd-analyze --user verify "$unit_dir/bc-wiki-maintain-all.timer"
   systemd-analyze --user verify "$unit_dir/bc-wiki-notify@.service"
   ```

5. **Enable the batch timer.** Only after the per-vault timers are disabled and the copied units
   verify successfully:

   ```bash
   systemctl --user daemon-reload
   systemctl --user enable --now bc-wiki-maintain-all.timer
   ```

6. **Confirm the resulting schedule and the untouched lint timer:**

   ```bash
   systemctl --user is-enabled bc-wiki-lint.timer
   systemctl --user status --no-pager bc-wiki-maintain-all.timer
   systemctl --user list-timers --all --no-pager
   ```

   The supplied batch timer is scheduled for 02:30 ±15 minutes and the supplied lint timer for
   04:15 ±15 minutes. A local unit copy may differ; trust the verified unit files and the timer
   listing on that machine.

### First-run supervised check

`run-promotion-all.sh` has no `--dry-run` flag. A first manual invocation is therefore a
**supervised one-shot**, not a read-only preview: it may invoke Pi and create one dedicated commit
per vault that has work. Set the same inputs as the copied service and run it before relying on the
schedule:

```bash
export AGENT_CONCEPTS="$HOME/path/to/agent-concepts"
export VAULT_LIST="$HOME/.config/agent-concepts/wiki-promotion-vaults.txt"
export PI_BIN="$HOME/.local/bin/pi"
"$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/run-promotion-all.sh"
```

A healthy run prints one `=== wiki promotion: ... ===` header per list entry, continues through
no-op or successful child runs, ends with `failures=0` and `failing vaults: (none)`, and exits 0.
A failed or missing vault is named in its per-vault error, later entries still run, the final
summary lists the failing paths, and the batch exits nonzero. A manual run does not trigger
systemd's `OnFailure=` notifier; inspect stderr and the final summary directly.

### Rollback to per-vault timers

Keep the batch and per-vault schedules mutually exclusive. To roll back, disable the batch timer,
restore or reinstall the copied one-vault service/timer pair for each desired vault using
[the one-vault install recipe below](#install-after-review), verify those copies, then re-enable
the per-vault timers:

```bash
systemctl --user disable --now bc-wiki-maintain-all.timer
# Restore/reinstall the per-vault copies using the one-vault recipe above, then reload them:
systemctl --user daemon-reload
# Enumerate the restored per-vault copies:
mapfile -t per_vault_timers < <(
  systemctl --user list-unit-files 'bc-wiki-maintain*.timer' --no-legend --no-pager |
    awk '$1 ~ /^bc-wiki-maintain(-[^.]*)?\.timer$/ && $1 != "bc-wiki-maintain-all.timer" { print $1 }'
)
((${#per_vault_timers[@]} > 0)) || {
  printf 'No restored per-vault promotion timers found; stop and inspect the unit files.\n' >&2
  exit 1
}
systemctl --user enable --now "${per_vault_timers[@]}"
systemctl --user is-enabled bc-wiki-lint.timer
```

Leave `bc-wiki-maintain-all.service` and `.timer` installed but disabled if a later migration is
likely, or remove those copied files only after the batch timer is disabled and the rollback is
confirmed. Do not disable the lint timer during rollback.

### Recover a vault that timed out

The batch runner prints that a timed-out vault **may now have uncommitted changes**. The timeout can
land mid-write; the next `run-promotion.sh` invocation refuses a dirty containing repository, so
the same vault fails closed on every later run until a human inspects it and either commits or
resets the leftover changes. The timeout's `--kill-after` bounds an uncooperative child, but it
does not undo partial writes.

Replace the example with the timed-out vault from the batch journal. These commands inspect the
whole containing repository because the per-vault runner requires the whole worktree to be clean:

```bash
vault="$HOME/path/to/your/project/.bc-agent"  # replace with the timed-out lint-list entry
repo_root="$(git -C "$vault" rev-parse --show-toplevel)"
vault_prefix="$(git -C "$vault" rev-parse --show-prefix)"
git -C "$repo_root" status --short --untracked-files=all
git -C "$repo_root" diff -- "$vault_prefix"
git -C "$repo_root" diff --cached -- "$vault_prefix"
git -C "$repo_root" ls-files --others --exclude-standard -- "$vault_prefix"
```

If the changes are the intended additive Markdown promotion, review the diff and stage only the
reviewed vault files. Confirm the staged path list before creating the recovery commit:

```bash
git -C "$repo_root" diff --check -- "$vault_prefix"
git -C "$repo_root" add -- "$vault_prefix"
git -C "$repo_root" diff --cached --name-status
git -C "$repo_root" commit -m "wiki: recover timed-out promotion"
git -C "$repo_root" status --short --untracked-files=all
```

If the partial changes are not wanted, restore tracked files and inspect untracked files before
removing them. The `git clean` preview is mandatory: remove only files you confirm were left by the
aborted promotion, never unrelated user work.

```bash
git -C "$repo_root" restore --source=HEAD --staged --worktree -- "$vault_prefix"
git -C "$repo_root" clean -nd -- "$vault_prefix"
# After reviewing the preview:
git -C "$repo_root" clean -fd -- "$vault_prefix"
git -C "$repo_root" status --short --untracked-files=all
```

The final status must be clean before the next scheduled run. If unrelated changes exist elsewhere
in the containing repository, resolve those separately; the promotion runner will continue to
refuse the vault until the complete worktree is clean.

## Install after review

Set `AGENT_CONCEPTS` to the checkout that contains this concept, then copy the units
and wrapper to the user systemd directory. Do not copy the wrapper alone: the service
uses the canonical concept path and the detection/skill files beside it.

```bash
export AGENT_CONCEPTS="$HOME/path/to/agent-concepts"  # your checkout of this workspace
unit_dir="$HOME/.config/systemd/user"
install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-maintain.service" \
  "$unit_dir/bc-wiki-maintain.service"
install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-maintain.timer" \
  "$unit_dir/bc-wiki-maintain.timer"
# Required: the service's OnFailure= points here. Without it a failed run notifies nobody.
install -Dm644 "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/bc-wiki-notify@.service" \
  "$unit_dir/bc-wiki-notify@.service"
$EDITOR "$unit_dir/bc-wiki-notify@.service"  # set AGENT_CONCEPTS
systemctl --user daemon-reload
systemctl --user enable --now bc-wiki-maintain.timer
```

To add another vault, copy the service and timer to a new name (`bc-wiki-maintain-other.service`
and matching `.timer`), edit `WorkingDirectory` / `VAULT_ROOT` / `SyslogIdentifier`, and give
the timer a different `OnCalendar` so two promotion agents do not start at once. The notifier
template is instanced per failed unit, so one copy of it serves every vault. One unit per
vault: a dirty tree in one project must not skip the others. The wrapper already accepts
`.bc-agent/`, `.agent/`, or any other vault subdirectory.

The supplied unit uses `%h` (the systemd user home specifier) and placeholder paths:

- `AGENT_CONCEPTS=%h/path/to/agent-concepts`
- `VAULT_ROOT=%h/path/to/your/project/.bc-agent`
- `PI_BIN=%h/.local/bin/pi`

If the checkout or Pi binary is elsewhere, edit the copied service before
`daemon-reload` (or use a user drop-in). Keep `VAULT_ROOT` pointed at one vault;
the wrapper requires it as an explicit environment value and never guesses another
vault.

## What the wrapper requires

`run-promotion.sh` is parameterized through these environment variables:

- `VAULT_ROOT` — the project-local vault to inspect. The pilot service sets this to
  `%h/path/to/your/project/.bc-agent`.
- `AGENT_CONCEPTS` — canonical concepts checkout; used to locate `wiki_lint.py` and
  `SKILL.md`.
- `PI_BIN` — optional Pi executable/path; defaults to `pi` when run manually.
- `DETECTION_SCRIPT` — optional override for the detection script.
- `PROMOTION_SKILL` — optional override for the loaded skill file.

The detection script receives the vault root as its sole positional argument and must
emit exactly one anchored pair of machine-readable lines, plus one `PROMOTION_HEADING`
line per unpromoted heading when promotion is required:

```text
PROMOTION_REQUIRED=0
PROMOTION_RANGE=none
```

or, when dated log headings need promotion:

```text
PROMOTION_REQUIRED=1
PROMOTION_RANGE=2026-08-10..2026-08-14
PROMOTION_HEADING	## [2026-08-10] first
PROMOTION_HEADING	## [2026-08-14] last
```

The range is computed from standard `## [YYYY-MM-DD] ...` headings: all log headings on
an initial pass, or headings added after the latest relevant dedicated promotion commit on later
passes. If any unpromoted heading is non-standard, the detector keeps promotion required and emits
`PROMOTION_RANGE=invalid`; the wrapper fails closed instead of guessing a range. It may emit a
human-readable report around the contract lines. Missing, duplicate, or malformed results fail closed.
`PROMOTION_REQUIRED=0` exits before Pi is checked or invoked.
The parent integration must preserve this contract when wiring the detection script.

Before detection, and again before promotion, the wrapper requires a clean Git
worktree. It also checks that the promotion agent did not commit unexpectedly, stage any
index changes, touch files outside the vault, or delete an existing file. If the agent
changed vault files, the wrapper refuses the dedicated commit unless
`wiki_lint.py --verify-classify` accepts a JSONL file covering every unpromoted heading, and
it refuses any new non-Markdown file left in the vault. That JSONL is a temp path exported as
`CLASSIFY_PATH`; it is not a vault page and is not committed. Its verdicts become the commit
body, so `git log -1` explains why each heading was promoted, skipped, or flagged. The file is
removed after a successful run and kept — with its path printed — after a failure. The wrapper
owns the dedicated commit and uses the detector's exact range; a failed safety check leaves
changes uncommitted for inspection rather than resetting them.

The verified headless command is Pi 0.84.2 with the installed Luna model:

```bash
pi --print --no-session --approve \
  --model openai-codex/gpt-5.6-luna:max --thinking max \
  --skill "$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/SKILL.md" \
  "<promotion prompt>"
```

A no-tools probe of this exact model/flag combination returned status 0 on this
machine. The real runner keeps tools enabled because the agent must read and edit the
vault; it passes additive-only, classify-every-heading, stale-vs-exclusive, and no-commit
rules in the prompt and then performs the commit itself.

## Check a run

```bash
systemctl --user status bc-wiki-maintain.timer
systemctl --user status bc-wiki-maintain.service
journalctl --user -u bc-wiki-maintain.service --since today
```

A successful promotion ends with a dedicated commit. Review it before relying on the
new pages:

```bash
cd "$HOME/path/to/your/project"
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
