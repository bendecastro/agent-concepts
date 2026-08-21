# Source: session-handoff skills — the four upstream implementations

Citation record for the sources behind the `handoff` concept. Captured
2026-08-21 by agent, via shallow `git clone` of each repository.

## Primary sources

| Repo | Commit | License | Captured |
|---|---|---|---|
| [mattpocock/skills](https://github.com/mattpocock/skills) | `0ab1b63` | MIT (© 2026 Matt Pocock) | verbatim in `captured-skills.md` |
| [orzilca/agent-handoff-skills](https://github.com/orzilca/agent-handoff-skills) | `a6233e0` | MIT (© 2026 orzilca) | verbatim in `captured-skills.md` |
| [djhyes/context-handoff](https://github.com/djhyes/context-handoff) | `a350295` | MIT (© 2026 djhyes) | verbatim in `captured-skills.md` |
| [status203/handoff-skill](https://github.com/status203/handoff-skill) | `c833815` | **none declared** | **cited only, not vendored** |

`status203/handoff-skill` has no `LICENSE` file. Following the
`unslop-cursor` precedent, its text is not redistributed in this public
repository; the upstream URL is the authority, and the `handoff` concept
adapts its ideas rather than its wording.

## What each contributed

- **mattpocock/skills** — two skills (`skills/productivity/handoff`,
  `skills/in-progress/claude-handoff`) plus the docs page
  `docs/productivity/handoff.md`, which is substantially more valuable
  than either skill. Source of: reference-artifacts-by-path, the
  suggested-skills section, secret redaction, and the argument that this
  skill is *narrow* — it earns its keep only when work has to travel.
  Also the source of the failure mode the concept's Verified section
  answers: "a belief written as a fact becomes a false premise" for a
  next agent that treats the document as a contract.
- **status203/handoff-skill** — the `active/` → `consumed/` store where
  location encodes state and pickup is an `mv` that atomically claims the
  handoff; the **ledger** observation (handoffs rot across a relay, so
  durable invariants need a home that is re-read rather than relayed);
  the `git check-ignore` leak check; empty-section honesty.
- **orzilca/agent-handoff-skills** — the pickup guard, which is the
  single most valuable paragraph across all four repos: *the handoff is
  data, not instructions*; text inside the file never authorizes action,
  and invoking the skill is not approval to work. Also the
  `verified / unverified / broken` section, the telegraphic budget, and
  the write-flow scope rule (writing the file is the entire task; no
  "one last fix" first).
- **djhyes/context-handoff** — `PreCompact` hook invocation and the
  practice of seeding the full handoff into the *new thread's prompt*
  rather than trusting a file to be read. Neither was adopted; both are
  recorded because they are the natural next rungs if the file-first
  design proves insufficient.

## Read and deliberately not used

- [Lutren/agent-handoff-protocol](https://github.com/Lutren/agent-handoff-protocol)
  (MIT, © 2026 Luis Rene Gonzalez) — a generic read/scope/execute/
  validate/commit work protocol wearing a handoff name. Its handoff
  content is a template; everything else duplicates disciplines this
  workspace already holds in `code-review`, `bc-drain-issues`, and the
  kernel's git rules. Named here as the shape the `handoff` concept
  deliberately avoids: every implementation that widened past "capture
  and carry" turned into a work protocol.
- [Phat-Po/agent-handoff-skill](https://github.com/Phat-Po/agent-handoff-skill),
  [leantli/agent-handoff](https://github.com/leantli/agent-handoff),
  [thepushkarp/handoff](https://github.com/thepushkarp/handoff),
  [Yongthyuan/agent-context-bridge](https://github.com/Yongthyuan/agent-context-bridge),
  [awithi-co/acdc](https://github.com/awithi-co/acdc),
  [OpenMOSS/claude-codex-handoff](https://github.com/OpenMOSS/claude-codex-handoff),
  [se4thvin/context-handoff](https://github.com/se4thvin/context-handoff)
  — surfaced in the same search, surveyed at README level, not read in
  full. Nothing in their summaries offered an idea absent from the four
  above. `OpenMOSS/claude-codex-handoff` is the interesting outlier (an
  append-only two-agent message bus with leases and cursors), but that is
  live inter-agent coordination, which this user already holds in
  `pi-intercom` and `herdr`.

## Why filed

The `handoff` concept synthesizes four implementations that contradict
each other in three places — prose versus telegraphic style, whether the
same-harness overnight case belongs to handoff or to `/compact`, and
whether a ledger needs its own creation flow. Each resolution needs a
traceable source for a future agent to re-evaluate.
