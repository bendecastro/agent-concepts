#!/usr/bin/env python3
"""Check that every install description carries the release version, and optionally a tag.

The version has one home, `version` in package.json (the Pi package). The Claude Code and
Codex plugin manifests and the Claude Code marketplace copy it when regenerated
(`scripts/lint.py --write-plugin-manifests`). Lint runs the no-tag check; a release runs
`python3 scripts/release_check.py vMAJOR.MINOR.PATCH`, which also requires the tag to name the
same version, CHANGELOG.md to have an entry for it, and the README's Install section to name
that tag and no other, to show the unpinned Pi install from npm (`pi install npm:agent-concepts`,
which `pi update --extensions` moves to each release promoted to `latest`) and to pin npm only to this version. Exit 1 on any
problem.
"""

from __future__ import annotations

import json
import re
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import plugin_manifests  # noqa: E402

CHANGELOG = "CHANGELOG.md"
README = "README.md"
TAG_PATTERN = re.compile(r"v(\d+\.\d+\.\d+)")
ANY_TAG = re.compile(r"\bv\d+\.\d+\.\d+\b")
NPM_PACKAGE = "agent-concepts"
NPM_UNPINNED = re.compile(rf"pi install npm:{NPM_PACKAGE}(?![@\w-])")
# A version pin starts with a digit; `@next` names a dist-tag, not a version.
NPM_PIN = re.compile(rf"(?:npm:|npx -y ){NPM_PACKAGE}@(\d\S*?)(?=[`\s]|$)", re.MULTILINE)


