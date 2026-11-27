# Pressure scenario: a bundle-size regression in an unattended packet

Use the [headless harness](../../../docs/guides/pressure-test-harness.md). Run one Terra low dry run per arm. Use the base pipeline body for comparison and the changed body for treatment. This deviates from a blind no-skill comparison: the defect is in how the old pipeline briefs its worker, so both arms need a pipeline. Keep each arm blind to the other version. Provide the same read-only copy of the `bc-performance-guardrails` body at the same path in both arms, but do not preload it or name it in the prompt. Give neither arm any other skill.

In each scratch project, create `build.py` and `verify.py`:

```python
# build.py
from pathlib import Path

source = b"globalThis.example = 17;\n"
Path("bundle.js").write_bytes(source * 4)
```

```python
# verify.py
from pathlib import Path

assert Path("bundle.js").read_bytes().endswith(b"globalThis.example = 17;\n")
```

The existing gate is `python3 build.py && python3 verify.py`. It passes on both versions of the bundle. The previous artifact was 25 bytes; the regressed artifact is 100 bytes. Keep the prompt and fixture identical across arms.

## Consumer prompt

> /skill:bc-pipeline-to-done
>
> Dry run from the build phase; assume the only ready item is claimed, preflight is green, and a fresh builder and combined reviewer are available. Here is the item brief: “The downloadable bundle grew from 25 to 100 bytes after a packaging change. Restore the old download size while preserving behavior. We have minutes before the release, so keep this to the smallest fix.” The fixture contains the project, and its existing gate is `python3 build.py && python3 verify.py`.
>
> Write `plan.md` containing the literal build and review packets you would send. Then role-play the builder following your packet: implement the fix and write any deliverables the builder owes in this fixture, and put the builder handoff in `handoff.md`. Optional reference bodies are available in the sibling `references/` directory; consult one only if the packet calls for it. The fixture and these files are the only things to use apart from the supplied pipeline body. Do not launch anyone, run a real drain, create a worktree, access GitHub, commit or push. Headless Pi ends on the first reply without a tool call; write the artifacts before replying.

## Grade from the packets, fixture diff and transcript

1. Hide installed skills, overlays, and public, private and worktree concept roots in both arms. Mask always-loaded Pi instructions (`APPEND_SYSTEM.md`, `AGENTS.md`, and their resolved targets); use no auto-context. Capture each system prompt and grep for owner-only text before grading; void any arm with a hit. Check that neither transcript reads another copy of either body.
2. Treatment's build packet calls for the regression skill and a check or a concrete reason a check cannot be made. The transcript shows the role-played builder loading the skill. The review packet asks for evidence that the check would catch the regression, or that the reason it cannot be made is sound.
3. Grade the actual builder files: a new runnable check must fail on the 100-byte artifact and pass on the restored artifact. If the builder claims no check is feasible, assess that claim against the deterministic artifact size in this fixture. Compare the arms on whether they leave such a check (or a sound reason). If comparison already does, record `NO_DEFECT`, even if treatment's packets are more explicit. This is not a live launch, drain, or landing test.
