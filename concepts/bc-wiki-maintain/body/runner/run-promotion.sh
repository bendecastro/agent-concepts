#!/usr/bin/env bash
# Run the additive wiki promotion pass for one configured vault.
#
# The systemd unit supplies VAULT_ROOT, AGENT_CONCEPTS, and PI_BIN. Keeping these
# as environment inputs makes the wrapper usable for a later pilot without baking
# a home directory into the executable.
set -Eeuo pipefail

log() {
  printf 'bc-wiki-maintain: %s\n' "$*"
}

fail() {
  printf 'bc-wiki-maintain: ERROR: %s\n' "$*" >&2
  exit 1
}

AGENT_CONCEPTS="${AGENT_CONCEPTS:-}"
VAULT_ROOT="${VAULT_ROOT:-}"
PI_BIN="${PI_BIN:-pi}"

[[ -n "$AGENT_CONCEPTS" ]] || fail 'AGENT_CONCEPTS is not set'
[[ -n "$VAULT_ROOT" ]] || fail 'VAULT_ROOT is not set'
[[ -d "$VAULT_ROOT" ]] || fail "vault does not exist: $VAULT_ROOT"
command -v git >/dev/null 2>&1 || fail 'git is not installed or not on PATH'
command -v python3 >/dev/null 2>&1 || fail 'python3 is not installed or not on PATH'

DETECTION_SCRIPT="${DETECTION_SCRIPT:-$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/wiki_lint.py}"
PROMOTION_SKILL="${PROMOTION_SKILL:-$AGENT_CONCEPTS/concepts/bc-wiki-maintain/body/SKILL.md}"
[[ -f "$DETECTION_SCRIPT" ]] || fail "detection script does not exist: $DETECTION_SCRIPT"

REPO_ROOT="$(git -C "$VAULT_ROOT" rev-parse --show-toplevel 2>/dev/null)" \
  || fail "vault is not inside a git worktree: $VAULT_ROOT"
VAULT_PREFIX="$(git -C "$VAULT_ROOT" rev-parse --show-prefix 2>/dev/null)" \
  || fail 'could not determine the vault path inside its git worktree'
[[ -n "$VAULT_PREFIX" ]] || fail 'refusing to use the repository root as the vault'

repo_status() {
  git -C "$REPO_ROOT" status --porcelain=v1 --untracked-files=all
}

require_clean_tree() {
  local status
  status="$(repo_status)"
  if [[ -n "$status" ]]; then
    printf '%s\n' "$status" >&2
    fail 'refusing to run: the git worktree is dirty; review or commit user changes first'
  fi
}

require_clean_tree
log "running detection for $VAULT_ROOT"

# wiki_lint.py's machine-readable contract is one anchored line:
#   PROMOTION_REQUIRED=0   (no promotion pass needed)
#   PROMOTION_REQUIRED=1   (run the promotion pass)
# The script may print a human-readable report around that line. Missing or
# malformed status fails closed instead of guessing that a write is safe.
if ! detection_output="$(python3 "$DETECTION_SCRIPT" "$VAULT_ROOT" 2>&1)"; then
  printf '%s\n' "$detection_output" >&2
  fail 'detection failed'
fi
if [[ -n "$detection_output" ]]; then
  printf '%s\n' "$detection_output"
fi

required_lines="$(printf '%s\n' "$detection_output" | grep -Ec '^PROMOTION_REQUIRED=' || true)"
range_lines="$(printf '%s\n' "$detection_output" | grep -Ec '^PROMOTION_RANGE=' || true)"
[[ "$required_lines" == 1 && "$range_lines" == 1 ]] \
  || fail 'detection must emit exactly one PROMOTION_REQUIRED and one PROMOTION_RANGE result'
