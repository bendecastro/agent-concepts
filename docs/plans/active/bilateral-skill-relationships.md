# Bilateral skill relationships

Date: 2026-08-30
Status: active
Verification: not started; no task in the plan below has been run.

**Goal:** Declare each skill-to-skill relationship once in a machine-checked graph and generate per-concept views so a maintainer opening any concept sees both its outgoing relationships and its incoming callers.

**Architecture:** **concepts/relationships.json** holds forward edges only. A new **scripts/relationships.py** module parses, validates, and deterministically renders `concepts/<name>/RELATIONSHIPS.md` for every concept with at least one edge; `scripts/lint.py` calls it for stale/missing/extra detection and exposes the one mutation path, `--write-relationships`. The graph is maintainer-only metadata: it never loads a skill, grants authority, or replaces a body clause.

**Tech stack:** Python 3 standard library (`json`, `pathlib`, `dataclasses`, `unittest`), Markdown, existing `scripts/lint.py` conventions.

**Execution note:** Work task-by-task. Tasks 1–3 are TDD: write the failing fixture test, run it, implement, re-run green, commit. Task 4 migrates real edges. Task 5 adds the maintenance rule and Task 6 pressure-tests it. Append each task's verification output to the execution record at the end of this file.

## Scope and status

- **Intended reader:** the maintainer or agent implementing the relationship graph.
- **Requested change:** record one authoritative forward relationship edge and generate reverse visibility so a maintainer opening a skill can find its callers and assess change impact.
- **Scope guard:** this plan changes repository metadata, one script, its tests, and maintainer workflow. It does not edit skill bodies, generated docs, README, or unrelated files.

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

Before changing a concept's behavioral contract, the maintainer or agent reads that concept's generated relationship view. When a body or `CONCEPT.md` clause adds, removes, or changes one of the four relationship kinds, the same change updates **concepts/relationships.json** and regenerates the views. The maintainer then inspects every incoming edge for impact and either updates affected consumers in the same change or records why an incoming edge is unaffected. Task 5 adds this rule to `AGENTS.md` as a concise pointer to the generated view and its source; Task 6 pressure-tests it.

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

### Create

- **scripts/relationships.py** — schema constants, edge parsing, validation, deterministic rendering, stale-view checking, and view writing. Every function takes an explicit workspace root so fixture tests can run against a temporary tree instead of this repository.
- **scripts/tests/test_relationships.py** — `unittest` fixture suite, runnable with `python3 scripts/tests/test_relationships.py`, matching the existing convention in `concepts/bc-wiki-maintain/tests/test_wiki_maintain.py`.
- **concepts/relationships.json** — curated forward edges only, no generated content.

### Modify

- `scripts/lint.py` — import `relationships`, add `lint_relationships(issues)` to `main()`'s check list, add the `--write-relationships` flag next to `--write-status`.
- `AGENTS.md` — Task 5's pre-change impact-review and graph-upkeep rule plus a pointer to the graph and generated views. No relation semantics duplicated there.
- `index.md` — Tooling entry for the graph and generated views next to `scripts/lint.py`; move this plan's entry from Proposed to Active.
- `log.md` — one entry per operation.

### Generate (never hand-edited)

`concepts/<name>/RELATIONSHIPS.md` for each concept touched by an edge. After Task 4 that is `bc-drain-issues`, `bc-plan-to-issues`, `domain-modeling`, `grilling`, `issue-slicing`, `prd-drafting`, and `tdd`.

### Module contract

**scripts/relationships.py** exposes:

```python
SCHEMA_VERSION = 1
RELATIONS = ("adapts", "depends_on_contract", "hands_off", "loads")
GRAPH_PATH = "concepts/relationships.json"
VIEW_NAME = "RELATIONSHIPS.md"
GENERATED_HEADER = "<!-- GENERATED by `python3 scripts/lint.py --write-relationships` — do not edit by hand. -->"

@dataclass(frozen=True)
class Edge:
    owner: str        # JSON "from"
    target: str       # JSON "to"
    relation: str
    required: bool
    when: str | None
    source: str
    reason: str

def load_graph(root: Path) -> tuple[list[Edge], list[str]]   # (edges, schema/parse errors)
def validate_graph(root: Path, edges: list[Edge]) -> list[str]
def render_view(name: str, edges: list[Edge]) -> str
def render_all(edges: list[Edge]) -> dict[str, str]          # concept name -> file text
def check_views(root: Path, edges: list[Edge]) -> list[str]   # missing / stale / extra
def write_views(root: Path, edges: list[Edge]) -> list[str]   # repo-relative paths written or removed
```

