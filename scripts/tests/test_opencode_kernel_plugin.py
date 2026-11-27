"""Exercise the OpenCode V2 plugin through its session hook boundary."""

from pathlib import Path
from shutil import copytree, rmtree, which
import subprocess

import pytest


PACKAGE = Path(__file__).resolve().parents[2] / "packages/agent-kernel-opencode"


@pytest.mark.skipif(which("node") is None, reason="Node.js is needed to run the OpenCode plugin")
def test_opencode_context_appends_exact_kernel_without_reloading(tmp_path):
    installed = tmp_path / "installed plugin"
    try:
        copytree(PACKAGE, installed)
        (installed / "AGENT-KERNEL.md").write_bytes(b"# Agent Kernel\r\n\r\nExact bytes.\n")
        subprocess.run(["node", "--input-type=module", "-e", r'''
            import assert from "node:assert/strict";
            import { writeFileSync } from "node:fs";
            import plugin from "./index.js";

            let context;
            await plugin.setup({ session: { async hook(kind, handler) {
                assert.equal(kind, "context");
                assert.equal(context, undefined);
                context = handler;
            } } });
            assert.equal(typeof context, "function", "plugin did not register the context hook");

            for (const prompt of ["first", "next"]) {
                const prelude = { type: "text", text: "Keep the original instruction." };
                const event = { system: [prelude], prompt };
                await context(event);
                assert.deepEqual(event.system, [prelude, {
                    type: "text", text: "# Agent Kernel\r\n\r\nExact bytes.\n",
                }]);
                writeFileSync("AGENT-KERNEL.md", "changed on disk");
            }
        '''], cwd=installed, check=True)
    finally:
        if installed.exists():
            rmtree(installed)
