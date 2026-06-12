#!/usr/bin/env python3
"""Answer the objective part of the publish policy: may this push be allowed?

Usage:
  publish-check.py --repo PATH --remote URL --branch NAME [--changed-file F]...

Checks path/remote/branch against policies/publish.yaml allow rules and
enforces self-amendment immunity (changes under agents/policies/ are never
publishable by rule). The subjective `when` conditions (agent-authored-only,
after-agent-commit) remain the agent's judgment — this script cannot see them.

Exit codes: 0 = rule matches (verify `when` conditions yourself, then push),
2 = no rule matches (ask the user; if asking is impossible, do not publish).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ASK: PyYAML unavailable, cannot evaluate policy — treat as no matching rule")
    sys.exit(2)

POLICY = Path(__file__).resolve().parents[1] / "policies" / "publish.yaml"


def norm(p: str) -> Path:
    return Path(p).expanduser().resolve()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--remote", required=True)
    ap.add_argument("--branch", required=True)
    ap.add_argument("--changed-file", action="append", default=[],
                    help="repo-relative path changed by the commits to be pushed (repeatable)")
    args = ap.parse_args()

    if not POLICY.is_file():
        print("ASK: no policy file (off-vault?) — no rule can match; ask the user or do not publish")
        return 2

    policy = yaml.safe_load(POLICY.read_text())
    repo = norm(args.repo)

    for rule in policy.get("rules", []):
        scope = rule.get("scope", {})
        paths = [norm(p) for p in scope.get("paths", [])]
        if not any(repo == p or p in repo.parents for p in paths):
            continue
        if args.remote not in scope.get("remotes", []):
            continue
        if args.branch not in rule.get("branches", []):
            continue
        excluded = rule.get("exclude_changes_under", []) + ["agents/policies/"]
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
        return 0

    print("ASK: no allow rule matches this repo/remote/branch — "
          "publishing requires current explicit user instruction; if asking is impossible, do not publish")
    return 2


if __name__ == "__main__":
    sys.exit(main())