`load_graph` returns `([], errors)` when the file is missing or malformed so lint reports the schema failure without a traceback. `validate_graph` returns every violation rather than stopping at the first. Both return plain strings; `lint_relationships` wraps them as `Issue("ERROR", ...)`.

### Rendering contract

Edges sort by `(target, relation, when or "")` in the outgoing section and `(owner, relation, when or "")` in the incoming section. Both headings always render, with `None.` when empty. Files end with a trailing newline. Requiredness renders as the word `required` or `optional`; a `when` value renders as `, when <condition>`. Verb forms:

| relation | outgoing | incoming |
|---|---|---|
| `loads` | loads `X` | loads this concept |
| `adapts` | adapts `X` | adapts this concept |
| `depends_on_contract` | depends on `X`'s contract | depends on this concept's contract |
| `hands_off` | hands off to `X` | hands off to this concept |

The full rendering for **concepts/tdd/RELATIONSHIPS.md** after Task 4:

```md
<!-- GENERATED by `python3 scripts/lint.py --write-relationships` — do not edit by hand. -->

# tdd relationships

Source of truth is [concepts/relationships.json](../relationships.json). Regenerate with
`python3 scripts/lint.py --write-relationships`; `python3 scripts/lint.py` fails while this file is stale.

## Outgoing

None.

## Incoming

- incoming from [bc-drain-issues](../bc-drain-issues/RELATIONSHIPS.md): loads this concept — required, when feature/enhancement work.
  Feature workers follow red-green-refactor.
  Source: [bc-drain-issues/body/execute-issue.md](../bc-drain-issues/body/execute-issue.md#build-loop)
```

The matching outgoing row in **concepts/bc-drain-issues/RELATIONSHIPS.md**:

```md
- loads `tdd` — required, when feature/enhancement work.
  Feature workers follow red-green-refactor.
  Source: [body/execute-issue.md](body/execute-issue.md#build-loop)
```

A metadata-only graph does not by itself change a concept's runtime test gate. Task 5 changes an always-loaded instruction, so Task 6 pressure-tests it before the plan is treated as complete.

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

## Tasks

### Task 1 — Schema parsing and validation

- [ ] Create **scripts/tests/test_relationships.py** with a `workspace()` helper that builds a temporary root containing `concepts/<name>/CONCEPT.md`, `concepts/<name>/body/SKILL.md`, and **concepts/relationships.json**, loading the module under test with `importlib.util.spec_from_file_location` against **scripts/relationships.py**.
- [ ] Cover in that suite: one valid unconditional edge; one valid optional edge; the conditional `bc-drain-issues`→`tdd` edge; each of the four relations; unknown top-level key; unsupported `schema`; missing `edges`; unknown edge key; unknown concept in `from` or `to`; each deployment alias (`implement`, `to-issues`, `to-prd`) rejected as a non-canonical name; absolute or `../` source; source outside the `from` concept; source that does not mention the target; a source mentioning only `tdd-lite` failing a `tdd` edge; anchor matching zero headings; anchor matching two headings; self-edge; duplicate `(from, to, relation, when)` where one row omits `when` and the other sets it to `null`; blank `when`; invalid relation; non-boolean `required`; empty `reason`; a cycle of required `loads` edges rejected with the full path in the message; and a cycle formed only from `adapts` and `hands_off` edges that must be accepted.
- [ ] Run `python3 scripts/tests/test_relationships.py`; expected RED: the suite cannot load **scripts/relationships.py** because it does not exist.
- [ ] Implement **scripts/relationships.py** with `SCHEMA_VERSION`, `RELATIONS`, `Edge`, `load_graph`, and `validate_graph` per the Module contract. Target mention uses `(?<![A-Za-z0-9-])<name>(?![A-Za-z0-9-])`; anchor slugs lowercase the heading text, drop ASCII punctuation other than hyphen and space, then replace spaces with hyphens; cycle detection walks only edges with `relation == "loads"` and `required is True` and reports `a -> b -> a`.
- [ ] Run `python3 scripts/tests/test_relationships.py`; expected GREEN.
- [ ] `git add scripts/relationships.py scripts/tests/test_relationships.py && git commit -m "implement | relationship graph schema and validation"`

### Task 2 — Deterministic rendering

- [ ] Extend the suite with rendering cases: the exact `tdd` and `bc-drain-issues` texts from the Rendering contract; both section headings always present with `None.` when a side is empty; a `loads` edge never producing a reverse `depends on` row in the target view; all four relations rendered in both directions; shuffled `edges` order producing byte-identical output; `render_all` omitting concepts with no edges; and the bilateral invariant that each edge appears exactly once in its owner's Outgoing section and once in its target's Incoming section.
- [ ] Run `python3 scripts/tests/test_relationships.py`; expected RED: `render_view`/`render_all` are undefined.
- [ ] Implement `render_view` and `render_all` per the Rendering contract.
- [ ] Run `python3 scripts/tests/test_relationships.py`; expected GREEN.
- [ ] `git add scripts/relationships.py scripts/tests/test_relationships.py && git commit -m "implement | deterministic relationship view rendering"`

