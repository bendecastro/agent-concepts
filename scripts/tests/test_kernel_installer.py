"""Exercise the standalone CLI against a named instructions file."""

import runpy
import subprocess
import sys
from pathlib import Path
from shutil import copyfile, rmtree

import pytest
from hypothesis import HealthCheck, example, given, settings, strategies as st


INSTALLER = Path(__file__).resolve().parents[2] / "packages/agent-kernel/install.py"
BEGIN = b"<!-- agent-kernel:begin v1 -->\n"
END = b"<!-- agent-kernel:end v1 -->\n"


@pytest.fixture
def instructions(tmp_path):
    case = tmp_path / "case"
    case.mkdir()
    try:
        yield case / "instructions.md"
    finally:
        rmtree(case)


def run_installer(instructions, *options, installer=INSTALLER):
    return subprocess.run(
        [sys.executable, "-I", str(installer), str(instructions), *options],
        cwd=instructions.parent, capture_output=True,
    )


def block():
    return BEGIN + INSTALLER.with_name("AGENT-KERNEL.md").read_bytes() + END


def test_install_appends_kernel_without_changing_existing_bytes(instructions):
    original = b"# My rules\r\nKeep me: \xff\n"
    instructions.write_bytes(original)
    standalone = instructions.parent / "standalone-package"
    standalone.mkdir()
    copyfile(INSTALLER, standalone / INSTALLER.name)
    copyfile(INSTALLER.with_name("AGENT-KERNEL.md"), standalone / "AGENT-KERNEL.md")
    result = run_installer(instructions, installer=standalone / INSTALLER.name)
    assert result.returncode == 0, result.stderr
    assert instructions.read_bytes() == original + block()


def test_upgrade_replaces_old_version_in_place(instructions):
    before, after = b"# Before\r\n", b"# After without a final newline"
    old = b"<!-- agent-kernel:begin v0 -->\r\nOld kernel\r\n<!-- agent-kernel:end v0 -->\r\n"
    instructions.write_bytes(before + old + after)
    result = run_installer(instructions)
    assert result.returncode == 0, result.stderr
    assert instructions.read_bytes() == before + block() + after


def test_remove_preserves_bytes_before_and_after_block(instructions):
    before, after = b"Before\r\n", b"After without newline \xff"
    instructions.write_bytes(before + block() + after)
    result = run_installer(instructions, "--remove")
    assert result.returncode == 0, result.stderr
    assert instructions.read_bytes() == before + after


def test_identical_install_does_not_rewrite_file(instructions):
    instructions.write_bytes(b"# My rules\n" + block())
    before = instructions.stat()
    result = run_installer(instructions)
    assert result.returncode == 0, result.stderr
    after = instructions.stat()
    assert (after.st_ino, after.st_mtime_ns) == (before.st_ino, before.st_mtime_ns)


@pytest.mark.parametrize("markers", [
    pytest.param(BEGIN, id="orphan-begin"),
    pytest.param(END, id="orphan-end"),
    pytest.param(END + BEGIN, id="reversed"),
    pytest.param(BEGIN + END.replace(b"v1", b"v2"), id="version-mismatch"),
    pytest.param(BEGIN + BEGIN + END, id="nested-begin"),
    pytest.param((BEGIN + END) * 2, id="duplicate-block"),
    pytest.param(b" <!-- agent-kernel:begin v1 -->\n" + END, id="indented-marker"),
    pytest.param(b"<!-- agent-kernel:begin v1\n" + END, id="invalid-marker"),
])
@pytest.mark.parametrize("options", [(), ("--remove",)], ids=["install", "remove"])
def test_refuses_malformed_or_duplicate_markers_without_writing(instructions, markers, options):
    original = b"Before\n" + markers + b"After\n"
    instructions.write_bytes(original)
    result = run_installer(instructions, *options)
    assert result.returncode != 0
    assert b"malformed or duplicate agent-kernel markers" in result.stderr
    assert instructions.read_bytes() == original


# Each generated example overwrites the same tmp_path-owned file before use.
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(original=st.binary(max_size=256).filter(lambda value: b"agent-kernel" not in value))
@example(original=b"\x00")
@example(original=b"\xef\xbb\xbf# My rules without a final newline")
def test_install_then_remove_restores_all_original_bytes(instructions, original):
    update_file = runpy.run_path(str(INSTALLER))["update_file"]
    instructions.write_bytes(original)
    try:
        update_file(instructions)
        assert instructions.read_bytes() != original
        update_file(instructions, remove=True)
        assert instructions.read_bytes() == original
    finally:
        instructions.unlink()
