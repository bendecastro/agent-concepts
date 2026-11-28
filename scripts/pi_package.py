#!/usr/bin/env python3
"""Generate and check the Pi package manifest (`package.json`, `pi` key).

`pi install` reads `pi.skills` to find skill directories. Each entry points at a
public skill's existing `concepts/<name>/body`, so the package ships the
canonical bodies with no copy. The list comes from concepts/public-skills.json;
`files` (what `npm pack` and `npm publish` ship) is the same bodies plus the Pi kernel
extension and the kernel installer behind the `agent-concepts` bin, so nothing else in
the repository reaches npm. npm adds package.json, README and LICENSE itself. Other package.json fields (name, version) are kept as written.
"""

from __future__ import annotations

import json
from pathlib import Path

from public_skills import skill_path


MANIFEST_PATH = "package.json"
PUBLIC_LIST_PATH = "concepts/public-skills.json"
KERNEL_EXTENSION_DIR = "packages/agent-kernel-pi/"
# The `agent-concepts kernel install <file>` bin runs install.py and copies the
# AGENT-KERNEL.md staged beside it, so the whole directory ships.
KERNEL_INSTALLER_DIR = "packages/agent-kernel/"
BIN = {"agent-concepts": "packages/agent-kernel/cli.js"}
BASE_MANIFEST = {
    "name": "agent-concepts",
    "description": "Agent skills from agent-concepts, packaged for Pi.",
    "license": "MIT",
    "keywords": ["pi-package"],
}


def skill_paths(root: Path) -> list[str]:
    listing = json.loads((root / PUBLIC_LIST_PATH).read_text(encoding="utf-8"))
    return [skill_path(root, name) for name in sorted(listing["skills"])]


def shipped_files(root: Path) -> list[str]:
    return [path[2:] + "/" for path in skill_paths(root)] + [KERNEL_EXTENSION_DIR, KERNEL_INSTALLER_DIR]


def render_manifest(root: Path) -> str:
    path = root / MANIFEST_PATH
    manifest = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else dict(BASE_MANIFEST)
    pi = manifest.setdefault("pi", {})
    pi["skills"] = skill_paths(root)
    manifest.pop("private", None)
    manifest["files"] = shipped_files(root)
    manifest["bin"] = dict(BIN)
    return json.dumps(manifest, indent=2) + "\n"


def write_manifest(root: Path) -> Path:
    path = root / MANIFEST_PATH
    text = render_manifest(root)
    path.write_text(text, encoding="utf-8")
    return path


def check_manifest(root: Path) -> list[str]:
    path = root / MANIFEST_PATH
    if not path.is_file():
        return [f"missing {MANIFEST_PATH}; run scripts/lint.py --write-pi-package"]
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("pi", {}).get("skills") != skill_paths(root):
        return [f"{MANIFEST_PATH} `pi.skills` does not match {PUBLIC_LIST_PATH}; run scripts/lint.py --write-pi-package"]
    if manifest.get("files") != shipped_files(root):
        return [f"{MANIFEST_PATH} `files` does not match {PUBLIC_LIST_PATH}; run scripts/lint.py --write-pi-package"]
    if manifest.get("bin") != BIN:
        return [f"{MANIFEST_PATH} `bin` does not match {BIN}; run scripts/lint.py --write-pi-package"]
    return []
