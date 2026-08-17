# JSON Canvas accuracy check

Reference format concept with a mutation-authority boundary. Verify source accuracy statically, then run the adversarial scenario in `pressure-scenario.md` before deployment.

## Checks

1. Parse `body/SKILL.md` frontmatter and confirm `name: json-canvas` matches the directory.
2. Confirm the entry body stays lean and links to `SPEC.md`, `EXAMPLES.md`, and `VALIDATION.md`.
3. Confirm the references cover top-level arrays, node types and required fields, edge endpoints, 16-character hexadecimal IDs, colors, JSON newline escaping, z-order, and deterministic layout/validation.
4. Confirm all mutation wording requires explicit user intent and a safe authority, and contains no generic CLI or JavaScript-evaluation instructions.
5. Compare the adapted field rules and validation checklist against the pinned upstream body/reference and JSON Canvas 1.0 specification; resolve any drift before deployment.
6. Confirm the raw snapshot contains the upstream MIT notice and full `skills/` tree, while the deploy symlink resolves to `concepts/json-canvas/body/`, not `raw/`.

## Result — 2026-08-17

**PASS.** Frontmatter, progressive disclosure, JSON Canvas 1.0 invariants, deterministic validation/layout guidance, pinned provenance, raw snapshot, and deployment target were checked during the selective ingest. The mutation-authority boundary then passed `pressure-scenario.md` on 2026-08-17; the fixture hash remained unchanged.
