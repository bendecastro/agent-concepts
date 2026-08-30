# Bilateral skill relationships

Date: 2026-08-30
Status: proposed

## Scope and status

- **Intended reader:** the maintainer or agent implementing the relationship graph.
- **Requested change:** record one authoritative forward relationship edge and generate reverse visibility so a maintainer opening a skill can find its callers and assess change impact.
- **Scope guard:** this design changes repository metadata and maintainer workflow only. It does not edit skill bodies, tooling, generated docs, README, or unrelated files.

The current problem is that composition facts are scattered between prose, concept records, and workflow documents. For example, the drain's worker contract says feature work must load TDD, but an agent starting from TDD cannot discover that caller or its AFK-specific contract. The implementation must make that relationship discoverable from both ends without maintaining two copies of the same edge.

### Evidence anchors

- `AGENTS.md:24-29` defines `concepts/<name>/` as the canonical layer: `CONCEPT.md` holds design and provenance, while `body/` is "the actual instruction content an agent consumes."
- **concepts/bc-drain-issues/body/execute-issue.md:23** says: "For feature/enhancement work, load and follow the repo-available `tdd` discipline."
- **concepts/bc-drain-issues/body/SKILL.md:18** says minimal roles "do not inherit the broad skill catalog" and that worker disciplines must be passed explicitly.
- **docs/plans/implemented/portability.md:43-49** records: "No `requires:` key in `SKILL.md` frontmatter. No harness reads it, so it would imply enforcement that does not exist."
- **concepts/prompting-agents/body/SKILL.md:18** requires the smallest set of high-signal tokens and progressive disclosure; automatic transitive loading would work against that constraint.
- **scripts/lint.py:262-370** provides the existing generated-output pattern: a source of truth is rendered deterministically, and stale output fails normal lint.

## Resolved architecture

### One forward declaration, generated bilateral visibility

Create **concepts/relationships.json** as the sole source of relationship metadata. Each relationship is declared once by its owner, using `from` and `to`. Generate `concepts/<name>/RELATIONSHIPS.md` for every concept that has at least one incoming or outgoing edge. The generated view contains two explicitly labelled sections:

- **Outgoing** — relationships this concept declares toward another concept.
- **Incoming** — callers or upstream workflows that point at this concept, including the edge condition and reason.

For an edge `A loads B`, the generated view for `B` must say `incoming from A`. It must never render the incoming row as `B depends on A`, because the reverse view is a change-impact projection, not a reciprocal declaration. The JSON edge is authoritative; generated Markdown is navigation and review context.

Before changing a concept's behavioral contract, the maintainer or agent reads that concept's generated relationship view. When a body or `CONCEPT.md` clause adds, removes, or changes one of the four relationship kinds, the same change updates **concepts/relationships.json** and regenerates the views. The maintainer then inspects every incoming edge for impact and either updates affected consumers in the same change or records why an incoming edge is unaffected. This rule belongs in `AGENTS.md` during implementation as a concise pointer to the generated view and its source. The plan does not add that rule now because this design record is the requested change set.

### Runtime boundary

The relationship graph is maintainer-only. Runtime `body/SKILL.md` files remain the execution contract. The graph does not auto-load skills, grant authority, alter invocation class, or replace caller-specific packet instructions. A worker still receives `tdd` explicitly when the drain's feature/enhancement condition is active. This keeps the graph portable across harnesses and avoids turning a discoverability mechanism into hidden runtime behavior.

This also explains why `requires:` remains rejected in skill frontmatter: the portability decision says no harness reads that key, so adding it would suggest enforcement that does not exist. Relationship metadata belongs in the canonical workspace graph, separate from Agent Skills frontmatter and the lifecycle fields in `CONCEPT.md`.

## Relationship schema

**concepts/relationships.json** uses schema version `1` and a fixed top-level shape:

```json
{
  "schema": 1,
  "edges": [
    {
      "from": "bc-drain-issues",
      "to": "tdd",
      "relation": "loads",
      "required": true,
      "when": "feature/enhancement work",
      "source": "concepts/bc-drain-issues/body/execute-issue.md#build-loop",
      "reason": "Feature workers follow red-green-refactor."
    }
  ]
}
```

Each edge has:

