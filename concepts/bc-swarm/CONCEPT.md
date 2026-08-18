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
- **The tooth names role, model, and thinking, not just child/parent.** The
  user wants to see the fleet's cost and capability at the same decision
  point. Cadence stays announce-then-launch: a wait-for-ok on every swarm
  would fight the go-wide posture. Chat uses this session's routing names,
  not vendor ids (the `Luna max` shape in the body is an example of that
  vocabulary, not a portable requirement). The same fields go on the
  manifest so the durable copy matches. Parent-kept tracks stay parent +
  why; they are not subagents. The list is a promise: on Pi, pass `thinking` on
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
  swarm resumption is not a demonstrated need.
- **Evidence anchors are the thin-parent guard.** Aggressive delegation
  buys speed by thinning the parent's context, which silently removes its
  ability to catch a confidently wrong child. Re-reading everything defeats
  the delegation and trusting everything scales confabulation with fan-out;
  an anchor makes spot-checking cheap and constant per claim. Verifying
  *all* anchors was considered and rejected as the same cost as re-reading.
- **Read-shaped, with a handoff.** Investigation, analysis, and review
  only. `subagent-driven-development` and `bc-drain-issues` already own
  implementation fan-out with worker packets, spec/standards review,
  worktree isolation, and rework loops. A thinner competing path would lose
  in ways nobody notices until something is merged, and keeping children
  read-only keeps the durability contract simple: artifacts are files, not
  conflicting edits.
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

## Tests

`tests/pressure-bc-swarm.md` — discipline-enforcing, so the test gate
applies before deploy. Five checks attacking the predictable excuses: skip
the manifest because it's only a few children, re-run the whole fan-out
instead of recovering, accept a fluent unanchored child report, "just read
it yourself, it's faster", and "run it synchronously so I can see results
now." Check 1 also grades the listing fields: each child line in chat and
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

Other harnesses: manual bootstrap; see `../../harnesses.md`.

**Dependency:** the thin-parent guard's consumption half lives in
`agent-kernel`. Until that delta is propagated to a harness's always-on
instructions, this skill enforces anchors in packets but nothing stops that
harness relaying an unanchored claim as fact.
