#!/usr/bin/env python3
"""Run changed tests against archived old production code, without touching Git state.

Untracked environment such as .venv is not copied: pass absolute interpreter paths.
For tests-only changes against unchanged code, use a manual behavioural mutation.
A nonzero command can reflect environment failure, not a meaningful behavioural RED;
inspect the output. This runs the supplied command, not a security sandbox.
"""
import argparse
import fnmatch
import io
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile

DEFAULT_TESTS = ['tests/**', '**/test_*.py', '**/*_test.py', '**/*.test.*', '**/*.spec.*']


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)


def matches(name, patterns):
    # **/ also matches root-level files, as in conventional recursive globs.
    return any(fnmatch.fnmatchcase(name, p) or
               (p.startswith('**/') and fnmatch.fnmatchcase(name, p[3:]))
               for p in patterns)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='HEAD', metavar='REV')
    parser.add_argument('--tests', nargs='+', metavar='GLOB', default=DEFAULT_TESTS)
    raw = sys.argv[1:]
    if '--help' in raw or '-h' in raw:
        parser.print_help()
        return 0
    if '--' not in raw:
        parser.error('separate the test command with --')
    split = raw.index('--')
    args = parser.parse_args(raw[:split])
    command = raw[split + 1:]
    if not command:
        parser.error('a test command is required')
    try:
        root = Path(git(Path.cwd(), 'rev-parse', '--show-toplevel').decode().strip())
        base = git(root, 'rev-parse', '--verify', args.base + '^{commit}').decode().strip()
        changed = git(root, 'diff', '--name-only', '-z', base, '--').split(b'\0')
        untracked = git(root, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0')
        names = sorted({os.fsdecode(n) for n in changed + untracked if n
                        and matches(os.fsdecode(n), args.tests)})
        if not names:
            print('Infrastructure error: no changed test files')
            return 2
        archive = git(root, 'archive', '--format=tar', base)
        with tempfile.TemporaryDirectory(prefix='confirm-red-') as temp:
            target = Path(temp)
            with tarfile.open(fileobj=io.BytesIO(archive)) as tree:
                tree.extractall(target, filter='data')
            for name in names:
                source, dest = root / name, target / name
                # Do not follow archive symlinks when overlaying current tests.
                if any(p.is_symlink() for p in [dest, *dest.parents] if p != target.parent):
                    raise ValueError('test overlay traverses a symlink: ' + name)
                if source.is_symlink():
                    raise ValueError('symlink test overlay is unsupported: ' + name)
                if source.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, dest)
                elif dest.exists():
                    dest.unlink()
            print('Overlaid tests:\n' + '\n'.join(names))
            print('Command: ' + shlex.join(command))
            result = subprocess.run(command, cwd=target, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, errors='replace')
            output = result.stdout
            print('Command exit code: ' + str(result.returncode))
            print('\n'.join(output.splitlines()[-40:]))
            pytest = any('pytest' in Path(part).name for part in command)
            if pytest and result.returncode in (4, 5):
                print('Infrastructure error: pytest usage error or no tests collected')
                return 2
            if result.returncode == 0:
                print('NOT red: tests passed against old code; they cannot catch the change')
                return 1
            print('Confirmed red: command failed against old code')
            if (pytest and result.returncode == 2) or any(marker in output for marker in
                    ('ImportError', 'ModuleNotFoundError', 'NameError', 'AttributeError: module')):
                print('WARNING: collection/missing-symbol red only proves the symbol is new; '
                      'use a behavioural mutation check')
            return 0
    except (OSError, subprocess.CalledProcessError, ValueError, tarfile.TarError) as error:
        print('Infrastructure error: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
