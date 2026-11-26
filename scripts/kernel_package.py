#!/usr/bin/env python3
"""Stage the canonical kernel bytes for the standalone package."""

from pathlib import Path


CANONICAL = Path("concepts/agent-kernel/body/AGENT-KERNEL.md")
STAGED = Path("packages/agent-kernel/AGENT-KERNEL.md")
BUILD_COMMAND = "python3 scripts/kernel_package.py"


def _has_linked_parent(root: Path) -> bool:
    return any((root / parent).is_symlink() for parent in STAGED.parents if parent != Path("."))


def stage_kernel(root: Path) -> None:
    if _has_linked_parent(root):
        raise ValueError(f"refusing to stage through a symlink in {STAGED.parent}")
    canonical = (root / CANONICAL).read_bytes()
    staged = root / STAGED
    staged.parent.mkdir(parents=True, exist_ok=True)
    if staged.is_symlink():
        staged.unlink()
    if staged.exists():
        if not staged.is_file():
            raise ValueError(f"cannot stage {STAGED}: path is not a regular file")
        if staged.read_bytes() == canonical:
            return
    staged.write_bytes(canonical)


def check_staged_kernel(root: Path) -> list[str]:
    staged = root / STAGED
    try:
        if (_has_linked_parent(root) or staged.is_symlink() or not staged.is_file()
                or staged.read_bytes() != (root / CANONICAL).read_bytes()):
            return [f"{STAGED} must be a regular copy of {CANONICAL}; run {BUILD_COMMAND}"]
    except OSError as exc:
        return [f"cannot check {STAGED}: {exc}; run {BUILD_COMMAND}"]
    return []


if __name__ == "__main__":
    try:
        stage_kernel(Path(__file__).resolve().parents[1])
    except (OSError, ValueError) as exc:
        raise SystemExit(f"cannot stage agent kernel: {exc}") from None
