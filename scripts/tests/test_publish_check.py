"""Exercise the bundled and compatibility CLIs using only a disposable policy."""

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
BUNDLED = ROOT / "concepts/bc-pipeline-to-done/body/scripts/publish-check.py"
LEGACY = ROOT / "scripts/publish-check.py"
REMOTE = "https://example.invalid/project.git"


@pytest.mark.parametrize("entry_point", [BUNDLED, LEGACY], ids=["bundled", "legacy"])
def test_publish_check(entry_point, tmp_path):
    repo = tmp_path / "repo"
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", REMOTE], check=True)
    config = tmp_path / "config"
    policy = config / "agent-concepts" / "publish.yaml"
    policy.parent.mkdir(parents=True)
    env = {**os.environ, "XDG_CONFIG_HOME": str(config)}

    def run(branch):
        return subprocess.run(
            [sys.executable, str(entry_point), "--repo", str(repo), "--remote", REMOTE,
             "--branch", branch],
            cwd=tmp_path, env=env, capture_output=True, text=True,
        )

    missing = run("main")
    assert (missing.returncode, missing.stdout, missing.stderr) == (
        2, f"ASK: no policy at {policy} — no rule can match; ask the user or do not publish\n"
        "PUSH AFTER COMMIT clause: could not be found because the policy file is unavailable; "
        "do not infer it.\n", "",
    )

    policy.write_text("# PUSH AFTER COMMIT: sample clause\n" + json.dumps({"rules": [{
        "id": "fixture", "scope": {"paths": [str(repo)], "remotes": [REMOTE]},
        "branches": ["main"], "allow": ["push"], "when": ["agent-authored-only"],
    }]}), encoding="utf-8")
    match = run("main")
    assert (match.returncode, match.stdout, match.stderr) == (
        0, "MATCH: rule 'fixture' allows push here.\n"
        "Before pushing, verify these conditions yourself (not machine-checkable): agent-authored-only.\n"
        "PUSH AFTER COMMIT clause from policy:\nPUSH AFTER COMMIT: sample clause\n", "",
    )

    no_match = run("other")
    assert (no_match.returncode, no_match.stdout, no_match.stderr) == (
        2, "ASK: no allow rule matches this repo/remote/branch — publishing requires current "
        "explicit user instruction; if asking is impossible, do not publish\n", "",
    )
