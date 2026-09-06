#!/usr/bin/env python3
"""Answer the objective part of the publish policy: may this push be allowed?

Usage:
  publish-check.py --repo PATH --remote URL --branch NAME [--changed-file F]...

Checks path/remote/branch against the user-owned policy at
~/.config/agent-concepts/publish.yaml and enforces self-amendment immunity (a
commit touching the policy file is never publishable by rule). The subjective
`when` conditions (agent-authored-only, after-agent-commit) remain the agent's
judgment — this script cannot see them.

The policy is deliberately read from outside the repository, and there is no
in-repo fallback: a private authorization file living inside a public checkout
is one `git add -f` away from being published. See policies/publish.example.yaml.

Exit codes: 0 = rule matches (verify `when` conditions yourself, then push),
2 = no rule matches (ask the user; if asking is impossible, do not publish).
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ASK: PyYAML unavailable, cannot evaluate policy — treat as no matching rule")
    sys.exit(2)

CONFIG_HOME = Path(os.environ.get("XDG_CONFIG_HOME", "~/.config")).expanduser()
POLICY = CONFIG_HOME / "agent-concepts" / "publish.yaml"


def norm(p: str) -> Path:
    return Path(p).expanduser().resolve()


def push_after_commit_clause(policy_text: str) -> str | None:
    """Return the policy's contiguous PUSH AFTER COMMIT comment block."""
    lines = policy_text.splitlines()
    start = next(
        (i for i, line in enumerate(lines)
         if line.lstrip().startswith("#") and "PUSH AFTER COMMIT:" in line),
        None,
    )
    if start is None:
        return None

    block: list[str] = []
    for line in lines[start:]:
        stripped = line.lstrip()
        if not stripped.startswith("#"):
            break
        content = stripped[1:]
        if content.startswith(" "):
            content = content[1:]
        block.append(content)
    return "\n".join(block)


def policy_path_within(repo: Path) -> str | None:
    """Repo-relative path of the policy file, if it lives inside this repo.

    Self-amendment immunity has to follow the actual file rather than a fixed
    string: the policy usually sits outside any repository, but a user may sync
    their config directory through one (via a symlink), in which case pushing
    that repo could carry a policy change.
    """
    try:
        return str(POLICY.resolve().relative_to(repo))
    except (ValueError, OSError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--remote", required=True)
    ap.add_argument("--branch", required=True)
    ap.add_argument("--changed-file", action="append", default=[],
                    help="repo-relative path changed by the commits to be pushed (repeatable)")
    args = ap.parse_args()

    if not POLICY.is_file():
        print(f"ASK: no policy at {POLICY} — no rule can match; ask the user or do not publish")
        print("PUSH AFTER COMMIT clause: could not be found because the policy file is unavailable; do not infer it.")
        return 2

    try:
        policy_text = POLICY.read_text()
    except OSError:
        print(f"ASK: policy at {POLICY} could not be read — no rule can match; ask the user or do not publish")
        print("PUSH AFTER COMMIT clause: could not be found because the policy file could not be read; do not infer it.")
        return 2

    policy = yaml.safe_load(policy_text)
    repo = norm(args.repo)

    for rule in policy.get("rules", []):
        scope = rule.get("scope", {})
        paths = [norm(p) for p in scope.get("paths", [])]
        if not any(repo == p or p in repo.parents for p in paths):
            continue
        if args.remote not in scope.get("remotes", []):
            continue
        # Branch patterns support glob wildcards (fnmatch); a plain name with no
        # wildcards still matches only itself. Lets rules authorize families like
        # `bc-drain-claims/issue-*` without listing every issue number.
        if not any(fnmatch.fnmatch(args.branch, b) for b in rule.get("branches", [])):
            continue
        excluded = list(rule.get("exclude_changes_under", []))
        own_path = policy_path_within(repo)
        if own_path:
            excluded.append(own_path)
        hits = [f for f in args.changed_file
                if any(f.startswith(e.rstrip("/") + "/") or f == e.rstrip("/") for e in excluded)]
        if hits:
            print(f"ASK: rule '{rule.get('id')}' matches repo/remote/branch, but these changes "
                  f"are excluded from rule-based publishing: {', '.join(hits)} — "
                  "policy changes require current explicit user instruction")
            return 2
        when = ", ".join(rule.get("when", [])) or "none"
        print(f"MATCH: rule '{rule.get('id')}' allows {', '.join(rule.get('allow', []))} here.")
        print(f"Before pushing, verify these conditions yourself (not machine-checkable): {when}.")
        print("PUSH AFTER COMMIT clause from policy:")
        clause = push_after_commit_clause(policy_text)
        if clause is None:
            print("Could not find the PUSH AFTER COMMIT clause in the policy file; do not infer it.")
        else:
            print(clause)
        return 0

    print("ASK: no allow rule matches this repo/remote/branch — "
          "publishing requires current explicit user instruction; if asking is impossible, do not publish")
    return 2


if __name__ == "__main__":
    sys.exit(main())
