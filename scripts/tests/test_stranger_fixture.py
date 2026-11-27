"""Test the starting state of the stranger scenario without Pi or network."""
import os
import subprocess
import sys
from pathlib import Path


FIXTURE = Path(__file__).resolve().parents[1] / "stranger_fixture.py"


def test_fixture_starts_on_main_with_only_a_local_origin(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    env = {"PATH": os.defpath, "HOME": str(home), "GIT_CONFIG_NOSYSTEM": "1",
           "GIT_ALLOW_PROTOCOL": "file", "PYTHONDONTWRITEBYTECODE": "1"}
    subprocess.run([sys.executable, str(FIXTURE), str(tmp_path)], env=env, check=True)
    project = tmp_path / "tinylabels"
    origin = tmp_path / "origin.git"

    def git(*args):
        return subprocess.check_output(["git", *args], cwd=project, env=env, text=True).strip()

    assert git("status", "--porcelain") == ""
    assert git("branch", "--show-current") == "main"
    assert git("remote", "-v").splitlines() == [
        f"origin\t{origin} (fetch)", f"origin\t{origin} (push)"]
    assert git("symbolic-ref", "refs/remotes/origin/HEAD") == "refs/remotes/origin/main"
    assert git("rev-parse", "HEAD") == git("--git-dir", str(origin), "rev-parse", "refs/heads/main")
    assert git("ls-files").splitlines() == [".gitignore", "README.md", "pyproject.toml",
                                           "tests/test_labels.py", "tinylabels/__init__.py"]
    result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"],
                            cwd=project, env=env, capture_output=True, text=True, check=True)
    assert "Ran 2 tests" in result.stderr
