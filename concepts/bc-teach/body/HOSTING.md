# Teach hosting: the marker and hosted path maps

This file is the one home for how `bc-teach` state maps onto a hosted `.bc-agent` vault: the
marker, the two path maps and the never-create rules. `bc-teach` resolves its hosted paths from
it, `bc-setup-project`'s scaffold keeps its marker text in step with it (a test fails when they
disagree), and `bc-wiki-maintain` reads its teach-owned boundary from it. Why: three copies could
drift silently.

## The marker

The marker is `references/teach-skill.md` inside the `.bc-agent` vault
(`.bc-agent/references/teach-skill.md` from the project root). It is valid only when its first
line is exactly `<!-- teach-host-adapter: v1 -->` and its complete `## Hosted teach path map`
table exactly matches one of the two maps below (they differ only in the Glossary row). A
prefix-only, missing-row, or altered-map file is incomplete and is not a host contract. Do not
infer a host from directory names alone when the marker is absent.

The marker is a thin path adapter, not a generic config framework or a copied teach body. It is
the opt-in for an existing initializer host, never an instruction to run `bc-setup-project`.

## Vault host map

A vault host (the `learning` archetype) uses this map. All paths are relative to `<teach-root>`,
the marked `.bc-agent` directory:

| Teach surface | Hosted path | Owner |
|---|---|---|
| Mission | `learning/plan.md` (no hosted `MISSION.md`) | `bc-teach` |
| Review queue | `learning/review.md` | `bc-teach` |
| Learning records | `learning/records/` | `bc-teach` |
| Lessons and session artifacts | existing `sessions/` (never `learning/sessions/`) | `bc-teach` |
| Notes | `learning/notes.md` | `bc-teach` |
| Raw sources | existing `sources/` | `bc-teach` |
| Compiled knowledge / wiki concepts | existing `concepts/` | `bc-teach` |
| Resource catalog | `references/teach-resources.md` | `bc-teach` |
| Glossary | the existing Glossary section of `project/overview.md` | `bc-teach` |
| Catalog and history | shared `index.md` and `log.md` | `bc-setup-project` host schema; `bc-teach` updates teach entries |

In a vault host `bc-teach` owns the Glossary section of `project/overview.md`; planning and
maintenance skills leave that section alone, and its other sections stay with their owners.

## Hybrid host map

A visible-layout hybrid host (code or operations work plus learning) uses the vault map except
for the Glossary row, which names the project's root `glossary.md`, one level above
`<teach-root>`:

| Teach surface | Hosted path | Owner |
|---|---|---|
| Glossary | the project's root `glossary.md` (`../glossary.md`), shared with the project | the project; `bc-teach` adds and refines learner terms |

In a hybrid host there is one glossary. Add and refine the terms the learner needs there, in
that file's one-line format, and do not remove or redefine project terms without asking the
user; `bc-domain-modeling` and planning skills keep using the same file.

## Never create

- No root `MISSION.md`, `REVIEW.md`, `GLOSSARY.md`, `RESOURCES.md`, or `NOTES.md` in a hosted
  workspace.
- No `learning/sessions/`; lessons and session artifacts use the existing `sessions/`.
- No second learning or knowledge home beside the mapped paths.

The host `index.md` and `log.md` are shared catalog and history surfaces: they receive teach
entries without replacing host orientation or unrelated project history.