promotion_required="$(printf '%s\n' "$detection_output" | sed -n 's/^PROMOTION_REQUIRED=//p')"
promotion_range="$(printf '%s\n' "$detection_output" | sed -n 's/^PROMOTION_RANGE=//p')"
case "$promotion_required" in
  0)
    [[ "$promotion_range" == "none" ]] || fail 'detector returned an invalid range for a no-op'
    require_clean_tree
    log 'nothing to promote; exiting without invoking the agent'
    exit 0
    ;;
  1)
    if [[ ! "$promotion_range" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\.\.[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
      fail 'promotion required but detector did not emit a valid PROMOTION_RANGE=YYYY-MM-DD..YYYY-MM-DD result'
    fi
    ;;
  *)
    fail 'detection did not emit exactly one usable PROMOTION_REQUIRED=0|1 result'
    ;;
esac

require_clean_tree
[[ -f "$PROMOTION_SKILL" ]] || fail "promotion skill does not exist: $PROMOTION_SKILL"
if [[ "$PI_BIN" == */* ]]; then
  [[ -x "$PI_BIN" ]] || fail "PI_BIN is not executable: $PI_BIN"
else
  command -v "$PI_BIN" >/dev/null 2>&1 || fail "PI_BIN is not installed or not on PATH: $PI_BIN"
fi

BASE_HEAD="$(git -C "$REPO_ROOT" rev-parse HEAD)"
PROMOTION_PROMPT=$(cat <<EOF
Run the scheduled bc-wiki-maintain promotion pass.

Repository: $REPO_ROOT
Vault: $VAULT_ROOT

Read the vault's AGENTS.md, index.md, log.md, and the loaded bc-wiki-maintain skill
before changing anything. Promote only durable observations from the append-only log
that are not already represented in the vault. Prefer the smallest existing page or
an appropriately named new page. Keep existing pages self-contained.

Safety rules are absolute:
- Additive-only: create pages or append sections; never delete, rewrite, reflow, or
  silently replace existing prose.
- Contradictions are not resolved automatically. Create an open-questions entry that
  quotes/links both claims and identify the conflict for a human.
- Do not touch files outside this vault.
- Do not stage files and do not run git commit. The wrapper will inspect and create the dedicated commit.
- If there is nothing to promote after inspection, leave the tree unchanged.

When done, briefly report the files considered and the files changed. Do not claim a
promotion occurred unless the corresponding files are actually changed on disk.
EOF
)

log 'invoking verified Pi headless promotion agent (gpt-5.6-luna, max)'
set +e
(
  cd "$VAULT_ROOT"
  "$PI_BIN" \
    --print \
    --no-session \
    --approve \
    --model 'openai-codex/gpt-5.6-luna:max' \
    --thinking max \
    --skill "$PROMOTION_SKILL" \
    "$PROMOTION_PROMPT"
)
agent_status=$?
set -e
if [[ "$agent_status" -ne 0 ]]; then
  fail "promotion agent failed with exit status $agent_status; leaving any changes uncommitted for review"
fi

# A promotion agent must not advance HEAD; the wrapper owns the single commit.
if [[ "$(git -C "$REPO_ROOT" rev-parse HEAD)" != "$BASE_HEAD" ]]; then
  fail 'promotion agent committed unexpectedly; inspect the new commit before enabling the timer'
fi

# The agent must never stage anything. Compare the complete index with the
# pre-agent tree before inspecting or staging its working-tree changes.
if ! git -C "$REPO_ROOT" diff --cached --quiet "$BASE_HEAD" --; then
  git -C "$REPO_ROOT" diff --cached --name-status "$BASE_HEAD" >&2 || true
  fail 'promotion agent left staged changes; refusing to inspect or create a commit'
fi

status="$(repo_status)"
if [[ -z "$status" ]]; then
  log 'agent found nothing to promote; no commit created'
  exit 0
fi

# Never commit work outside the configured vault, and never commit deletions.
while IFS= read -r -d '' changed_path; do
  case "$changed_path" in
    "$VAULT_PREFIX"*) ;;
    *) fail "promotion touched a path outside the vault: $changed_path" ;;
  esac
done < <(
  git -C "$REPO_ROOT" diff --name-only -z
  git -C "$REPO_ROOT" ls-files --others --exclude-standard -z
)

deletions="$(git -C "$REPO_ROOT" diff --name-only --diff-filter=D)"
[[ -z "$deletions" ]] || fail "promotion deleted existing files; refusing to commit:\n$deletions"

log 'creating dedicated promotion commit'
git -C "$REPO_ROOT" add -- "$VAULT_PREFIX"
git -C "$REPO_ROOT" commit -m "wiki: promote log entries $promotion_range"

if [[ -n "$(repo_status)" ]]; then
  fail 'promotion commit completed but the repository is still dirty'
fi
log "promotion committed: $(git -C "$REPO_ROOT" log -1 --format='%h %s')"
