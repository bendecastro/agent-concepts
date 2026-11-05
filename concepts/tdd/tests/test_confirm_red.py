"""Behavioral checks for confirm-red's disposable old-code tree."""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / 'body/scripts/confirm-red.py'


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


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


def test_help_documents_limits():
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
