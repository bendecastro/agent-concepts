---
test_kind: pressure
test_status: not-run
tested: never
deployed: no
---
# Concept: naming-things

Model-invoked advisory criteria for clear domain and public code names, applied at first choice or during an explicit audit/rename. Local variables and one-line fixes are excluded.

## Design decisions

- Own naming criteria, not vocabulary persistence, conflict reconciliation or ADR policy: those remain in [domain-modeling](../domain-modeling/body/SKILL.md). The reply lists choices without adding an approval gate; existing reconciliation still applies to conflicts.
- Eight rules and a cold-read test keep the entry lean. Existing-project audit and safe compatibility migration live in `body/rename-recipe.md`, loaded only for that mode.
- **Saved in categories, not implementation locations (2026-10-29).** Supervisor resolved the apparent conflict with domain-modeling's pure-glossary rule: entries list conceptual persistence surfaces only, flagging rename cost without paths, module names or literal keys. Optional exact locations belong beside the single source of truth in code comments, never the glossary.
- Relationship impact: brainstorming, bc-plan-to-issues, writing-plans and bc-init-agent gain one conditional naming load where names are chosen. Their approval, capture, publication, scaffold and execution contracts remain unchanged. Existing outgoing relationships (planning handoffs/loads; kernel storage safety; initializer claim/wiki/teach adapters) are unaffected because these pointers change only name selection, not control flow or host schema. The initializer's incoming teach contract is unchanged: no generated host content changes. Domain-modeling's existing incoming callers retain its unchanged purity, discovery and reconciliation contracts; the new caller delegates rather than restating them. Codebase-design's fixed reference vocabulary is consumed as context, not changed or replaced.

## Provenance

- Owner-approved naming criteria and migration recipe, observed in a private multi-stage automation pipeline rename (2026-10).
- [domain-modeling](../domain-modeling/body/SKILL.md) — glossary purity, persistence, conflict reconciliation and ADR ownership.
- [prompting-agents](../prompting-agents/body/SKILL.md) — explain-the-why, scope discipline, model-invoked composition and progressive disclosure.
- [codebase-design](../codebase-design/body/SKILL.md) — consistent vocabulary and one responsibility behind an interface.

## Tests

[Pressure scenarios](tests/pressure-naming.md) cover new names, persistence pressure, state boundaries, negative invocation and audit/rename artifacts. Authored, not run; no consuming-agent pressure pass is claimed. Pointer consumers have not been re-pressure-tested with this addition.

## Deploy targets

Not deployed. Intended for model invocation through native skill discovery; pressure validation and explicit deployment remain pending. No deployment tooling run.
