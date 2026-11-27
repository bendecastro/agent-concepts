"""Exercise the Codex marketplace hook command from a disposable installed copy."""

import json
import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[2]


def test_session_start_emits_exact_kernel_as_developer_context(tmp_path):
    marketplace = json.loads((ROOT / ".agents/plugins/marketplace.json").read_text())
    entry = next(plugin for plugin in marketplace["plugins"] if plugin["name"] == "agent-kernel")
    package = tmp_path / "installed plugin"
    project = tmp_path / "project"
    try:
        shutil.copytree(ROOT / entry["source"]["path"], package)
        project.mkdir()
        kernel = b"# Agent Kernel\r\n\r\nExact bytes, including the trailing newline.\n"
        (package / "AGENT-KERNEL.md").write_bytes(kernel)
        assert json.loads((package / ".codex-plugin/plugin.json").read_text())["name"] == entry["name"]
        config = json.loads((package / "hooks/hooks.json").read_text())
        [matcher] = config["hooks"]["SessionStart"]
        [hook] = matcher["hooks"]
        result = subprocess.run(hook["command"], shell=True, check=True, capture_output=True,
                                cwd=project, env={**os.environ, "PLUGIN_ROOT": str(package)},
                                input=b'{"hook_event_name":"SessionStart","source":"startup"}')
        assert json.loads(result.stdout) == {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": kernel.decode("utf-8"),
            },
        }
    finally:
        if package.exists():
            shutil.rmtree(package)
        if project.exists():
            project.rmdir()
