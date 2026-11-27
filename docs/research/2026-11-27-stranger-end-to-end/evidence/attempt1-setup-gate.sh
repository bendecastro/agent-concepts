#!/usr/bin/env bash
# Local full gate; see .bc-agent/conventions/validation.md.
set -euo pipefail
python3 -m unittest discover -s tests
