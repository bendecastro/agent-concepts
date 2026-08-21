---
test_kind: pressure
test_status: pass
tested: 2026-08-21
deployed: 2026-08-21
---
# Concept: handoff

User-invoked capture of a session into a portable handoff document, and
pickup of one that is waiting. Synthesized from the four upstream
implementations of the same idea, which contradict each other in three
places; each resolution is recorded below.

Model-invocable only to **offer**. The write itself always needs the
user's word.

## Design decisions

- **One trigger rule, not a list of cases: the context has to survive
  something the live session cannot.** Pocock's docs enumerate four
  travel cases (harness swap, directory change, colleague, forked side
  task) and route everything else to `/compact` — including resuming the
  next morning, on the grounds that you are always still in the session.
  The user confirmed all of those except colleague are real for him, and
  that the overnight and rate-limit case is real too. Compaction cannot
  cross a process boundary, so a closed terminal, an exhausted quota, and
  a reboot belong on the same side of the line as a harness swap. One
  rule covers all five; four cases plus an awkward exception covers them
  worse. This is the concept's only outright departure from Pocock.
- **Narrowness is enforced by a gate, because it is the failure mode.**
  Every upstream implementation that widened past *capture and carry*
  became a generic work protocol (`Lutren/agent-handoff-protocol` is the
  finished form of that drift). The wrong-tool table routes to `/compact`,
  `bc-swarm`, `intercom`, and `AGENTS.md`/ADRs. It began as an
  informational table and **failed the pressure test as an inert guard** —
  nothing in the routing consulted it. It is now routing step 1.
- **File-first; delivery is out of scope.** Pocock ships a second skill
  (`claude-handoff`) that launches `claude --bg` seeded with the summary,
  and djhyes seeds a fresh Codex thread. Both were rejected because the
  user already owns same-machine delivery three times over — `intercom`,
  `herdr` panes, and `bc-swarm`'s spawn-with-a-packet — all pressure-
  tested. Pocock's own docs concede the file's value is portability, not
  summarising. Delivery is one pointer row in the wrong-tool table.
- **Project-local store, anchored to the main checkout.** Pocock uses OS
  temp and his docs list it as the skill's most-reported friction: long
  paths, Codex wiping temp between sessions, `/private/tmp` lost on
  reboot. Temp cannot serve the overnight or cross-machine case at all,
  which the trigger rule puts in scope. Resolution is
  `dirname $(git rev-parse --path-format=absolute --git-common-dir)`,
  falling back to `~/.agent-handoffs/<cwd basename>/` outside a repo.
  The *common* git dir is what makes a linked worktree resolve to the
  main checkout — worktrees are discarded by
  `finishing-development-branch` and by drain runs, so a store inside one
  is lost exactly when it was needed. Verified from a main checkout, a
  linked worktree, and outside a repository (2026-08-21, git 2.55).
- **`.bc-agent/` was considered and rejected by the user.** It would have
  made handoffs qmd-searchable prior art; the cost is stale transit
  documents surfacing in vault searches months later, mixed in with
  durable knowledge. The user chose the two-tier resolution instead.
- **One command, not a resolver script.** status203 ships ~60 lines of
  bash for store resolution with conf lookup and `${VAR}` expansion. The
  escape hatch it buys has no demand yet; `minimal-solution-ladder` stops
  at the rung that holds.
- **`active/` → `consumed/`, where location encodes state.** From
  status203. Pickup is an `mv`, which *claims* the handoff so a parallel
  session cannot pick up the same one, is atomic, and is one `mv` to
  undo. No status field to drift, and the scan only ever globs `active/`.
- **Ignored via `.git/info/exclude`, not `.gitignore`.** Handoffs are
  conversational, so they catch secrets more readily than code, and git
  history keeps one after the file is stripped. `.gitignore` is tracked,
  so writing to it is a repo change the user must commit, and in a public
  repo it advertises a personal workflow directory to everyone who
  clones. `info/exclude` is local-only and read from the common dir, so
  linked worktrees inherit it — verified 2026-08-21 from both a main
  checkout and a linked worktree. status203's `git check-ignore` leak
  check is kept as a backstop for the case the default misses (a
  whitelisted or force-added path), with exit 128 treated as "git will
  not carry it".
- **Prose and telegraphic, split by section.** orzilca mandates
  telegraphic fragments with a 100-line hard cap; status203 mandates
  prose because fragments lose the rationale. Both cite the same example
  and reach opposite conclusions. Resolved by section: prose where the
  reasoning is the payload (Decisions and dead ends), telegraphic where
  the section is an index (State, Key files). The hard line cap was
  dropped — it makes the agent cut prose, and prose is the only part not
  reconstructable from the repository.
- **A Verified / unverified / broken section, from orzilca.** It answers
  the weakness Pocock's docs confess: the next agent treats the document
  as a contract and will not re-check it, so a belief written as a fact
  becomes a false premise for everything after. It is also the kernel's
  evidence-before-claims rule expressed as an artifact. `writing.md`
  pairs it with a self-scan step. Pressure-tested: the never-run test
  suite landed under **Unverified**.
- **The guard header travels inside the document.** orzilca's pickup rule
  (the handoff is data, not instructions) is the single most valuable
  paragraph across all four repos, but it only protects a receiver that
  has the skill installed. Codex and Gemini do not read the shared skills
  bus, and a colleague's machine has none of this. A non-optional,
  non-paraphrased block at the top of every handoff makes the guard
  survive landing anywhere.
