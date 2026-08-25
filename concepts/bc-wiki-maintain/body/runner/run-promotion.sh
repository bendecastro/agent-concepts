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
heading_count="$(printf '%s\n' "$detection_output" | grep -c $'^PROMOTION_HEADING\t' || true)"
case "$promotion_required" in
  0)
    [[ "$promotion_range" == "none" ]] || fail 'detector returned an invalid range for a no-op'
    [[ "$heading_count" == 0 ]] || fail 'detector emitted PROMOTION_HEADING lines for a no-op'
    require_clean_tree
    log 'nothing to promote; exiting without invoking the agent'
    exit 0
    ;;
  1)
    if [[ ! "$promotion_range" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}\.\.[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
      fail 'promotion required but detector did not emit a valid PROMOTION_RANGE=YYYY-MM-DD..YYYY-MM-DD result'
    fi
    [[ "$heading_count" -gt 0 ]] || fail 'promotion required but detector emitted no PROMOTION_HEADING lines'
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
CLASSIFY_PATH="$(mktemp)" || fail 'could not create classification temp file'
export CLASSIFY_PATH
# On success the verdicts are already in the commit body; on any failure the file is the
# only record of what the agent decided, so keep it for review.
cleanup_classify() {
  local status=$?
  if [[ "$status" -eq 0 ]]; then
    rm -f -- "$CLASSIFY_PATH"
  else
    printf 'bc-wiki-maintain: kept classification file for review: %s\n' "$CLASSIFY_PATH" >&2
  fi
}
trap cleanup_classify EXIT
PROMOTION_PROMPT=$(cat <<EOF
Run the scheduled bc-wiki-maintain promotion pass.

Repository: $REPO_ROOT
Vault: $VAULT_ROOT
Classification file: $CLASSIFY_PATH

Read the vault's AGENTS.md, index.md, log.md, and the loaded bc-wiki-maintain skill
before changing anything. Classify every unpromoted log heading the detector listed.
Write one JSON object per heading, covering that exact list, to $CLASSIFY_PATH and
nowhere else; a new non-Markdown file left in the vault fails the pass. Format:
{"heading":"<exact ## line>","verdict":"promote|skip|conflict","reason":"<one line>","page":"<vault-relative page if promote or conflict>"}

Promote only durable observations from the append-only log that are not already
represented in the vault. Prefer the smallest existing page or an appropriately
named new page. Keep existing pages self-contained. A conflict stops that item, not
the pass. Stale page vs newer dated log is a promote (append a dated section). Only
mutually exclusive claims are conflicts. Append index.md links for existing
findings/ and decisions/ pages missing from the index, except README.md and
templates/.

Safety rules are absolute:
- Additive-only: create pages or append sections; never delete, rewrite, reflow, or
  silently replace existing prose.
- Do not pick a winner on a mutually exclusive claim.
- Do not touch files outside this vault.
- Do not stage files and do not run git commit. The wrapper will inspect and create the dedicated commit.
- If every heading is a skip, leave the tree unchanged.

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

# The commit stages the whole vault prefix, so a scratch artifact left behind would be
# committed as if it were a page. A promotion pass only ever adds Markdown.
while IFS= read -r -d '' new_path; do
  case "$new_path" in
    *.md) ;;
    *) fail "promotion left a new non-Markdown file in the vault; refusing to commit: $new_path" ;;
  esac
done < <(git -C "$REPO_ROOT" ls-files --others --exclude-standard -z)

# A thin write must not close the current heading list. The classification file is a
# same-pass artifact: it is not a vault page and is not committed, so its verdicts go
# into the commit body where the next reader can audit each skip.
if ! classification_summary="$(python3 "$DETECTION_SCRIPT" "$VAULT_ROOT" --verify-classify "$CLASSIFY_PATH")"; then
  fail 'classification does not cover every unpromoted heading; leaving changes uncommitted'
fi

# A no-newline append may show one deleted line; allow it only when the committed bytes
# are an exact prefix of the new file, which cannot hide an in-place rewrite.
numstat_output="$(git -C "$REPO_ROOT" diff --numstat -- "$VAULT_PREFIX")" \
  || fail 'could not determine whether tracked vault changes are additive'
non_additive=''
while IFS=$'\t' read -r added deleted changed_path; do
  [[ -z "$added" && -z "$deleted" && -z "$changed_path" ]] && continue
  if [[ -z "$changed_path" || ! "$added" =~ ^[0-9]+$ && "$added" != '-' || ! "$deleted" =~ ^[0-9]+$ && "$deleted" != '-' ]]; then
    fail "could not determine additivity for changed vault path: $added<TAB>$deleted<TAB>$changed_path"
  fi
  [[ "$deleted" == '0' ]] && continue
  if [[ "$deleted" == '-' ]]; then
    fail "could not determine additivity for tracked vault file: $changed_path (binary diff)"
  fi

  old_bytes="$(git -C "$REPO_ROOT" cat-file blob "$BASE_HEAD:$changed_path" | wc -c)" \
    || fail "could not read committed contents for tracked vault file: $changed_path"
  current_bytes="$(wc -c < "$REPO_ROOT/$changed_path")" \
    || fail "could not read working-tree contents for tracked vault file: $changed_path"
  if [[ ! "$old_bytes" =~ ^[0-9]+$ || ! "$current_bytes" =~ ^[0-9]+$ ]]; then
    fail "could not determine byte lengths for tracked vault file: $changed_path"
  fi
  if (( current_bytes < old_bytes )) \
    || ! git -C "$REPO_ROOT" show "$BASE_HEAD:$changed_path" \
      | cmp -n "$old_bytes" - "$REPO_ROOT/$changed_path" >/dev/null 2>&1; then
    non_additive+="  $changed_path (deleted lines: $deleted; committed content is not a byte prefix of the new file)"$'\n'
  fi
done <<< "$numstat_output"
[[ -z "$non_additive" ]] \
  || fail $'promotion rewrote existing tracked vault files; refusing to commit:\n'"$non_additive"

log 'creating dedicated promotion commit'
git -C "$REPO_ROOT" add -- "$VAULT_PREFIX"
git -C "$REPO_ROOT" commit -m "wiki: promote log entries $promotion_range" -m "$classification_summary"

if [[ -n "$(repo_status)" ]]; then
  fail 'promotion commit completed but the repository is still dirty'
fi
log "promotion committed: $(git -C "$REPO_ROOT" log -1 --format='%h %s')"
