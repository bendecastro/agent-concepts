# check-work

User-invoked Grok self-verification orchestrator: spawn a verifier subagent to review diffs, run builds/tests, and loop fixes until pass — supports same-turn (post-task) and standalone modes.

## Design decisions

- **Upstream-maintained body (user-scope).** Lives at `~/.grok/skills/check-work/`; xAI-shipped, not vendored here.
- **Complements agent-kernel verification.** Kernel says verify before claims; this skill operationalizes that with a structured subagent loop and optional focus area.
- **Overlap with obra verification-before-completion.** Absorbed at provenance level only — no duplicate runtime concept; this is the Grok-native orchestrator with concrete steps.

## Provenance

- `raw/grok-user-skills/snapshot/check-work/SKILL.md`

## Tests

Discipline-enforcing. Pressure scenarios not yet authored.

## Deploy targets

- **Grok:** `~/.grok/skills/check-work/` (user-scope; auto-discovered).
- **Other harnesses:** manual bootstrap or adapt into harness-specific verify flows.