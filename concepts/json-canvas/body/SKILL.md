---
name: json-canvas
description: Author and validate JSON Canvas 1.0 .canvas files with nodes, edges, groups, links, and deterministic layout. Use for Obsidian canvases, mind maps, flowcharts, and visual boards.
---

# JSON Canvas 1.0

A `.canvas` file is JSON Canvas data: top-level `nodes` and `edges` arrays containing positioned nodes and their connections. This skill teaches the open JSON Canvas 1.0 format; it is not permission to mutate a vault.

## Authority boundary

For an existing vault, use the available safe Obsidian/vault authority for retrieval, validation, and any targeted write. A write requires explicit user intent and an explicit safe target. Do not use generic CLI commands, JavaScript evaluation, shell redirection, or direct filesystem writes to bypass approval and path-safety rails. Do not infer a canvas target, bulk-edit canvases, or overwrite one by inference.

## Workflow

1. Identify the exact `.canvas` target and inspect its current nodes, edges, coordinate system, and local layout conventions.
2. Create or edit the smallest valid JSON structure. Generate unique lowercase 16-character hexadecimal IDs and never reuse an ID across nodes or edges.
3. Give every node its required `id`, `type`, `x`, `y`, `width`, and `height`; add type-specific fields and only valid optional fields.
4. Add edges only when both endpoint IDs exist. Use explicit sides/end markers when they make the relationship clearer.
5. Choose deterministic positions: align to a grid, leave readable spacing, and keep children inside group bounds. Preserve unrelated node order because array order controls z-order.
6. Parse the result as JSON and run the [validation checklist](references/VALIDATION.md). Load [format details](references/SPEC.md) and [examples](references/EXAMPLES.md) only as needed.

## Minimal shape

```json
{
  "nodes": [],
  "edges": []
}
```

Text nodes contain Markdown text. File nodes use a vault-relative `file` path, and link nodes use a URL. JSON strings must contain escaped newlines (`\n`), not literal line breaks.

## References

- [JSON Canvas 1.0 specification](https://jsoncanvas.org/spec/1.0/)
- [JSON Canvas project](https://github.com/obsidianmd/jsoncanvas)
- [Format details](references/SPEC.md)
- [Examples](references/EXAMPLES.md)
- [Validation and layout](references/VALIDATION.md)