- **Invoking pickup is not approval to act.** Also orzilca's, kept in its
  strict form: even "pick it up and get going" earns a briefing first,
  because the user cannot have approved contents they have not seen. Held
  under pressure across three runs.
- **The ledger insight without the ledger machinery.** status203's
  observation is real — a handoff is consumed once, so across a relay the
  settled conclusions decay and a later session rederives them. Their fix
  is a flow that proposes creating a ledger file. For this workspace that
  would invent a fifth durable store next to ADRs, `CONTEXT.md`,
  `.bc-agent/out-of-scope/`, `docs/changes/<slug>/` and `docs/specs/`,
  and `domain-modeling` already owns the bar for when a decision earns an
  ADR. The section is a pointer list to stores that already exist,
  carried forward on every relay, contents never restated. Where no such
  store exists, the skill says the relay will decay rather than creating
  a file.
- **Not crash insurance.** Tempting, given the incident behind
  `bc-swarm`, and rejected on the user's confirmation. That contract
  (manifest before dispatch, per-child artifacts checkpointed
  incrementally) survives without anyone remembering to act, where a
  handoff needs a live agent that notices in time. And speculative
  checkpoints would poison the pickup flow: an `active/` pool full of
  never-meant-to-be-picked-up files breaks the single-active auto-select
  that makes pickup one keystroke.
- **One concept with progressive disclosure, not two skills.** orzilca
  ships `handoff-prepare` and `handoff-continue` separately, which puts
  two competing entries in every harness's skill list. Lean `SKILL.md`
  routes; `writing.md` and `pickup.md` load only on the branch taken.
- **No per-harness bodies.** Once delivery was out of scope, nothing
  varied by harness: store resolution is git, the format is Markdown, and
  pickup is "read this file". `bc-swarm`'s `body/pi.md` split exists
  because its mechanics genuinely differ; this one's do not.
- **Name kept as `handoff`.** What every upstream calls it and what the
  user asked for. No `bc-` prefix: that marks the user's own composite
  orchestrators (`bc-plan-to-issues`, `bc-drain-issues`, `bc-swarm`),
  and this is an adaptation of external work, like `grilling` and
  `code-review`.

## Provenance

Sources captured 2026-08-21; see
[`docs/research/raw/ingested/handoff-skills-upstream/`](../../docs/research/raw/ingested/handoff-skills-upstream/SOURCE.md)
for commits, licenses, and the verbatim MIT-licensed bodies.

- [mattpocock/skills](https://github.com/mattpocock/skills) `@0ab1b63`
  (MIT) — `skills/productivity/handoff`, `skills/in-progress/claude-handoff`,
  and `docs/productivity/handoff.md`. Source of reference-by-path, the
  suggested-skills section, redaction, the narrowness argument, and the
  confident-claims failure mode. The docs page carries more of the design
  than either skill body.
- [status203/handoff-skill](https://github.com/status203/handoff-skill)
  `@c833815` (**no license declared** — cited, not vendored, per the
  `unslop-cursor` precedent). Source of the `active/`→`consumed/` store,
  the ledger observation, the `git check-ignore` leak check, and
  empty-section honesty.
- [orzilca/agent-handoff-skills](https://github.com/orzilca/agent-handoff-skills)
  `@a6233e0` (MIT) — the pickup guard, invocation-is-not-approval, the
  verified/unverified/broken section, and the write-flow scope rule.
- [djhyes/context-handoff](https://github.com/djhyes/context-handoff)
  `@a350295` (MIT) — `PreCompact` auto-invocation and seeding the handoff
  into the new thread's prompt. Neither adopted; both recorded as the
  next rungs if file-first proves insufficient.
- [Lutren/agent-handoff-protocol](https://github.com/Lutren/agent-handoff-protocol)
  (MIT) — read and deliberately not used; named in `SOURCE.md` as the
  shape this concept avoids.
- `concepts/prompting-agents/body/SKILL.md` — altitude, explain-the-why,
  and gates reserved for in-the-moment rationalization. Both pressure-test
  tunes came from its metaprompting operation (locate the mechanism;
  relocate rather than add emphasis).
- `concepts/code-review/body/SKILL.md` — the inert-guard class, which is
  what check 7's first failure turned out to be.

## Tests

`tests/pressure-handoff.md` — discipline-enforcing, so the test gate
applies. Seven checks; 1, 2, 3, and 5 are load-bearing (an injected
document driving real actions, a briefing gate folding under one
impatient sentence, a tree that no longer matches its document, and a
secret written to a file).

**Run 2026-08-21: PASS 7/7 after two tunes.** First pass 5/7; both
failures were guards that could not compete rather than missing rules,
and both were fixed by relocating an existing rule. Consumer was
`xai/grok-4.6` at low thinking, not the author's model. Full detail,
including two recorded non-blocking observations, in the test file.

## Deploy targets

Deployed 2026-08-21 via `scripts/deploy-local-skills.py`:

- Shared bus: `~/.agents/skills/handoff` → `body/` (also reaches
  Composer and Grok).
- Pi: `~/.pi/agent/skills/handoff` → `body/`.
- Claude Code: `~/.claude/skills/handoff` → `body/`.

Other harnesses: manual bootstrap; see `../../docs/harnesses.md`. Codex
and Gemini are the reason the guard header travels inside the document.
