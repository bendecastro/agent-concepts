"""Build and lint the staged kernel with a disposable checkout fixture."""

import sys
from pathlib import Path
from shutil import rmtree

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def checkout(tmp_path):
    root = tmp_path / "checkout"
    canonical = root / "concepts/agent-kernel/body/AGENT-KERNEL.md"
    canonical.parent.mkdir(parents=True)
    canonical.write_bytes(b"# Agent Kernel\r\n\nKeep exact bytes.\n")
    try:
        yield root, canonical, root / "packages/agent-kernel/AGENT-KERNEL.md"
    finally:
        rmtree(root)


def test_build_stages_canonical_bytes_without_rewriting_an_identical_copy(checkout):
    from kernel_package import stage_kernel

    root, canonical, staged = checkout
    stage_kernel(root)
    assert staged.is_file() and not staged.is_symlink()
    assert staged.read_bytes() == canonical.read_bytes()
    before = staged.stat()
    stage_kernel(root)
    after = staged.stat()
    assert (after.st_ino, after.st_mtime_ns) == (before.st_ino, before.st_mtime_ns)


def test_lint_rejects_edited_staged_bytes(checkout, monkeypatch):
    import lint
    from kernel_package import stage_kernel

    root, _, staged = checkout
    monkeypatch.setattr(lint, "ROOT", root)
    stage_kernel(root)
    issues = []
    lint.lint_kernel_package(issues)
    assert issues == []
    staged.write_bytes(b"# Edited copy\n")
    lint.lint_kernel_package(issues)
    assert len(issues) == 1
    assert issues[0].severity == "ERROR"
    assert "python3 scripts/kernel_package.py" in issues[0].message
