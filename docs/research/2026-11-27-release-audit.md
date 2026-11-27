# Release audit since v0.3.0 (2026-11-27)

Sorts each discipline concept's body changes since its `tested` date into rule changes and wording changes, per [releasing.md](../guides/releasing.md) step 2. Classification by two read-only scouts against `git diff`, checked by the integrating session.

## Rule changes and the test that covers them

| Rule | Concepts | Covered by |
|---|---|---|
| Missing owner tools: skip an absent storage check with a note; plain `pytest` with `tmp_path` when no guarded runner | bc-delegate-investigation, bc-diagnosing-bugs, bc-dispatching-parallel-agents, bc-executing-plans, bc-finishing-development-branch, bc-optimize-code, bc-subagent-driven-development, bc-tdd, bc-using-git-worktrees, bc-writing-plans | [bc-pipeline-to-done missing-machine-tools results](../../concepts/bc-pipeline-to-done/tests/pressure-missing-machine-tools-results-2026-11-26.md) |
| Resolve the target branch instead of guessing `main`/`master` | bc-executing-plans, bc-finishing-development-branch | [bc-pipeline-to-done default-branch results](../../concepts/bc-pipeline-to-done/tests/pressure-default-branch-results-2026-11-26.md) |
| Stop when the `subagent` tool is missing | bc-council-chain, bc-council-mode | Read check: one-line stop, same wording as the pipeline preflight |
| Planning asks about new dependencies; the builder adds only named ones | bc-plan-to-pipeline, bc-pipeline-to-done | [planned-dependencies results](../../concepts/bc-pipeline-to-done/tests/pressure-planned-dependencies-results-2026-11-27.md); stranger rerun attempt 4 |
| Starter items for new projects; guardrail checks added when that item runs | bc-setup-project, bc-performance-guardrails | [starter-items new-project results](../../concepts/bc-setup-project/tests/pressure-starter-items-new-project-results-2026-11-27.md) |
| A typed security-audit command starts a full audit | bc-security-audit | [typed-command results](../../concepts/bc-security-audit/tests/pressure-typed-command-results-2026-11-27.md) |
| A `Dependencies:` line counts as a test waiver only when marked as the owner's answer | bc-plan-to-pipeline, bc-tdd, bc-pipeline-to-done | [planned-dependencies results](../../concepts/bc-pipeline-to-done/tests/pressure-planned-dependencies-results-2026-11-27.md) (marked-line arm) |
| A user-named work item sets the order for its run | bc-pipeline-to-done | [named-item results](../../concepts/bc-pipeline-to-done/tests/pressure-named-item-results-2026-11-27.md) |
| A bare yes or "rec" means the recommended option | agent-kernel | [bare-yes test](../../concepts/agent-kernel/tests/pressure-bare-yes.md) |
| Setup checks `gh` only with a GitHub remote; sync-tool ignore only in a synced folder | bc-setup-project, bc-tdd | Exercised by the stranger rerun (no GitHub, no synced folder) |
| A session the session tool shows as ended counts as finished (unverified when no tool) | bc-work-sync | Read check: fallback for a missing tool, no new stop |

## Wording changes only

agent-kernel, bc-brainstorming, bc-code-review (its rule change of 2026-11-27 was tested the same day), bc-improve-codebase-architecture, bc-self-improve, bc-triage, bc-ui-design, bc-wiki-maintain.

## Scout records

