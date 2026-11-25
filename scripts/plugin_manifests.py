#!/usr/bin/env python3
"""Generate and check the Claude Code and Codex plugin manifests and marketplaces.

The repository root is one plugin for both agents. Each manifest lists every
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
# The Releases step sets this to the release tag's version.
PLUGIN_VERSION = "0.1.0"
DESCRIPTION = ("Every public agent-concepts skill: planning, TDD, code review, debugging, "
               "subagent workflows and upkeep, with bc- names.")
AUTHOR = {"name": "agent-concepts contributors"}
LICENSE = "MIT"

LIST_PATH = "concepts/public-skills.json"
CLAUDE_PLUGIN = ".claude-plugin/plugin.json"
CLAUDE_MARKETPLACE = ".claude-plugin/marketplace.json"
CODEX_PLUGIN = ".codex-plugin/plugin.json"
CODEX_MARKETPLACE = ".agents/plugins/marketplace.json"


def _skill_paths(root: Path) -> list[str]:
    listing = json.loads((root / LIST_PATH).read_text(encoding="utf-8"))
    return [f"./concepts/{name}/body" for name in sorted(listing["skills"])]


def render_manifests(root: Path) -> dict[str, dict]:
    skills = _skill_paths(root)
    plugin = {
        "name": PLUGIN_NAME,
        "version": PLUGIN_VERSION,
        "description": DESCRIPTION,
        "author": AUTHOR,
        "license": LICENSE,
        "skills": skills,
    }
    return {
        CLAUDE_PLUGIN: plugin,
        CLAUDE_MARKETPLACE: {
            "name": PLUGIN_NAME,
            "owner": AUTHOR,
            "metadata": {"description": DESCRIPTION},
            "plugins": [{"name": PLUGIN_NAME, "source": "./", "description": DESCRIPTION}],
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
        CODEX_MARKETPLACE: {
            "name": PLUGIN_NAME,
            "interface": {"displayName": "Agent Concepts"},
            "plugins": [{
                "name": PLUGIN_NAME,
                "source": {"source": "local", "path": "./"},
                "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                "category": "Coding",
            }],
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
