# JSON Canvas validation and layout

Run these checks after creating or editing a canvas:

1. Parse the complete file as JSON.
2. Confirm the top-level value is an object and `nodes`/`edges` are arrays when present.
3. Collect every node and edge ID; reject duplicates and IDs that are not unique across both arrays.
4. Confirm every node has a unique 16-character lowercase hexadecimal ID, an allowed type, integer coordinates, positive width, and positive height.
5. Require `text` for text nodes, `file` for file nodes, and `url` for link nodes.
6. Confirm every edge endpoint exists in the node ID set.
7. Restrict `fromSide`/`toSide` to `top`, `right`, `bottom`, or `left`; restrict `fromEnd`/`toEnd` to `none` or `arrow`.
8. Accept preset colors only as strings `"1"`–`"6"`, or validate hexadecimal colors.
9. Check that JSON text uses escaped `\n` sequences and that group-contained nodes remain within readable bounds.

## Deterministic layout defaults

- Use a fixed grid such as 20px increments.
- Leave roughly 50–100px between unrelated nodes.
- Keep 20–50px of padding inside groups.
- Use 300–450px widths for medium text/file nodes and size heights to the content.
- Place a source to the left of its result when the edge reads left-to-right; use explicit sides for stable anchors.
- Preserve existing node array order unless changing z-order is part of the request.

For a new ID, generate a random 64-bit value and render it as 16 lowercase hexadecimal characters. Never derive a new ID by truncating an existing one, and never use a duplicate merely because a node looks similar.

If a check fails, report the exact invariant and repair the data before writing. Refer to the [JSON Canvas 1.0 specification](https://jsoncanvas.org/spec/1.0/) for application-specific extensions.
