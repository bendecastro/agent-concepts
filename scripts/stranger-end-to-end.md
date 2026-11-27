# Run the Pi stranger test

This test runs the whole loop the way a stranger meets it: install the skills into a fresh Pi home with no private configuration and none of the author's own tools, set up a generated sample repository, plan one change, then build and land it with the pipeline. It complements `fresh_install_test.py`, which checks installation only.

Needs: x86-64 Linux with a merged `/usr`, `bwrap`, Git, Python 3, Node and npm in `/usr/bin`, network access to npm, and a Pi login for the model's provider.

```bash
EVIDENCE=/absolute/new/dir MODEL=provider/model-id THINKING=low scripts/stranger_end_to_end.sh
```

Choose `MODEL` and `THINKING` on your side (for example from your pressure-test configuration); the sandbox never sees that file. `STRANGER_AUTH` names the Pi `auth.json` to copy the provider's credential from (default `~/.pi/agent/auth.json`); only that one provider entry is copied into the sandbox, and it is deleted with it. The script installs the **committed** `HEAD` of this checkout through `pi install <path>`; to test a release instead, change that line to the README's `pi install git:…@<tag>` command and record why.

## What the script does

1. **Sandbox.** Every Pi process runs under `bwrap --clearenv` with only `/usr`, a few `/etc` files and a scratch directory mounted as `/box`, and with `HOME=/box/home`. No host home, checkout or skill directory is mounted. Pi's always-loaded instruction files are bound read-only to empty data. Before anything runs, it checks that `~/.config/agent-concepts`, `/home` and `/root` are absent, no `bc-*` command is on `PATH`, and both instruction files are empty.
2. **Fixture.** `stranger_fixture.py` creates `tinylabels`, a small Python package with two passing tests, on `main`, with no CI and a local bare repository as `origin`.
3. **Install.** Pi 1.6.1 from npm, this checkout through `pi install`, and `pi-subagents` from npm, as the README's pipeline prerequisites say. The example roles from `concepts/bc-pipeline-to-done/body/examples/agents/` are copied into the sandbox's agent directory with `MODEL` and `THINKING` pinned.
4. **Three sessions,** each run by `stranger_rpc_driver.py` as a long-lived Pi RPC process (print mode would exit before the pipeline's background children report back): setup with `/skill:bc-setup-project`, planning with `/skill:bc-plan-to-pipeline`, and the build with `/skill:bc-pipeline-to-done max-iters=1 max-parallel=1`, which loads `pi-subagents` explicitly with `-e` while keeping other extensions off. Each phase's opening request and first scripted answer are in the script. They are honest answers a stranger would give, not hints from the skills. Later questions get a neutral go-ahead, up to three answers per phase.
5. **Evidence.** The script writes the install log, installed revision, versions, each phase's RPC stream, session and final reply, the fixture files (without `.git`), and the bare remote's `main` log into `EVIDENCE`, then deletes the scratch directory. It also saves each distinct system prompt from the RPC stream to `EVIDENCE/system-prompts/`.

Run it once, with at most one retry for an infrastructure failure. Never retry to make a stalled step pass: a stopped test is a result.

## Audit and grade

Before trusting a run, grep every saved system prompt for distinctive phrases that only your own machine's configuration contains (`grep -Ff <your-private-list> "$EVIDENCE"/system-prompts/*`). Exit status 1 is clean; a match voids the run. Keep the phrase list, full session logs and prompts private.

Grade from the files, not the agent's replies:

- **Setup:** project instructions and layout exist, and the local check script passes.
- **Planning:** a work item marked ready for an agent, with requirements and one buildable step.
- **Build:** a commit with the change and its test on the bare remote's `main`, not only a local commit.
- **Full suite:** compare each worker's test command in its transcript with the project's full check; a worker should run targeted tests only.
- **Stalls:** for every point where the agent stopped, needed a private tool or failed, record a transcript quote or file and line, and either fix it or write a work item for it.
