# Run the Pi stranger test

This is a live test of the public install, not a test of the checkout's skill bodies. Run on an x86-64 Linux system with a merged `/usr`, `bwrap`, Git, Python 3, and a supported Node/npm in `/usr/bin`. The model driver needs credentials for the selected provider. Use an isolated login, not a copy of the real Pi configuration. A release may lag the checkout; record the installed revision and do not attribute its behavior to unshipped fixes.

## Prepare the sandbox and install

From this repository, in Bash, set `EVIDENCE` to a **new absolute directory outside the sandbox**. On the driver side, select `MODEL` (`provider/id`) and `THINKING` from your pressure-test configuration or equivalent. Pass the values, never mount the configuration. Use one attempt, with at most one infrastructure retry; do not retry a behavioral stall.

```bash
set -euo pipefail
: "${EVIDENCE:?Set an absolute evidence path}" "${MODEL:?Set provider/model}" "${THINKING:?Set effort}"
[[ "$EVIDENCE" = /* ]]
mkdir -m 700 "$EVIDENCE"
scratch=$(mktemp -d)
trap 'rm -rf -- "$scratch"' EXIT
mkdir -p "$scratch"/{home/.pi/agent,logs}
cp scripts/stranger_fixture.py "$scratch"/fixture.py

box() {
  bwrap --die-with-parent --unshare-pid --clearenv \
    --ro-bind /usr /usr --symlink usr/bin /bin --symlink usr/bin /sbin \
    --symlink usr/lib /lib --symlink "$(realpath --relative-to=/ /lib64)" /lib64 \
    --dev /dev --proc /proc --tmpfs /tmp \
    --ro-bind "$(readlink -f /etc/resolv.conf)" /etc/resolv.conf \
    --ro-bind /etc/ssl /etc/ssl --ro-bind-try /etc/ca-certificates /etc/ca-certificates \
    --bind "$scratch" /box --chdir "$1" \
    --ro-bind-data 3 /box/home/.pi/agent/AGENTS.md \
    --ro-bind-data 4 /box/home/.pi/agent/APPEND_SYSTEM.md \
    --setenv HOME /box/home --setenv PATH /box/cli/node_modules/.bin:/usr/bin \
    --setenv LANG C.UTF-8 --setenv GIT_CONFIG_NOSYSTEM 1 \
    --setenv GIT_ALLOW_PROTOCOL "${GIT_PROTOCOLS:-file}" -- "${@:2}" 3</dev/null 4</dev/null
}
box /box bash -ec 'for f in "$HOME/.config/agent-concepts" /home /root; do test ! -e "$f"; done
  if compgen -c bc-; then echo "private tools on PATH" >&2; exit 1; fi
  for f in AGENTS.md APPEND_SYSTEM.md; do
    test -r "$HOME/.pi/agent/$f"; test ! -s "$HOME/.pi/agent/$f"
  done'
box /box python3 /box/fixture.py /box 2>&1 | tee "$EVIDENCE/fixture.log"
box /box npm install --prefix /box/cli --no-audit --no-fund @earendil-works/pi-coding-agent@1.6.1
GIT_PROTOCOLS=https box /box pi install git:github.com/bendecastro/agent-concepts@v0.3.0 \
  2>&1 | tee "$EVIDENCE/install.log"
box /box pi --version | tee "$EVIDENCE/pi-version.txt"
box /box bash -ec 'pkg=$(find "$HOME/.pi/agent/git" -name .git -print -quit)
  test -n "$pkg"; git -C "${pkg%/.git}" rev-parse HEAD' | tee "$EVIDENCE/installed-revision.txt"
box /box pi auth login "${MODEL%%/*}" --no-browser
box /box pi auth check --model "$MODEL" --no-refresh
box /box pi --offline -ne -nc --no-mcp --list-models "${MODEL#*/}" | tee "$EVIDENCE/models.txt"
awk -v provider="${MODEL%%/*}" -v id="${MODEL#*/}" \
  '$1 == provider && $2 == id { exact = 1 } END { exit !exact }' "$EVIDENCE/models.txt"
```

The mount allowlist is deliberate: no host home, checkout, owner skill trees, or symlink targets are mounted. The throwaway Pi instruction files are bound to `/dev/null` read-only, so neither the host files nor their targets can inject text. No inherited environment or local tool directories are passed. `/usr/bin` must contain no private `bc-*` helpers. The model stage uses only the `file` Git transport and must only change the fixture and push to its local bare remote. Do not supply a GitHub token or copy auth/config/settings files into the reports.

## Conduct three headless sessions

