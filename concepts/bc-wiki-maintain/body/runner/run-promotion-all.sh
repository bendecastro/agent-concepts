#!/usr/bin/env bash
# Run the additive wiki promotion pass for every vault in a configured list.
#
# Each vault is delegated to run-promotion.sh so its per-vault safety gates remain
# the single implementation of promotion policy.
set -Eeuo pipefail

fail() {
  printf 'bc-wiki-maintain-all: ERROR: %s\n' "$*" >&2
  exit 1
}

VAULT_LIST="${VAULT_LIST:-}"

[[ -n "$VAULT_LIST" ]] || fail 'VAULT_LIST is not set'
[[ -f "$VAULT_LIST" ]] || fail "vault list does not exist: $VAULT_LIST"
[[ -r "$VAULT_LIST" ]] || fail "vault list is not readable: $VAULT_LIST"

runner_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROMOTION_RUNNER="${PROMOTION_RUNNER:-$runner_dir/run-promotion.sh}"
[[ -f "$PROMOTION_RUNNER" ]] || fail "promotion runner does not exist: $PROMOTION_RUNNER"
[[ -r "$PROMOTION_RUNNER" ]] || fail "promotion runner is not readable: $PROMOTION_RUNNER"

# One unit covers every vault, so a hung agent run would consume the whole
# TimeoutStartSec budget and the vaults after it would never run. Per-vault units
# never had that exposure. Bounding each child keeps a hang to one vault.
#
# --kill-after is load-bearing, not defensive: plain `timeout` sends SIGTERM and then
# waits forever, so a child that traps or ignores it is not bounded at all. Measured
# against a SIGTERM-ignoring child, `timeout 1s` ran the full 60s.
PROMOTION_TIMEOUT="${PROMOTION_TIMEOUT:-30m}"
PROMOTION_KILL_AFTER="${PROMOTION_KILL_AFTER:-30s}"
# GNU timeout signals the child's whole process group; uutils timeout (Ubuntu 26.04's default
# `timeout`) signals only the direct child, so a timed-out agent's descendants keep running.
# Ubuntu ships GNU's as `gnutimeout`, so prefer that name when present.
timeout_bin=''
for candidate in gnutimeout timeout; do
  if command -v "$candidate" >/dev/null 2>&1; then
    timeout_bin="$candidate"
    break
  fi
done
[[ -n "$timeout_bin" ]] || fail 'timeout is not installed or not on PATH'
[[ "$("$timeout_bin" --version 2>/dev/null || true)" == *'GNU coreutils'* ]] \
  || fail "GNU timeout is required: $timeout_bin is not GNU coreutils, and a non-GNU timeout leaves descendants of a timed-out vault running; install GNU coreutils (on Ubuntu: the gnu-coreutils package, which provides gnutimeout)"

declare -a vaults=()
while IFS= read -r line || [[ -n "$line" ]]; do
  # Accept files created on Windows and ignore surrounding whitespace around entries.
  line="${line%$'\r'}"
  line="${line#"${line%%[![:space:]]*}"}"
  line="${line%"${line##*[![:space:]]}"}"
  [[ -z "$line" || "$line" == \#* ]] && continue

  case "$line" in
    "~") vaults+=("$HOME") ;;
    \~/*) vaults+=("$HOME/${line#\~/}") ;;
    *) vaults+=("$line") ;;
  esac
done < "$VAULT_LIST"

((${#vaults[@]} > 0)) || fail "vault list contains no vault paths: $VAULT_LIST"

failures=0
checked=0
declare -a failed_vaults=()
for vault in "${vaults[@]}"; do
  checked=$((checked + 1))
  printf '\n=== wiki promotion: %s ===\n' "$vault"
  if [[ ! -d "$vault" ]]; then
    printf 'bc-wiki-maintain-all: ERROR: vault is not a directory: %s\n' "$vault" >&2
    failures=$((failures + 1))
    failed_vaults+=("$vault")
    continue
  fi

  # The assignment is exported only to this child; PI_BIN is inherited.
  if VAULT_ROOT="$vault" "$timeout_bin" --kill-after="$PROMOTION_KILL_AFTER" "$PROMOTION_TIMEOUT" "$PROMOTION_RUNNER"; then
    printf 'bc-wiki-maintain-all: PASS: promotion completed for %s\n' "$vault"
  else
    status=$?
    # 124 is a child that honoured SIGTERM; 137 is one that had to be SIGKILLed.
    if ((status == 124 || status == 137)); then
      printf 'bc-wiki-maintain-all: ERROR: promotion timed out after %s for %s\n' "$PROMOTION_TIMEOUT" "$vault" >&2
      # A timeout can land mid-write, and run-promotion.sh refuses a dirty tree, so this
      # vault fails closed every night until a human clears it. Say so where it is seen.
      printf 'bc-wiki-maintain-all: %s may now have uncommitted changes; review and clear it before the next run\n' "$vault" >&2
    else
      printf 'bc-wiki-maintain-all: ERROR: promotion failed for %s (exit %s)\n' "$vault" "$status" >&2
    fi
    failures=$((failures + 1))
    failed_vaults+=("$vault")
  fi
done

printf '\nbc-wiki-maintain-all: checked %s vault(s), failures=%s\n' "$checked" "$failures"
if ((failures > 0)); then
  printf 'bc-wiki-maintain-all: failing vaults:\n'
  printf '%s\n' "${failed_vaults[@]}"
  exit 1
fi
printf 'bc-wiki-maintain-all: failing vaults: (none)\n'
exit 0
