"""pi_sandbox.py: masks the harness's global instruction files and checks the system prompt before a run.

Only the Pi process is faked: FAKE_PI loads instruction files the way Pi 1.6.1 does
(agent-dir AGENTS.md and APPEND_SYSTEM.md, the project's AGENTS.md unless -nc) and
reports them in an RPC system message. The bwrap masks are real.
"""
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1]
HELPER = SCRIPTS / "pi_sandbox.py"
sys.path.insert(0, str(SCRIPTS))
import pi_sandbox  # noqa: E402

FAKE_PI = r'''#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
args = sys.argv[1:]
agent = Path(os.environ["HOME"]) / ".pi/agent"
def text(path):
    return path.read_text() if path.is_file() else ""
context = text(agent / "AGENTS.md")
if "-nc" not in args:
    context += text(Path.cwd() / "AGENTS.md")
if "--mode" not in args:
    Path("ran.txt").write_text(" ".join(args) + "\n" + context + text(agent / "APPEND_SYSTEM.md"))
    sys.exit(0)
sys.stdin.readline()
print(json.dumps({"type": "message_start", "message": {"role": "system", "sections": {
    "addendum": text(agent / "APPEND_SYSTEM.md"),
    "project_context": "<project_context>" + context + "</project_context>"}}}), flush=True)
sys.stdin.readline()
'''

needs_bwrap = pytest.mark.skipif(shutil.which("bwrap") is None, reason="bwrap not installed")


@pytest.fixture
def sandbox(tmp_path, monkeypatch):
    home, project = tmp_path / "home", tmp_path / "project"
    (home / ".pi/agent").mkdir(parents=True)
    (home / ".pi/agent/AGENTS.md").write_text("Use xx-private-tool for tests.\n")
    (home / ".pi/agent/APPEND_SYSTEM.md").write_text("Ask examplehost first.\n")
    (home / ".config/agent-concepts").mkdir(parents=True)
    (home / ".config/agent-concepts/personal-terms.txt").write_text("xx-private-tool\nexamplehost\n")
    (home / ".agents/skills/private-skill").mkdir(parents=True)
    project.mkdir()
    subprocess.run(["git", "init", "-q", str(project)], check=True)
    (project / "AGENTS.md").write_text("# Project rules\n\nRun make check.\n")
    fake = tmp_path / "fake-pi"
    fake.write_text(FAKE_PI)
    fake.chmod(0o755)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.delenv("AGENT_CONCEPTS_PERSONAL_TERMS", raising=False)
    monkeypatch.delenv("PI_CODING_AGENT_DIR", raising=False)
    monkeypatch.chdir(project)
    return project, fake


def run_helper(fake, *args):
    return subprocess.run([sys.executable, str(HELPER), *args, "--", str(fake), "-p", "go"],
                          capture_output=True, text=True, timeout=60)


def test_check_fails_when_a_global_instruction_file_leaks(sandbox, monkeypatch):
    project, fake = sandbox
    monkeypatch.setattr(pi_sandbox, "sandboxed", lambda command, cwd: (list(command), []))
    problems, _ = pi_sandbox.check_system_prompt([str(fake), "-p", "go"], str(project))
    assert problems == ["personal term in system prompt: 'examplehost'",
                        "personal term in system prompt: 'xx-private-tool'"]


@needs_bwrap
def test_default_masks_global_files_keeps_project_file_and_runs(sandbox):
    project, fake = sandbox
    result = run_helper(fake, "--prompt-out", "prompt.json")
    assert result.returncode == 0, result.stderr
    ran = (project / "ran.txt").read_text()
    assert ran.splitlines()[0] == "-p go"
    assert "Run make check." in ran and "xx-private-tool" not in ran and "examplehost" not in ran
    assert "Run make check." in json.loads((project / "prompt.json").read_text())["project_context"]


@needs_bwrap
def test_check_fails_with_no_context_files_in_a_project_that_has_agents_md(sandbox):
    project, fake = sandbox
    result = subprocess.run([sys.executable, str(HELPER), "--", str(fake), "-nc", "-p", "go"],
                            capture_output=True, text=True, timeout=60)
    assert result.returncode == 3
    assert f"project instructions did not load: {project / 'AGENTS.md'}" in result.stderr
    assert not (project / "ran.txt").exists()


@needs_bwrap
def test_check_only_does_not_run_and_absent_denylist_is_noted(sandbox):
    project, fake = sandbox
    (Path(os.environ["HOME"]) / ".config/agent-concepts/personal-terms.txt").unlink()
    result = run_helper(fake, "--check-only")
    assert result.returncode == 0, result.stderr
    assert "personal-term check skipped" in result.stderr
    assert not (project / "ran.txt").exists()


def test_mask_plan_resolves_symlinks_and_skips_absent_files(sandbox, tmp_path):
    project, _ = sandbox
    agent = Path(os.environ["HOME"]) / ".pi/agent"
    real = tmp_path / "synced-agents.md"
    real.write_text("x")
    (agent / "AGENTS.md").unlink()
    (agent / "AGENTS.md").symlink_to(real)
    files, dirs = pi_sandbox.mask_plan(str(project))
    assert files == sorted([str(real), str(agent / "APPEND_SYSTEM.md")])
    assert str(Path(os.environ["HOME"]) / ".agents/skills") in dirs
