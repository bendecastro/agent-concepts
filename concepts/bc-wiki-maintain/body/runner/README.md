# Scheduled runner

This directory contains a **user-scope** systemd timer template for one vault. It is a
reviewable template: these files do not install, enable, or start anything.

The timer runs `bc-wiki-maintain.service` daily at 03:30 local time, with a random
15-minute delay. The service is `Type=oneshot`, writes stdout/stderr to the journal,
and fails visibly when detection, the agent, or the dedicated commit fails. systemd
is intentional here: `journalctl --user` and `systemctl --user status` make silent
scheduler failures observable.

## Failure notifications

Both runner services set `OnFailure=bc-wiki-notify@%n.service`. When either service exits
nonzero, systemd starts the `bc-wiki-notify@.service` template with the failed unit name as
`%i`. The runner-local `notify-failure.sh` resolves that unit's `VAULT_ROOT`, reads a short
error from its user journal, and sends a critical desktop notification with `notify-send`.
If the vault or journal cannot be inspected, the message says so; if `notify-send` is missing
or fails, the notifier exits nonzero instead of silently succeeding.

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