- `from` — the canonical dash-case concept that owns the relationship.
- `to` — the canonical dash-case concept being loaded, adapted, relied on, or handed work to.
- `relation` — one of `loads`, `adapts`, `depends_on_contract`, or `hands_off`.
- `required` — a boolean. It describes whether the edge is required when its relationship applies; it does not cause runtime loading.
- `when` — an optional human-readable condition. Omit it for an unconditional relationship. Natural-language conditions are descriptive metadata in v1, not executable predicates.
- `source` — a repository-relative source file, optionally followed by a heading anchor. The file must belong to `from`'s concept and identify the `to` concept.
- `reason` — a short explanation of why the relationship exists.

The relation vocabulary is intentionally closed:

- `loads`: the source workflow activates the target's instructions for a path.
- `adapts`: the source narrows or copies a bounded part of the target's guidance; this is a relationship to inspect when either contract changes.
- `depends_on_contract`: the source relies on behavior or parameters owned by the target without necessarily loading the target's instructions.
- `hands_off`: the source produces the next-stage artifact or outcome for the target; this is workflow routing, not a prerequisite.

`required` and `when` must remain separate. A conditional required load is still required when its condition holds. An optional relationship must not become a hard prerequisite in generated impact output. A handoff can be required for a workflow route, but `required` describes relationship applicability rather than granting permission to skip the user gate; implementation should define and test this distinction before using such rows.

### Concrete edge

The first migration must include:

```json
{
  "from": "bc-drain-issues",
  "to": "tdd",
  "relation": "loads",
  "required": true,
  "when": "feature/enhancement work",
  "source": "concepts/bc-drain-issues/body/execute-issue.md#build-loop",
  "reason": "Feature workers follow red-green-refactor."
}
```

The generated drain view must render the authoritative outgoing direction and its source:

```md
- loads `tdd` when feature/enhancement work.
  Feature workers follow red-green-refactor.
  Source: [execute-issue.md](body/execute-issue.md#build-loop)
```

The generated TDD view must render the incoming projection and preserve the same source anchor:

```md
- incoming from [bc-drain-issues](../bc-drain-issues/RELATIONSHIPS.md): loads this skill when feature/enhancement work.
  Feature workers follow red-green-refactor.
  Source: [execute-issue.md](../bc-drain-issues/body/execute-issue.md#build-loop)
```

It must not create a generated outgoing row claiming that TDD depends on `bc-drain-issues`. Every outgoing and incoming row carries its `source` link.

## Generator and lint contract

Implement a deterministic generator, exposed through an explicit write mode such as `python3 scripts/lint.py --write-relationships`. Ordinary `python3 scripts/lint.py` remains read-only and fails when any generated relationship view is missing or stale. The generated files carry a clear generated/do-not-edit header. Sort concepts, sections, and edges deterministically so equivalent JSON produces stable output.

The implementation must reject:

1. Missing or malformed **concepts/relationships.json**, an unsupported `schema`, a missing `edges` array, or unknown top-level/edge keys.
2. Missing, non-canonical, aliased, or non-existent `from`/`to` concept names. Graph identity uses concept directories, not deployment aliases such as `implement`, `to-issues`, or `to-prd`.
3. A `source` that is not repository-relative, does not exist, is outside the `from` concept, or does not mention the target concept. A mention is the exact canonical `to` name bounded by characters outside `[A-Za-z0-9-]`; this is a narrow consistency check, not a natural-language completeness proof. If a fragment is present, it must match exactly one ATX heading after lowercasing, removing ASCII punctuation other than hyphens and spaces, and replacing spaces with hyphens.
4. Self-edges and duplicate edge identities. At minimum, `(from, to, relation, when)` must be unique; omitted `when` canonicalizes to `null`, while a blank string is invalid.
5. Unknown relations, a non-boolean `required`, blank conditions, malformed source anchors, or empty reasons.
6. Cycles made solely from mandatory `loads` edges. Report the cycle path. Do not infer cycles from `adapts`, `depends_on_contract`, or `hands_off` unless a later design explicitly gives them load semantics.
7. Missing, extra, or stale generated `RELATIONSHIPS.md` files compared with the deterministic rendering. Normal lint must report the mismatch rather than rewrite it.

The graph check should also assert that every declared edge appears exactly once in the source's outgoing section and exactly once in the target's incoming section. This is the mechanical bilateral invariant. It does not assert that every prose mention is a relationship: migration classification is curated because examples, ordinary references, negative “do not load” boundaries, and optional handoffs cannot be identified safely by name scraping.

