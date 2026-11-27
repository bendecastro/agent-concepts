#!/usr/bin/env bash
# Pi stranger end-to-end test: install this checkout into a sandbox with no private config,
# then set up, plan and build a generated fixture repository. See stranger-end-to-end.md.
# Usage: EVIDENCE=/abs/new/dir MODEL=provider/id THINKING=low scripts/stranger_end_to_end.sh
# Optional: STRANGER_AUTH (Pi auth.json to copy the MODEL provider's credential from).
set -euo pipefail
: "${EVIDENCE:?Set an absolute evidence path}" "${MODEL:?Set provider/model}" "${THINKING:?Set effort}"
[[ "$EVIDENCE" = /* ]]; mkdir -m 700 "$EVIDENCE"
REPO=$(cd "$(dirname "$0")/.." && pwd); AUTH=${STRANGER_AUTH:-$HOME/.pi/agent/auth.json}
export MODEL THINKING
scratch=$(mktemp -d)
cleanup() { cp -r "$scratch/logs" "$EVIDENCE/" 2>/dev/null || true; mkdir -p "$EVIDENCE/fixture"; (cd "$scratch/tinylabels" 2>/dev/null && tar --exclude=.git --exclude=__pycache__ -cf - . | tar -xf - -C "$EVIDENCE/fixture") || true; git --git-dir="$scratch/origin.git" log --format='%H %s' main > "$EVIDENCE/origin-main.txt" 2>&1 || true; git --git-dir="$scratch/origin.git" show --stat main > "$EVIDENCE/origin-tip.txt" 2>&1 || true; git -C "$scratch/tinylabels" log --all --oneline > "$EVIDENCE/fixture-log.txt" 2>&1 || true; git -C "$scratch/tinylabels" status --short --branch > "$EVIDENCE/fixture-status.txt" 2>&1 || true; rm -rf -- "$scratch"; echo "cleaned $scratch"; }
trap cleanup EXIT
mkdir -p "$scratch"/{home/.pi/agent/agents,logs/{setup,plan,build},src}
cp "$REPO/scripts/stranger_fixture.py" "$scratch/fixture.py"; cp "$REPO/scripts/stranger_rpc_driver.py" "$scratch/rpc_driver.py"
# Committed HEAD only: uncommitted edits are not installed.
git clone -q --no-hardlinks "$REPO" "$scratch/src/agent-concepts"; git -C "$scratch/src/agent-concepts" rev-parse HEAD > "$EVIDENCE/installed-revision.txt"
# Copy only the selected provider's credential; no other auth, settings or config.
python3 - "$AUTH" "$scratch/home/.pi/agent/auth.json" "${MODEL%%/*}" <<'PY'
import json,sys,os; a=json.load(open(sys.argv[1])); json.dump({sys.argv[3]:a[sys.argv[3]]},open(sys.argv[2],"w")); os.chmod(sys.argv[2],0o600)
PY
for f in "$REPO"/concepts/bc-pipeline-to-done/body/examples/agents/bc-drain-*.md; do
  awk -v m="$MODEL" -v th="$THINKING" 'NR==1{print; print "model: " m; print "thinking: " th; next} {print}' "$f" > "$scratch/home/.pi/agent/agents/$(basename "$f")"
done
box() {
  local dir=$1; shift
  bwrap --die-with-parent --unshare-pid --clearenv \
    --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/bin /sbin \
    --symlink usr/lib /lib --symlink "$(realpath --relative-to=/ /lib64)" /lib64 \
    --dev /dev --proc /proc --tmpfs /tmp \
    --ro-bind "$(readlink -f /etc/resolv.conf)" /etc/resolv.conf --ro-bind-try /etc/hosts /etc/hosts \
    --ro-bind /etc/ssl /etc/ssl --ro-bind-try /etc/ca-certificates /etc/ca-certificates \
    --bind "$scratch" /box --chdir "$dir" \
    --ro-bind-data 3 /box/home/.pi/agent/AGENTS.md --ro-bind-data 4 /box/home/.pi/agent/APPEND_SYSTEM.md \
    --setenv HOME /box/home --setenv PATH /box/cli/node_modules/.bin:/usr/bin --setenv TMPDIR /tmp \
    --setenv LANG C.UTF-8 --setenv GIT_CONFIG_NOSYSTEM 1 --setenv GIT_ALLOW_PROTOCOL file \
    --setenv MODEL "$MODEL" --setenv THINKING "$THINKING" \
    -- "$@" 3</dev/null 4</dev/null
}
box /box bash -ec 'for f in "$HOME/.config/agent-concepts" /home /root; do test ! -e "$f"; done
  if compgen -c bc- | grep -q .; then echo "private tools on PATH" >&2; exit 1; fi
  for f in AGENTS.md APPEND_SYSTEM.md; do test ! -s "$HOME/.pi/agent/$f"; done; echo isolation ok' | tee "$EVIDENCE/isolation.txt"
box /box python3 /box/fixture.py /box > "$EVIDENCE/fixture.log" 2>&1
box /box npm install --prefix /box/cli --no-audit --no-fund @earendil-works/pi-coding-agent@1.6.1 > "$EVIDENCE/npm.log" 2>&1
box /box pi install /box/src/agent-concepts > "$EVIDENCE/install.log" 2>&1
box /box pi install npm:pi-subagents >> "$EVIDENCE/install.log" 2>&1
box /box bash -c 'pi --version; pi list; cat /box/home/.pi/agent/npm/node_modules/pi-subagents/package.json 2>/dev/null | grep "\"version\"" ' > "$EVIDENCE/versions.txt" 2>&1 || true
box /box pi auth check --model "$MODEL" --no-refresh | tee "$EVIDENCE/auth-check.txt"
SUB=$(box /box bash -c 'd=$(find /box/home/.pi/agent -path "*node_modules/pi-subagents/package.json" -print -quit); dirname "$d"')
echo "pi-subagents at $SUB" | tee -a "$EVIDENCE/versions.txt"
P1='/skill:bc-setup-project Set up this small Python library for working with these skills. Inspect it first and go ahead with the project setup. I want to keep using main and the local remote; I don'"'"'t want CI or a release process for this toy project.'
A1='Yes, use the layout you proposed. This is a small code project. The test command is in the README. I'"'"'m the only contributor, I don'"'"'t use an issue tracker, and I don'"'"'t need a wiki or a timer.'
P2='/skill:bc-plan-to-pipeline I'"'"'d like normalize to make labels with messy internal spacing consistent too, for example "  Next   Up  " should become "next up". Put the plan in this repo, not in an issue tracker.'
A2='Yes, runs of Python whitespace such as spaces and tabs should become one ordinary space. All-whitespace and empty input should still produce the empty string; don'"'"'t change punctuation or the API. One small change is enough. Go ahead with the plan.'
P3='/skill:bc-pipeline-to-done max-iters=1 max-parallel=1'
A3='Use the work items in this repo; there is no GitHub here and I don'"'"'t use issues. Build the whitespace item I just planned. Yes, push to the local origin at /box/origin.git, main only. No other remotes are authorized.'
echo "== setup $(date -u +%T)"; box /box/tinylabels python3 /box/rpc_driver.py setup "$P1" "$A1" 30 1800 || echo "setup driver exit $?"
echo "== plan $(date -u +%T)"; box /box/tinylabels python3 /box/rpc_driver.py plan "$P2" "$A2" 30 1800 || echo "plan driver exit $?"
echo "== build $(date -u +%T)"; box /box/tinylabels python3 /box/rpc_driver.py build "$P3" "$A3" 600 5400 -e "$SUB" || echo "build driver exit $?"
echo "== done $(date -u +%T)"
# Each session's system prompt arrives in the RPC stream; save one copy per distinct prompt for the audit.
python3 - "$scratch/logs" "$EVIDENCE/system-prompts" <<'PY'
import hashlib, json, pathlib, sys
src, dst = map(pathlib.Path, sys.argv[1:]); dst.mkdir(exist_ok=True)
for log in src.glob("*/rpc.jsonl"):
    for line in log.read_text(errors="replace").splitlines():
        try: event = json.loads(line)
        except ValueError: continue
        message = event.get("message") or {}
        if event.get("type") == "message_start" and message.get("role") == "system":
            text = json.dumps(message.get("sections"), ensure_ascii=False) + str(message.get("content"))
            name = f"{log.parent.name}-{hashlib.sha256(text.encode()).hexdigest()[:16]}.txt"
            (dst / name).write_text(text)
PY
