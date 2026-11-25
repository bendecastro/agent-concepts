# JSON Canvas 1.0 format reference

A canvas is a JSON object with optional `nodes` and `edges` arrays:

```json
{
  "nodes": [],
  "edges": []
}
```

## Nodes

Every node has a unique 16-character hexadecimal `id`, a `type`, integer `x`, `y`, `width`, and `height`. Types are `text`, `file`, `link`, and `group`.

| Type | Required content | Notes |
|---|---|---|
| `text` | `text` | Markdown text. Escape newlines as `\n` in JSON. |
| `file` | `file` | Path to a file; optional `subpath` starts with `#`. |
| `link` | `url` | External URL. |
| `group` | — | Optional `label`, `background`, and `backgroundStyle` (`cover`, `ratio`, or `repeat`). |

The optional `color` is a preset string (`"1"` through `"6"`) or a hexadecimal color. Applications choose the visual meaning of presets.

```json
{
  "id": "6f0ad84f44ce9c17",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# Start\n\nA **Markdown** node."
}
```

## Edges

An edge has a unique `id`, `fromNode`, and `toNode`, both referring to existing node IDs. Optional `fromSide` and `toSide` are `top`, `right`, `bottom`, or `left`; `fromEnd` and `toEnd` are `none` or `arrow`; `label` and `color` are optional.

```json
{
  "id": "0123456789abcdef",
  "fromNode": "6f0ad84f44ce9c17",
  "fromSide": "right",
  "toNode": "a1b2c3d4e5f67890",
  "toSide": "left",
  "toEnd": "arrow",
  "label": "leads to"
}
```

Array order determines z-order: later nodes are drawn above earlier nodes. Coordinates can be negative; `x` increases right and `y` increases down.

See the [JSON Canvas 1.0 specification](https://jsoncanvas.org/spec/1.0/) when a detail is not covered here.
