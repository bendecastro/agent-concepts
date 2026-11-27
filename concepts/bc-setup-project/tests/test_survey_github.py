"""SKILL.md recon: the setup survey mentions `gh` only for a project with a GitHub remote."""
from pathlib import Path

SKILL = (Path(__file__).resolve().parents[1] / "body/SKILL.md").read_text()
RECON = SKILL[SKILL.index("2. **Recon before grilling.**"):SKILL.index("**Kernel in the current harness")]


def test_github_readiness_is_checked_and_reported_only_with_a_github_remote():
    [line] = [l for l in RECON.splitlines() if "GitHub readiness" in l]
    assert "only when a remote points at GitHub" in line
    assert "say nothing about `gh`" in line


def test_issue_lookup_needs_a_github_remote():
    [line] = [l for l in RECON.splitlines() if "open GitHub issues" in l]
    assert "with a GitHub remote" in line
