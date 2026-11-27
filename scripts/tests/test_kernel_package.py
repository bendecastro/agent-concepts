"""Build and lint the staged kernel with a disposable checkout fixture."""

import subprocess
import sys
from pathlib import Path
from shutil import rmtree, which

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PACKAGES = (
    "agent-kernel", "agent-kernel-pi", "agent-kernel-claude",
    "agent-kernel-codex", "agent-kernel-opencode",
)


@pytest.fixture
def checkout(tmp_path):
    root = tmp_path / "checkout"
    canonical = root / "concepts/agent-kernel/body/AGENT-KERNEL.md"
    canonical.parent.mkdir(parents=True)
    canonical.write_bytes(b"# Agent Kernel\r\n\nKeep exact bytes.\n")
    try:
        yield root, canonical
    finally:
        rmtree(root)


@pytest.mark.parametrize("package", PACKAGES)
def test_build_stages_canonical_bytes_without_rewriting_an_identical_copy(checkout, package):
    from kernel_package import stage_kernel

    root, canonical = checkout
    staged = root / "packages" / package / "AGENT-KERNEL.md"
    stage_kernel(root)
    assert staged.is_file() and not staged.is_symlink()
    assert staged.read_bytes() == canonical.read_bytes()
    before = staged.stat()
    stage_kernel(root)
    after = staged.stat()
    assert (after.st_ino, after.st_mtime_ns) == (before.st_ino, before.st_mtime_ns)


@pytest.mark.parametrize("package", PACKAGES)
def test_lint_rejects_edited_staged_bytes(checkout, monkeypatch, package):
    import lint
    from kernel_package import stage_kernel

    root, _ = checkout
    path = Path("packages") / package / "AGENT-KERNEL.md"
    monkeypatch.setattr(lint, "ROOT", root)
    stage_kernel(root)
    issues = []
    lint.lint_kernel_package(issues)
    assert issues == []
    staged = root / path
    staged.parent.mkdir(parents=True, exist_ok=True)
    staged.write_bytes(b"# Edited copy\n")
    lint.lint_kernel_package(issues)
    assert len(issues) == 1
    assert issues[0].severity == "ERROR"
    assert str(path) in issues[0].message
    assert "python3 scripts/kernel_package.py" in issues[0].message


@pytest.mark.skipif(which("node") is None, reason="Node.js is needed to run the Pi extension")
def test_pi_extension_reads_once_and_keeps_the_same_section(checkout):
    from kernel_package import stage_kernel

    root, _ = checkout
    stage_kernel(root)
    package = root / "packages/agent-kernel-pi"
    source = Path(__file__).resolve().parents[2] / "packages/agent-kernel-pi"
    for name in ("index.js", "package.json"):
        (package / name).write_bytes((source / name).read_bytes())
    subprocess.run(["node", "--input-type=module", "-e", r"""
        import assert from "node:assert/strict";
        import fs from "node:fs";
        import { syncBuiltinESMExports } from "node:module";

        const kernel = new URL("./AGENT-KERNEL.md", import.meta.url);
        const original = fs.readFileSync;
        let reads = 0;
        fs.readFileSync = (path, ...args) => {
            if (String(path).endsWith("/AGENT-KERNEL.md")) reads++;
            return original(path, ...args);
        };
        syncBuiltinESMExports();

        const { default: extension } = await import("./index.js");
        let beforeStart;
        extension({ on(event, fn) {
            assert.equal(event, "before_agent_start");
            assert.equal(beforeStart, undefined);
            beforeStart = fn;
        } });

        for (const prompt of ["first", "next"]) {
            const options = { sections: { other: "keep me" }, selectedTools: ["read"] };
            assert.equal(await beforeStart({ prompt, systemPromptOptions: options }), undefined);
            assert.deepEqual(options, {
                sections: { other: "keep me", "agent-kernel": "# Agent Kernel\r\n\nKeep exact bytes.\n" },
                selectedTools: ["read"],
            });
            assert.deepEqual(Object.keys(options.sections), ["other", "agent-kernel"]);
            fs.writeFileSync(kernel, "changed on disk");
        }
        assert.equal(reads, 1);
    """], cwd=package, check=True)
