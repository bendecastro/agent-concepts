#!/usr/bin/env python3
"""Install the bundled agent kernel into a named Markdown instructions file."""

from __future__ import annotations

import argparse
import re
import stat
from codecs import BOM_UTF8
from pathlib import Path
from tempfile import NamedTemporaryFile


PACKAGE = Path(__file__).resolve().parent
PAYLOAD = PACKAGE / "AGENT-KERNEL.md"
MARKER_VERSION = b"v1"
BEGIN = b"<!-- agent-kernel:begin %s -->\n" % MARKER_VERSION
END = b"<!-- agent-kernel:end %s -->\n" % MARKER_VERSION
MARKER_PREFIX = re.compile(rb"[ \t]*<!--[ \t]*agent-kernel(?=[: \t]|-->|$)")
MARKER = re.compile(rb"<!-- agent-kernel:(begin|end) (v[0-9]+) -->")


def _marker_span(content: bytes) -> tuple[int, int] | None:
    error = "malformed or duplicate agent-kernel markers; expected one matching begin/end pair"
    markers = []
    offset = 0
    for line in content.splitlines(keepends=True):
        marker_line = line.removesuffix(b"\n").removesuffix(b"\r")
        if MARKER_PREFIX.match(marker_line):
            marker = MARKER.fullmatch(marker_line)
            if marker is None or len(markers) == 2:
                raise ValueError(error)
            markers.append((marker[1], marker[2], offset, offset + len(line)))
        offset += len(line)
    if not markers:
        return None
    if (len(markers) != 2 or markers[0][0] != b"begin" or markers[1][0] != b"end"
            or markers[0][1] != markers[1][1]):
        raise ValueError(error)
    return markers[0][2], markers[1][3]


def _replace_bytes(path: Path, content: bytes, mode: int | None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stream = NamedTemporaryFile(dir=path.parent, prefix=".agent-kernel-", delete=False)
    pending = Path(stream.name)
    try:
        with stream:
            stream.write(content)
        if mode is not None:
            pending.chmod(mode)
        # ceiling: assumes a single writer; concurrent editors need a shared lock.
        pending.replace(path)
    finally:
        pending.unlink(missing_ok=True)


def update_file(path: Path, *, remove: bool = False) -> None:
    path = path.resolve()
    if path in (PAYLOAD, PACKAGE / "install.py"):
        raise ValueError("choose an instructions file outside the package files")
    try:
        info = path.stat()
    except FileNotFoundError:
        original, mode = b"", None
    else:
        if not stat.S_ISREG(info.st_mode):
            raise ValueError("instructions path is not a regular file")
        original, mode = path.read_bytes(), stat.S_IMODE(info.st_mode)
    preamble = BOM_UTF8 if original.startswith(BOM_UTF8) else b""
    content = original[len(preamble):]
    existing = _marker_span(content)
    if remove:
        if existing is None:
            return
        block = b""
    else:
        kernel = PAYLOAD.read_bytes()
        block = BEGIN + kernel + (b"" if kernel.endswith(b"\n") else b"\n") + END
    if existing is None:
        # Avoid adding a separator byte to a file with no final newline.
        updated = block + content if content and not content.endswith((b"\r", b"\n")) else content + block
    else:
        start, end = existing
        updated = content[:start] + block + content[end:]
    updated = preamble + updated
    if updated != original:
        _replace_bytes(path, updated, mode)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("instructions", type=Path, help="path to the instructions file")
    parser.add_argument("--remove", action="store_true", help="remove the managed block")
    args = parser.parse_args()
    try:
        update_file(args.instructions, remove=args.remove)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"{args.instructions}: {exc}\n")


if __name__ == "__main__":
    main()
