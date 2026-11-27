"""Create the tinylabels repository and its local bare remote under a scratch directory."""

from pathlib import Path
import subprocess
import sys


def main(scratch: Path) -> None:
    scratch = scratch.resolve(strict=True)
    project = scratch / "tinylabels"
    origin = scratch / "origin.git"
    if origin.exists() or origin.is_symlink():
        raise FileExistsError(origin)
    project.mkdir()

    def git(*args: str) -> None:
        subprocess.run(["git", *args], cwd=project, check=True)

    files = {
        ".gitignore": "__pycache__/\n*.egg-info/\n.venv/\n",
        "README.md": "# tinylabels\n\nA small library for normalizing labels.\n\n"
                     "Run the tests: `python3 -m unittest discover -s tests`.\n",
        "pyproject.toml": '[project]\nname = "tinylabels"\nversion = "0.1.0"\n'
                          'requires-python = ">=3.10"\n',
        "tinylabels/__init__.py": 'def normalize(label: str) -> str:\n'
                                  '    """Remove surrounding whitespace and lowercase a label."""\n'
                                  '    return label.strip().lower()\n',
        "tests/test_labels.py": 'import unittest\n\nfrom tinylabels import normalize\n\n\n'
                                'class NormalizeTests(unittest.TestCase):\n'
                                '    def test_whitespace(self):\n'
                                '        self.assertEqual(normalize("  urgent  "), "urgent")\n\n'
                                '    def test_case(self):\n'
                                '        self.assertEqual(normalize("Next"), "next")\n',
    }
    for name, content in files.items():
        path = project / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    git("init", "--bare", "--initial-branch=main", str(origin))
    git("init", "--initial-branch=main")
    git("config", "user.name", "Fixture User")
    git("config", "user.email", "fixture@example.invalid")
    git("add", "--", *files)
    git("commit", "-m", "Create tinylabels fixture")
    git("remote", "add", "origin", str(origin))
    git("-c", "protocol.file.allow=always", "push", "--set-upstream", "origin", "main")
    git("-c", "protocol.file.allow=always", "remote", "set-head", "origin", "--auto")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} SCRATCH_DIRECTORY")
    main(Path(sys.argv[1]))