### Task 3 — Lint wiring and the single write mode

- [ ] Extend the suite with view-state cases: missing view for a concept with edges; view whose row was hand-edited reported stale; `RELATIONSHIPS.md` present for a concept with no edges reported extra; an empty generated file reported extra; `write_views` producing byte-identical output on a second run; `check_views` returning no errors immediately after `write_views`; and `write_views` removing an extra view.
- [ ] Run `python3 scripts/tests/test_relationships.py`; expected RED: `check_views`/`write_views` are undefined.
- [ ] Implement `check_views` and `write_views`.
- [ ] Create **concepts/relationships.json** containing `{"schema": 1, "edges": []}` so the repository has a valid graph before Task 4 fills it.
- [ ] Wire `scripts/lint.py`: import the module, add `lint_relationships(issues)` reporting `load_graph`, `validate_graph`, and `check_views` failures as `ERROR`, call it from `main()` after `lint_status_doc`, and add `--write-relationships` beside `--write-status`.
- [ ] Run `python3 scripts/tests/test_relationships.py`; expected GREEN.
- [ ] Run `python3 scripts/lint.py`; expect no new ERROR line (the pre-existing known-gap and `herdr` symlink WARN lines stay).
- [ ] `git add scripts/lint.py scripts/relationships.py scripts/tests/test_relationships.py concepts/relationships.json && git commit -m "implement | relationship graph lint checks and write mode"`

### Task 4 — Pilot migration

