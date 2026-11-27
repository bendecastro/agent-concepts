#!/usr/bin/env python3
"""Stage the canonical kernel bytes for the standalone packages."""

from pathlib import Path


CANONICAL = Path("concepts/agent-kernel/body/AGENT-KERNEL.md")
STAGED_COPIES = (
    Path("packages/agent-kernel/AGENT-KERNEL.md"),
    Path("packages/agent-kernel-pi/AGENT-KERNEL.md"),
    Path("packages/agent-kernel-claude/AGENT-KERNEL.md"),
)
BUILD_COMMAND = "python3 scripts/kernel_package.py"


def _has_linked_parent(root: Path, copy: Path) -> bool:
    return any((root / parent).is_symlink() for parent in copy.parents if parent != Path("."))


def stage_kernel(root: Path) -> None:
    for copy in STAGED_COPIES:
        if _has_linked_parent(root, copy):
            raise ValueError(f"refusing to stage through a symlink in {copy.parent}")
    canonical = (root / CANONICAL).read_bytes()
    for copy in STAGED_COPIES:
        staged = root / copy
        staged.parent.mkdir(parents=True, exist_ok=True)
        if staged.is_symlink():
            staged.unlink()
        if staged.exists():
            if not staged.is_file():
                raise ValueError(f"cannot stage {copy}: path is not a regular file")
            if staged.read_bytes() == canonical:
                continue
        staged.write_bytes(canonical)


def check_staged_kernel(root: Path) -> list[str]:
    try:
        canonical = (root / CANONICAL).read_bytes()
    except OSError as exc:
        return [f"cannot read {CANONICAL}: {exc}"]
    errors = []
    for copy in STAGED_COPIES:
        staged = root / copy
        try:
            if (_has_linked_parent(root, copy) or staged.is_symlink() or not staged.is_file()
                    or staged.read_bytes() != canonical):
                errors.append(f"{copy} must be a regular copy of {CANONICAL}; run {BUILD_COMMAND}")
        except OSError as exc:
            errors.append(f"cannot check {copy}: {exc}; run {BUILD_COMMAND}")
    return errors


if __name__ == "__main__":
    try:
        stage_kernel(Path(__file__).resolve().parents[1])
    except (OSError, ValueError) as exc:
        raise SystemExit(f"cannot stage agent kernel: {exc}") from None
