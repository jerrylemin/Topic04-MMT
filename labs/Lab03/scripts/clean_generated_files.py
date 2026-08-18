from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "evidence" / name for name in ("traces", "requests", "responses", "logs", "database", "audit", "snippets")]
TARGETS.append(ROOT / "report")

removed = 0
for folder in TARGETS:
    for path in folder.glob("*"):
        if path.is_file() and path.name != ".gitkeep":
            path.unlink()
            removed += 1
print(f"Removed {removed} generated evidence/report files; screenshots and external data were preserved.")
