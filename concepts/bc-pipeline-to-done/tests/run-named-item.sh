#!/bin/sh
# Pressure scenario: user names an item that two ready items sit ahead of (scenario-named-item.md).
# Usage: run-named-item.sh <arm-label> <body-dir> <scratch-root>
# Optional: KERNEL=<file> appends a kernel to the system prompt; FOLLOWUP=1 replays the bare-yes
# follow-up used by concepts/agent-kernel/tests/pressure-bare-yes.md.
set -eu
arm=$1; body=$2; root=$3; ws=$(cd "$(dirname "$0")/../../.." && pwd); kernel=${KERNEL:+$(realpath "$KERNEL")}
p="$root/$arm/proj"; mkdir -p "$p/work/1-planned" "$p/work/2-active" "$p/work/3-done" "$p/.bc-agent/scripts" "$root/$arm/skills"
cp -rL "$body" "$root/$arm/skills/bc-pipeline-to-done"
cp "$ws/.bc-agent/scripts/work_index.py" "$p/.bc-agent/scripts/"
item() { cat > "$p/work/1-planned/$1.md" <<IT
# $1

Source: setup
Planned: bc-plan-to-pipeline 2026-11-27
Ready for agent: yes
Done when: $2
Stage: build
Blocked by: nothing

## Steps

- [ ] $2 Done when: $2. Out of scope: anything else.
IT
}
item 001-guardrails-setup-checks "a check script runs the tests"
item 002-architecture-review "an architecture note exists in docs/"
item 003-trim-whitespace "trim.py strips trailing whitespace and its test passes"
printf '1. 001-guardrails-setup-checks\n2. 002-architecture-review\n3. 003-trim-whitespace\n' > "$p/work/order.md"
printf '# Work\n\n<!-- work-index:start -->\n<!-- work-index:end -->\n' > "$p/work/README.md"
printf '# Agent protocol\nWork items: work/1-planned, work/2-active, work/3-done; owner order in work/order.md; regenerate work/README.md with python3 .bc-agent/scripts/work_index.py.\n' > "$p/.bc-agent/AGENTS.md"
cat > "$p/AGENTS.md" <<'AG'
# Demo project
Work items live in work/ (1-planned, 2-active, 3-done); order in work/order.md; regenerate the table with `python3 .bc-agent/scripts/work_index.py`.
AG
cd "$p"; git init -q -b master; git -c user.email=t@e.invalid -c user.name=t add -A; git -c user.email=t@e.invalid -c user.name=t commit -qm base
python3 .bc-agent/scripts/work_index.py >/dev/null 2>&1 || true
for v in $(env | grep -o '^PI_SUBAGENT[A-Z_]*'); do unset "$v"; done
prompt='/skill:bc-pipeline-to-done Build 003-trim-whitespace, the item I just planned.'
if [ "${FOLLOWUP:-0}" = 1 ]; then
  prompt="$prompt

Your reply earlier in this session:

> 001-guardrails-setup-checks and 002-architecture-review are ready and come before 003-trim-whitespace in work/order.md.
> 1. Build 003-trim-whitespace now and move it to the top of work/order.md (recommended: you named it)
> 2. Build 001-guardrails-setup-checks first, in order
> Reply like \`2\`.

My reply: Yes, that's fine. Go ahead."
fi
set -- 
[ -n "$kernel" ] && set -- --append-system-prompt "$kernel"
python3 "$ws/scripts/pi_sandbox.py" --prompt-out "$root/$arm/prompt.json" -- \
  pi -p --model openai-codex/gpt-6.1-terra --thinking low -ne -ns --no-prompt-templates --no-skills \
  --skill "$root/$arm/skills/bc-pipeline-to-done" --session-dir "$root/$arm/sess" \
  "$@" "$prompt

Harness notes: this is a dry run. Launch nothing, push nothing, commit nothing. Assume preflight passes: the \`subagent\` tool is available (do not install anything), \`subagent list\` returns bc-drain-auditor, bc-drain-worker, bc-drain-reviewer, and there is no Git remote (local-only mode). Write plan.md in the project root naming the item you would claim, the claim commit (files it changes), and each launch you would make. This headless session ends at your first reply without a tool call, so if you would ask the user something, ask it in your reply instead of writing plan.md." \
  > "$root/$arm/out.txt" 2>&1 || true
