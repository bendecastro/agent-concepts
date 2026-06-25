# Concept: dispatching-parallel-agents

Model-invoked coordination pattern for splitting independent investigations or reviews across fresh, isolated agents while the parent remains responsible for integration.

## Design decisions

- **Coordination, not abdication.** Parallel agents accelerate independent domains; the parent still scopes prompts, reviews outputs, checks conflicts, and verifies the combined result.
- **Independence gate.** The body is strict about not parallelizing related failures or shared-state edits, because parallelism can amplify confusion.
- **Pi-compatible.** Upstream Task-tool examples are translated to a generic subagent packet usable with Pi `subagent`, Claude Code, or another harness.

## Provenance

- `raw/obra-superpowers/skills/dispatching-parallel-agents/SKILL.md` — one-agent-per-independent-domain rule, prompt structure, integration checklist.
- `concepts/bc-drain-issues/` — local AFK executor uses a stricter issue-queue variant; this concept covers ad hoc parallel diagnosis/review.

## Tests

`tests/scenario.md` — pending pressure run for independent vs related failures, over-broad prompt rejection, and parent-side verification.

## Deploy targets

Not deployed yet. Discipline-enforcing concept; deploy after pressure test.
