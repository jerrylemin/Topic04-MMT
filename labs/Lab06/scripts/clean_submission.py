"""Remove only disposable Lab06 artifacts while preserving source and final evidence."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAFE_DIRECTORIES = (
    ROOT / ".pytest_cache",
    ROOT / "htmlcov",
    ROOT / "tmp",
    ROOT / "report" / "tmp",
    ROOT / "evidence" / "tmp",
)
SAFE_FILES = (ROOT / ".coverage",)
TEST_DATABASE_PATTERNS = ("*test*.sqlite3", "*test*.db")


def _inside_root(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT.resolve())
        return True
    except ValueError:
        return False


def _is_project_artifact(path: Path) -> bool:
    """Accept disposable project artifacts, never virtualenv dependencies."""
    if not _inside_root(path):
        return False
    relative = path.resolve().relative_to(ROOT.resolve())
    return not relative.parts or relative.parts[0] != ".venv"


def clean_submission() -> list[str]:
    removed: list[str] = []
    directories = list(SAFE_DIRECTORIES)
    directories.extend(path for path in ROOT.rglob("__pycache__") if _is_project_artifact(path))
    for path in sorted(set(directories), key=lambda item: len(item.parts), reverse=True):
        if path.exists() and _is_project_artifact(path):
            shutil.rmtree(path)
            removed.append(str(path.relative_to(ROOT)))
    files = list(SAFE_FILES)
    files.extend(ROOT.rglob("*.pyc"))
    files.extend(ROOT.rglob("*.pyo"))
    for pattern in TEST_DATABASE_PATTERNS:
        files.extend(ROOT.rglob(pattern))
    files.extend((ROOT / "evidence" / "logs").glob("*.tmp") if (ROOT / "evidence" / "logs").exists() else ())
    for path in sorted(set(files)):
        if path.is_file() and _is_project_artifact(path):
            path.unlink()
            removed.append(str(path.relative_to(ROOT)))
    return removed


def main() -> int:
    removed = clean_submission()
    print(f"Removed {len(removed)} disposable Lab06 artifact(s).")
    for item in removed:
        print(f"- {item}")
    print("Preserved source, demo database, final evidence, screenshots, tests, README and reports.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