Direct relationships are the complete v1 generated view. Do not calculate a transitive closure or auto-load transitive bodies. A future impact command may traverse direct relationships if direct views prove insufficient, but it must preserve relation, condition, and requiredness along each path and remain a maintainer tool.

## Migration and ownership

Migration is curated rather than a prose scrape:

1. Inventory actual operational relationships from bodies, concept records, and existing workflow maps.
2. Classify each relationship manually as `loads`, `adapts`, `depends_on_contract`, or `hands_off`.
3. Add one forward row to **concepts/relationships.json** with a source anchor and reason.
4. Preserve the existing runtime clause in the source body. The graph improves reverse discovery; it does not replace the instruction that tells an agent when and how to load a skill.
5. Generate the per-concept views and review both ends of each edge.
6. Treat structural lint as schema/consistency evidence only. Do not claim the graph is complete merely because lint passes; unresolved prose mentions require maintainer classification.

Initial migration should seed the actual operational paths, including the requested drain→TDD edge and other relationships confirmed during implementation. It should not turn every name in a concept record into an edge. In particular, negative boundaries such as the thin `plain-language` clauses and optional retrieval/tooling paths need deliberate classification or exclusion.

The graph's one-home rule prevents a second hand-maintained reverse list. If an edge changes, edit the JSON owner and regenerate; never hand-edit a generated incoming row. The generated view is a stable place for an agent to begin impact analysis, while the source anchor directs it to the behaviorally authoritative clause.

## Implementation scope and file map

The implementation plan is:

- **Create concepts/relationships.json.** Add schema-versioned, curated forward edges and no generated content.
- **Extend `scripts/lint.py`.** Add parsing/validation, deterministic rendering, stale-output checking, and an explicit `--write-relationships` mode. Keep ordinary lint non-mutating. This is implementation work, not part of this proposal's approved tracked change set.
- **Generate `concepts/<name>/RELATIONSHIPS.md`.** Generate only for concepts with at least one incoming or outgoing relationship. Omit empty views, and treat any leftover empty generated file as an extra stale file. Do not place generated content in `SKILL.md`.
- **Update `AGENTS.md`.** Add the concise pre-change impact-review and source-graph upkeep rule, plus a pointer to the graph/generated views. Do not duplicate relation semantics there.
- **Update catalog/navigation ownership.** Add the graph and generated-view convention to the Tooling section of `index.md`, next to `scripts/lint.py`. Do not duplicate the edge table in `docs/pipeline.md`; its existing narrative should remain the home for pipeline explanation.
- **Add deterministic fixture tests.** Keep graph validation tests near the lint implementation or in the repository's existing test convention; add cases listed below before treating the schema as reliable.
- **Record implementation provenance and status.** Move this plan to `docs/plans/implemented/` after rollout and append the implementation and verification record here. A metadata-only graph does not by itself change a concept's runtime test gate; changing bodies or always-loaded instructions does.

The current design-document change itself is limited to this plan, its catalog entry, and its journal entry. It intentionally does not create the graph, generated views, linter, or AGENTS rule.

## Test cases and acceptance criteria for implementation

### Deterministic unit/fixture cases

At minimum, test:

- one valid unconditional edge;
- one valid optional edge;
- one valid conditional edge, including the concrete `bc-drain-issues`→`tdd` row;
- each relation value in the closed vocabulary;
- generated outgoing and incoming rows, with incoming wording preserving direction;
- unknown concept and deployment alias rejection;
- missing source, source outside the `from` concept, missing target mention, and malformed heading anchor;
- self-edge and duplicate-edge rejection;
- invalid relation, non-boolean `required`, blank `when`, and empty `reason` rejection;
- mandatory `loads` cycle rejection with a readable cycle path;
- non-load relationship cycle behavior as specified, without falsely rejecting workflow handoffs;
- stale, missing, or manually changed generated views failing ordinary lint;
- explicit write mode regenerating identical output and ordinary lint remaining non-mutating;
- direct-only output: no transitive or auto-load behavior is generated.

### Acceptance criteria

