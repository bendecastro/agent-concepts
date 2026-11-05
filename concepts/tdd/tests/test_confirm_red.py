"""Behavioral checks for confirm-red's disposable old-code tree."""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / 'body/scripts/confirm-red.py'


def git(repo, *args):
    return subprocess.check_output(['git', '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null', '-C', str(repo), *args])


@pytest.fixture
def repo(tmp_path):
    git(tmp_path, 'init', '-q')
    git(tmp_path, 'config', 'user.email', 'test@example.invalid')
    git(tmp_path, 'config', 'user.name', 'Test')
    (tmp_path / 'calc.py').write_text('def value(): return 1\n')
    (tmp_path / 'test_calc.py').write_text('from calc import value\nassert value() == 1\n')
    git(tmp_path, 'add', '.')
    git(tmp_path, 'commit', '-qm', 'baseline')
    return tmp_path


def run(repo, *options):
    return subprocess.run([sys.executable, str(SCRIPT), *options, '--',
                           sys.executable, 'test_calc.py'], cwd=repo,
                          capture_output=True, text=True)


def test_confirmed_red_and_working_tree_untouched(repo):
    (repo / 'calc.py').write_text('def value(): return 2\n')
    (repo / 'test_calc.py').write_text('from calc import value\nassert value() == 2\n')
    before = {p.name: p.read_bytes() for p in repo.iterdir() if p.is_file()}
    status = git(repo, 'status', '--porcelain')
    result = run(repo)
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'test_calc.py' in result.stdout
    assert 'AssertionError' in result.stdout
    assert git(repo, 'status', '--porcelain') == status
    assert {p.name: p.read_bytes() for p in repo.iterdir() if p.is_file()} == before


def test_not_red(repo):
    (repo / 'test_calc.py').write_text('from calc import value\nassert value() > 0\n')
    assert run(repo).returncode == 1


def test_no_changed_tests(repo):
    assert run(repo).returncode == 2


def test_untracked_test_overlaid(repo):
    (repo / 'test_new.py').write_text('from calc import value\nassert value() == 2\n')
    result = subprocess.run([sys.executable, str(SCRIPT), '--', sys.executable,
                             'test_new.py'], cwd=repo, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'test_new.py' in result.stdout
    assert 'AssertionError' in result.stdout


def test_help_documents_limits_lint():
    result = subprocess.run([sys.executable, str(SCRIPT), '--help'],
                            capture_output=True, text=True)
    assert result.returncode == 0
    help_text = ' '.join(result.stdout.split())
    assert 'absolute interpreter paths' in help_text
    assert 'manual behavioural mutation' in help_text


def test_missing_command_is_infrastructure_error(repo):
    (repo / 'test_calc.py').write_text('assert True\n')
    result = subprocess.run([sys.executable, str(SCRIPT), '--',
                             '/nonexistent-test-command'], cwd=repo,
                            capture_output=True, text=True)
    assert result.returncode == 2
    assert 'Infrastructure error' in result.stderr


def command(repo, *cmd, options=(), env=None):
    return subprocess.run([sys.executable, str(SCRIPT), *options, '--', *cmd],
                          cwd=repo, env=env, capture_output=True, text=True)


def changed(repo):
    (repo / 'test_calc.py').write_text('assert False, "behavioural red"\n')


def test_symlinked_temp_ancestor(repo, tmp_path):
    import os
    real = repo / 'real'
    real.mkdir()
    link = repo / 'link'
    link.symlink_to(real, target_is_directory=True)
    (real / 'sub').mkdir()
    changed(repo)
    result = command(repo, sys.executable, 'test_calc.py',
                     env=dict(os.environ, TMPDIR=str(link / 'sub')))
    assert result.returncode == 0, result.stderr
    assert 'AssertionError' in result.stdout


def test_unexpected_exception_is_infrastructure(repo):
    wrapper = ('import runpy,sys,tempfile; '
               'tempfile.TemporaryDirectory=lambda **kw: 1/0; '
               f'sys.argv=[{str(SCRIPT)!r},"--","true"]; '
               f'runpy.run_path({str(SCRIPT)!r},run_name="__main__")')
    changed(repo)
    result = subprocess.run([sys.executable, '-c', wrapper], cwd=repo,
                            capture_output=True, text=True)
    assert result.returncode == 2, result.stderr
    assert 'Infrastructure error' in result.stderr


def test_caller_subdirectory(repo):
    pkg = repo / 'pkg'
    pkg.mkdir()
    (pkg / 'test_sub.py').write_text('assert False, "subdirectory red"\n')
    result = command(pkg, sys.executable, 'test_sub.py')
    assert result.returncode == 0
    assert 'subdirectory red' in result.stdout
    assert 'AssertionError' in result.stdout


def test_rename_removes_old_test(repo):
    (repo / 'test_calc.py').write_text('assert True\n' * 30)
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'long test')
    git(repo, 'mv', 'test_calc.py', 'test_renamed.py')
    result = command(repo, sys.executable, '-c',
                     'from pathlib import Path; assert not Path("test_calc.py").exists()')
    assert result.returncode == 1, result.stdout


def test_export_ignore_does_not_remove_support(repo):
    (repo / '.gitattributes').write_text('calc.py export-ignore\n')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'attributes')
    (repo / 'test_calc.py').write_text('from calc import value\nassert value() == 2\n')
    result = run(repo)
    assert result.returncode == 0
    assert 'AssertionError' in result.stdout
    assert 'ModuleNotFoundError' not in result.stdout


