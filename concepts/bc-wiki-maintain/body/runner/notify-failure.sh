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
  fi
else
  vault_display='unavailable (could not inspect the failed unit environment)'
fi

reason='unavailable (could not read the user journal)'
journal_output=''
if command -v journalctl >/dev/null 2>&1; then
  if journal_output="$(journalctl --user -u "$failed_unit" -p err..emerg -n 5 --no-pager -o cat 2>/dev/null)"; then
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
