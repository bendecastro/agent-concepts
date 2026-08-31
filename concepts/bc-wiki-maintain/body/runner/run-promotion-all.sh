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

AGENT_CONCEPTS="${AGENT_CONCEPTS:-}"
VAULT_LIST="${VAULT_LIST:-}"

[[ -n "$AGENT_CONCEPTS" ]] || fail 'AGENT_CONCEPTS is not set'
[[ -n "$VAULT_LIST" ]] || fail 'VAULT_LIST is not set'
[[ -f "$VAULT_LIST" ]] || fail "vault list does not exist: $VAULT_LIST"
[[ -r "$VAULT_LIST" ]] || fail "vault list is not readable: $VAULT_LIST"

PROMOTION_RUNNER="${PROMOTION_RUNNER:-$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/runner/run-promotion.sh}"
[[ -f "$PROMOTION_RUNNER" ]] || fail "promotion runner does not exist: $PROMOTION_RUNNER"
[[ -r "$PROMOTION_RUNNER" ]] || fail "promotion runner is not readable: $PROMOTION_RUNNER"

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

  # The assignment is exported only to this child; AGENT_CONCEPTS and PI_BIN are inherited.
  if VAULT_ROOT="$vault" "$PROMOTION_RUNNER"; then
    printf 'bc-wiki-maintain-all: PASS: promotion completed for %s\n' "$vault"
  else
    status=$?
    printf 'bc-wiki-maintain-all: ERROR: promotion failed for %s (exit %s)\n' "$vault" "$status" >&2
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