@pytest.mark.parametrize('message', ["AttributeError: object has no attribute bar",
                                    'TypeError: unexpected keyword argument',
                                    'Cannot find module', 'is not a function', 'undefined:'])
def test_missing_symbol_warning(repo, message):
    changed(repo)
    result = command(repo, sys.executable, '-c', f'print({message!r}); exit(1)')
    assert result.returncode == 0
    assert 'WARNING' in result.stdout


@pytest.mark.parametrize('code', [3, 4, 5])
def test_pytest_infrastructure_exits(repo, code):
    changed(repo)
    result = command(repo, sys.executable, '-c', f'exit({code})', 'pytest')
    assert result.returncode == 2, result.stdout


def test_signal_is_infrastructure(repo):
    changed(repo)
    result = command(repo, sys.executable, '-c',
                     'import os,signal; os.kill(os.getpid(), signal.SIGTERM)')
    assert result.returncode == 2, result.stdout


@pytest.mark.parametrize('name', ['example_test.go', 'test/check.js', '__tests__/check.js',
                                  'conftest.py', 'nested/test_check.py'])
def test_default_test_paths(repo, name):
    path = repo / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('assert False\n')
    result = command(repo, sys.executable, name)
    assert result.returncode == 0, result.stdout
    assert 'AssertionError' in result.stdout


def test_production_under_test_named_directory_not_overlaid(repo):
    path = repo / 'src/test_utils/helper.py'
    path.parent.mkdir(parents=True)
    path.write_text('VALUE = 1\n')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'helper')
    path.write_text('VALUE = 2\n')
    (repo / 'test_calc.py').write_text('from src.test_utils.helper import VALUE\nassert VALUE == 2\n')
    result = run(repo)
    assert result.returncode == 0, result.stdout
    assert 'AssertionError' in result.stdout


def test_full_output_preserved(repo):
    changed(repo)
    result = command(repo, sys.executable, '-c',
                     'print("FAILURE FIRST"); print("noise\\n" * 50); exit(1)')
    assert result.returncode == 0
    assert '\nFAILURE FIRST\n' in result.stdout


def test_command_help_is_forwarded(repo):
    changed(repo)
    result = command(repo, sys.executable, '-c', 'import sys; print(sys.argv[1]); exit(1)', '--help')
    assert result.returncode == 0
    assert 'Confirmed red' in result.stdout
    assert '\n--help\n' in result.stdout


def test_deleted_test_removed(repo):
    (repo / 'test_calc.py').unlink()
    result = command(repo, sys.executable, '-c',
                     'from pathlib import Path; assert not Path("test_calc.py").exists()')
    assert result.returncode == 1, result.stdout


def test_explicit_base(repo):
    base = git(repo, 'rev-parse', 'HEAD').decode().strip()
    (repo / 'calc.py').write_text('def value(): return 2\n')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'new implementation')
    (repo / 'test_calc.py').write_text('from calc import value\nassert value() == 2\n')
    result = run(repo, '--base', base)
    assert result.returncode == 0, result.stdout
    assert 'AssertionError' in result.stdout


def test_staged_only_test_change(repo):
    changed(repo)
    git(repo, 'add', 'test_calc.py')
    result = run(repo)
    assert result.returncode == 0, result.stdout
    assert 'AssertionError' in result.stdout


def test_symlink_overlay_rejected(repo):
    (repo / 'test_calc.py').unlink()
    (repo / 'test_calc.py').symlink_to('calc.py')
    result = run(repo)
    assert result.returncode == 2
    assert 'symlink' in result.stderr


def test_python39_without_tar_filter_api(repo):
    changed(repo)
    # Reproduce the Python 3.9.6 signature on newer interpreters too.
    wrapper = ('import runpy,sys,tarfile; '
               'exec("def extractall(self, path):\\n pass", tarfile.__dict__); '
               'tarfile.TarFile.extractall=tarfile.extractall; '
               f'sys.argv=[{str(SCRIPT)!r},"--",{sys.executable!r},"test_calc.py"]; '
               f'runpy.run_path({str(SCRIPT)!r},run_name="__main__")')
    result = subprocess.run([sys.executable, '-c', wrapper], cwd=repo,
                            capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'AssertionError' in result.stdout


def test_export_subst_keeps_literal_support(repo):
    (repo / '.gitattributes').write_text('calc.py export-subst\n')
    (repo / 'calc.py').write_text('VALUE = "$Format:%H$"\n')
    git(repo, 'add', '.')
    git(repo, 'commit', '-qm', 'literal support')
    (repo / 'test_calc.py').write_text('from calc import VALUE\nassert VALUE == "$Format:%H$"\n')
    result = run(repo)
    assert result.returncode == 1, result.stdout + result.stderr


def test_submodule_is_explicit_infrastructure_error(repo):
    base = git(repo, 'rev-parse', 'HEAD').decode().strip()
    git(repo, 'update-index', '--add', '--cacheinfo', '160000,' + base + ',dependency')
    git(repo, 'commit', '-qm', 'gitlink')
    changed(repo)
    result = run(repo)
    assert result.returncode == 2, result.stdout + result.stderr
    assert 'submodules are unsupported' in result.stderr
