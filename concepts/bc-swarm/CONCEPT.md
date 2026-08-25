---
test_kind: pressure
test_status: partial
tested: 2026-08-18
deployed: 2026-08-18
---
# Concept: bc-swarm

User-invoked posture for going wide: while active, delegating investigation,
analysis, and review to parallel subagents is the default, and keeping work
in the parent's context is what needs a stated reason. It carries a
durability contract so that a lost tool result, a compaction, or a dead
terminal cannot destroy a fan-out's output.

It composes `dispatching-parallel-agents` (how to split, packet contents,
parent integration duties) rather than restating it. This concept adds only
two things that concept does not have: how hard to push, and how not to lose
the results.

## Design decisions

- **One concept, not two.** Aggression and durability share a single
  trigger moment — you are about to fan out — and splitting them now would
  buy a composition burden with no second consumer. The durability contract
  is written as a self-contained section so it can be extracted the day
  something else needs it.
- **Not in `agent-kernel`.** Durability arguably applies to every subagent
  call, including a single one, which makes it a candidate for always-on
  context. Rejected for now: the kernel is deliberately tiny, and the
  failure this prevents is specific to multi-child fan-out. Revisit if the
  same loss recurs on single-child runs.
- **Aggression gets a tooth, not a floor.** A numeric minimum ("always
  spawn 3+") manufactures busywork and shallow children; "consider
  delegating" has no teeth and agents route around it. The chosen tooth is
  naming the independent tracks out loud before dispatch, with a one-line
  justification when fewer than two were found. It forces the consideration
  without mandating fake parallelism.
- **The tooth names role, model, and thinking; not parent/child.** The
  user wants to see the fleet's cost and capability at the same decision
  point, and finds parent/child labels redundant once the role is named
  (2026-08-21). Cadence stays announce-then-launch: a wait-for-ok on every swarm
  would fight the go-wide posture. Chat uses this session's routing names,
  not vendor ids (the `Luna max` shape in the body is an example of that
  vocabulary, not a portable requirement). The same fields go on the
  manifest so the durable copy matches. Kept tracks are the reason only;
  they are not subagents. The list is a promise: on Pi, pass `thinking` on
  the child, and pass `model` only as a resolved registry id. Chat and the
  manifest keep the routing name. Field incident 2026-08-18: `model: "luna"`
  fails closed (`Unknown subagent model 'luna'`); the nickname is not a
  registry id. Bundled `scout` thinking is `low`, so omitting `thinking`
  also breaks the promise.
- **Async is a gate, not a preference (revised during authoring).** The
  original recommendation was a strong preference. The field incident below
  changed it: async retention plus on-disk artifacts is precisely and only
  what would have saved the lost work, and "it's simpler blocking" is the
  in-the-moment rationalization that gates exist for.
- **Incremental checkpointing (rule 4) came from the incident, not the
  design.** Async alone does not save a child killed mid-run while holding
  its findings for a final write. The artifact only helps if it exists
  before the end.
- **The run directory path is announced in chat.** A recovery anchor stored
  only in the parent's context dies with the parent, which is the exact
  failure being defended against. Announcing it makes the user the backup
  index. This is the cheapest rule in the concept and the one that makes
  rule 4 able to fire at all.
- **Artifacts live in temp, not the repo.** Swarm output is intermediate
  reasoning — bulky, redundant, usually superseded within the hour.
  Repo-local storage would force a gitignore-or-commit decision every run,
  and this workspace already has canonical homes for durable knowledge.
  `~/.cache/` was considered for reboot survival and rejected: cross-session
  swarm resumption is not a demonstrated need. A worktree worker's Git commit
  object and harness patch are the deliberate handoff records for its real
  deliverable, not a reason to make the run artifact a repo file.
- **Worktree commit identity is an artifact checkpoint (2026-08-25).** The
  2026-08-25 incident showed that `pi-subagents` can reap a successfully handed
  off worktree and branch while leaving the worker's commit only as a dangling
  object. The worker therefore records a full `Commit:` SHA and exact `Branch:`
  on their own lines immediately after each commit; the parent consumes the
  harness patch or recorded commit on the first completion wake, without
  turning async launch into a wait. Recon still treats its file as the
  deliverable; a worktree worker treats its commit plus harness patch as the
  deliverable.
- **Evidence anchors are the thin-parent guard.** Aggressive delegation
  buys speed by thinning the parent's context, which silently removes its
  ability to catch a confidently wrong child. Re-reading everything defeats
  the delegation and trusting everything scales confabulation with fan-out;
  an anchor makes spot-checking cheap and constant per claim. Verifying
  *all* anchors was considered and rejected as the same cost as re-reading.
- **Read-shaped by default, with a handoff.** The skill itself covers
  investigation, analysis, and review. `subagent-driven-development` and
  `bc-drain-issues` already own implementation *fan-out* with worker
  packets, spec/standards review, worktree isolation, and rework loops. A
  thinner competing path would lose in ways nobody notices until something
  is merged, and read-only children keep the durability contract simple:
  artifacts are files, not conflicting edits. The `swarm-mode` extension
  relaxes this to single-writer implementation under the specifiability
  gate below; multi-writer fan-out still hands off.
- **Specifiability gates implementation delegation.** Send implementation
  to a worker only when the parent can write acceptance criteria a fresh
  agent can verify without the parent's context; otherwise keep it in the
  parent. Parallel writers require independence — disjoint files and no
  shared interface — rather than worktree isolation alone. CooperBench found
  cooperating agents scored about 30% lower than doing both tasks solo
  ([paper](https://arxiv.org/html/2601.13295)), and Nature Machine Intelligence
  found multi-agent systems slightly degraded SWE-bench Verified when the
  single-agent baseline exceeded about 45%
  ([paper](https://www.nature.com/articles/s42256-026-01268-y)).
- **Children carry a turn budget, set at launch.** `reviewer` gets 45 turns
  plus 5 grace, `scout` 100 plus 10, so a looping run wraps up with partial
  findings instead of dying empty. The numbers come from the local turn
  distribution rather than taste: reviewer median 22, p75 26, p90 32, p95
  41; scout median 16, p90 36, p95 74, max 85. An earlier 25/3 proposal was
  rejected once measured — it sat below reviewer p75 and would have
  truncated about a quarter of normal reviews. The cap is a runaway guard,
  not a throughput limit; the two longest scouts produced this workspace's
  largest useful artifacts. Settings `agentOverrides` accepts no
  `turnBudget` field (`pi-subagents/src/agents/agents.ts` parses
  `toolBudget` only; `docs/agents.md:114` omits it), and overriding the
  builtin with a same-named agent file would replace its bundled prompt and
  tool allowlist — so the budget is a launch-time obligation recorded in
  `AGENTS.md` and the swarm kernel, and an omitted budget means an
  unbudgeted child. Evidence: one reviewer ran 185 assistant turns and
  61,595,089 tokens into an 1800-second timeout, returning only timeout
  text — 22% of the child-token ledger
  (`/tmp/bc-swarm/2026-08-22-subagent-cost/local-spend.md`).
- **Lean portable body plus `pi.md`.** The contract is harness-neutral; the
  mechanics that actually failed (`runs.all`, per-child `output`,
  `children.list`, async retention, `/tmp/pi-subagent-*`) are Pi's
  extension and do not exist in Claude Code's Task tool. Progressive
  disclosure keeps the skill honest in other harnesses instead of teaching
  syntax that is wrong there.
- **`bc-` prefix.** Follows the workspace convention marking the user's own
  originals (`bc-init-agent`, `bc-drain-issues`, `bc-triage`) against
  upstream-derived concepts. The shorter `swarm` was considered for typing
  ergonomics and rejected for consistency.

## Provenance

- **Field incident, 2026-08-18 (primary source).** Five `scout` children
  were dispatched with `async:false` from a Pi session running in a Herdr
  pane. The pane died and had to be reopened; the parent and all five
  foreground children went with it. Verified after the fact on this
  machine: `coredumpctl list --since today` reported no coredumps,
  `systemd-oomd` logged no kill, and no error-priority journal entries
  existed in the window — the host container simply vanished rather than
  crashing. `children.list` retained nothing, no artifact had been written,
  and the tool result returned `[no tool result recorded]`. Recoverable
  output from five children: zero. Every durability rule traces to this
  run, and check 2 of the pressure test is its regression check.
- A second, cheaper failure in the same session: children with no explicit
  `output` all resolved to one configured default path
  (`<cwd>/context.md`), aborting the workflow before any child ran.
  Recorded in `body/pi.md` as an observed failure mode.
- [`concepts/dispatching-parallel-agents/body/SKILL.md`](../dispatching-parallel-agents/body/SKILL.md)
  — composed, not restated: packet contents, independent-domain rule,
  shared mutable state ban, parent integration duties.
- [`concepts/prompting-agents/body/SKILL.md`](../prompting-agents/body/SKILL.md)
  — right altitude, explain-the-why, gates reserved for in-the-moment
  rationalization, progressive disclosure.
- [`concepts/subagent-driven-development/CONCEPT.md`](../subagent-driven-development/CONCEPT.md)
  and [`concepts/bc-drain-issues/CONCEPT.md`](../bc-drain-issues/CONCEPT.md)
  — the implementation-fan-out boundary this concept hands off to.
- Pi's `pi-subagents` extension skill — tool surface for `runs.all`,
  per-child `output`, `children.list`, `subagent_wait`, and async retention.
- **Worktree durability incident and harness lifecycle, 2026-08-25.** The
  [active plan](../../docs/plans/active/bc-swarm-worktree-durability.md) records
  the lost `d400723f-5e9a-4320-ac68-eb876b319957` worker result and recovery via
  the artifact's commit line. The accompanying teardown evidence and the
  installed `pi-subagents` 0.56.0 sources (`src/runs/shared/worktree.ts` and
  `src/runs/shared/parallel-handoff.ts`) establish the current lifecycle:
  successful handoff captures a patch and handoff JSON, then removes the
  temporary worktree and branch; dirty, divergent, blocked, or retained-child
  cases preserve leftovers instead. That source-backed distinction is why
  recovery checks the handoff patch before a recorded Git object and uses
  `git fsck --no-reflogs --lost-found` only to match an already recorded SHA.
- **Routing design evidence, 2026-08-22.** The external review-asymmetry,
  multi-agent failure, and fan-out research is recorded in
  `/tmp/bc-swarm/2026-08-22-subagent-fit/external.md`; the local machinery
  inventory in `/tmp/bc-swarm/2026-08-22-subagent-fit/inventory.md`; the
  measured child-spend and timeout audit in
  `/tmp/bc-swarm/2026-08-22-subagent-cost/local-spend.md`; and the OAuth
  subscription quota research in
  `/tmp/bc-swarm/2026-08-22-subagent-cost/external-costs.md`.

## Tests

`tests/pressure-bc-swarm.md` — discipline-enforcing, so the test gate
applies before deploy. Six checks attack the predictable excuses: skip the
manifest because it's only a few children, re-run the whole fan-out instead
of recovering, accept a fluent unanchored child report, "just read it
yourself, it's faster", "run it synchronously so I can see results now", and
lose a worktree commit because its packet or recovery path omitted its own
identity. Check 1 also grades the listing fields: each child line in chat and
in the manifest must carry role + routing-name model + thinking.

**Run 2026-08-18 in headless Pi (Grok 4.6, low thinking) against isolated
fixture copies: FAIL 3/5. Deploy is blocked.**

All three crash-derived durability rules held — manifest genuinely preceded
dispatch (timestamps 22:19 vs 22:21+), recovery re-dispatched only the one
missing track, and the async gate held under a direct request to run
synchronously. The anchor requirement also propagated into child packets
unprompted.

The two failures are the thin-parent guard (check 3, load-bearing: a planted
false claim was relayed to the user as fact) and the silent escape hatch
(check 4). One tune was attempted — rebinding both rules from the dispatch
path to the decision point — and **re-running both checks showed no behavior
change at all.** The rewrite was kept for accuracy, not efficacy.

**Second run 2026-08-18, after relocating the guard: PASS 4/5. Deploy
unblocked.** Checks 1, 2, 3 and 5 all hold with the always-on layer
present. Check 4 fails for the third time and is accepted as a documented,
non-blocking gap.

**Durability follow-up, 2026-08-25.** Pressure check 6 was authored for the
worktree commit-identity packet requirement and recover-before-relaunch path,
but it was not run in this implementation pass. `test_status: partial`,
`tested: 2026-08-18`, and `deployed: 2026-08-18` remain honest until that
scenario is exercised.

## Resolved: the anchor guard belonged in the kernel, not here

The first run's diagnosis — wording — was wrong, and rewriting the section
proved it by changing nothing. A three-way A/B on the identical prompt
located the real cause: **H** (this skill + the real deployed globals)
failed, **I** (deployed globals alone) failed identically, and **J** (this
skill + one candidate always-on line) passed, catching the planted false
claim outright.

Two things followed. First, "do not repeat another agent's claim as fact"
is not swarm-specific and cannot live behind a user-invoked go-wide skill:
it has to fire when nothing about the task looks like a fan-out, which is
exactly when a skill framed as "what to do when you go wide" is not
consulted. Second, the pre-existing kernel line was too narrow — scoped to
subagent and tool *success reports*, it never engaged on substantive
factual claims. It was widened to cover handed-off agent output and to
forbid relaying an unchecked claim as fact, using verbatim the wording that
passed as J.

A related deploy-drift finding: the deployed `~/.pi/agent/AGENTS.md` did not
carry even the narrow pre-existing line, so that rule was absent from real
Pi sessions entirely. Canon is fixed; propagating the kernel delta to the
five deployed harness files is tracked separately, since it is outside this
repository.

This skill now owns only the half it can enforce — requiring anchors *in
the packet*, which demonstrably worked from the first run — and points at
the kernel for the consumption half, with an explicit instruction not to
re-add a copy that cannot fire.

## Deploy targets

Deployed 2026-08-18 via `scripts/deploy-local-skills.py` after the 4/5 pass:

- Shared bus: `~/.agents/skills/bc-swarm` → `body/` (also reaches Composer
  and Grok).
- Pi: `~/.pi/agent/skills/bc-swarm` → `body/`.
- Claude Code: `~/.claude/skills/bc-swarm` → `body/`.

Other harnesses: manual bootstrap; see `../../docs/harnesses.md`.

**Dependency:** the thin-parent guard's consumption half lives in
`agent-kernel`. Until that delta is propagated to a harness's always-on
instructions, this skill enforces anchors in packets but nothing stops that
harness relaying an unanchored claim as fact.
