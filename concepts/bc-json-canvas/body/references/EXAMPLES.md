# JSON Canvas examples

## Small connected canvas

```json
{
  "nodes": [
    {
      "id": "6f0ad84f44ce9c17",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 320,
      "height": 160,
      "text": "# Question\n\nWhat should we explore?"
    },
    {
      "id": "a1b2c3d4e5f67890",
      "type": "file",
      "x": 420,
      "y": 0,
      "width": 360,
      "height": 220,
      "file": "Research/Answer.md",
      "subpath": "#Conclusion"
    }
  ],
  "edges": [
    {
      "id": "0123456789abcdef",
      "fromNode": "6f0ad84f44ce9c17",
      "fromSide": "right",
      "toNode": "a1b2c3d4e5f67890",
      "toSide": "left",
      "toEnd": "arrow",
      "label": "answer"
    }
  ]
}
```

## Group with a link node

```json
{
  "nodes": [
    {
      "id": "1111111111111111",
      "type": "group",
      "x": -40,
      "y": -40,
      "width": 900,
      "height": 420,
      "label": "Sources",
      "color": "5"
    },
    {
      "id": "2222222222222222",
      "type": "link",
      "x": 40,
      "y": 40,
      "width": 360,
      "height": 160,
      "url": "https://jsoncanvas.org/spec/1.0/"
    }
  ],
  "edges": []
}
```

The examples are deterministic fixtures, not instructions to infer paths or overwrite an existing canvas. Replace the file path with an explicit, known target and validate the complete result.
