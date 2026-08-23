#!/usr/bin/env bash
# Run the read-only wiki detector for every vault in a configured list.
#
# This runner never invokes an agent, writes Git state, or commits. It continues
# after a vault-level failure so one broken vault cannot hide the remaining reports.
set -Eeuo pipefail

fail() {
  printf 'bc-wiki-lint: ERROR: %s\n' "$*" >&2
  exit 1
}

AGENT_CONCEPTS="${AGENT_CONCEPTS:-}"
VAULT_LIST="${VAULT_LIST:-}"

[[ -n "$AGENT_CONCEPTS" ]] || fail 'AGENT_CONCEPTS is not set'
[[ -n "$VAULT_LIST" ]] || fail 'VAULT_LIST is not set'
[[ -f "$VAULT_LIST" ]] || fail "vault list does not exist: $VAULT_LIST"
[[ -r "$VAULT_LIST" ]] || fail "vault list is not readable: $VAULT_LIST"
command -v python3 >/dev/null 2>&1 || fail 'python3 is not installed or not on PATH'

DETECTION_SCRIPT="$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/wiki_lint.py"
[[ -f "$DETECTION_SCRIPT" ]] || fail "detection script does not exist: $DETECTION_SCRIPT"
[[ -r "$DETECTION_SCRIPT" ]] || fail "detection script is not readable: $DETECTION_SCRIPT"

declare -a vaults=()
while IFS= read -r line || [[ -n "$line" ]]; do
  # Accept files created on Windows and ignore surrounding whitespace around entries.
  line="${line%$'\r'}"
  line="${line#"${line%%[![:space:]]*}"}"
  line="${line%"${line##*[![:space:]]}"}"
  [[ -z "$line" || "$line" == \#* ]] && continue

  case "$line" in
    "~") vaults+=("$HOME") ;;
    "~/"*) vaults+=("$HOME/${line#\~/}") ;;
    *) vaults+=("$line") ;;
  esac
done < "$VAULT_LIST"

((${#vaults[@]} > 0)) || fail "vault list contains no vault paths: $VAULT_LIST"

failures=0
ran=0
for vault in "${vaults[@]}"; do
  printf '\n=== wiki lint: %s ===\n' "$vault"
  if [[ ! -d "$vault" ]]; then
    printf 'bc-wiki-lint: ERROR: vault is not a directory: %s\n' "$vault" >&2
    failures=$((failures + 1))
    continue
  fi

  ran=$((ran + 1))
  # wiki_lint.py returns nonzero for broken/ambiguous links. Its advisory findings
  # (orphans, missing index, stale references, and log backlog) remain non-fatal.
  if python3 "$DETECTION_SCRIPT" "$vault"; then
    printf 'bc-wiki-lint: PASS: detector completed for %s\n' "$vault"
  else
    status=$?
    printf 'bc-wiki-lint: ERROR: detector failed for %s (exit %s)\n' "$vault" "$status" >&2
    failures=$((failures + 1))
  fi
done

printf '\nbc-wiki-lint: checked %s vault(s), failures=%s\n' "$ran" "$failures"
if ((failures > 0)); then
  exit 1
fi
exit 0
