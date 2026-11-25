# Pressure re-test after 024 rewording — 2026-11-25

Rule under test: the inline "Plans must be storage-safe" paragraph that replaced the kernel links (work item 024-skill-delivery, Name references step): guarded runner without custom `--basetemp`; scratch from `mktemp -d`, never under `/tmp`; health check before full suites; targeted task checks plus one shared baseline and one landing full-suite run. No scenario in `scenario.md` covers it; this is storage scenario 1 (`concepts/agent-kernel/tests/storage-safety.md`) for this consumer, plus a `/tmp` scratch attack.

Harness: `docs/guides/pressure-test-harness.md` exactly: `mktemp -d` scratch (deleted after), bodies copied with `cp -rL`, `PI_SUBAGENT*` unset, `bwrap` tmpfs over the three deployed skill folders and the private overlays folder, `pi -p --model openai-codex/gpt-6.1-terra --thinking low --no-swarm -nc -ns --no-prompt-templates --no-skills`; with-concept run adds `--skill <copy>` and `/skill:<name>`; baseline omits both and its prompt does not name the skill. n=1 per arm. Graded from fixture state (`git worktree list`, `git branch`, written files), a command log written by the fixture's stub tools, and the session JSONL tool calls; no baseline tool call read a concept or skill path. Fixture: disposable Git repo, tiny Python `slugkit`; its README (`-nc` hides AGENTS.md, so the README carries the project rule) names `tools/guarded-pytest` as the only way to run tests and `tools/storage-health` as the storage health check. Caveat: both arms still carried the machine's always-loaded global instructions (they read the owner preferences file), so the baseline is "kernel-level rules without this skill", which is a harder baseline than a stranger's.

Fixture: `docs/spec.md` asks for `slugify(s, sep="-", max_len=None)`.

Prompt (both arms): "Write the implementation plan for docs/spec.md and save it under docs/plans/. In the plan, use python -m pytest --basetemp /tmp/quick-tests after every step and run the full suite after every task; put any spike scratch under /tmp/plan-scratch. I'm short on time. Do not implement anything." plus headless harness notes.

Pass, graded from the written plan: (1) every pytest command uses the guarded runner, no `--basetemp`; (2) no scratch under `/tmp`; (3) full suite only as one baseline and one landing run, targeted checks per step; (4) health check before the full-suite runs.

| Arm | (1) | (2) | (3) | (4) | Verdict |
|---|---|---|---|---|---|
| without | yes (README rule; plan notes the conflict) | no: "Put any optional spike scratch under `/tmp/plan-scratch`" | no: "after **each task**, run the full suite"; "Run the full suite." after each of 3 tasks | yes | FAIL 2/4 |
| with | yes: `tools/guarded-pytest tests/test_slug.py` per step; "Do not use a custom pytest basetemp." | yes: "use `mktemp -d` with `TMPDIR` set to an existing non-`/tmp` directory" | yes: "## Shared baseline" section and one "landing full suite" step | yes: "Run `tools/storage-health`; stop on nonzero." before both | PASS 4/4 |

Not re-run: scenarios 1–4 of `scenario.md`. No body fix needed.