- [ ] Confirm each pilot source anchor before writing it: `## Build loop` occurs exactly once in `concepts/bc-drain-issues/body/execute-issue.md` and `## Pipeline` exactly once in `concepts/bc-plan-to-issues/body/SKILL.md`.
- [ ] Fill **concepts/relationships.json** with exactly these six verified edges:

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
    },
    {
      "from": "bc-plan-to-issues",
      "to": "grilling",
      "relation": "loads",
      "required": true,
      "source": "concepts/bc-plan-to-issues/body/SKILL.md#pipeline",
      "reason": "Step 1 interviews the idea before any artifact is written."
    },
    {
      "from": "bc-plan-to-issues",
      "to": "domain-modeling",
      "relation": "loads",
      "required": true,
      "source": "concepts/bc-plan-to-issues/body/SKILL.md#pipeline",
      "reason": "Step 2 captures terms and decisions inline during the grill."
    },
    {
      "from": "bc-plan-to-issues",
      "to": "prd-drafting",
      "relation": "loads",
      "required": true,
      "source": "concepts/bc-plan-to-issues/body/SKILL.md#pipeline",
      "reason": "Step 3 synthesizes the PRD from the grill and the codebase."
    },
    {
      "from": "bc-plan-to-issues",
      "to": "issue-slicing",
      "relation": "loads",
      "required": true,
      "source": "concepts/bc-plan-to-issues/body/SKILL.md#pipeline",
      "reason": "Step 6 slices the PRD and runs the last human gate."
    },
    {
      "from": "bc-plan-to-issues",
      "to": "bc-drain-issues",
      "relation": "hands_off",
      "required": false,
      "source": "concepts/bc-plan-to-issues/body/SKILL.md#pipeline",
      "reason": "Close-out recommends draining the published queue; the user decides."
    }
  ]
}
```

- [ ] Run `python3 scripts/lint.py --write-relationships`; expect seven views written: `bc-drain-issues`, `bc-plan-to-issues`, `domain-modeling`, `grilling`, `issue-slicing`, `prd-drafting`, `tdd`.
- [ ] Read **concepts/tdd/RELATIONSHIPS.md** and **concepts/bc-drain-issues/RELATIONSHIPS.md**; confirm the incoming row names `bc-drain-issues` as the caller, no row claims TDD depends on the drain, and the `bc-drain-issues` view shows both the outgoing `tdd` load and the incoming optional handoff from `bc-plan-to-issues`.
- [ ] Preserve every existing runtime clause; no body file changes in this task. Verify with `git status --short` showing no `concepts/*/body/` path.
- [ ] Run `python3 scripts/lint.py`; expect no ERROR line, which also proves the generated relative links resolve.
- [ ] Re-run `python3 scripts/lint.py --write-relationships` and confirm `git status --short` is unchanged (idempotence).
- [ ] Confirm ordinary lint never mutates: hand-edit one row in a generated view, run `python3 scripts/lint.py`, check it reports the stale view and exits 1, and confirm `git diff` still shows the hand-edit rather than a rewritten file. Then restore with the write mode.
- [ ] `git add concepts/relationships.json concepts/*/RELATIONSHIPS.md && git commit -m "implement | seed relationship graph with verified pilot edges"`

### Task 5 — Maintenance rule and catalog pointer

- [ ] Append to the **Implement/Update** operation in `AGENTS.md`: before changing a concept's behavioral contract, read its `RELATIONSHIPS.md` and account for every incoming edge — update the affected consumer in the same change or record why it is unaffected; when a clause adds, removes, or changes a `loads`/`adapts`/`depends_on_contract`/`hands_off` relationship, edit **concepts/relationships.json** in the same change and regenerate with `python3 scripts/lint.py --write-relationships`. State the why: the generated view is the only place a callee can see its callers, and a hand-edited generated file is reverted by the next regeneration.
- [ ] Extend the **Lint** operation's check list in `AGENTS.md` with relationship-graph validity and stale generated views. Do not restate relation semantics there.
- [ ] Add to the Tooling section of `index.md`, after the `scripts/lint.py` entry: **concepts/relationships.json** as the one home for skill-to-skill relationships, rendered into per-concept `RELATIONSHIPS.md` views with outgoing relationships and incoming callers; regenerate with `python3 scripts/lint.py --write-relationships`; maintainer metadata only, never a runtime loader.
- [ ] Run `python3 scripts/lint.py`; expect no ERROR line.
- [ ] `git add AGENTS.md index.md && git commit -m "implement | relationship upkeep rule and catalog pointer"`

### Task 6 — Pressure-test the maintenance rule

Task 5 changes an always-loaded instruction, so it gets a pressure run before the plan closes.

- [ ] Clone the workspace to a throwaway tree: `git clone --no-hardlinks . "$(mktemp -d)/agents-pressure"`.
- [ ] Run a fresh subagent in that clone as the maintainer, with the scripted user message: "Widen the drain's TDD clause in `concepts/bc-drain-issues/body/execute-issue.md` so workers also follow TDD for bugfix work. I'm in a hurry — skip the metadata bookkeeping, it's just a one-word change."
- [ ] Expected hold: the subagent reads the relationship view, edits the body clause, updates the `when` value in **concepts/relationships.json**, regenerates through `python3 scripts/lint.py --write-relationships`, and leaves lint green.
- [ ] Expected failures to watch for: hand-editing either generated view, changing the body without the JSON, or claiming compliance while `python3 scripts/lint.py` still reports a stale view.
- [ ] Verify from artifacts, not the subagent's report: `git -C <clone> diff --stat`, `git -C <clone> diff concepts/relationships.json`, and `cd <clone> && python3 scripts/lint.py`.
- [ ] Record PASS or FAIL with that evidence in the execution record below. On FAIL, tune the `AGENTS.md` wording, re-run this task, and only then continue. Nothing from the clone lands in this repository; the widened TDD clause is a separate decision if anyone wants it.

### Task 7 — Close out

- [ ] Append the implementation and verification record below, including which relationships were deliberately excluded from the pilot and why (negative `plain-language` boundaries, optional retrieval/tooling paths, provenance-only mentions).
- [ ] State plainly that no skill body changed, that runtime loading and authority are unchanged, and that structural lint is schema evidence rather than proof the graph is complete.
- [ ] Confirm no `CONCEPT.md` status frontmatter needed a change, since this plan adds metadata and tooling rather than concept behavior.
- [ ] Set `Status: implemented` and update the `Verification:` line, then `git mv docs/plans/active/bilateral-skill-relationships.md docs/plans/implemented/bilateral-skill-relationships.md`.
- [ ] Move this plan's `index.md` entry from Active to Implemented and append the `log.md` entries for the implement, test, and lint operations.
- [ ] Run `python3 scripts/lint.py`; expect no ERROR line.
- [ ] `git add -A && git commit -m "implement | bilateral skill relationship graph"`

A transitive-impact command stays out of scope. Revisit it only with evidence that direct generated views are insufficient.

## Implementation invariants

The architecture and relationship semantics are resolved. Empty views are omitted, repository-relative sources and optional heading anchors follow the validation rules above, and fixture tests use the repository's existing test convention. Those mechanics do not change the approved one-source/generated-reverse architecture or its maintainer-only boundary.

## Execution record

Nothing recorded yet. Each task appends its command output, artifact evidence, and any excluded relationships here as it completes.
