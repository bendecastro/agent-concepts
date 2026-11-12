"""Visible work layout emitted by the scaffold CLI."""
from pathlib import Path
import subprocess
import sys

SCAFFOLD = Path(__file__).resolve().parents[1] / "body/scaffold.py"


def test_code_scaffold_creates_visible_work_layout(tmp_path):
    subprocess.run([sys.executable, str(SCAFFOLD), '--root', str(tmp_path), '--slug', 'demo'], check=True)
    assert (tmp_path / 'glossary.md').is_file()
    assert (tmp_path / 'work/0-ideas.md').is_file()
    for stage in ('1-planned', '2-active', '3-done', '4-dropped'):
        assert (tmp_path / 'work' / stage).is_dir()
    for path in ('docs/decisions', 'docs/research'):
        assert (tmp_path / path).is_dir()
    assert {p.name for p in (tmp_path / '.bc-agent').iterdir()} == {
        'AGENTS.md', 'map.md', 'log.md', 'conventions', 'references', 'templates'}


def test_where_things_go_table_has_stable_role_paths(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location('scaffold', SCAFFOLD)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for archetype in ('code', 'ops', 'hybrid'):
        root = tmp_path / archetype
        root.mkdir()
        subprocess.run([sys.executable, str(SCAFFOLD), '--root', str(root), '--slug', 'demo', '--archetype', archetype], check=True)
        roles = module.parse_where_things_go((root / '.bc-agent/AGENTS.md').read_text())
        assert set(roles) >= {'work-planned', 'work-active', 'work-done', 'work-dropped', 'ideas', 'decisions', 'research', 'glossary', 'requirements', 'architecture', 'project-skills', 'project-agents'}
        assert roles['work-planned'] == 'work/1-planned/'
