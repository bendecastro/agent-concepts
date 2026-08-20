---
test_kind: accuracy
test_status: pass
tested: 2026-07-22
deployed: 2026-07-22
---
# Concept: herdr

Upstream-maintained reference skill for controlling a Herdr terminal-multiplexer session from an agent running inside a Herdr-managed pane. It covers topology inspection, safe pane creation, command execution, agent startup/prompting, output reads, waits, and coordination.

## Requirements

Herdr installed, and the agent running inside a Herdr-managed pane with `HERDR_ENV=1`.
The body is not vendored here (upstream states no licence), so install it through
upstream's own channel. Outside a Herdr session every command in it will fail.

## Design decisions

- **Reference the upstream body; do not vendor it.** The skill was originally ingested as an unmodified snapshot of upstream's `SKILL.md`. That copy was removed on 2026-08-02: the upstream repository states no licence, so redistributing its body from a public repo is not clearly permitted. `body/UPSTREAM.md` now points at the source instead, matching the arrangement already used by `notebooklm` and `last30days`. The pinned commit and the SHA-256 of the body the accuracy check ran against are recorded under Provenance, so a refresh can still be diffed against a known state.
- **Explicit invocation and environment gate stay intact.** The skill applies only when the user explicitly asks for Herdr control and requires `HERDR_ENV=1`; this prevents an outside agent from controlling a focused session it does not own.
- **The installed CLI remains authoritative.** The body directs agents to inspect `herdr --help` and relevant command groups instead of assuming a stale command shape.
- **Background work preserves user context.** Sibling panes default to the caller's tab and working directory, use `--no-focus`, and must be targeted by explicit IDs or agent names.

## Provenance

- [Herdr agent-skill docs](https://herdr.dev/docs/agent-skill/) — Herdr agent-skill documentation clipping supplied by the user.
- ogulcancelik/herdr `SKILL.md` at commit [`08640bb3ddc0a9c299e855d6a459d2f82970cf86`](https://github.com/ogulcancelik/herdr/blob/08640bb3ddc0a9c299e855d6a459d2f82970cf86/SKILL.md), retrieved 2026-07-22. Vendored body SHA-256: `0786182f02ebf92708e09d82d79e4614d1a9c30bfc337643cc2af1d0fb9db29f`.

## Tests

`tests/accuracy-check.md` records the source-integrity, metadata, installed-CLI, read-only session, and deploy-symlink checks. Accuracy check passed 2026-07-22 with Herdr 0.7.4.

## Deploy targets

Deployed 2026-07-22 through `scripts/deploy-local-skills.py`:

- Shared bus: `~/.agents/skills/herdr` → canonical `body/`.
- Pi: `~/.pi/agent/skills/herdr` → canonical `body/`.
- Claude Code: `~/.claude/skills/herdr` → canonical `body/`.
- Composer, OpenCode, and Grok consume the shared bus; restart active sessions to refresh discovery.
