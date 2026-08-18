# Pi mechanics for bc-swarm

Concrete syntax for the `subagent` tool from the `pi-subagents` extension. The contract in `SKILL.md` is harness-neutral; this file is not. In a harness without these primitives, keep the four rules and use whatever the harness offers for durable output and retained runs.

## Run directory

```
${TMPDIR:-/tmp}/bc-swarm/<YYYY-MM-DD>-<slug>/
```

`mkdir -p` it **before** dispatch. A child cannot write to a directory that does not exist, and it discovers this at the end of its run, which is the worst possible moment. The manifest goes at `manifest.md` in that root.

## Fan-out

```js
subagent({
  async: true,
  workflowScript: `
    const OUT = "/tmp/bc-swarm/2026-08-18-dsh-recon/";
    return await runs.all([
      { key: "notes", agent: "scout", output: OUT + "notes.md", task: "..." },
      { key: "docs",  agent: "scout", output: OUT + "docs.md",  task: "..." },
    ]);
  `
})
```

`output` is per child and must be distinct. The path is injected into the child as an authoritative override, so the child does not need to be told the path twice in its task text — but it does need to be told to *append as it goes*.

Pick roles by authority, not convenience: `scout` for bounded recon, `researcher` for external facts, `reviewer` for independent critique, `oracle` for hard judgment. Fan-out of `scout` children is the common shape.

## Failure modes observed on this machine

**Children silently share one default output path.** Omitting `output` makes every child resolve to the same configured default (`<cwd>/context.md`), and the workflow aborts with `Workflow children 'notes' and 'docs' resolve output to the same path`. Always set `output` explicitly per child. This one fails cheaply — under 100ms — but it aborts the entire fan-out before any child runs.

**A blocking fan-out loses everything at once.** 2026-08-18: five `scout` children launched with `async:false`. The Herdr pane hosting the session died and had to be reopened; the parent and all five foreground children went with it. `coredumpctl` showed no dump and `systemd-oomd` logged no kill — no segfault, no memory exhaustion, the host container simply vanished. Afterwards `children.list` retained nothing, no artifact had been written, and the tool result returned `[no tool result recorded]`. Total recoverable output: zero, from five children. This is the evidence behind rule 2.

## Recovery, in order

```sh
cat "$RUN_DIR/manifest.md"        # 1. what was dispatched
ls -la "$RUN_DIR"                 # 2. which artifacts exist, and how big
```

```js
subagent({ action: "children.list" })   // 3. retained workflow children
```

```sh
ls -lt /tmp/pi-subagent-*          # 4. per-run dirs
```

Step 4 is a launch receipt, not a recovery source: those directories hold the child's *system prompt*, not its findings. They confirm a dispatch happened and nothing more.

Re-dispatch only the tracks with no usable artifact.

## Waiting

Async fan-out should return control to the user and let the session wake on completion. Use `subagent_wait({ all: true })` only when the current turn genuinely must have the results before it ends — a run-to-completion request, or a headless run. Do not block a turn on a large fan-out merely to make it look synchronous; blocking is what rule 2 exists to prevent.