Run from `/box/tinylabels` in order. Pass a phase name, a unique turn number and any additional Pi flags to the function below; the prompt comes last. Use `--continue` in the same phase for a scripted response, not another skill invocation. Audit before running the turn as described below. If a phase stops, copy its evidence before proceeding; do not fabricate the missing artifact needed by the next phase. Stop on model unavailability, quota exhaustion, or a prompt audit hit. A stopped test is a result, not permission to change the prompts until it passes.

```bash
turn() {
  local phase=$1 number=$2
  shift 2
  mkdir -p "$scratch/logs/$phase"
  box /box/tinylabels pi -p --mode json -nc -ne --no-mcp --no-prompt-templates \
    --model "$MODEL" --thinking "$THINKING" --session-dir "/box/logs/$phase" "$@" \
    >"$scratch/logs/$phase/turn-$number.jsonl" 2>"$scratch/logs/$phase/turn-$number.stderr"
}
```

- **Setup:** `/skill:bc-setup-project Set up this small Python library for working with these skills. Inspect it first and go ahead with the project setup. I want to keep using main and the local remote; I don't want CI or a release process for this toy project.` If asked, answer: `Yes, use the layout you proposed. This is a small code project. The test command is in the README. I'm the only contributor, I don't use an issue tracker, and I don't need a wiki or a timer.`
- **Plan:** `/skill:bc-plan-to-pipeline I'd like normalize to make labels with messy internal spacing consistent too, for example "  Next   Up  " should become "next up". Put the plan in this repo, not in an issue tracker.` If asked, answer: `Yes, runs of Python whitespace such as spaces and tabs should become one ordinary space. All-whitespace and empty input should still produce the empty string; don't change punctuation or the API. One small change is enough. Go ahead with the plan.`
- **Build:** `/skill:bc-pipeline-to-done max-iters=1 max-parallel=1` If asked for push permission, answer: `Yes, push to the local origin at /box/origin.git, main only. No other remotes are authorized.` Never replace a required worker or reviewer with the driver.

The build phase is the one exception to extension-free **discovery**, not a reason to enable the real Pi configuration. Before a live build, follow **Install prerequisites for the pipeline** in the [README](../README.md#install-prerequisites-for-the-pipeline) *inside the sandbox*: install `npm:pi-subagents`, set up the public role profiles, and explicitly load only that extension with `-e` while keeping `-ne -nc`. Pin and record the extension version and the roles/models you configured. Confirm that any nested Pi process inherits the same sandbox, uses only the intended public resources, and writes logs below `/box/logs`; do not run if that is not true. A run without the extension can check the documented preflight stop, but does not test building or landing. Do not fake `subagent` responses.

### Audit prompt and save evidence

Before sending an extension-free turn, inspect the prompt in the same cwd and agent directory via the public SDK: use `DefaultResourceLoader({cwd, agentDir, noExtensions: true, noContextFiles: true, noPromptTemplates: true})`, await `loader.reload()`, and read `session.systemPrompt` from `createAgentSession({cwd, agentDir, resourceLoader: loader, sessionManager: SessionManager.inMemory()})`. For a pipeline turn or child, capture the effective prompt at dispatch (e.g. a test-only Pi observer subscribed to `context_with_system` in each process, recording only system messages and returning nothing); a base SDK snapshot cannot see extension modifications. No other extension should load. Grep each captured prompt with `grep -Ff` against a nonempty **driver-only** list of distinctive owner-only phrases (exit 1 is clean; exit 0 or 2 voids the run). A missing capture also voids the run. Do not publish raw prompts or the phrase list. Record the check and a hash of each audited prompt. The skill package is the only allowed skill source. Keep full session JSONL directories privately for review, not in the public repository.

After each phase, copy `/box/logs/<phase>` (including child sessions and turn diagnostics) from `"$scratch/logs"` into `"$EVIDENCE"` before removing scratch. Save fixture artifacts after each phase, including uncommitted setup or plan files, excluding `.git`, caches, and environment/auth files. Also save Git evidence, e.g.:

```bash
box /box git --git-dir=/box/origin.git log --format='%H %s' refs/heads/main >"$EVIDENCE/origin-main.txt"
box /box git --git-dir=/box/origin.git show --stat refs/heads/main >"$EVIDENCE/origin-tip.txt"
box /box/tinylabels git status --short --branch >"$EVIDENCE/fixture-status.txt"
```

Grade from artifacts: setup instructions/layout and executable local check; a ready work item with requirements and a buildable slice; a feature commit (including test) on the **bare remote's** `main`, not just a local commit; each worker's actual validation command from its transcript compared with the fixture's full gate. Distinguish a driver gate from a worker running the full suite. For every stall record a transcript quote with its location, or the relevant file/line, and link a fix or work-item draft. Copy only small reviewed excerpts into the public results.
