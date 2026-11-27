# Ship the kernel as an opt-in package

Why: The README tells strangers to copy the kernel by hand into an always-on instructions file. A copy goes stale, each harness keeps that file in a different place, and setup runs per project while the kernel is per machine. Installing the skills must not silently add always-on rules, so the kernel ships as its own package.
Done when: Pi, Claude Code, Codex and OpenCode each have a separate kernel package built from the one canonical `AGENT-KERNEL.md`; a marker-block install script covers any other harness; setup reports a missing kernel with the install command and writes nothing; README and `docs/guides/harnesses.md` describe it; requirements in [requirements.md](requirements.md).
Stage: now
Blocked by: nothing
Kind: feature
Source: owner decision 2026-11-26 (kernel delivery, option 1); research in the owner's local swarm state (kernel-delivery)
Planned: bc-plan-to-pipeline 2026-11-26
Ready for agent: yes
Held by: pi 01a218e4 since 2026-11-26 22:54 +00:00

## Steps

- [x] Staged package root and fallback script: a build script stages a self-contained package folder (a new `packages/agent-kernel/`) with real Markdown bytes from the canonical kernel; lint or the gate fails when the staged copy drifts; a marker-block install script writes the kernel between versioned begin/end markers into a named instructions file, replaces the block on upgrade, removes it on `--remove`, and leaves every other line untouched. Tests watched failing first. Blocked by: nothing. Stories 1, 5. Done when the drift check fails on an edited copy and the script's install, upgrade, remove and no-op runs pass. Out of scope: harness packages.
  - Review: approved by tier-1 2026-11-26
  - Gate: pass ./scripts/gate at 299f4d7 2026-11-26
  - Landed in `299f4d7`.
- [x] Pi package: a separate package (distinct npm name) whose extension adds the kernel as one fixed structured prompt section, read once per extension instance, same bytes and position for the whole session; the root skills package stays unchanged. Blocked by: step 1. Story 2. Done when a local install loads the kernel in a fresh session, removing it unloads it, and the owner's prompt-cache check passes. Out of scope: npm publishing.
  - Review: approved by tier-1 2026-11-27
  - Gate: pass ./scripts/gate at eb8dbd0 2026-11-27
  - Landed in `eb8dbd0`.
- [x] Claude Code plugin: a second marketplace entry `agent-kernel` with a SessionStart hook that splits the kernel at section boundaries into payloads under the 10,000-character cap (owner answer 2026-11-26: split hook, not a forced output style), reading the bundled Markdown through the plugin root; payload measured against the cap in a test. Blocked by: step 1. Story 2. Done when a user-scope install shows the full kernel at start and after compaction and uninstall removes it. Out of scope: the existing skills plugin.
  - Review: approved by tier-1 2026-11-27
  - Gate: pass ./scripts/gate at bccfbde 2026-11-27
  - Landed in `bccfbde`.
  - Human-only verification: an authenticated Claude Code session with the plugin shows both kernel parts at start and after `/compact` (the build's isolated client was not logged in).
- [ ] Codex and OpenCode packages: Codex plugin with a trusted SessionStart hook (own hooks file, separate from Claude's) and a local marketplace entry; OpenCode V2 plugin adding the kernel through its context hook. Blocked by: step 1. Story 2. Done when each loads the kernel in a fresh session on the local client, or the step records which client version could not be tested as a human-only verification. Out of scope: OpenCode V1.
- [ ] Setup checks for the kernel, and docs: `bc-setup-project`'s survey checks whether the kernel is loaded (package installed, marker block or `# Agent Kernel` heading in the always-on file); when missing it names the install command for the harness and writes nothing; one ideas-file line if the user declines. README Install gains an optional kernel section (install, disable, remove, pins); `docs/guides/harnesses.md` separates package delivery from manual deltas; CONCEPT deploy targets, `index.md`, `.bc-agent/log.md`. Pressure scenario. Blocked by: steps 2 to 4. Stories 3, 4. Done when the with-change run reports the missing kernel and writes nothing while the baseline does not report it; lint has 0 ERROR and the gate passes. Out of scope: kernel content.

## Outcome