1. A maintainer opening any related concept can find both its outgoing relationships and incoming callers/change-impact rows without a manually maintained reverse list.
2. The TDD view identifies `bc-drain-issues` as an incoming caller under feature/enhancement work and preserves the source anchor.
3. Direction is unambiguous: `A loads B` never becomes `B depends on A` in generated output.
4. Schema, names, source ownership, target mention, relation values, conditions, duplicate/self edges, and mandatory-load cycles are mechanically validated.
5. Generated relationship views are deterministic and stale output fails normal lint; the explicit write mode is the only generator mutation path.
6. Runtime skill loading and authority remain unchanged. The graph does not auto-load, authorize, or replace body/packet instructions.
7. Migration records actual operational relationships and preserves existing body clauses; structural lint is not presented as proof of graph completeness.
8. Before a behavioral contract change, the maintainer/agent checks the relationship view and accounts for each incoming edge in the same change or with a recorded unaffected rationale. Adding, removing, or changing a relationship clause also updates **concepts/relationships.json** and regenerates the views in that change.
9. Existing portability, status-frontmatter, deploy, and concept test gates remain intact. A body or always-loaded instruction change receives the relevant pressure test before deployment; metadata-only generation does not silently claim runtime behavior was tested.

## Non-goals

- Do not add `requires:` to Agent Skills frontmatter or imply that any harness consumes it.
- Do not auto-load direct or transitive skills in Pi, Claude Code, OpenCode, or other harnesses.
- Do not hand-maintain incoming/backlink sections.
- Do not infer relationships from every prose mention, slash command, provenance citation, or example.
- Do not replace source-body execution clauses, worker packets, acceptance matrices, or caller authority with graph metadata.
- Do not redesign invocation classes, dependency conditions into an executable policy language, or deployment topology in v1.
- Do not create a second pipeline composition map that duplicates `docs/pipeline.md`.
- Do not treat a generated relationship view as an authorization or approval record.
- Do not require transitive impact traversal until direct views demonstrate a real gap.

## Risks and mitigations

- **Graph/body drift:** the runtime body remains authoritative and can change without a metadata edit. Require source anchors and same-change graph upkeep when a relationship clause changes. Curated migration exclusions belong in this plan's implementation record, not in a prose-scraping warning system.
- **False reverse semantics:** a target may be mistaken as depending on its caller. Label generated rows `incoming from` and keep outgoing/incoming wording distinct.
- **Context bloat or accidental activation:** a graph could be mistaken for an import system. Keep it maintainer-only, direct-only, and out of runtime frontmatter.
- **Condition ambiguity:** natural-language conditions cannot drive a harness. Preserve `when` as descriptive text; introduce an executable condition vocabulary only through a separate approved design.
- **Generated-file conflicts:** contributors may edit views directly or forget regeneration. Mark them generated, make normal lint stale-check them, and provide one explicit write mode.
- **Private overrides:** private concepts can override public same-name bodies, but public graph metadata cannot safely inspect private configuration. Reject unknown public targets and define private-graph merge semantics separately if needed.
- **Load cycles:** conditional prose can still form an unsafe load loop. Reject cycles of mandatory `loads` edges and report the full path.
- **Overclassification:** `adapts`, `depends_on_contract`, and `hands_off` can become a dumping ground. Keep the vocabulary closed and require a source and reason for every row.

## Rollout steps

1. Review and approve this proposed design record.
2. Implement schema validation and deterministic rendering behind the explicit write mode.
3. Add fixture tests before migrating the full inventory.
4. Pilot the concrete drain→TDD edge and a small set of clearly established relationships; inspect generated views from both ends.
5. Curate the remaining operational relationships, preserving runtime clauses and documenting exclusions.
6. Add the concise AGENTS maintenance rule and catalog pointer.
7. Run normal lint, diff checks, and the relationship fixtures; inspect generated output for direction and stale-file behavior.
8. If only metadata/tooling changed, record that the runtime skill behavior was unchanged. If skill bodies or always-loaded instructions changed, run the relevant pressure test and update status honestly before deployment.
9. Keep a later transitive-impact command as a separate decision, triggered by evidence that direct generated views are insufficient.

## Implementation invariants

The architecture and relationship semantics are resolved. Empty views are omitted, repository-relative sources and optional heading anchors follow the validation rules above, and fixture tests use the repository's existing test convention. Those mechanics do not change the approved one-source/generated-reverse architecture or its maintainer-only boundary.
