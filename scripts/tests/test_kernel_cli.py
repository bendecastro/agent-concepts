"""Run the `agent-concepts kernel` bin from the packed npm tarball, with no checkout."""

import subprocess
from pathlib import Path
from shutil import rmtree, which
from tempfile import mkdtemp

import pytest


ROOT = Path(__file__).resolve().parents[2]
KERNEL = ROOT / "packages/agent-kernel/AGENT-KERNEL.md"
BEGIN = b"<!-- agent-kernel:begin v1 -->\n"
END = b"<!-- agent-kernel:end v1 -->\n"

pytestmark = pytest.mark.skipif(not (which("npm") and which("node") and which("python3")),
                                reason="needs npm, node and python3")


@pytest.fixture(scope="module")
def bin_path():
    scratch = Path(mkdtemp(prefix="agent-concepts-pack-"))
    try:
        subprocess.run(["npm", "pack", "--pack-destination", str(scratch)],
                       cwd=ROOT, check=True, capture_output=True)
        [tarball] = scratch.glob("*.tgz")
        prefix = scratch / "install"
        subprocess.run(
            ["npm", "install", "--offline", "--no-audit", "--no-fund", "--prefix", str(prefix), str(tarball)],
            check=True, capture_output=True)
        yield prefix / "node_modules/.bin/agent-concepts"
    finally:
        rmtree(scratch)


def run(bin_path, *args):
    return subprocess.run([str(bin_path), *args], capture_output=True)


def block():
    return BEGIN + KERNEL.read_bytes() + END


def test_install_reinstall_and_remove_round_trip(bin_path, tmp_path):
    target = tmp_path / "AGENTS.md"
    original = b"# My rules\n"
    target.write_bytes(original)
    assert run(bin_path, "kernel", "install", str(target)).returncode == 0
    assert target.read_bytes() == original + block()
    assert run(bin_path, "kernel", "install", str(target)).returncode == 0
    assert target.read_bytes() == original + block()
    assert run(bin_path, "kernel", "remove", str(target)).returncode == 0
    assert target.read_bytes() == original


def test_install_creates_a_missing_file_and_remove_leaves_a_missing_file_alone(bin_path, tmp_path):
    target = tmp_path / "missing" / "GEMINI.md"
    target.parent.mkdir()
    assert run(bin_path, "kernel", "remove", str(target)).returncode == 0
    assert not target.exists()
    assert run(bin_path, "kernel", "install", str(target)).returncode == 0
    assert target.read_bytes() == block()


def test_unknown_command_prints_usage(bin_path, tmp_path):
    result = run(bin_path, "kernel", "add", str(tmp_path / "x.md"))
    assert result.returncode == 2
    assert b"usage: agent-concepts kernel install|remove" in result.stderr
