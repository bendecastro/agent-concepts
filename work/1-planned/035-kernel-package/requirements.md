# Requirements: ship the kernel as an opt-in package

## Solution

1. **One source, staged copies.** `concepts/agent-kernel/body/AGENT-KERNEL.md` stays the only edited file. A build script stages a self-contained package folder with real bytes (no symlinks out of the package root: Claude Code does not copy files outside the plugin folder). A check fails when a staged copy differs from canon.
2. **Separate packages.** The kernel never rides in the skills packages. Pi: own package with an extension that adds a fixed prompt section. Claude Code: own plugin entry in the existing marketplace. Codex: own plugin with a trusted SessionStart hook. OpenCode: own V2 plugin. Each installs, disables and removes on its own.
3. **Prompt cache.** Read the kernel once per session and keep its bytes and position fixed; no mid-session reload.
4. **Fallback script.** For any other harness, or users who prefer a file: versioned begin/end markers around the kernel in an instructions file the user names; install, upgrade in place, remove; nothing outside the block changes.
5. **Setup only checks.** Setup is per project and the kernel is per machine, so setup reports a missing kernel and the install command, and writes nothing.

## User Stories

1. As a stranger, I install the kernel with one command and upgrade it by upgrading the package.
2. As a stranger on Pi, Claude Code, Codex or OpenCode, the kernel loads in every session after one install.
3. As a stranger, installing the skills alone adds no always-on rules.
4. As a stranger, setup tells me when the kernel is missing and how to add it.
5. As a stranger on another harness, a script adds and removes the kernel without touching my own lines.

## Testing Decisions

Unit tests for the build/drift check and the marker script (install, upgrade, remove, no-op, foreign lines untouched). Live smoke per harness: fresh install, first request, resume or compaction, removal. Pi prompt-cache check. Claude payload size test against the 10,000-character hook cap. Pressure scenario for the setup check (missing kernel reported, nothing written).

## Out of Scope

- Kernel content; publishing to npm or other registries; OpenCode V1; deciding auto-update pins for users.

## Evidence

Research report `kernel-delivery.md` in the owner's local swarm state, 2026-11-26: Pi `before_agent_start` and structured sections (Pi 1.6.1 docs); Claude Code SessionStart `additionalContext` capped at 10,000 characters per payload, output styles with `force-for-plugin`; Codex plugin SessionStart developer context, plugin `AGENTS.md` not discovered; OpenCode V2 context hook or `instructions` array. Kernel size measured 2026-11-26: 14,435 characters.