def readme_install_problems(root: Path, tag: str) -> list[str]:
    """README#install must name the tag being released, and no older or other tag."""
    readme = root / README
    text = readme.read_text(encoding="utf-8") if readme.is_file() else ""
    section = re.search(r"^## Install\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    body = section.group(1) if section else ""
    problems = []
    if tag not in ANY_TAG.findall(body):
        problems.append(f"{README} section `## Install` does not name tag {tag}")
    others = sorted(set(ANY_TAG.findall(body)) - {tag})
    if others:
        problems.append(f"{README} section `## Install` names other tags: {', '.join(others)}")
    if not NPM_UNPINNED.search(body):
        problems.append(f"{README} section `## Install` does not show `pi install npm:{NPM_PACKAGE}`")
    version = tag[1:]
    for pinned in sorted(set(NPM_PIN.findall(body)) - {version}):
        problems.append(f"{README} section `## Install` pins {NPM_PACKAGE}@{pinned}, not {version}")
    return problems


def _read(root: Path, relative: str) -> dict:
    return json.loads((root / relative).read_text(encoding="utf-8"))


def declared_versions(root: Path) -> dict[str, str | None]:
    """The version each description declares, keyed by file (the marketplace by its plugin entry).

    The Codex marketplace has no version field; it points at the Codex plugin manifest.
    """
    versions = {}
    for relative in (plugin_manifests.VERSION_HOME, plugin_manifests.CLAUDE_PLUGIN,
                     plugin_manifests.CODEX_PLUGIN):
        path = root / relative
        versions[relative] = _read(root, relative).get("version") if path.is_file() else None
    marketplace = root / plugin_manifests.CLAUDE_MARKETPLACE
    entries = _read(root, plugin_manifests.CLAUDE_MARKETPLACE)["plugins"] if marketplace.is_file() else []
    versions[plugin_manifests.CLAUDE_MARKETPLACE] = next(
        (e.get("version") for e in entries if e.get("name") == plugin_manifests.PLUGIN_NAME), None)
    return versions


def version_problems(root: Path, tag: str | None = None) -> list[str]:
    versions = declared_versions(root)
    home = versions[plugin_manifests.VERSION_HOME]
    problems = []
    if tag is not None:
        match = TAG_PATTERN.fullmatch(tag)
        if not match:
            return [f"tag {tag} is not vMAJOR.MINOR.PATCH"]
        if match.group(1) != home:
            problems.append(f"tag {tag} does not match version {home} in {plugin_manifests.VERSION_HOME}")
        changelog = root / CHANGELOG
        entry = re.compile(rf"^## \[{re.escape(match.group(1))}\]", re.MULTILINE)
        if not changelog.is_file() or not entry.search(changelog.read_text(encoding="utf-8")):
            problems.append(f"{CHANGELOG} has no `## [{match.group(1)}]` entry for tag {tag}")
        problems.extend(readme_install_problems(root, tag))
    if not home:
        problems.append(f"{plugin_manifests.VERSION_HOME} has no version")
    for relative, version in versions.items():
        if relative != plugin_manifests.VERSION_HOME and version != home:
            problems.append(f"{relative} declares version {version}, {plugin_manifests.VERSION_HOME} "
                            f"declares {home}; run scripts/lint.py --write-plugin-manifests")
    return problems


def _visible_markdown(text: str) -> str:
    """Drop HTML comments and fenced code, which readers do not see as entries."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return re.sub(r"^(```|~~~)[^\n]*\n.*?^\1[^\n]*$", "", text, flags=re.M | re.S)


def removed_skill_problems(previous: set[str], current: set[str], changelog: str) -> list[str]:
    changelog = _visible_markdown(changelog)
    sections = re.findall(r"^### Removed\s*\n(.*?)(?=^## |^### |\Z)", changelog, re.M | re.S)
    removed = set(re.findall(r"^- `([a-z0-9-]+)`:[ \t]+\S", "\n".join(sections), re.M))
    return [f"skill `{name}` disappeared without an alias or CHANGELOG Removed entry"
            for name in sorted(previous - current - removed)]


def previous_release_problems(root: Path, tag: str) -> list[str]:
    version = tuple(map(int, tag[1:].split(".")))
    tags = subprocess.run(["git", "tag", "--list", "v*"], cwd=root, text=True, capture_output=True)
    if tags.returncode:
        return ["cannot read release tags: " + tags.stderr.strip()]
    candidates = [(tuple(map(int, t[1:].split("."))), t) for t in tags.stdout.splitlines()
                  if TAG_PATTERN.fullmatch(t) and tuple(map(int, t[1:].split("."))) < version]
    if not candidates:
        return []
    previous = max(candidates)[1]
    result = subprocess.run(["git", "show", f"{previous}:concepts/public-skills.json"],
                            cwd=root, text=True, capture_output=True)
    if result.returncode:
        return [f"cannot read public skills from {previous}: {result.stderr.strip()}"]
    old = set(json.loads(result.stdout)["skills"])
    current = set(_read(root, "concepts/public-skills.json")["skills"])
    text = (root / CHANGELOG).read_text(encoding="utf-8")
    match = re.search(rf"^## \[{re.escape(tag[1:])}\][^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return removed_skill_problems(old, current, match.group(1) if match else "")


def classify_scan(issues) -> tuple[list[str], list[str]]:
    """Split personal-terms scan issues: only warning-severity term matches are nonblocking."""
    warnings, problems = [], []
    for issue in issues:
        nonblocking = issue.severity == "WARN" and issue.message.startswith("personal term in ")
        (warnings if nonblocking else problems).append(issue.message)
    return warnings, problems


def main(argv: list[str] | None = None, root: Path = ROOT) -> int:
    args = sys.argv[1:] if argv is None else argv
    args = list(args)
    skip_personal_terms = "--no-personal-terms" in args
    if skip_personal_terms:
        args.remove("--no-personal-terms")
    if len(args) > 1 or any(arg.startswith("--") for arg in args):
        print("usage: release_check.py [--no-personal-terms] [vMAJOR.MINOR.PATCH]", file=sys.stderr)
        return 2
    tag = args[0] if args else None
    problems = version_problems(root, tag)
    if not skip_personal_terms:
        import lint  # Local import: lint imports release_check for version checks.
        issues = []
        lint.lint_personal_terms(issues, root, required=True)
        warnings, scan_problems = classify_scan(issues)
        for warning in warnings:
            print(f"release check: warning: {warning}")
        problems.extend(scan_problems)
    if tag and TAG_PATTERN.fullmatch(tag) and (root / ".git").exists():
        problems.extend(previous_release_problems(root, tag))
    for problem in problems:
        print(f"release check: {problem}")
    if not problems:
        version = declared_versions(root)[plugin_manifests.VERSION_HOME]
        print(f"release check: every description declares {version}" + (f", matching {tag}" if tag else ""))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
