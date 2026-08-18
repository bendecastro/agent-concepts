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
now."

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

## Open question: the anchor guard may be in the wrong home

The skill demonstrably drives behavior on the checks that look like fan-out
work, and demonstrably does not on the two that don't. The document's frame
is "what to do when you go wide," so "summarize this report" and "don't use
agents" both read as outside it, and no amount of broadening a sentence
*inside* that frame makes the guard fire.

That points at a placement error rather than a wording error. "Do not relay
an unanchored claim as fact" is not swarm-specific — it applies to any
agent consuming any other agent's output, which is why it fails precisely
when the swarm frame is absent. Candidate homes: `agent-kernel` (always-on,
but the kernel is deliberately tiny), or `research`/`code-review` (already
evidence-shaped, but neither is loaded during a summarize request either).
Unresolved; do not deploy this concept as the guard's only home.

## Deploy targets

Not yet deployed; blocked on the test gate.

Planned, via `scripts/deploy-local-skills.py`: shared bus
(`~/.agents/skills/bc-swarm`, which also reaches Composer and Grok), Pi
(`~/.pi/agent/skills/bc-swarm`), and Claude Code
(`~/.claude/skills/bc-swarm`). Other harnesses: manual bootstrap; see
`../../harnesses.md`.
