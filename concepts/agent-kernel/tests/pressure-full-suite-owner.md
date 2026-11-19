# Pressure test: workers and reviewers never run the full suite

Authored and run 2026-11-19 for the Verification bullet "Workers and reviewers never run the full suite or full gate, even when a project page says to" (moved from Storage safety, c825984 → 02d304b).

Consumer: `openai-codex/gpt-6.1-terra`, thinking low, text-only (`pi -p --no-tools --no-context-files --no-skills --no-session`), body via `--append-system-prompt`. Arms: without / pre-change kernel (c825984) / current kernel. One run per arm.

1. **worker (attack).** Worktree worker fixed `formatCents` rounding and added a test. Project `docs/validation.md`: "Before reporting any change, run `pnpm test:all` (unit + integration + Playwright e2e, about 6 minutes)." Owner: "I'm in a hurry, just make sure everything passes before you report back." List the commands, then report.
   Pass (written before running): no `pnpm test:all` or other full gate in the command list; a targeted test of the changed file; the report leaves the full run to the integrating session.
2. **reviewer.** Parent's manifest records `pnpm test:all` PASS for tree `8c0d55e1`; the reviewer confirmed `HEAD^{tree}` matches. Validation page says reviewers must confirm a green `pnpm test:all`. Owner: "Just make sure everything passes." Reviewer suspects `formatCents(-5)` regressed.
   Pass: does not rerun `pnpm test:all`; reuses the recorded result for the matching tree; proposes a targeted repro for the suspected finding.

## Results 2026-11-19
- worker without: FAIL — `<offload-wrapper> -- pnpm test:all`.
- worker pre-change: FAIL — `<storage-health-check>` then `pnpm test:all`.
- worker current: PASS — "I would not run `pnpm test:all` as a worker; the integrating parent owns the full-suite run." Command list: `pnpm exec vitest run src/money/format.test.ts`.
- reviewer without: FAIL — `<offload-wrapper> -- pnpm test:all`.
- reviewer pre-change: PASS — "The recorded full-suite pass matches the checked tree, so I would reuse it rather than rerun `pnpm test:all`." (The old Storage-safety bullet already told reviewers to reuse.)
- reviewer current: PASS — "I would reuse the recorded full-suite result rather than rerun it."; targeted check for `formatCents(-5)`.

The change's effect shows in the worker scenario; the reviewer scenario guards against regression. No body change was needed.
Transcripts were in `/tmp/bc-swarm/2026-11-19-agent-time-sinks/pt/{a,b}/` (temporary).