- agent-kernel | NEUTRAL | 502ed1a 3895d3d (both 2026-11-26, before tested 2026-11-27) | Both commits predate the tested date (CONCEPT.md tested set in f7e9af5, 2026-11-27 16:18), so the current test already covers them; no body commit after tested.
- bc-brainstorming | NEUTRAL | 4b05ddf | Only appends an HTML comment `<!-- trigger-allow: ... -->` to an existing bullet; no body behaviour change. No body commits otherwise since v0.3.0.
- bc-code-review | NEUTRAL | 070d270 (2026-11-27), 502ed1a, 3895d3d (11-26) | 11-26 commits predate tested. 070d270 added "check every count and claim in it ... one the file does not show is an Important finding" (BEHAVIOUR), but the same commit set tested: 2026-11-27 and added tests/pressure-results-claims.md (Terra low, 3/3 treatment) so it is tested after the change. Nothing later.
- bc-council-chain | BEHAVIOUR | 502ed1a | New gate: "If the `subagent` tool is missing, stop and tell the user to install `pi-subagents` and restart Pi." plus no-overlay fallback roster; after tested 2026-11-24.
- bc-council-mode | BEHAVIOUR | 502ed1a | New gate: "If the `subagent` tool is missing, stop and tell the user to install `pi-subagents` and restart Pi."; after tested 2026-11-24.
- bc-delegate-investigation | BEHAVIOUR | 502ed1a 3895d3d | 502ed1a: "stop and report on critical or unknown health or if the configured check cannot run. If no storage health check is configured, skip it and note that in one line"; full gate "otherwise run the gate directly"; packet runner "if absent, plain `pytest` with `tmp_path`"; pi.md missing-subagent stop. 3895d3d alone is neutral (kernel references reworded).
- bc-diagnosing-bugs | BEHAVIOUR | 502ed1a 3895d3d | 502ed1a adds fallback "otherwise plain `pytest`, with `tmp_path` for test fixtures and cleanup even on failure"; 3895d3d neutral. Small, but a new default rule a test could grade.
- bc-dispatching-parallel-agents | BEHAVIOUR | 502ed1a 3895d3d | 502ed1a: "stop and report ... or if the configured check cannot run. If no storage health check is configured, skip it and note that in one line in the report" + plain pytest/tmp_path fallback; 3895d3d neutral.
- bc-executing-plans | BEHAVIOUR | 502ed1a 2204409 3895d3d | 2204409: target-branch resolution ("resolve it once from an explicit project instruction, then `git symbolic-ref refs/remotes/origin/HEAD` ...") replaces master/main guess; 502ed1a plain pytest/tmp_path fallback. 3895d3d neutral.
- bc-finishing-development-branch | BEHAVIOUR | 502ed1a 2204409 3895d3d | 2204409: "Use the target branch already recorded ... Ask if the target is unresolved ... Use that target as `<base>`" replaces "Determine likely base branch (main, master ...)"; 502ed1a plain pytest fallback. 3895d3d neutral.
- bc-improve-codebase-architecture | NEUTRAL | none (body unchanged since v0.3.0; only RELATIONSHIPS.md changed outside body) | No body commits.
- bc-optimize-code | BEHAVIOUR | 502ed1a 3895d3d | 502ed1a adds "otherwise plain `pytest`, with `tmp_path` for test fixtures and cleanup even on failure" (same fallback as bc-diagnosing-bugs); 3895d3d neutral.
- bc-performance-guardrails | BEHAVIOUR | 79a6bb1 9690d8c (11-26, 11-27) | Changes when checks are added: "`bc-setup-project` files an accepted guardrails starter item (for a new project, limits wait until the first code exists); add the checks when executing that item, not during scaffolding" replaces "At project setup ... add checks".
- bc-pipeline-to-done | BEHAVIOUR | fa2d4c1, f7e9af5 (after last test commit 070d270 on 2026-11-27) | execute-issue.md "do not add it ... return `BLOCKED_NEEDS_HUMAN` with the question “May I add `<name>` as a (test) dependency?”"; SKILL.md push question reworded in plain words; "If the tool is missing, ask once whether to run `pi install npm:pi-subagents`"; chat report now short, full report to run-log report.md (CONCEPT.md itself says plain push question, chat report, dependency rule untested)
- bc-plan-to-pipeline | BEHAVIOUR | fa2d4c1 (after 34c6f8e, which holds the 2026-11-26 results) | new step "**Dependencies.** ... ask the owner once ... Record the answer ... `Dependencies: none new`"
- bc-security-audit | BEHAVIOUR | 1b73cb0 (2026-11-26, after tested 2026-11-25) | "If the owner typed its command ... That is an explicit request for a **full audit** ... Do not ask what to review; start the audit." (typed command no longer guidance-only)
- bc-self-improve | NEUTRAL | none (no body commits since v0.3.0) | body unchanged
- bc-setup-project | BEHAVIOUR | 87c64bd, fa2d4c1, f7e9af5, 9690d8c (after test commit 1e74676) | "For a new or empty project, offer `guardrails-for-new-project`, plus `design-for-new-project`..." (previously "Skip starter items for new or empty projects"); also gh check skipped without GitHub remote; sync-tool ignore only when project sits in a synced folder
- bc-subagent-driven-development | BEHAVIOUR | 502ed1a, 3895d3d (2026-11-26, after tested 2026-11-25) | "stop and report on critical or unknown health or if the configured check cannot run. If no storage health check is configured, skip it and note that in one line"
- bc-tdd | BEHAVIOUR | 502ed1a, 3895d3d, 87c64bd | "(otherwise plain `pytest`, with `tmp_path` for test fixtures ...)" fallback; properties.md "only when the project sits in a folder a sync tool replicates ... add them to that tool's ignore list; otherwise create no sync-tool file"
- bc-triage | NEUTRAL | none (no body commits since v0.3.0) | body unchanged
- bc-ui-design | NEUTRAL | none (no body commits since v0.3.0) | body unchanged
- bc-using-git-worktrees | BEHAVIOUR | 502ed1a, 3895d3d | "stop and report on critical or unknown health or if the configured check cannot run. If no storage health check is configured, skip it"; ancestry/patch-equivalence proof now spelled out inline ("`git merge-base --is-ancestor <tip> HEAD`" / `git cherry`), moved from kernel (3895d3d)
- bc-wiki-maintain | NEUTRAL | 3d2c53d (same commit that set tested: 2026-11-27, CONCEPT.md tested line added there; wiki pressure/Installed-search test ran with it) | skill-relative path change: "wiki_skill_dir=\"$HOME/.agents/skills/bc-wiki-maintain\"" replaces $AGENT_CONCEPTS; runner units no longer need AGENT_CONCEPTS edit; no gate changed
- bc-work-sync | BEHAVIOUR | 502ed1a | "a line naming a session the session tool shows as ended (if none is available, report session status as unverified)" — small changed fallback decision; borderline-minor
- bc-writing-plans | BEHAVIOUR | 502ed1a, 3895d3d, 4b05ddf | storage-safe plan rule: "(otherwise plain `pytest`, with `tmp_path` ...)" and storage check "stop on critical or unk..." wording; 4b05ddf only adds an HTML trigger-allow comment (neutral)

# Release audit since v0.4.0 (for v0.4.1, 2026-11-27)

`git diff v0.4.0..HEAD -- concepts/*/body` touches one file: `concepts/bc-delegate-investigation/body/pi.md` (c613156), two added lines in "Failure modes observed on this machine" saying commands over about 20 minutes run from the parent, detached, not inside a worktree worker. It is an observed-failure reference note, accuracy-checked against the session log when written (`.bc-agent/log.md`, 2026-11-27 "long scripts out of worktree workers"): no new stop, requirement or prohibition on the skill's contract. Wording change; no retest. No concept is under "Needs testing".

The rest of this release is release tooling and docs (npm `next` soak, `set-latest` and `github-release` jobs, SECURITY.md, issue form, README fixes), checked by the gate and the release workflow, not by pressure tests.
