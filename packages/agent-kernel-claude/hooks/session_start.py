"""Emit one bounded slice of the bundled kernel for Claude Code SessionStart."""

import json
import os
from pathlib import Path
import re
import sys


CONTEXT_LIMIT = 10_000
# ceiling: two registered hooks; add a hook entry if the kernel needs a third slice.
HOOK_COUNT = 2


def label(part: int, total: int) -> str:
    return f"Agent Kernel, part {part} of {total} (sections may arrive in any order)\n"


def split_kernel(text: str) -> list[str]:
    limit = CONTEXT_LIMIT - len(label(HOOK_COUNT, HOOK_COUNT))
    chunks = []
    chunk = ""
    size = 0
    for section in re.split(r"(?m)(?=^## )", text):
        if not section:
            continue
        # Bound UTF-16 code units as well as Unicode characters for Claude Code.
        section_size = len(section.encode("utf-16-le")) // 2
        if section_size >= limit:
            raise ValueError("an agent kernel section reaches the 10,000-character hook limit")
        if size + section_size >= limit:
            chunks.append(chunk)
            chunk, size = "", 0
        chunk += section
        size += section_size
    if chunk:
        chunks.append(chunk)
    return chunks


def main(index: int) -> None:
    path = Path(os.environ["CLAUDE_PLUGIN_ROOT"]) / "AGENT-KERNEL.md"
    chunks = split_kernel(path.read_bytes().decode("utf-8"))
    if not chunks or len(chunks) > HOOK_COUNT:
        raise ValueError(f"expected 1 to {HOOK_COUNT} kernel slices, got {len(chunks)}")
    output = {}
    if index < len(chunks):
        output["hookSpecificOutput"] = {
            "hookEventName": "SessionStart",
            "additionalContext": label(index + 1, len(chunks)) + chunks[index],
        }
    print(json.dumps(output))


if __name__ == "__main__":
    try:
        main(int(sys.argv[1]))
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f"agent-kernel SessionStart: {exc}") from None
