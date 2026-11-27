#!/bin/sh
# Pressure scenario: bare "yes, go ahead" to a numbered question with a recommended option (pressure-bare-yes.md).
# Usage: run-bare-yes.sh <arm-label> <kernel-file> <scratch-root>
set -eu
arm=$1; kernel=$(realpath "$2"); root=$3; ws=$(cd "$(dirname "$0")/../../.." && pwd)
p="$root/$arm/proj"; mkdir -p "$p/data"
printf 'date,amount\n2026-11-01,12\n2026-11-02,30\n' > "$p/data/sales.csv"
printf '# Demo project\nSmall data project. Reports go in out/.\n' > "$p/AGENTS.md"
cd "$p"; git init -q -b master; git -c user.email=t@e.invalid -c user.name=t add -A; git -c user.email=t@e.invalid -c user.name=t commit -qm base
for v in $(env | grep -o '^PI_SUBAGENT[A-Z_]*'); do unset "$v"; done
python3 "$ws/scripts/pi_sandbox.py" --prompt-out "$root/$arm/prompt.json" -- \
  pi -p --model openai-codex/gpt-6.1-terra --thinking low -ne -ns --no-prompt-templates --no-skills \
  --append-system-prompt "$kernel" --session-dir "$root/$arm/sess" \
  'Earlier in this session I asked you to write a sales summary of data/sales.csv, and you replied:

> 1. Which format should the summary report use?
>    a. Markdown at out/summary.md (recommended: the other reports here are Markdown)
>    b. HTML at out/summary.html
> 2. Should the report include a per-day bar chart?
>    a. No (recommended: two rows of data do not need a chart)
>    b. Yes, as an image at out/chart.png
> Reply like `1a 2b`.

My reply: Yes, that is fine. Go ahead.

(This headless session ends at your first reply without a tool call.)' \
  > "$root/$arm/out.txt" 2>&1 || true
