import subprocess
from pathlib import Path


ROOT = Path(__file__).parents[1]
BINARY = ROOT / "build" / "secure_snprintf"


def run(value: str):
    return subprocess.run(
        [str(BINARY), value], cwd=ROOT, capture_output=True, text=True,
        timeout=2, check=False,
    )


def test_snprintf_patch_rejects_truncation():
    accepted = run("A" * 31)
    rejected = run("A" * 64)

    assert accepted.returncode == 0
    assert rejected.returncode == 67
    assert "snprintf would truncate" in rejected.stderr
    assert "Processed name:" not in rejected.stdout
