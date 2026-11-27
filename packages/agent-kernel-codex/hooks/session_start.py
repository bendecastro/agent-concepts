"""Return the packaged Markdown as Codex SessionStart developer context."""

import json
from pathlib import Path


if __name__ == "__main__":
    kernel = Path(__file__).resolve().parents[1] / "AGENT-KERNEL.md"
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": kernel.read_bytes().decode("utf-8"),
        },
    }))
