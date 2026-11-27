#!/usr/bin/env python3
"""Generate and check the Claude Code and Codex plugin manifests and marketplaces.

The repository root is the skills plugin for both agents. Each manifest lists every
public skill's `concepts/<name>/body` folder by path, read from the committed
public skill list, so no skill is copied or linked into a second tree. Why
paths rather than a `skills/` folder of symlinks: Claude Code's installer
copies symlinked folders as files, but Codex's installer (0.153) drops them,
leaving an empty skills folder. Both installers accept a list of skill paths.
"""

from __future__ import annotations

import json
from pathlib import Path


PLUGIN_NAME = "agent-concepts"
# The release version has one home, `version` in package.json; the manifests copy it.
VERSION_HOME = "package.json"
DESCRIPTION = ("Every public agent-concepts skill: planning, TDD, code review, debugging, "
               "subagent workflows and upkeep, with bc- names.")
AUTHOR = {"name": "agent-concepts contributors"}
LICENSE = "MIT"

LIST_PATH = "concepts/public-skills.json"
CLAUDE_PLUGIN = ".claude-plugin/plugin.json"
CLAUDE_MARKETPLACE = ".claude-plugin/marketplace.json"
CLAUDE_KERNEL_ROOT = "packages/agent-kernel-claude"
CLAUDE_KERNEL_PLUGIN = f"{CLAUDE_KERNEL_ROOT}/.claude-plugin/plugin.json"
CODEX_PLUGIN = ".codex-plugin/plugin.json"
CODEX_MARKETPLACE = ".agents/plugins/marketplace.json"
CODEX_KERNEL_ROOT = "packages/agent-kernel-codex"
CODEX_KERNEL_PLUGIN = f"{CODEX_KERNEL_ROOT}/{CODEX_PLUGIN}"


def _skill_paths(root: Path) -> list[str]:
    listing = json.loads((root / LIST_PATH).read_text(encoding="utf-8"))
    return [f"./concepts/{name}/body" for name in sorted(listing["skills"])]


def plugin_version(root: Path) -> str:
    return json.loads((root / VERSION_HOME).read_text(encoding="utf-8"))["version"]


def render_manifests(root: Path) -> dict[str, dict]:
    skills = _skill_paths(root)
    version = plugin_version(root)
    plugin = {
        "name": PLUGIN_NAME,
        "version": version,
        "description": DESCRIPTION,
        "author": AUTHOR,
        "license": LICENSE,
        "skills": skills,
    }
    kernel = {
        "name": "agent-kernel",
        "version": version,
        "description": "Opt-in always-on instructions for coding agents.",
        "author": AUTHOR,
        "license": LICENSE,
    }
    return {
        CLAUDE_KERNEL_PLUGIN: kernel,
        CLAUDE_PLUGIN: plugin,
        CLAUDE_MARKETPLACE: {
            "name": PLUGIN_NAME,
            "owner": AUTHOR,
            "metadata": {"description": DESCRIPTION},
            "plugins": [
                {"name": PLUGIN_NAME, "source": "./", "description": DESCRIPTION, "version": version},
                {"name": kernel["name"], "source": f"./{CLAUDE_KERNEL_ROOT}",
                 "description": kernel["description"], "version": version},
            ],
        },
        CODEX_PLUGIN: {
            **plugin,
            "interface": {
                "displayName": "Agent Concepts",
                "shortDescription": "Every public agent-concepts skill.",
                "developerName": AUTHOR["name"],
                "category": "Coding",
            },
        },
        CODEX_KERNEL_PLUGIN: kernel,
        CODEX_MARKETPLACE: {
            "name": PLUGIN_NAME,
            "interface": {"displayName": "Agent Concepts"},
            "plugins": [
                {
                    "name": name,
                    "source": {"source": "local", "path": path},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    "category": "Coding",
                }
                for name, path in ((PLUGIN_NAME, "./"), (kernel["name"], f"./{CODEX_KERNEL_ROOT}"))
            ],
        },
    }


def _text(document: dict) -> str:
    return json.dumps(document, indent=2) + "\n"


def write_manifests(root: Path) -> list[str]:
    written = []
    for relative, document in render_manifests(root).items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_text(document), encoding="utf-8")
        written.append(relative)
    return written


def check_manifests(root: Path) -> list[str]:
    errors = []
    for relative, document in render_manifests(root).items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing {relative}; run scripts/lint.py --write-plugin-manifests")
        elif path.read_text(encoding="utf-8") != _text(document):
            errors.append(f"{relative} is stale; run scripts/lint.py --write-plugin-manifests")
    return errors
