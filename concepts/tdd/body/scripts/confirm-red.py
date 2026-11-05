#!/usr/bin/env python3
"""Run changed tests against old production code, without touching Git state.

Untracked environment such as .venv is not copied: pass absolute interpreter paths.
Submodules are unsupported; LFS content requires a working Git smudge filter.
Test globs are repo-root-relative; the command runs from the caller's directory.
For tests-only changes against unchanged code, use a manual behavioural mutation.
A nonzero command can reflect environment failure, not a meaningful behavioural RED;
inspect the output. This runs the supplied command, not a security sandbox.
"""
import argparse
import fnmatch
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile

DEFAULT_TESTS = ['**/tests/**', '**/test/**', '**/__tests__/**', '**/test_*.py',
                 '**/*_test.py', '**/*_test.go', '**/*.test.*', '**/*.spec.*',
                 '**/conftest.py']


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)


def matches(name, patterns):
    # Match path components: only ** can cross directory boundaries.
    def match(parts, glob):
        if not glob:
            return not parts
        if glob[0] == '**':
            return match(parts, glob[1:]) or bool(parts) and match(parts[1:], glob)
        return bool(parts) and fnmatch.fnmatchcase(parts[0], glob[0]) and match(parts[1:], glob[1:])
    return any(match(name.split('/'), pattern.split('/')) for pattern in patterns)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='HEAD', metavar='REV')
    parser.add_argument('--tests', nargs='+', metavar='GLOB', default=DEFAULT_TESTS)
    raw = sys.argv[1:]
    if '--' not in raw and ('--help' in raw or '-h' in raw):
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
        changed = git(root, 'diff', '--no-renames', '--name-only', '-z', base, '--').split(b'\0')
        untracked = git(root, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0')
        names = sorted({os.fsdecode(n) for n in changed + untracked if n
                        and matches(os.fsdecode(n), args.tests)})
        if not names:
            print('Infrastructure error: no changed test files')
            return 2
        caller = Path.cwd().resolve().relative_to(root.resolve())
        if any(entry.startswith(b'160000 ') for entry in
               git(root, 'ls-tree', '-r', base).splitlines()):
            raise ValueError('submodules are unsupported')
        with tempfile.TemporaryDirectory(prefix='confirm-red-') as temp:
            target = Path(temp)
            # An isolated index bypasses export-ignore/subst without changing Git state.
            env = dict(os.environ, GIT_INDEX_FILE=str(target / 'index'))
            subprocess.run(['git', '-C', str(root), 'read-tree', base], env=env, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', '-C', str(root), 'checkout-index', '-a',
                            '--prefix=' + str(target / 'tree') + os.sep],
                           env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            target = target / 'tree'
            for name in names:
                source, dest = root / name, target / name
                # Do not follow old-tree symlinks when overlaying current tests.
                if any(target.joinpath(*Path(name).parts[:i]).is_symlink()
                       for i in range(1, len(Path(name).parts) + 1)):
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
            result = subprocess.run(command, cwd=target / caller, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT, text=True, errors='replace')
            output = result.stdout
            print('Command exit code: ' + str(result.returncode))
            print(output, end='' if output.endswith('\n') else '\n')
            pytest = any('pytest' in Path(part).name for part in command)
            if result.returncode < 0 or (pytest and result.returncode in (3, 4, 5)):
                print('Infrastructure error: signal, pytest internal/usage error or no tests collected')
                return 2
            if result.returncode == 0:
                print('NOT red: tests passed against old code; they cannot catch the change')
                return 1
            print('Confirmed red: command failed against old code')
            if (pytest and result.returncode == 2) or any(marker in output for marker in
                    ('ImportError', 'ModuleNotFoundError', 'NameError', 'AttributeError',
                     'unexpected keyword argument', 'Cannot find module', 'is not a function', 'undefined:')):
                print('WARNING: collection/missing-symbol red only proves the symbol is new; '
                      'use a behavioural mutation check')
            return 0
    except Exception as error:
        print('Infrastructure error: ' + str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as error:
        print('Infrastructure error: ' + str(error), file=sys.stderr)
        sys.exit(2)
