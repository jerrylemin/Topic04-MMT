from __future__ import annotations

from pathlib import Path

from scripts.clean_submission import SAFE_DIRECTORIES, SAFE_FILES, _is_project_artifact


ROOT = Path(__file__).resolve().parents[1]


def test_cleanup_targets_only_disposable_paths_inside_lab06():
    for path in (*SAFE_DIRECTORIES, *SAFE_FILES):
        path.resolve().relative_to(ROOT.resolve())
    protected = {ROOT / "app.py", ROOT / "README.md", ROOT / "report", ROOT / "evidence"}
    assert protected.isdisjoint(set(SAFE_FILES))


def test_cleanup_never_targets_virtual_environment_dependencies():
    dependency_cache = ROOT / ".venv" / "Lib" / "site-packages" / "example" / "__pycache__"
    assert _is_project_artifact(dependency_cache) is False
