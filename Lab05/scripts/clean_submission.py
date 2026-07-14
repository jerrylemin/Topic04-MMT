"""Remove caches and temporary files while preserving Lab05 deliverables."""

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def clean(root: Path = ROOT) -> list[str]:
    removed: list[str] = []
    protected_files = {root / "lab05.sqlite3"}

    directories = [
        path
        for path in root.rglob("*")
        if path.is_dir()
        and path.name in {"__pycache__", ".pytest_cache", "htmlcov", "tmp", "pdf_pages"}
        and ".venv" not in path.parts
    ]
    for path in sorted(directories, key=lambda item: len(item.parts), reverse=True):
        if path.exists():
            shutil.rmtree(path)
            removed.append(str(path.relative_to(root)))

    for pattern in ("*.pyc", "*.pyo", ".coverage", "*test*.sqlite3"):
        for path in root.rglob(pattern):
            if ".venv" in path.parts or not path.is_file() or path in protected_files:
                continue
            path.unlink()
            removed.append(str(path.relative_to(root)))

    log = root / "evidence" / "logs" / "submission_cleanup.txt"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(
        "LAB05 SUBMISSION CLEANUP\n"
        + ("\n".join(sorted(removed)) if removed else "No cache or temporary files found.")
        + "\n",
        encoding="utf-8",
    )
    return sorted(removed)


def main() -> int:
    removed = clean()
    print(f"Removed {len(removed)} cache/temporary paths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
