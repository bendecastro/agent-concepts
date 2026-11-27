"""Exercise the installed plugin interface and the section-splitting rule."""

import importlib.util
import json
import os
import subprocess
from pathlib import Path
from shutil import copytree, rmtree

from hypothesis import example, given, strategies as st


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "packages/agent-kernel-claude"


def test_session_start_hooks_emit_the_whole_kernel_in_bounded_sections(tmp_path):
    kernel = (ROOT / "concepts/agent-kernel/body/AGENT-KERNEL.md").read_bytes()
    installed = tmp_path / "installed plugin"
    hooks = json.loads((PLUGIN / "hooks/hooks.json").read_bytes())["hooks"]
    copytree(PLUGIN, installed)
    try:
        assert (installed / "AGENT-KERNEL.md").read_bytes() == kernel
        for source in ("startup", "resume", "clear", "compact"):
            payloads = []
            for group in hooks["SessionStart"]:
                if group.get("matcher") and source not in group["matcher"].split("|"):
                    continue
                for hook in group["hooks"]:
                    assert hook["type"] == "command"
                    args = [arg.replace("${CLAUDE_PLUGIN_ROOT}", str(installed)) for arg in hook["args"]]
                    result = subprocess.run(
                        [hook["command"], *args], cwd=tmp_path, check=True, capture_output=True,
                        env={**os.environ, "CLAUDE_PLUGIN_ROOT": str(installed)},
                        input=json.dumps({"hook_event_name": "SessionStart", "source": source}).encode(),
                    )
                    output = json.loads(result.stdout)["hookSpecificOutput"]
                    assert output["hookEventName"] == "SessionStart"
                    payloads.append(output["additionalContext"])
            assert len(payloads) == 2
            assert all(0 < len(p.encode("utf-16-le")) // 2 < 10_000 for p in payloads)
            parts = []
            for index, payload in enumerate(payloads, 1):
                label, part = payload.split("\n", 1)
                assert label == f"Agent Kernel, part {index} of 2 (sections may arrive in any order)"
                parts.append(part)
            assert all(p.startswith("## ") for p in parts[1:])
            assert "".join(parts).encode("utf-8") == kernel
    finally:
        rmtree(installed)


@given(st.lists(st.tuples(st.sampled_from(["a", "é", "😀"]), st.integers(0, 4_900)),
                min_size=1, max_size=8))
@example([("😀", 4_957), ("a", 1)])
def test_section_split_preserves_bytes_and_bounds(sections):
    spec = importlib.util.spec_from_file_location("session_start", PLUGIN / "hooks/session_start.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    kernel = "# Kernel\r\n\r\n" + "".join(f"## Section\r\n\r\n{char * n}\r\n" for char, n in sections)
    chunks = module.split_kernel(kernel)
    assert "".join(chunks) == kernel
    for index, chunk in enumerate(chunks, 1):
        payload = f"Agent Kernel, part {index} of {len(chunks)} (sections may arrive in any order)\n{chunk}"
        assert 0 < len(payload.encode("utf-16-le")) // 2 < 10_000
    assert all(p.startswith("## ") for p in chunks[1:])
