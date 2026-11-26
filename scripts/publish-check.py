#!/usr/bin/env python3
"""Compatibility entry point for the pipeline skill's bundled publish checker."""

from pathlib import Path
from runpy import run_path


if __name__ == "__main__":
    checker = Path(__file__).resolve().parents[1] / (
        "concepts/bc-pipeline-to-done/body/scripts/publish-check.py"
    )
    run_path(str(checker), run_name="__main__")
