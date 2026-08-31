#!/usr/bin/env bash
# Display a concise desktop notification for a failed wiki runner unit.
#
# The failed unit name is passed by bc-wiki-notify@.service. Keep this helper
# independent of any machine-local notification library: a missing or failing
# notify-send must remain visible as a nonzero result.
set -Eeuo pipefail

usage() {
  printf 'Usage: %s FAILED_UNIT\n' "$0" >&2
  exit 2
}

[[ "$#" -eq 1 ]] || usage
failed_unit="$1"
[[ -n "$failed_unit" ]] || usage

if ! command -v notify-send >/dev/null 2>&1; then
  printf 'bc-wiki-notify: ERROR: notify-send is unavailable; cannot display failure for %s\n' \
    "$failed_unit" >&2
  exit 1
fi

syslog_identifier=''
if identifier_output="$(systemctl --user show -p SyslogIdentifier "$failed_unit" 2>/dev/null)"; then
  syslog_identifier="${identifier_output#SyslogIdentifier=}"
fi

vault_display='unavailable (could not read VAULT_ROOT from the failed unit)'
environment_output=''
if environment_output="$(systemctl --user show -p Environment "$failed_unit" 2>/dev/null)"; then
  environment_value="${environment_output#Environment=}"
  if [[ "$environment_value" =~ (^|[[:space:]])VAULT_ROOT=([^[:space:]]*) ]]; then
    vault_root="${BASH_REMATCH[2]}"
    if [[ -n "$vault_root" ]]; then
      vault_display="$vault_root"
    else
      vault_display='unavailable (VAULT_ROOT is empty on the failed unit)'
    fi
  elif [[ "$environment_value" =~ (^|[[:space:]])VAULT_LIST=([^[:space:]]+) ]]; then
    # A list-driven unit has no single vault by design. Without this the notification
    # reads like a notifier fault; the runner names the failing vaults in the journal.
    vault_display="batch over ${BASH_REMATCH[2]} (see reason for failing vaults)"
  fi
else
  vault_display='unavailable (could not inspect the failed unit environment)'
fi

# No priority filter: systemd logs unit stderr at notice, not err, so filtering on
# err..emerg silently matches nothing. Scope by SyslogIdentifier to drop systemd's own
# lifecycle lines, then fall back unscoped so a unit killed before printing still reports.
read_journal() {
  if [[ -n "$syslog_identifier" ]]; then
    journal_output="$(journalctl --user -u "$failed_unit" -t "$syslog_identifier" -n 5 --no-pager -o cat 2>/dev/null)" || return 1
    [[ "$journal_output" =~ [^[:space:]] ]] && return 0
  fi
  journal_output="$(journalctl --user -u "$failed_unit" -n 5 --no-pager -o cat 2>/dev/null)" || return 1
  return 0
}

reason='unavailable (could not read the user journal)'
journal_output=''
if command -v journalctl >/dev/null 2>&1; then
  if read_journal; then
    if [[ "$journal_output" =~ [^[:space:]] ]]; then
      reason="${journal_output//$'\n'/; }"
      reason="${reason//$'\r'/}"
      reason="${reason//$'\t'/ }"
      reason="${reason#"${reason%%[![:space:]]*}"}"
      reason="${reason%"${reason##*[![:space:]]}"}"
      if (( ${#reason} > 500 )); then
        reason="${reason:0:497}..."
      fi
    else
      reason='no error output found in the user journal'
    fi
  else
    reason='unavailable (journalctl could not read the user journal)'
  fi
else
  reason='unavailable (journalctl is not installed)'
fi

title="bc-wiki runner failed: $failed_unit"
body=$'Vault: '"$vault_display"$'\nReason: '"$reason"
if ! notify-send --urgency=critical --app-name=bc-wiki-maintain "$title" "$body"; then
  printf 'bc-wiki-notify: ERROR: notify-send could not display failure for %s\n' \
    "$failed_unit" >&2
  exit 1
fi

printf 'bc-wiki-notify: displayed failure for %s\n' "$failed_unit"
